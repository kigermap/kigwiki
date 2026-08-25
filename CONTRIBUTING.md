# 贡献指南

感谢你帮助维护 Kigurumi 编年志。项目接受史料补录、事实校勘、翻译、无障碍改进、样式修复和工程维护。提交内容前，请先确认资料适合公开，并保留可复核的来源与授权边界。

## 开始之前

- 公开 Issue 可以用于一般错误、功能建议和不含敏感信息的资料线索。
- 私人联系方式、详细地址、未公开身份、私人聊天、未授权照片及安全漏洞不得放入公开 Issue 或 Pull Request。
- 第三方图片、海报、访谈和社交平台内容不会因进入仓库而自动采用项目许可；请写明原作者、原始位置和授权状态。
- 行为与协作要求见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)，安全问题见 [SECURITY.md](SECURITY.md)。

## 本地验证

项目要求 Python 3.12 或更高版本。安装依赖后，提交前依次运行：

```bash
python3 -m py_compile scripts/build_indexes.py scripts/site_hooks.py
python3 scripts/build_indexes.py
git diff --check
mkdocs build --strict --clean
```

`scripts/build_indexes.py` 会检查年度和月度档案的语言路径、前置元数据、索引入口及导航数量。严格构建必须无站点警告地完成。

## 内容贡献

每条可发布记录至少应包含：日期或时间范围、主题、公开来源、证据边界和仍未确认的事项。请区分活动预告、参与者记录与主办方结项，不根据播放量、投稿量、照片数量或小说情节推算参与规模或现实事件。

年度内容按一个年份一卷维护，已整理年份不重复建立。跨年度连续主题只在首次可核验节点保留完整背景，后续年份记录实际变化并回链。月度采集在同一个月份页面中滚动更新，不建立重复的日页面。

自动化发布的年度编年与月度采集必须同时提供以下五种语言：

```text
zh-Hans
zh-Hant
en
ja
ru
```

新增档案页时，还需同步更新五个语言索引、五个编年索引、`mkdocs.yml` 的语言导航与默认导航，以及 `scripts/site_hooks.py` 的本地化页面描述。

## Pull Request

- 保持改动聚焦，避免把内容更新和无关重构放在同一个 Pull Request。
- 在说明中列出新增或更改的来源、去重判断、授权限制和已运行的验证命令。
- 不提交 `site/`、虚拟环境、缓存、凭据或本地配置。
- 修改样式或交互时，同时检查桌面与移动端；修改静态资源后同步更新 `mkdocs.yml` 中的缓存版本参数。

代码使用 MIT License；项目原创整理文字默认使用 CC BY 4.0；第三方资料仍由原权利人控制。完整边界见 [LICENSE-CONTENT.md](LICENSE-CONTENT.md)。
