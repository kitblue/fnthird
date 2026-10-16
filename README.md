# 飞牛 fnOS 应用收录源（fnthird）

本项目是 **FnUnify 聚合源的子源**，作为飞牛 fnOS 第三方应用源，可为第三方应用商店（如 FnDepot）直接收录。

**定位**：收录两类内容——

1. **原生 manifest 应用**：有 manifest 但缺 `fnpack.json` 的原生 app 项目；
2. **独立应用条目**：已有完整 fnpack 条目的独立应用（如 **FanTune**，原 KITblue/fantune 仓库的 `fancontrolserver` 应用；以及 **Blue-Mink/FnDepot** 中的 9 个独立应用条目：global-radio、com.trek.app、com.dongguaha.vm、new-api、dockflare、dog-dev、kspeeder、com.istoreos.vm、ryzen-power-control）。

其中 FanTune 等独立应用仅在本源以索引条目形式收录（条目 `_src` 保留 `KITblue/fantune` 溯源），原仓库本体不做转移，其索引收录由本源承接。

## 源信息

- 源名：`fnthird`
- 源文件：`fnpack.json`（FnDepot V2 schema）
- 收录应用：**41 条**（均为带 `_src` 溯源的上游应用条目，含承接的 FanTune 独立应用）

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

## 每日自动检查更新

仓库内置 GitHub Actions（`.github/workflows/daily-update.yml`），每天自动检查已收录 app 的上游 GitHub Releases 是否有新版本：

- 脚本：`scripts/check_updates.py`（依据 `fnpack.json` 中每个 app 的 `_src` 定位上游仓库，查询最新 release，重新下载资产并核算 sha256/size）
- 发现新版本时自动更新 `fnpack.json` 的 releases 字段并推送（仅保留最新版本）
- 可手动触发：Actions 页面 Run workflow
