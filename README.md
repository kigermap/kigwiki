# 编年史 / 修志 Wiki

这是一个无数据库的静态 Wiki 工程，适合做地方志、校史、家族史、机构史、项目编年等长期维护型资料站。

核心思路：

- 正文放在 `docs/`，用 Markdown 写。
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
  chronicle/     编年说明
  gazetteer/     志书分目
  people/        人物专页
  places/        地点专页
  sources/       资料来源说明
```

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

它会更新 `docs/generated/` 下的自动索引页。

## GitHub Pages 部署

本工程已经带了 `.github/workflows/pages.yml`。推送到 GitHub 后：

1. 新建 GitHub 仓库。
2. 把本目录推送到仓库的 `main` 分支。
3. 到仓库 `Settings -> Pages`。
4. Source 选择 `GitHub Actions`。
5. 之后每次 push 都会自动构建并发布。

常用推送命令：

```bash
git init
git add .
git commit -m "Initial chronicle wiki"
git branch -M main
git remote add origin https://github.com/<your-name>/<repo-name>.git
git push -u origin main
```

## 免费线上方案

- GitHub Pages：最省事，适合公开仓库，仓库协作者可编辑，所有人可访问。
- Cloudflare Pages：免费额度慷慨，国内外访问速度通常不错，适合绑定自己的域名。
- Netlify：配置简单，适合静态站和预览部署。

如果编辑者不懂 Git，可以后续加 Decap CMS，让编辑者通过网页后台提交 Markdown 到仓库。

