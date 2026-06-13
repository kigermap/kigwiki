# Kigurumi 编年志

Kigurumi 编年志是一个面向 kigurumi 社群的静态资料馆项目，用来整理公开可引用的社群编年史、地点志、人物传略、来源目录和参与流程。项目当前以 MkDocs Material 构建，强调资料来源、公开边界、多语言扩展和长期维护。

站点不是临时资讯页，而是一个“先立体例，再持续补录”的修志工程：编年负责按时间建立主轴，志目负责按地点、人物、来源等类别建立索引，参与页负责说明如何提交资料、校对线索和加入协作。

## 项目特性

- 使用 `MkDocs Material` 构建静态站，适合部署到 Cloudflare Pages、Netlify 或任意静态托管服务。
- 使用 `mkdocs-static-i18n` 维护文件夹式多语言结构，默认语言为 `zh-Hans`。
- 当前核心栏目包括首页、关于介绍、参与加入、贡献与支持、编年、年份目录、地点目录、人物目录和来源目录。
- 自定义 `extra.css` 和 `archive-ui.js` 提供资料馆风格、移动端导航、搜索提示和页面交互。
- 使用 `scripts/site_hooks.py` 在构建后修正 404 页面、语言入口和嵌套 sitemap 等静态站细节。
- 内容开发遵循“可公开、可追溯、可校勘、可持续维护”的原则。

## 技术栈

- Python 3.12+
- MkDocs
- Material for MkDocs
- mkdocs-static-i18n
- PyMdown Extensions
- Cloudflare Wrangler，用于 GitHub Actions 自动部署

## 目录结构

```text
.
├── docs/
│   ├── zh-Hans/                 # 简体中文，默认语言与内容母本
│   │   ├── index.md             # 首页
│   │   ├── about/index.md       # 关于介绍
│   │   ├── join/index.md        # 参与加入
│   │   ├── support/index.md     # 贡献与支持
│   │   ├── chronicle/index.md   # 编年总览
│   │   ├── years/index.md       # 年份目录
│   │   ├── places/index.md      # 地点目录
│   │   ├── people/index.md      # 人物目录
│   │   └── sources/index.md     # 来源目录
│   ├── zh-Hant/                 # 繁体中文
│   ├── en/                      # English
│   ├── ja/                      # 日本語
│   ├── ru/                      # Русский
│   └── assets/
│       ├── images/              # 共享图片与二维码等资源
│       ├── stylesheets/extra.css
│       └── javascripts/archive-ui.js
├── scripts/site_hooks.py        # MkDocs 构建后处理
├── mkdocs.yml                   # 站点、导航、多语言和主题配置
├── requirements.txt             # Python 依赖
├── netlify.toml                 # Netlify 构建配置
└── .github/workflows/pages.yml  # Cloudflare Pages 自动部署
```

## 本地开发

首次安装：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

启动本地预览：

```bash
source .venv/bin/activate
mkdocs serve -a 127.0.0.1:8021
```

打开 `http://127.0.0.1:8021` 查看站点。

构建静态站：

```bash
source .venv/bin/activate
mkdocs build --strict --clean
```

构建产物会输出到 `site/`。如果只是快速验证，也可以运行：

```bash
mkdocs build --clean
```

## 页面开发约定

每个页面优先在 `docs/zh-Hans/` 下维护，再根据需要补齐其他语言。同一路径页面会对应不同语言版本，例如：

```text
docs/zh-Hans/about/index.md
docs/zh-Hant/about/index.md
docs/en/about/index.md
docs/ja/about/index.md
docs/ru/about/index.md
```

如果某个语言暂时缺少同路径页面，`mkdocs-static-i18n` 会回退到默认语言内容。新增页面时需要同时检查：

- `mkdocs.yml` 顶层 `nav`
- `mkdocs.yml` 各语言 `plugins.i18n.languages[].nav`
- 页脚社交链接和 `extra.social` 是否需要加入入口
- `scripts/site_hooks.py` 中 404 默认导航是否需要同步
- 页面中的图片路径是否指向 `docs/assets/images/`
- 修改 CSS 或 JS 后是否需要更新 `mkdocs.yml` 中的版本查询参数，避免浏览器缓存旧资源

## 编年史页面如何开发

编年页面是全站资料主轴，当前由两个入口组成：

- `docs/zh-Hans/chronicle/index.md`：编年总览，用来说明编年体例、时间线和编辑方向。
- `docs/zh-Hans/years/index.md`：年份目录，用来按年度分卷管理事件、资料批次和待考事项。

开发编年内容时建议按以下顺序推进：

1. 先确认事件能否公开，是否涉及私人聊天、未授权照片、详细地址或敏感身份。
2. 记录基础字段：年份、月份或日期、事件名称、地点、相关人物、来源、公开范围、可信度、待考事项。
3. 把事件挂到正确的年份分卷，再从地点、人物、来源页面建立反向索引。
4. 对跨年度事件建立专题线索，说明起因、经过、影响和可引用来源。
5. 对来源不足的内容明确标记“待补来源”“待核日期”或“待确认授权”，不要把线索写成定论。

年度页面可以按这种结构扩展：

```markdown
# 2025 年

<section class="archive-page-intro" markdown>
  <p class="archive-kicker">Year Record</p>
  <h1>2025 年</h1>
  <p>这一年社群活动、资料整理、公开记录和待考线索的总体说明。</p>
</section>

## 年度概述

## 主要事件

| 日期 | 事件 | 地点 | 相关人物 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 2025-xx-xx | 待补事件名称 | 待补 | 待补 | 待补 | 待考 |

## 关联地点

## 关联人物

## 来源与待考
```

新增年度页后，需要在 `years/index.md` 添加入口，并在 `mkdocs.yml` 的编年导航中加入页面。

## 修志页面如何开发

“修志”是编年以外的分类整理工作，当前对应 `志目` 栏目：

- `docs/zh-Hans/places/index.md`：地点目录，记录会馆、工坊、展场、聚会空间、摄影棚、线上据点等。
- `docs/zh-Hans/people/index.md`：人物目录，记录公开可写的社群角色和贡献。
- `docs/zh-Hans/sources/index.md`：来源目录，维护照片、海报、访谈、网页存档等证据链。

开发志目页面时，重点不是堆叠资料，而是建立可长期维护的条目体例：

- 地点条目要说明公开名称、空间类型、社群功能、关联年份和来源依据，不公开敏感地址。
- 人物条目要尊重当事人意愿，使用本人同意的公开称谓或匿名代号，避免私人资料化。
- 来源条目要记录标题、作者或提供者、日期、原始位置、可访问状态、授权说明和引用格式。
- 每个志目条目都应该能回到至少一个编年事件或年度页面。
- 每个编年事件也应尽量链接到对应的地点、人物和来源。

地点条目可以按这种结构扩展：

```markdown
# 某地点公开名称

<section class="archive-page-intro" markdown>
  <p class="archive-kicker">Place Record</p>
  <h1>某地点公开名称</h1>
  <p>地点的公开说明，不包含敏感地址。</p>
</section>

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 空间类型 | 会馆 / 工坊 / 展场 / 线上据点 |
| 社群功能 | 活动、维护、展示、访谈、资料整理 |
| 关联年份 | 2024-至今 |
| 公开边界 | 可公开 / 需匿名 / 需模糊处理 |

## 相关纪事

## 来源依据

## 待考事项
```

人物和来源页面也应保持相同风格：先说明公开边界，再列可核实事实，最后保留待考说明。

## 内容与隐私原则

公开资料馆比普通 Wiki 更需要谨慎。提交内容前请确认：

- 是否有可靠来源，是否能说明资料来自哪里。
- 是否获得公开授权，是否需要署名、打码、匿名或延后发布。
- 是否涉及私人联系方式、详细地址、聊天记录、未授权照片或敏感身份。
- 是否把猜测、传闻和未核实线索写成了事实。
- 是否保留了上下文，避免断章取义地引用人物或事件。

原则上宁可暂缓发布，也不要把来源不明、授权不明或可能伤害当事人的资料写成公开事实。

## 样式与交互开发

- 全站样式集中在 `docs/assets/stylesheets/extra.css`。
- 页面交互集中在 `docs/assets/javascripts/archive-ui.js`。
- 图片、二维码、视觉素材放在 `docs/assets/images/`。
- 设计参考图放在 `docs/assets/design/`，不直接作为页面内容。
- 修改移动端导航、卡片、按钮、二维码等视觉组件后，需要在桌面和移动端都预览。
- 修改 `extra.css` 或 `archive-ui.js` 后，建议同步更新 `mkdocs.yml` 里的 `?v=...` 查询参数，避免缓存影响验证。

## 多语言策略

默认内容先写 `zh-Hans`。其他语言可以逐步补齐：

```text
zh-Hans -> zh-Hant -> en -> ja -> ru
```

新增中文页面后，如果其他语言暂时没有翻译，可以先依赖默认语言回退。等栏目稳定后，再补齐对应语言目录，并在各语言导航中加入对应标题。

## 部署

### Cloudflare Pages

项目包含 `.github/workflows/pages.yml`。推送到 `main` 分支后，GitHub Actions 会：

1. 安装 Python 依赖。
2. 运行 `mkdocs build --strict`。
3. 使用 Wrangler 发布 `site/` 到 Cloudflare Pages。

默认 Cloudflare Pages 项目名为 `kigwiki`。需要在 GitHub 仓库 `Settings -> Secrets and variables -> Actions` 配置：

```text
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID
```

### Netlify

项目也包含 `netlify.toml`：

```toml
[build]
command = "mkdocs build --strict"
publish = "site"
```

如果部署到 Netlify，确保构建环境使用 Python 3.12，并安装 `requirements.txt`。

## 常用检查命令

```bash
# 检查 Python hook 语法
python3 -m py_compile scripts/site_hooks.py

# 严格构建
mkdocs build --strict --clean

# 临时静态预览构建结果
python3 -m http.server 8021 --directory site
```

## 协作入口

站点的参与说明位于 `docs/zh-Hans/join/index.md`。当前页面提供 KigerMap 社区交流群入口：

- QQ 群号：`1067398012`
- 入群链接：`https://qm.qq.com/q/gpzX280qkw`

提交资料、修正页面或扩展栏目时，请优先说明资料来源、授权状态和希望公开到什么程度。
