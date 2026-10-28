
# 飞牛 fnOS 应用收录源（fnthird）

本项目是 **FnUnify 聚合源的子源**，作为飞牛 fnOS 第三方应用源，可为第三方应用商店（如 FnDepot）直接收录。

**定位**：收录两类内容——

1. **原生 manifest 应用**：有 manifest 但缺 `fnpack.json` 的原生 app 项目；
2. **独立应用条目**：已有完整 fnpack 条目的独立应用（如 **Blue-Mink/FnDepot** 中的 9 个独立应用条目：global-radio、com.trek.app、com.dongguaha.vm、new-api、dockflare、dog-dev、kspeeder、com.istoreos.vm、ryzen-power-control）。

独立应用以索引条目形式收录（条目 `_src` 保留上游仓库溯源），原仓库本体不做转移，其索引收录由本源承接。

2026-10-17 扩充：新增 11 个单作者小仓库的 23 条 unique_valid 应用（RONGLINC93、jiaaom、BearHero520、lianhua、ZhangZsky、mayishidai、JaxSupero、maxsusu、yoqie、ccrabit、frankluise5220），均保留 `_src` 溯源至各自上游仓库。

## 源信息

- 源名：`fnthird`
- 源文件：`fnpack.json`（FnDepot V2 schema）
- 收录应用：**65 条**（均为带 `_src` 溯源的上游应用条目）

第三方应用商店添加本仓库为源后，即可安装其中收录的应用。

## 完整源地址

- 仓库主页：<https://github.com/kitblue/fnthird>
- 源文件完整原地址（fnpack.json）：<https://raw.githubusercontent.com/kitblue/fnthird/main/fnpack.json>

在 FnDepot 等支持 FnDepot V2 的第三方应用商店中，将上述 `fnpack.json` 完整原地址添加为第三方源，即可收录并正常安装本源的 app（各 app 均符合第三方应用商店正常使用标准）。

本源已收录进 [kitblue/FnUnify](https://github.com/kitblue/FnUnify) 聚合源（见其 `repo_list.txt`），经 FnUnify 聚合后亦可统一安装。

## 目录结构

```
manifests/<owner>-<repo>/
  manifest.json    # 原生 manifest 的 JSON 化版本
fnpack.json        # 源文件（商店收录入口）
```

## 收录标准

- 已发布到飞牛 fnOS 第三方应用中心
- 原生 manifest 应用需有可读取的 manifest 文件；独立应用需有完整 fnpack 条目（含 releases 下载信息）
- 项目活跃、非僵尸仓库

## 新增项目

1. **原生 manifest 应用**：在 `manifests/<owner>-<repo>/manifest.json` 保存原 manifest 的 JSON 化版本，并在 `fnpack.json` 的 `apps` 中添加对应应用条目（含 releases 下载信息）。
2. **独立应用**：直接在 `fnpack.json` 的 `apps` 中添加完整条目，保留 `_src` 溯源字段。
3. 提交推送。

## 版本发布策略

本源属于"内置源"性质的**网址型源**：源地址固定为 `https://raw.githubusercontent.com/kitblue/fnthird/main/fnpack.json`，更新源信息不会改变该地址。因此：

- **只在官方软件发版时才同步新版本**：上游（`_src` 指向的官方仓库）发布新 release 后，才把该版本写入 `fnpack.json`；
- **不删除任何历史版本**：`releases` 为累积字典，新版本只做追加，旧版本条目永久保留，商店/用户侧仍可回退安装；
- **本源自身不发布 GitHub Release / tag**：无需为源仓库新建版本号或发布包，源内容更新即生效；
- 上游 tag 必须是含点分版本号的语义 tag（如 `1.2.1`、`v26.10.23`、`magpie-v1.1.14`），中文说明式或无语义 tag 不入源；资产名须与 appname 或原资产名匹配，防止同仓库多应用抓错包。

## 每日自动检查更新

仓库内置 GitHub Actions（`.github/workflows/daily-update.yml`），每天自动检查已收录 app 的上游 GitHub Releases 是否有新版本：

- 脚本：`scripts/check_updates.py`（依据 `fnpack.json` 中每个 app 的 `_src` 定位上游仓库，查询最新 release）
- 校验值优先取 GitHub Release 资产自带的 `sha256` digest 与 size，无需逐个下载 fpk（仅在上游未提供 digest 时回退下载核算）
- 发现新版本时只把新版本**追加**进 `fnpack.json` 的 `releases` 并推送源信息（历史版本全部保留）
- 可手动触发：Actions 页面 Run workflow
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
