# 编年史 / 修志 Wiki

这是一个无数据库的静态 Wiki 工程，适合做地方志、校史、家族史、机构史、项目编年等长期维护型资料站。

核心思路：

- 正文按语言放在 `docs/<locale>/`，用 Markdown 写。默认源语言是 `docs/zh-Hans/`。
- 事件、人物、地点、来源放在 `data/*.yml`，方便生成索引。
- 编辑权限交给 GitHub/GitLab 仓库权限控制。
- 公开阅读通过 GitHub Pages、Cloudflare Pages、Netlify 等静态托管实现。
- 不需要数据库，不需要后端服务。

## 本地预览

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_indexes.py
mkdocs serve
```

打开 `http://127.0.0.1:8000` 查看。

## 日常编辑

编辑正文：

```text
docs/
  zh-Hans/       简体中文源内容，也是未翻译页面的默认回退
  zh-Hant/       繁体中文翻译
  en/            英文翻译
  ja/            日语翻译
  ru/            俄语翻译
  assets/        所有语言共享的图片、样式和脚本
```

每种语言目录内部保持相同路径，例如：

```text
docs/zh-Hans/places/county-seat.md
docs/en/places/county-seat.md
docs/ja/places/county-seat.md
```

如果某个语言暂时没有同路径页面，构建会回退到 `docs/zh-Hans/` 的默认页面。

编辑结构化资料：

```text
data/events.yml   事件
data/people.yml   人物
data/places.yml   地点
data/sources.yml  来源
```

修改 `data/*.yml` 后运行：

```bash
python scripts/build_indexes.py
```

它会更新 `docs/<locale>/generated/` 下的自动索引页。

## Cloudflare Pages 自动部署

本工程已经带了 `.github/workflows/pages.yml`。每次推送到 GitHub `main` 分支后，GitHub Actions 会自动：

1. 安装 Python 依赖。
2. 根据 `data/*.yml` 生成多语言索引页。
3. 构建 MkDocs 静态站到 `site/`。
4. 使用 Wrangler 发布到 Cloudflare Pages。

Cloudflare Pages 项目名默认是 `kigwiki`。需要在 GitHub 仓库 `Settings -> Secrets and variables -> Actions` 添加：

```text
CLOUDFLARE_API_TOKEN   Cloudflare API Token，需要 Cloudflare Pages 编辑权限
CLOUDFLARE_ACCOUNT_ID  Cloudflare 账号 ID
```

如果 Cloudflare Pages 里还没有 `kigwiki` 项目，可以先在本地登录 Wrangler 后执行一次：

```bash
npx wrangler pages project create kigwiki --production-branch=main
```

常用推送命令：

```bash
git init
git add .
git commit -m "Initial kigwiki"
git branch -M main
git remote add origin https://github.com/kigermap/kigwiki.git
git push -u origin main
```

## 免费线上方案

- Cloudflare Pages：免费额度慷慨，国内外访问速度通常不错，适合绑定自己的域名。
- GitHub Pages：也可用，但当前 workflow 默认发布到 Cloudflare Pages。
- Netlify：配置简单，适合静态站和预览部署。

如果编辑者不懂 Git，可以后续加 Decap CMS，让编辑者通过网页后台提交 Markdown 到仓库。
