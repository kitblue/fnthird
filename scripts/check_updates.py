# -*- coding: utf-8 -*-
"""fnthird 每日自动更新检查

读取本源 fnpack.json 中收录的每个 app（_src 指向上游 GitHub 仓库），
检查上游 Releases 是否有比当前记录更新的版本；如有，则下载新资产并
重新计算 sha256/size，把新版本**追加**进 fnpack.json 的 releases 字段
（历史版本条目全部保留，绝不删除），最后通过 GitHub Contents API 推送。

发布策略（本仓库为"内置源"性质的网址型源）：
- 仅当上游官方软件发布新版本时，才同步写入新的 release 条目；
- 本源自身不发布 GitHub Release / tag，源地址固定不变，只更新源信息；
- 已发布的旧版本条目永久保留，商店侧仍可回滚安装。

本地测试：python check_updates.py           # 仅检查并打印摘要，不写文件
          python check_updates.py --apply   # 写回本地 fnpack.json 但不推送
          python check_updates.py --push    # 写回并推送远程 main
"""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.request
import ssl
from pathlib import Path

VERIFY = False
ctx = ssl._create_unverified_context()
BASE = Path(__file__).resolve().parent.parent
FNPACK = BASE / "fnpack.json"
REPO = "kitblue/fnthird"
BRANCH = "main"


def get_token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t:
        return t.strip()
    p = BASE / ".tmp_sync" / "github_token.txt"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return ""


def http_json(url, token=""):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "fnthird/1.0"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))


def http_bytes(url, token=""):
    headers = {"Accept": "application/octet-stream", "User-Agent": "fnthird/1.0"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
        return r.read()


def version_key(v):
    if not v:
        return (0, 0, 0, 0)
    nums = [int(x) for x in re.findall(r"\d+", str(v))][:4]
    while len(nums) < 4:
        nums.append(0)
    return tuple(nums)


def match_asset_name(old_url, new_ver, assets):
    """依据旧 download_url 的文件名模式推断新资产名，优先精确、其次模糊。"""
    old_name = old_url.rstrip("/").split("/")[-1]
    old_ver_candidates = []
    for key in re.findall(r"\d+(?:\.\d+)+", old_name):
        old_ver_candidates.append(key)
    # 候选新文件名：把旧文件名里的版本号替换为新版本
    candidates = []
    for ov in old_ver_candidates:
        for nv in (new_ver, f"v{new_ver}", f"V{new_ver}", new_ver.lstrip("v")):
            candidates.append(old_name.replace(ov, nv, 1))
    for c in candidates:
        if c in assets:
            return c
    # 模糊：与候选最接近的资产名
    import difflib
    best = difflib.get_close_matches(candidates[0], assets, n=1, cutoff=0.6) if candidates else []
    return best[0] if best else ""


def _norm(s):
    return re.sub(r"[^0-9a-z]+", "", str(s).lower())


def asset_related(name, appname, old_url):
    """资产必须与 appname 或旧资产名相关，避免同仓库多应用时抓错包。"""
    import difflib
    n = _norm(name)
    a = _norm(appname)
    if a and a in n:
        return True
    o = _norm(old_url.rstrip("/").split("/")[-1]) if old_url else ""
    if o and difflib.SequenceMatcher(None, o, n).ratio() >= 0.75:
        return True
    return False


def check_app(appname, entry, token):
    src = entry.get("_src") or ""
    if "/" not in src:
        return None, "无 _src 上游信息"
    owner, repo = src.split("/", 1)
    releases = entry.get("releases") or {}
    old_ver = max(releases.keys(), key=version_key) if releases else ""
    try:
        rel = http_json(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", token)
    except Exception as e:
        return None, f"查询上游 releases 失败: {e}"
    tag = rel.get("tag_name") or ""
    new_ver = tag.lstrip("vV")
    # 上游 tag 必须含点分版本号（1.2.1 / v26.10.23 / magpie-v1.1.14 均可），
    # 纯中文说明式 tag（如「3-修复端口识别」）或无语义 tag 不入源
    if not re.search(r"\d+(?:\.\d+)+", new_ver):
        return None, f"上游最新 tag「{tag}」不是版本号格式，跳过"
    if version_key(new_ver) <= version_key(old_ver):
        return None, f"已是最新（{old_ver}）"
    assets = rel.get("assets") or []
    names = {a["name"] for a in assets}
    by_name = {a["name"]: a for a in assets}
    new_packages = {}
    missing = []
    for arch, pkg in (releases.get(old_ver, {}).get("packages") or {}).items():
        old_url = pkg.get("download_url", "")
        name = match_asset_name(old_url, new_ver, names) if old_url else ""
        if not name or name not in by_name:
            # 无旧 URL 参考时按平台关键词匹配
            kw = {"x86_64": ["x86_64", "x86"], "arm64": ["arm64", "aarch64"], "arm": ["arm"], "x86": ["x86"]}.get(arch, [arch])
            cand = [n for n in names if any(k in n.lower() for k in kw)]
            if not cand:
                # 兜底：资产名不含架构关键字时，取唯一的 .fpk 资产
                fpk = [n for n in names if n.lower().endswith(".fpk")]
                if len(fpk) == 1:
                    cand = fpk
            if not cand:
                missing.append(arch)
                continue
            name = cand[0]
        if not asset_related(name, appname, old_url):
            missing.append(f"{arch}(资产与 appname 不匹配: {name})")
            continue
        asset = by_name[name]
        # 优先使用 GitHub 资产自带的 sha256 digest，避免逐个下载大包（数百 MB）
        digest = (asset.get("digest") or "").strip()
        sha256, size = "", asset.get("size") or 0
        if digest.lower().startswith("sha256:"):
            sha256 = digest.split(":", 1)[1].strip()
        if not sha256:
            try:
                data = http_bytes(f"https://api.github.com/repos/{owner}/{repo}/releases/assets/{asset['id']}", token)
            except Exception as e:
                missing.append(f"{arch}(下载失败: {e})")
                continue
            sha256, size = hashlib.sha256(data).hexdigest(), len(data)
        new_packages[arch] = {
            "download_url": asset.get("browser_download_url") or f"https://github.com/{owner}/{repo}/releases/download/{tag}/{name}",
            "sha256": sha256,
            "size": size,
        }
    if not new_packages:
        return None, f"发现新版本 {new_ver} 但无法匹配资产: {missing}"
    new_entry = dict(entry)
    # 保留全部历史版本，仅追加/覆盖当前新版本条目
    merged = dict(releases)
    merged[new_ver] = {"packages": new_packages}
    new_entry["releases"] = merged
    return new_entry, f"{old_ver} -> {new_ver}" + (f"（{';'.join(missing)} 未匹配）" if missing else "")


def push_file(token, path, content_b64, message):
    api = f"https://api.github.com/repos/{REPO}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json",
               "User-Agent": "fnthird/1.0"}
    try:
        req = urllib.request.Request(api + f"?ref={BRANCH}", headers=headers)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            sha = json.loads(r.read().decode())["sha"]
    except Exception:
        sha = None
    payload = {"message": message, "branch": BRANCH, "content": content_b64}
    if sha:
        payload["sha"] = sha
    req = urllib.request.Request(api, data=json.dumps(payload).encode("utf-8"), method="PUT", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            j = json.loads(r.read().decode())
            return j.get("content", {}).get("sha", "?")
    except Exception as e:
        raise RuntimeError(f"PUT {path} 失败: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="写回本地 fnpack.json")
    ap.add_argument("--push", action="store_true", help="写回并推送远程")
    args = ap.parse_args()

    token = get_token()
    if args.push and not token:
        print("缺少 GitHub token"); sys.exit(1)

    data = json.loads(FNPACK.read_text(encoding="utf-8"))
    apps = data.get("apps", {})
    changed = {}
    summaries = []
    for appname, entry in apps.items():
        new_entry, msg = check_app(appname, entry, token)
        summaries.append(f"{appname}: {msg}")
        if new_entry is not None:
            changed[appname] = new_entry

    print("\n".join(summaries))
    print(f"\n检查完成：{len(apps)} 个 app，{len(changed)} 个有更新")
    if not changed:
        return
    for an, ne in changed.items():
        apps[an] = ne
    data["apps"] = apps
    if args.apply or args.push:
        FNPACK.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("已写回本地 fnpack.json")
    if args.push:
        b64 = base64.b64encode(FNPACK.read_bytes()).decode("ascii")
        msg = "chore: 同步上游官方新版本（保留历史版本，仅更新源信息）\n\n- " + "；".join(f"{k} {v}" for k, v in changed.items())
        sha = push_file(token, "fnpack.json", b64, msg)
        print(f"已推送 fnpack.json -> sha={sha}")


if __name__ == "__main__":
    main()
