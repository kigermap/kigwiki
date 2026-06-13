# 部署指南

## Cloudflare Pages

这个工程已经内置 GitHub Actions workflow。推送到 GitHub `main` 分支后，会自动构建并发布到 Cloudflare Pages。

自动流程会执行：

1. 安装 Python 依赖。
2. 根据 `data/*.yml` 生成多语言索引页。
3. 构建 MkDocs 静态站。
4. 使用 Wrangler 发布到 Cloudflare Pages。

GitHub 仓库需要配置两个 Actions Secrets：

| Secret | 说明 |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API Token，需要 Cloudflare Pages 编辑权限 |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare 账号 ID |

默认 Cloudflare Pages 项目名是 `kigwiki`。如果项目还没创建，可以先在本地执行：

```bash
npx wrangler pages project create kigwiki --production-branch=main
```

## Cloudflare Pages 控制台导入

如果不用 GitHub Actions，也可以在 Cloudflare Pages 控制台直接连接 GitHub 仓库：

| 配置项 | 推荐值 |
| --- | --- |
| Production branch | `main` |
| Build command | `pip install -r requirements.txt && python scripts/build_indexes.py && mkdocs build --strict` |
| Build output directory | `site` |
| Environment variable | `PYTHON_VERSION=3.12` |

部署后会得到一个 `*.pages.dev` 域名，也可以绑定自定义域名。

## GitHub Pages

当前 workflow 默认发布到 Cloudflare Pages。如果要改回 GitHub Pages，需要把 `.github/workflows/pages.yml` 中的部署步骤替换为 `actions/configure-pages`、`actions/upload-pages-artifact` 和 `actions/deploy-pages`。

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
