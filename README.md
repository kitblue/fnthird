# 飞牛 fnOS 应用 Manifest 收录

收录飞牛 fnOS 第三方应用中 **有 manifest 但缺 fnpack.json** 的项目。

## 格式

每个项目放在 `manifests/<owner>-<repo>/manifest.json`，内容为原 manifest 的 JSON 化版本。

## 收录标准

- 已发布到飞牛 fnOS 第三方应用中心
- 有可读取的 manifest 文件
- 非 fnpack.json 标准格式
- 项目活跃、非僵尸仓库

## 示例

```
manifests/
  eric0101-fnos-terminal/
    manifest.json    # 终端应用 manifest
```

## 新增项目

提交新 manifest JSON 到 `manifests/<owner>-<repo>/manifest.json`。
