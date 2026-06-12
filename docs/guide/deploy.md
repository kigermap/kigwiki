# 部署指南

## GitHub Pages

这个工程已经内置 GitHub Actions workflow。推送到 GitHub 后，到仓库 `Settings -> Pages`，把 Source 设为 `GitHub Actions`。

之后每次推送到 `main` 分支都会自动：

1. 安装 Python 依赖。
2. 根据 `data/*.yml` 生成索引页。
3. 构建 MkDocs 静态站。
4. 发布到 GitHub Pages。

## Cloudflare Pages

Cloudflare Pages 也适合这个工程。连接 GitHub 仓库后可用：

| 配置项 | 值 |
| --- | --- |
| Production branch | `main` |
| Build command | `pip install -r requirements.txt && python scripts/build_indexes.py && mkdocs build --strict` |
| Build output directory | `site` |
| Environment variable | `PYTHON_VERSION=3.12` |

部署后会得到一个 `*.pages.dev` 域名，也可以绑定自定义域名。

## Netlify

仓库里已经带 `netlify.toml`，导入仓库后 Netlify 会使用：

```toml
[build]
command = "python scripts/build_indexes.py && mkdocs build --strict"
publish = "site"
```

## 权限模型

静态站没有后端登录系统。推荐的权限模型是：

- 读者：访问公开网站。
- 编辑者：加入 GitHub/GitLab 仓库协作者。
- 审核者：通过 Pull Request 审核修改。
- 站点发布：由 CI 自动构建。

如果后续需要网页后台编辑，可以加 Decap CMS，但建议先用 Git 工作流跑通内容结构。

