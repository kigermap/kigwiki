from __future__ import annotations

import json
import re
import shutil
from html import unescape
from pathlib import Path


SITE_URL = "https://kigwiki.com/"
DEFAULT_LANG = "zh-Hans"
DEFAULT_SITE_NAME = "Kigurumi 编年志"
DEFAULT_DESCRIPTION = "面向 kigurumi 社群的编年史、修志与资料馆。"
DEFAULT_NOT_FOUND_TITLE = "404 - 页面未找到"
DEFAULT_IMAGE = f"{SITE_URL}assets/images/kigurumi-archive-hero-v2.png"
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
    <li class="md-nav__item">
      <a href="/citation/" class="md-nav__link">
        <span class="md-ellipsis">引用规范</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/faq/" class="md-nav__link">
        <span class="md-ellipsis">常见问题</span>
      </a>
    </li>
    <li class="md-nav__item">
      <a href="/license/" class="md-nav__link">
        <span class="md-ellipsis">开源协议</span>
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
PAGE_DESCRIPTIONS = {
    "/": "Kigurumi 编年志是面向 kigurumi 社群的公开资料馆，整理编年史、志目、人物、地点、来源和参与流程。",
    "/about/": "了解 Kigurumi 编年志的项目定位、资料馆体例、公开边界和长期修志目标。",
    "/join/": "了解如何参与 Kigurumi 编年志，提交资料、校对线索、翻译页面、维护站点并加入 KigerMap 社区交流群。",
    "/support/": "了解如何为 Kigurumi 编年志贡献资料、参与校对、支持维护和协助长期整理。",
    "/chronicle/": "Kigurumi 编年志编年总览，说明社群事件记录体例、预制时间线和年度资料整理方向。",
    "/years/": "Kigurumi 编年志年份目录，按年度浏览和补录事件、地点、人物、来源与待考事项。",
    "/years/2025/": "2025 年 Kigurumi 编年史，整理公开活动、跨境合作、官方 IP greeting、规则治理、产业链变化和年度图表。",
    "/zh-Hant/years/2025/": "2025 年 Kigurumi 編年史繁體中文整理版，收錄公開活動、跨境合作、官方 IP greeting、規則治理、產業鏈變化和年度圖表。",
    "/ja/years/2025/": "2025年 Kigurumi 編年史の日本語整理版。公開イベント、越境協力、公式 IP greeting、規則治理、産業変化を扱います。",
    "/ru/years/2025/": "Русская версия хроники Kigurumi 2025 года: публичные события, трансграничные связи, official IP greeting, правила и индустрия.",
    "/places/": "Kigurumi 编年志地点目录，记录会馆、工坊、展场、聚会空间、线上据点等公开可写的社群空间。",
    "/people/": "Kigurumi 编年志人物目录，记录公开可写的社群角色、贡献、参与阶段和来源依据。",
    "/sources/": "Kigurumi 编年志来源目录，维护照片、手册、访谈、网页存档和公开说明等证据链。",
    "/citation/": "Kigurumi 编年志引用规范，说明如何引用页面、事件、地点、人物、来源和素材并保留语境。",
    "/faq/": "Kigurumi 编年志常见问题，介绍项目是什么、成立目的、如何加入、免费开源和隐私原则。",
    "/license/": "Kigurumi 编年志开源协议说明，区分网站代码 MIT License、原创文字 CC BY 4.0 与第三方素材授权边界。",
}
LANG_PREFIXES = ("/zh-Hant", "/en", "/ja", "/ru")
FAQ_ITEMS = [
    (
        "基础介绍：Kigurumi 编年志是什么？",
        "Kigurumi 编年志是一个面向 kigurumi 社群的公开资料馆和修志项目，以静态网站形式整理公开介绍、编年线索、地点目录、人物贡献、来源目录、参与流程和引用规范。",
    ),
    (
        "成立目的：这个项目为什么成立？",
        "项目成立的目的，是把分散在活动现场、相册、访谈、网页、制作笔记和成员记忆中的公开资料，整理成可阅读、可引用、可校勘、可持续维护的资料体系。",
    ),
    (
        "如何加入：我可以怎样参与？",
        "你可以反馈错字、补充年份线索、校对地点说明、提供公开来源、整理照片批次、翻译页面或维护站点，也可以通过 QQ 群 1067398012 加入 KigerMap 社区交流群。",
    ),
    (
        "免费开源：Kigurumi 编年志是免费开源的吗？",
        "是的。站点面向公众免费访问，网站代码采用 MIT License 开源；原创说明文字默认采用 CC BY 4.0，可在署名、附链接、保留语境并标注改动的前提下分享和改写。第三方图片、访谈、海报、二维码和用户投稿仍保留原始权利。",
    ),
]


def _absolute_url(path: str) -> str:
    return f"{SITE_URL.rstrip('/')}/{path.lstrip('/')}"


def _page_url_from_output(site_dir: Path, path: Path) -> str:
    relative = path.relative_to(site_dir).as_posix()
    if relative == "index.html":
        return SITE_URL
    if relative.endswith("/index.html"):
        relative = relative[: -len("index.html")]
    return _absolute_url(relative)


def _canonical_path_from_output(site_dir: Path, path: Path) -> str:
    relative = path.relative_to(site_dir).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        relative = "/" + relative[: -len("index.html")]
    else:
        relative = "/" + relative
    return relative


def _content_path(pathname: str) -> str:
    for prefix in LANG_PREFIXES:
        if pathname == f"{prefix}/":
            return "/"
        if pathname.startswith(f"{prefix}/"):
            return pathname[len(prefix) :]
    return pathname


def _page_description(pathname: str) -> str:
    if pathname in PAGE_DESCRIPTIONS:
        return PAGE_DESCRIPTIONS[pathname]
    return PAGE_DESCRIPTIONS.get(_content_path(pathname), DEFAULT_DESCRIPTION)


def _extract_title(html: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    if not match:
        return DEFAULT_SITE_NAME
    return unescape(re.sub(r"\s+", " ", match.group(1)).strip())


def _extract_lang(html: str) -> str:
    match = re.search(r'<html lang="([^"]+)"', html)
    return match.group(1) if match else "zh"


def _meta_tag(name: str, content: str) -> str:
    return f'<meta name="{name}" content="{content}">'


def _property_tag(prop: str, content: str) -> str:
    return f'<meta property="{prop}" content="{content}">'


def _replace_or_insert_head(html: str, pattern: str, replacement: str) -> str:
    if re.search(pattern, html, flags=re.S):
        return re.sub(pattern, replacement, html, count=1, flags=re.S)
    return html.replace("</head>", f"  {replacement}\n  </head>", 1)


def _drop_managed_seo(html: str) -> str:
    html = re.sub(r'\s*<link rel="canonical" href="[^"]*">\n?', "\n", html)
    html = re.sub(r'\s*<meta (?:name|property)="(?:og:[^"]+|twitter:[^"]+)" content="[^"]*">\n?', "\n", html)
    html = re.sub(r'\s*<script type="application/ld\+json" data-archive-seo>.*?</script>\n?', "\n", html, flags=re.S)
    return html


def _json_ld(page_url: str, title: str, description: str, pathname: str, lang: str) -> list[dict]:
    home_url = _absolute_url("/")
    graph: list[dict] = [
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "@id": f"{home_url}#website",
            "url": home_url,
            "name": DEFAULT_SITE_NAME,
            "description": DEFAULT_DESCRIPTION,
            "inLanguage": lang,
            "publisher": {"@id": f"{home_url}#organization"},
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{home_url}?q={{search_term_string}}",
                "query-input": "required name=search_term_string",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "@id": f"{home_url}#organization",
            "name": "Kigurumi Chronicle Archive",
            "alternateName": ["Kigurumi 编年志", "KigerMap 社区资料馆"],
            "url": home_url,
            "logo": _absolute_url("/assets/images/sample-archive.svg"),
        },
    ]

    content_path = _content_path(pathname)
    page_type = "WebPage" if content_path == "/" else "Article"
    graph.append(
        {
            "@context": "https://schema.org",
            "@type": page_type,
            "@id": f"{page_url}#webpage",
            "url": page_url,
            "name": title,
            "headline": title,
            "description": description,
            "inLanguage": lang,
            "isPartOf": {"@id": f"{home_url}#website"},
            "publisher": {"@id": f"{home_url}#organization"},
            "image": DEFAULT_IMAGE,
        }
    )

    crumbs = [{"@type": "ListItem", "position": 1, "name": "首页", "item": home_url}]
    if content_path != "/":
        crumbs.append({"@type": "ListItem", "position": 2, "name": title.split(" - ")[0], "item": page_url})
        graph.append(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "@id": f"{page_url}#breadcrumb",
                "itemListElement": crumbs,
            }
        )

    if content_path == "/faq/":
        graph.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "@id": f"{page_url}#faq",
                "url": page_url,
                "inLanguage": lang,
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in FAQ_ITEMS
                ],
            }
        )

    return graph


def _inject_seo(html: str, *, page_url: str, pathname: str) -> str:
    html = _drop_managed_seo(html)
    title = _extract_title(html)
    lang = _extract_lang(html)
    description = _page_description(pathname)
    og_type = "website" if _content_path(pathname) == "/" else "article"

    html = _replace(
        r'<meta name="description" content="[^"]*">',
        _meta_tag("description", description),
        html,
    )
    html = _replace_or_insert_head(html, r'<meta name="robots" content="[^"]*">', _meta_tag("robots", "index,follow"))

    tags = [
        f'<link rel="canonical" href="{page_url}">',
        _property_tag("og:type", og_type),
        _property_tag("og:site_name", DEFAULT_SITE_NAME),
        _property_tag("og:title", title),
        _property_tag("og:description", description),
        _property_tag("og:url", page_url),
        _property_tag("og:image", DEFAULT_IMAGE),
        _meta_tag("twitter:card", "summary_large_image"),
        _meta_tag("twitter:title", title),
        _meta_tag("twitter:description", description),
        _meta_tag("twitter:image", DEFAULT_IMAGE),
        (
            '<script type="application/ld+json" data-archive-seo>'
            + json.dumps(_json_ld(page_url, title, description, pathname, lang), ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        ),
    ]
    return html.replace("</head>", "\n      " + "\n      ".join(tags) + "\n  </head>", 1)


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


def _patch_html_pages(site_dir: Path) -> None:
    for path in site_dir.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        pathname = _canonical_path_from_output(site_dir, path)
        html = _inject_seo(html, page_url=_page_url_from_output(site_dir, path), pathname=pathname)
        path.write_text(html, encoding="utf-8")


def on_post_build(config, **kwargs):
    site_dir = Path(config["site_dir"])
    _patch_html_pages(site_dir)
    _mirror_sitemaps(site_dir)

    path = site_dir / "404.html"
    if not path.exists():
        return

    html = path.read_text(encoding="utf-8")
    html = _drop_managed_seo(html)
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
    html = _inject_seo(html, page_url=_absolute_url("/404.html"), pathname="/404.html")

    path.write_text(html, encoding="utf-8")
