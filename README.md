# 飞牛 fnOS 应用 Manifest 收录源

本项目是一个 **飞牛 fnOS 第三方应用源**，可为第三方应用商店（如 FnDepot）直接收录。

**定位**：为有 manifest 但缺 fnpack.json 的原生 app 项目，以及其他尚未编写源的 app 项目，提供一条被商店收录的路径。

## 源信息

- 源名：`fnos-apps-manifests`
- 源文件：`fnpack.json`（FnDepot V2 schema）
- 收录应用：见 `fnpack.json` 的 `apps` 字段

第三方应用商店添加本仓库为源后，即可安装其中收录的应用。

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
