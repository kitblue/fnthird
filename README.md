---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 257c07a97525093c65a112a601161c42_24c2cf9dc91011f18b7f525400393706
    ReservedCode1: A7i421u+ZG81jzABiR6bB3hKneh7L3ZBolEDYQnnuLz/WzUiothBjyEs4DxHAmW1VS8ez/ECDdr8hwG+UgbIdwR9ZBdsOD6St1qUJzXeXsl0c8xJMEEtQhxa3IfDLX+GSZ16ilwipue1lpANteq08hjQ56ezH+6Xan7NHklndlc0k9oGZDyNrJaaf8c=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 257c07a97525093c65a112a601161c42_24c2cf9dc91011f18b7f525400393706
    ReservedCode2: A7i421u+ZG81jzABiR6bB3hKneh7L3ZBolEDYQnnuLz/WzUiothBjyEs4DxHAmW1VS8ez/ECDdr8hwG+UgbIdwR9ZBdsOD6St1qUJzXeXsl0c8xJMEEtQhxa3IfDLX+GSZ16ilwipue1lpANteq08hjQ56ezH+6Xan7NHklndlc0k9oGZDyNrJaaf8c=
---

# 飞牛 fnOS 应用 Manifest 收录源

本项目是一个 **飞牛 fnOS 第三方应用源**，可为第三方应用商店（如 FnDepot）直接收录。

**定位**：为有 manifest 但缺 fnpack.json 的原生 app 项目，以及其他尚未编写源的 app 项目，提供一条被商店收录的路径。

## 源信息

- 源名：`fnthird`
- 源文件：`fnpack.json`（FnDepot V2 schema）
- 收录应用：见 `fnpack.json` 的 `apps` 字段

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
- 有可读取的 manifest 文件
- 非 fnpack.json 标准格式（原生 manifest）
- 项目活跃、非僵尸仓库

## 新增项目

1. 在 `manifests/<owner>-<repo>/manifest.json` 保存原 manifest 的 JSON 化版本
2. 在 `fnpack.json` 的 `apps` 中添加对应应用条目（含 releases 下载信息）
3. 提交推送

## 每日自动检查更新

仓库内置 GitHub Actions（`.github/workflows/daily-update.yml`），每天自动检查已收录 app 的上游 GitHub Releases 是否有新版本：

- 脚本：`scripts/check_updates.py`（依据 `fnpack.json` 中每个 app 的 `_src` 定位上游仓库，查询最新 release，重新下载资产并核算 sha256/size）
- 发现新版本时自动更新 `fnpack.json` 的 releases 字段并推送（仅保留最新版本）
- 可手动触发：Actions 页面 Run workflow
*（内容由AI生成，仅供参考）*
