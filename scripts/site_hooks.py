from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


DEFAULT_LANG = "zh-Hans"
DEFAULT_SITE_NAME = "Kigurumi 编年志"
DEFAULT_DESCRIPTION = "面向 kigurumi 社群的编年史、修志与资料馆。"
DEFAULT_NOT_FOUND_TITLE = "404 - 页面未找到"
DEFAULT_COPYRIGHT = (
    "Copyright &copy; 2026 Kigurumi 编年志资料馆。"
    "本站内容用于资料整理、研究与教育参考；引用时请保留署名、出处与语境。"
)
DEFAULT_NAV = """
  <ul class="md-nav__list" data-md-scrollfix>
    <li class="md-nav__item">
      <a href="/" class="md-nav__link">
        <span class="md-ellipsis">首页</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/about/" class="md-nav__link">
        <span class="md-ellipsis">关于介绍</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/join/" class="md-nav__link">
        <span class="md-ellipsis">参与加入</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/support/" class="md-nav__link">
        <span class="md-ellipsis">贡献与支持</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/chronicle/" class="md-nav__link">
        <span class="md-ellipsis">编年总览</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/years/" class="md-nav__link">
        <span class="md-ellipsis">年份目录</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/places/" class="md-nav__link">
        <span class="md-ellipsis">地点目录</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/people/" class="md-nav__link">
        <span class="md-ellipsis">人物目录</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/sources/" class="md-nav__link">
        <span class="md-ellipsis">来源目录</span>
      </a>
    </li>
  </ul>
"""
DEFAULT_PRIMARY_NAV = f"""
<nav class="md-nav md-nav--primary" aria-label="导航栏" data-md-level="0">
  <label class="md-nav__title" for="__drawer">
    <a href="/" title="{DEFAULT_SITE_NAME}" class="md-nav__button md-logo" aria-label="{DEFAULT_SITE_NAME}" data-md-component="logo">
      <img src="/assets/images/sample-archive.svg" alt="logo">
    </a>
    {DEFAULT_SITE_NAME}
  </label>
{DEFAULT_NAV}
</nav>
"""
DEFAULT_LANGUAGE_LIST = """
      <ul class="md-select__list">
        <li class="md-select__item">
          <a href="/" hreflang="zh-Hans" class="md-select__link">简体中文</a>
        </li>
        <li class="md-select__item">
          <a href="/zh-Hant/" hreflang="zh-Hant" class="md-select__link">繁體中文</a>
        </li>
        <li class="md-select__item">
          <a href="/en/" hreflang="en" class="md-select__link">English</a>
        </li>
        <li class="md-select__item">
          <a href="/ja/" hreflang="ja" class="md-select__link">日本語</a>
        </li>
        <li class="md-select__item">
          <a href="/ru/" hreflang="ru" class="md-select__link">Русский</a>
        </li>
      </ul>
"""
DEFAULT_SEARCH_TRANSLATIONS = {
    "clipboard.copied": "已复制到剪贴板",
    "clipboard.copy": "复制到剪贴板",
    "search.result.more.one": "此页还有 1 个结果",
    "search.result.more.other": "此页还有 # 个结果",
    "search.result.none": "没有找到符合条件的结果",
    "search.result.one": "找到 1 个符合条件的结果",
    "search.result.other": "找到 # 个符合条件的结果",
    "search.result.placeholder": "键入以开始搜索",
    "search.result.term.missing": "缺少",
    "select.version": "选择版本",
}


def _replace(pattern: str, replacement: str, text: str) -> str:
    return re.sub(pattern, replacement, text, flags=re.S)


def _replace_primary_nav(html: str) -> str:
    start = html.find('<nav class="md-nav md-nav--primary"')
    marker = html.find('<div class="md-sidebar md-sidebar--secondary"', start)
    if start < 0 or marker < 0:
        return html

    end = html.rfind("</nav>", start, marker)
    if end < 0:
        return html

    end += len("</nav>")
    return f"{html[:start]}{DEFAULT_PRIMARY_NAV}{html[end:]}"


def _patch_config(match: re.Match[str]) -> str:
    prefix, raw_config, suffix = match.groups()
    try:
        config = json.loads(raw_config)
    except json.JSONDecodeError:
        return match.group(0)

    config["base"] = "/"
    config["translations"] = DEFAULT_SEARCH_TRANSLATIONS
    return f"{prefix}{json.dumps(config, ensure_ascii=False, separators=(',', ':'))}{suffix}"


def _mirror_sitemaps(site_dir: Path) -> None:
    sitemap_files = [path for path in (site_dir / "sitemap.xml", site_dir / "sitemap.xml.gz") if path.exists()]
    if not sitemap_files:
        return

    for index_path in site_dir.rglob("index.html"):
        directory = index_path.parent
        if directory == site_dir:
            continue
        for sitemap_file in sitemap_files:
            shutil.copyfile(sitemap_file, directory / sitemap_file.name)


def on_post_build(config, **kwargs):
    site_dir = Path(config["site_dir"])
    _mirror_sitemaps(site_dir)

    path = site_dir / "404.html"
    if not path.exists():
        return

    html = path.read_text(encoding="utf-8")
    html = html.replace('<html lang="ru"', f'<html lang="{DEFAULT_LANG}"')
    html = html.replace('<body ', '<body class="archive-error-page" ', 1)
    html = _replace(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{DEFAULT_DESCRIPTION}">',
        html,
    )
    html = _replace(r"<title>.*?</title>", f"<title>404 - {DEFAULT_SITE_NAME}</title>", html)
    html = _replace(
        r'<link rel="alternate" href="[^"]*" hreflang="zh-Hans">',
        '<link rel="alternate" href="/" hreflang="zh-Hans">',
        html,
    )
    html = _replace(
        r'<link rel="alternate" href="[^"]*" hreflang="zh-Hant">',
        '<link rel="alternate" href="/zh-Hant/" hreflang="zh-Hant">',
        html,
    )
    html = _replace(
        r'<link rel="alternate" href="[^"]*" hreflang="en">',
        '<link rel="alternate" href="/en/" hreflang="en">',
        html,
    )
    html = _replace(
        r'<link rel="alternate" href="[^"]*" hreflang="ja">',
        '<link rel="alternate" href="/ja/" hreflang="ja">',
        html,
    )
    html = _replace(
        r'<link rel="alternate" href="[^"]*" hreflang="ru">',
        '<link rel="alternate" href="/ru/" hreflang="ru">',
        html,
    )
    html = html.replace('aria-label="Верхний колонтитул"', 'aria-label="页眉"')
    html = html.replace("Переключить на темную тему", "切换到深色模式")
    html = html.replace("Переключить на светлую тему", "切换到浅色模式")
    html = html.replace('aria-label="Выберите язык"', 'aria-label="选择当前语言"')
    html = html.replace('aria-label="Поиск"', 'aria-label="搜索"', 1)
    html = html.replace('placeholder="Поиск"', 'placeholder="搜索"')
    html = html.replace('aria-label="Поиск"', 'aria-label="查找"')
    html = html.replace('title="Поделиться" aria-label="Поделиться"', 'title="分享" aria-label="分享"')
    html = html.replace('title="Очистить" aria-label="Очистить"', 'title="清空当前内容" aria-label="清空当前内容"')
    html = html.replace("Инициализация поиска", "正在初始化搜索引擎")
    html = html.replace('aria-label="Содержание"', 'aria-label="目录"')
    html = html.replace(">К началу<", ">回到页面顶部<")
    html = _replace(r">\s*К началу\s*</button>", ">\n  回到页面顶部\n</button>", html)
    html = _replace(
        r'<ul class="md-select__list">.*?</ul>',
        DEFAULT_LANGUAGE_LIST.strip(),
        html,
    )
    html = _replace(
        r'(<a href=")/ru/(" title=")[^"]*(" class="md-header__button md-logo" aria-label=")[^"]*(")',
        rf'\1/\2{DEFAULT_SITE_NAME}\3{DEFAULT_SITE_NAME}\4',
        html,
    )
    html = _replace(
        r'(<a href=")/ru/(" title=")[^"]*(" class="md-nav__button md-logo" aria-label=")[^"]*(")',
        rf'\1/\2{DEFAULT_SITE_NAME}\3{DEFAULT_SITE_NAME}\4',
        html,
    )
    html = _replace(
        r'(<div class="md-header__topic">\s*<span class="md-ellipsis">\s*)[^<]*(\s*</span>)',
        rf"\g<1>{DEFAULT_SITE_NAME}\g<2>",
        html,
    )
    html = _replace(
        r'(<div class="md-header__topic" data-md-component="header-topic">\s*<span class="md-ellipsis">\s*)[^<]*(\s*</span>)',
        rf"\g<1>{DEFAULT_NOT_FOUND_TITLE}\g<2>",
        html,
    )
    html = _replace_primary_nav(html)
    html = _replace(
        r'(<a href=")/ru/(" target="_blank" rel="noopener" title=")Главная(" class="md-social__link")',
        r'\1/\2首页\3',
        html,
    )
    html = _replace(
        r'(<a href=")/ru/join/(" target="_blank" rel="noopener" title=")Участие(" class="md-social__link")',
        r'\1/join/\2参与加入\3',
        html,
    )
    html = _replace(
        r'(<a href=")/ru/chronicle/(" target="_blank" rel="noopener" title=")Хроника(" class="md-social__link")',
        r'\1/chronicle/\2编年目录\3',
        html,
    )
    html = _replace(
        r'(<a href=")/ru/places/(" target="_blank" rel="noopener" title=")Места(" class="md-social__link")',
        r'\1/places/\2地点目录\3',
        html,
    )
    html = _replace(
        r'(<a href=")/ru/about/(" target="_blank" rel="noopener" title=")О проекте(" class="md-social__link")',
        r'\1/about/\2关于介绍\3',
        html,
    )
    html = _replace(
        r'(<a href=")/ru/support/(" target="_blank" rel="noopener" title=")Поддержать(" class="md-social__link")',
        r'\1/support/\2贡献与支持\3',
        html,
    )
    html = html.replace(">К началу<", ">回到页面顶部<")
    html = _replace(
        r'<div class="md-copyright__highlight">.*?</div>',
        f'<div class="md-copyright__highlight">\n      {DEFAULT_COPYRIGHT}\n    </div>',
        html,
    )
    html = html.replace("<h1>404 - Not found</h1>", f"<h1>{DEFAULT_NOT_FOUND_TITLE}</h1>")
    html = _replace(
        r'(<script id="__config" type="application/json">)(.*?)(</script>)',
        _patch_config,
        html,
    )

    path.write_text(html, encoding="utf-8")
