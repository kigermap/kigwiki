"""Render the reviewed maker dataset as crawlable MkDocs pages. No network at build time."""
from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

import yaml
import material
from build_shop_collection import entry_html, load_collection, LABELS, entry_images
from maker_ui import chips, cover, fact, gallery

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/assets/data/makers.yml"
DEST = ROOT / "docs/zh-Hans/makers"
ASSETS = ROOT / "docs/assets/images/makers"
STATUS = {"sales": "公开销售", "inquiry": "接受询价", "lottery": "周期抽选", "paused": "暂停定制", "unverified": "接单待核实"}
ACTIVE = {"sales", "inquiry", "lottery"}
COLLECTION = load_collection()
COLLECTION_ENTRIES = {entry['id']: entry for entry in COLLECTION['entries']}


def confirmed_platforms(maker):
    return list(dict.fromkeys(c[0] for c in maker["channels"] if not c[3].startswith("第三方")))


def esc(value):
    return escape(str(value), quote=True)


def link(label, url):
    if urlsplit(url).scheme not in {"https", "http", "mailto", "tel"}:
        raise ValueError(f"Unsupported public URL: {url}")
    return f'<a href="{esc(url)}" rel="noopener noreferrer">{esc(label)}</a>'


def ref(maker, key):
    if key not in maker["sources"]:
        raise ValueError(f"Missing source {key} for {maker['id']}")
    return f'<a href="#source-{esc(key)}">来源</a>'


def image_path(maker, kind):
    paths = sorted(ASSETS.glob(f"{maker['id']}-{kind}.*"))
    paths = [path for path in paths if path.suffix != ".json"]
    return paths[0] if paths else None


def artwork(maker):
    images = []
    photo = image_path(maker, 'photo')
    if photo:
        images.append({'src': f'/assets/images/makers/{photo.name}', 'caption': maker['photo_caption'], 'credit': f'#source-{maker["photo_source"]}'})
    for key in maker.get('collection_entries', []):
        entry = COLLECTION_ENTRIES[key]
        for image in entry_images(entry):
            if not any(x['src'] == image['src'] for x in images):
                images.append(image)
    return images


def brand_image(maker):
    path = image_path(maker, 'logo')
    return f'/assets/images/makers/{path.name}' if path else None


def style_tags(maker):
    tags = [c for c in maker['categories'] if c != '头壳（合集记录）']
    for key in maker.get('collection_entries', []):
        entry = COLLECTION_ENTRIES[key]
        if entry['category'] == 'anime':
            tags += [x.strip() for x in re.split('[，,、；;]', entry['fields'].get('风格适配（关键词 tag）', '')) if x.strip() and len(x.strip()) <= 20]
    return list(dict.fromkeys(tags))[:3]


def collection_section(maker):
    if not maker.get('collection_entries'):
        return ''
    only = maker.get('collection_only')
    opening = '<section class="maker-section" id="community"><h2>委托资料</h2>' if only else '<details class="maker-disclosure" id="community"><summary>社群补充资料 <span>飞书合集 · 2026-11-03</span></summary><div class="maker-disclosure-body">'
    lines = [opening, '<span id="2026-11-03" class="maker-anchor"></span><p class="maker-caption">禾芷溪溪溪溪溪溪整理的社群资料，价格、工期与批注保留原文口径。<a href="../collection/">浏览合集</a> · <a href="../../sources/shop-collections/hezhi-2026/">完整图文与校勘</a></p>']
    for key in maker['collection_entries']:
        entry = COLLECTION_ENTRIES[key]
        assert entry.get('maker_id') == maker['id'], key
        for note in COLLECTION['editorial_notes']:
            if note['entry_name'] == entry['name']:
                lines.append('<p class="maker-notice"><strong>校勘：</strong>' + esc(note['note']) + '</p>')
        lines.append(entry_html(entry, heading=len(maker['collection_entries']) > 1, show_images=False))
    lines.append('</section>' if only else '</div></details>')
    return '\n'.join(lines)


def contact_section(maker):
    lines = ['<section class="maker-section maker-contact-section" id="contact"><h2 id="_2">联系店铺</h2><p class="maker-caption">公开入口与业务联系方式</p><div class="maker-contact-list">']
    for platform, title, url, evidence, source in maker['channels']:
        lines.append(f'<div class="maker-contact"><a href="{esc(url)}" rel="noopener noreferrer"><span class="maker-contact-kind">{esc(platform)}</span><strong>{esc(title)}</strong><span aria-hidden="true">↗</span></a><small>{esc(evidence)} · {ref(maker, source)}</small></div>')
    lines.append('<span id="_3" class="maker-anchor"></span>')
    for kind, value, url, source in maker['contacts']:
        lines.append(f'<div class="maker-contact"><a href="{esc(url)}" rel="noopener noreferrer"><span class="maker-contact-kind">{esc(kind)}</span><strong>{esc(value)}</strong><span aria-hidden="true">↗</span></a><small>{ref(maker, source)}</small></div>')
    if not maker['channels'] and not maker['contacts']:
        lines.append('<p>暂无已记录的公开入口，可查看文末来源。</p>')
    lines.append('</div></section>')
    return '\n'.join(lines)


def product_section(maker):
    if not maker['products']:
        return ''
    lines = ['<section class="maker-section" id="products"><h2 id="_4">商品与报价</h2><p class="maker-caption">保留核实时的币种与报价口径。订金、配件和完整头壳分别标注，最终配置与档期请向店铺确认。</p><div class="maker-products">']
    for title, kind, currency, amount, basis, note, source in maker['products']:
        price = f'{currency} {amount}'.strip() if amount else '向店铺询价'
        lines.append(f'<article class="maker-product"><span class="maker-product-kind">{esc(kind)}</span><h3>{esc(title)}</h3><p class="maker-product-price">{esc(price)}</p><p class="maker-product-basis">{esc(basis)}</p><p class="maker-product-note">{esc(note)}</p>{ref(maker, source)}</article>')
    lines.append('</div></section>')
    return '\n'.join(lines)


def detail(maker, checked):
    name = maker['name']; only = maker.get('collection_only', False); images = artwork(maker)
    entry = next((COLLECTION_ENTRIES[k] for k in maker.get('collection_entries', []) if COLLECTION_ENTRIES[k]['category'] == 'anime'), None)
    lead = entry['fields'].get('工期时间') if entry else None
    price = maker['price_summary'].removeprefix('原文参考：')
    if price == '未填写': price = '报价待补充'
    primary = next((c for c in maker['channels'] if not c[3].startswith('第三方')), None)
    if primary is None and only and maker['channels']: primary = maker['channels'][0]
    lines = ['---', f'title: {json.dumps(name,ensure_ascii=False)}', f'description: {json.dumps(maker["summary"],ensure_ascii=False)}', 'hide:', '  - toc', '---', '', '<!-- Generated by scripts/build_makers.py; edit the structured datasets. -->', '', '<div class="maker-page maker-profile">',
             '<p class="maker-back"><a href="../">← 头壳店铺目录</a></p>', '<section class="maker-profile-hero">', gallery(images, name, brand_image(maker)), '<div class="maker-profile-overview">',
             f'<div class="maker-profile-eyebrow"><span>MAKER / {esc(maker["id"].upper())}</span><span class="maker-status maker-status--{maker["status"]}">{STATUS[maker["status"]]}</span></div>',
             f'<h1>{esc(name)}</h1><p class="maker-profile-summary">{esc(maker["summary"])}</p>', chips(style_tags(maker)),
             '<dl class="maker-quick-facts">', fact('合集参考价' if only else '公开价格摘要', price), fact('合集工期' if lead else '工期', lead or '以店铺确认为准'), fact('所在地区', maker['region']), fact('资料采集' if only else '第一方核实', checked), '</dl>', '<div class="maker-actions">']
    if primary:
        label = '合集所列店铺' if only else f'前往{primary[0]}'
        lines.append(f'<a class="maker-button maker-button--primary" href="{esc(primary[2])}" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>')
    lines.append('<a class="maker-button" href="#contact">联系方式 ↓</a></div>')
    lines.append('<p class="maker-caption">社群资料，尚待第一方复核；报价与接单情况请向店家确认。</p>' if only else '<p class="maker-caption">以上为公开资料快照；合集工期来自社群记录，当前报价与档期请向店家确认。</p>')
    lines += ['</div></section>', '<nav class="maker-section-nav" aria-label="店铺页面导航"><a href="#about">店铺介绍</a>']
    if maker['products']: lines.append('<a href="#products">商品与报价</a>')
    if maker.get('collection_entries'): lines.append('<a href="#community">委托资料</a>')
    lines += ['<a href="#contact">联系店铺</a><a href="#sources">资料来源</a></nav>', '<div class="maker-detail-grid"><div class="maker-detail-main">', '<section class="maker-section" id="about"><h2 id="_1">店铺与委托</h2>', f'<p>{esc(maker["description"])}</p>']
    if not only: lines.append(f'<p id="_5">{esc(maker["terms"])}</p>')
    lines += ['<dl class="maker-info-pairs">', fact('所在地', maker['location']), fact('名称与别名', ' / '.join(maker['aliases'])), fact('商品与服务', ' · '.join(maker['categories'])), '</dl>']
    if maker.get('address'): lines.append(f'<p>{esc(maker["address"])}</p>')
    lines += ['</section>', product_section(maker), collection_section(maker), '</div>', contact_section(maker), '</div>',
              '<section class="maker-section maker-source-section" id="sources"><h2 id="_7">来源与核实记录</h2>',
              f'<p class="maker-caption">{"社群资料采集" if only else "第一方资料核实"}：{checked}。图片权利归原权利人，保留来源署名。<a href="../methodology/">收录与复核说明 ↗</a></p>',
              '<details class="maker-disclosure"><summary>营业证据与跨平台记录 <span>查看依据</span></summary><div class="maker-disclosure-body">',
              f'<p><strong>营业证据：</strong>{esc(maker["status_note"])}</p><p id="_6">{esc(maker["merge_note"])}</p>']
    if maker['id'] in {'umoon','hidolls','blackcat'}:
        path = '../../digests/2026-08/' if maker['id']=='umoon' else '../../years/2025/'
        lines.append(f'<p><a href="{path}">本站关联历史记录</a>；历史活动资料仅作背景，不作为本次营业证明。</p>')
    lines += ['</div></details>', '<details class="maker-disclosure"><summary>原始链接与图像出处 <span>查看全部来源</span></summary><div class="maker-disclosure-body maker-source-links">']
    for key,(label,url) in maker['sources'].items():
        lines.append(f'<p id="source-{esc(key)}">{link(label, url)}</p>')
    if maker.get('logo'):
        lines.append(f'<p>品牌识别图来自 {link("官方公开图片",maker["logo"])}（{ref(maker,maker["logo_source"])}），仅用于店铺识别，不属于本站原创内容授权范围。</p>')
    if maker.get('logo_note'): lines.append(f'<p>{esc(maker["logo_note"])}</p>')
    if images: lines.append('<p>作品图的逐图来源见上方图集；点击图片可查看完整配图。社群图片原编者：禾芷溪溪溪溪溪溪。</p>')
    lines += ['<p>列出链接不代表验证了当前库存；社群记载和店方自述均保留其来源属性。未查到的电话、微信或详细地址不作推测。</p>', '</div></details></section>', '<p class="maker-bottom-links"><a href="../">← 返回店铺目录</a><a href="../../join/">提交补充或勘误 ↗</a></p>', '</div>', '']
    return '\n'.join(lines)


def index(makers, checked):
    total=len(makers);active=sum(m['status'] in ACTIVE for m in makers)
    regions=list(dict.fromkeys(m['region'] for m in makers));platforms=list(dict.fromkeys(p for m in makers for p in confirmed_platforms(m)))
    options=lambda values: ''.join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in values)
    lines=['---','title: 头壳店铺','description: 浏览国内外 Kigurumi 头壳店铺的作品、风格、价格与公开委托入口。','hide:','  - toc','---','','<!-- Generated by scripts/build_makers.py; edit docs/assets/data/makers.yml. -->','','<div class="maker-page maker-catalogue">',
           '<header class="maker-directory-heading"><div><p class="archive-kicker">KIGURUMI / MAKER DIRECTORY</p><h1>发现心仪的头壳店铺</h1><p>从作品与风格出发，了解价格与委托方式。</p></div>',
           f'<dl class="maker-directory-stats">{fact("店铺档案",total)}{fact("公开销售 / 询价",active)}{fact("地区分组",len(regions)-("地区待核实" in regions))}</dl></header>',
           '<nav class="maker-directory-tabs" aria-label="店铺目录分类"><a href="./" aria-current="page">头壳店铺 <span>119</span></a><a href="collection/">分类合集 · BJD · 肤色衣 <span>153</span></a><a class="maker-method-link" href="methodology/">收录与复核 ↗</a></nav>',
           '<div class="maker-directory" data-maker-directory><form class="maker-filters" role="search" aria-label="筛选头壳店铺">',
           '<label class="maker-search"><span>搜索店铺</span><input type="search" name="q" placeholder="店名、角色风格或关键词" autocomplete="off"></label>',
           f'<label><span>所在地区</span><select name="region" aria-label="所在地区"><option value="">全部地区</option>{options(regions)}</select></label>',
           '<label><span>营业证据</span><select name="status" aria-label="营业证据"><option value="all">全部档案</option><option value="active">公开销售 / 接受询价</option>'+''.join(f'<option value="{k}">{v}</option>' for k,v in STATUS.items())+'</select></label>',
           '<label><span>商品类型</span><select name="category" aria-label="商品类型"><option value="">全部类型</option>'+options(sorted(set(c for m in makers for c in m['categories'])))+'</select></label>',
           '<label><span>官方提及渠道</span><select name="platform" aria-label="官方提及渠道"><option value="">全部渠道</option>'+options(platforms)+'</select></label>',
           '<button type="reset" class="maker-reset" aria-label="重置筛选" title="重置筛选">↺</button></form>',
           f'<div class="maker-results-bar"><p data-maker-count role="status" aria-live="polite">{total} 家符合条件 / 共 {total} 份档案</p><a href="/assets/data/makers.json" download>下载目录 ↓</a></div><ul class="maker-card-grid">']
    order={key:i for i,key in enumerate(['meis','heyao','bhy','blackcat','hidolls','kigland','gko','sigma','munimuni','dame','teitoku','kaga','kigcos','middream','sensei','umoon'])}
    for maker in sorted(makers,key=lambda m:order.get(m['id'],total)):
        entries=[COLLECTION_ENTRIES[k] for k in maker.get('collection_entries',[])]
        query=' '.join([maker['name'],*maker['aliases'],maker['summary'],maker['location'],*[p[0] for p in maker['products']],*[c[1] for c in maker['contacts']],*[' '.join(e['fields'].values()) for e in entries]])
        query=' '.join(query.split());images=artwork(maker);price=maker['price_summary'].removeprefix('原文参考：')
        if price=='未填写':price='报价待补充'
        lines += [f'<li class="maker-row" data-search="{esc(query)}" data-region="{esc(maker["region"])}" data-status="{maker["status"]}" data-category="{esc("|".join(maker["categories"]))}" data-platform="{esc("|".join(confirmed_platforms(maker)))}">',
                  f'<a class="maker-card" href="{maker["id"]}/" aria-label="查看 {esc(maker["name"])} 的店铺档案">',cover(images,maker['name'],brand_image(maker)),
                  f'<div class="maker-card-body"><div class="maker-card-meta"><span>{esc(maker["region"])}</span><span class="maker-status maker-status--{maker["status"]}">{STATUS[maker["status"]]}</span></div><h2>{esc(maker["name"])}</h2>',
                  f'<p class="maker-card-summary">{esc(maker["summary"])}</p>',chips(style_tags(maker)),
                  f'<div class="maker-card-footer"><div><small>{"合集参考价" if maker.get("collection_only") else "公开价格"}</small><strong>{esc(price)}</strong></div><span class="maker-card-arrow" aria-hidden="true">↗</span></div></div></a></li>']
    lines += ['</ul><div class="maker-empty" data-maker-empty hidden><h2>没有匹配的店铺</h2><p>试试其他关键词，或清除部分筛选条件。</p><button type="button" data-maker-clear>清除筛选</button></div>',
              '<div class="maker-load-more"><button type="button" class="maker-button" data-maker-more hidden>查看更多店铺 ↓</button><p data-maker-progress></p></div></div>',
              '<details class="maker-disclosure maker-directory-notes" id="_1"><summary>关于这个目录 <span>范围、日期与复核说明</span></summary><div class="maker-disclosure-body">',
              f'<p>第一方核实：{checked} · 社群补录：2026-11-03。仅收录人脸 / 动漫角色头壳；Furry 兽头、兽装及连体睡衣不在本目录范围内。</p>',
              '<p>新增飞书合集包含 153 条分类记录与 379 处正文配图，为目录新增 79 份档案，并补充 31 份既有档案。<a href="collection/">浏览完整合集 →</a></p>',
              '<p>“公开销售 / 接受询价”表示核实时第一方网页存在商业入口，当前库存与档期仍需确认。原币价格、订金和配件分别记录；社群资料未自动更新第一方营业状态。</p>',
              '<ul><li>猫豆腐、虾饺工房、底层人员与抛瓦均有官方淘宝／闲鱼店名声明；平台 UID、库存与价格另行核实。底层人员与抛瓦分别建档。</li><li>官方提及渠道包括已提供链接与只声明店名两种；第三方历史关联不计入该筛选。</li><li>莓萌与拼好头合并，与偶域保持独立；KigLover 更名为 MidDreamKigu。</li><li>冉月新增业务群与进店咨询证据；哆啦、新颜、哈卡的新单状态待确认，Kigurumi Sensei 暂停定制。</li><li>深海工坊夏季促销、哈卡历史均价和星玥琦单日促销不作为当前报价。</li><li>HiDolls 的 Animal 系列不收录；Mirrodoll 当前域名转为宠物盲盒，不作为头壳营业证据。</li></ul>',
              '<p><a href="methodology/">来源、平台覆盖与去重依据</a> · <a href="../join/">提交补充或勘误</a></p></div></details></div>','']
    return '\n'.join(lines)


def validate(data):
    ids = set()
    for maker in data["makers"]:
        assert re.fullmatch(r"[a-z0-9-]+", maker["id"]), maker["id"]
        assert maker["id"] not in ids, f"Duplicate maker: {maker['id']}"
        ids.add(maker["id"])
        assert maker["status"] in STATUS
        for source in maker["sources"].values():
            assert len(source) == 2
            link(*source)
        for product in maker["products"]:
            assert len(product) == 7, product
            ref(maker, product[-1])
            assert product[2] in {"", "CNY", "USD", "JPY", "GBP", "HKD", "EUR"}
        for channel in maker["channels"]:
            assert len(channel) == 5
            ref(maker, channel[-1])
        for contact in maker["contacts"]:
            assert len(contact) == 4
            ref(maker, contact[-1])


def render(check=False):
    data = yaml.safe_load(DATA.read_text())
    validate(data)
    files = {DEST / "index.md": index(data["makers"], data["checked"])}
    files.update({DEST / m["id"] / "index.md": detail(m, m.get("checked", data["checked"])) for m in data["makers"]})
    exported = {"checked": data["checked"], "scope": data["scope"], "status_labels": STATUS,
                "product_fields": ["name", "category", "currency", "amount", "price_basis", "note", "source_id"],
                "contact_fields": ["channel", "value", "url", "source_id"],
                "channel_fields": ["platform", "name", "url", "verification", "source_id"],
                "makers": data["makers"]}
    files[ROOT / "docs/assets/data/makers.json"] = json.dumps(exported, ensure_ascii=False, indent=2) + "\n"
    outdated = []
    for path, value in files.items():
        if path.suffix == ".md":
            def icon(match):
                svg = Path(material.__file__).parent / "templates/.icons/material" / f"{match[1]}.svg"
                return '<span class="md-icon" aria-hidden="true">' + svg.read_text().strip() + '</span>'
            value = re.sub(r":material-([a-z0-9-]+):", icon, value)
        if check:
            if not path.exists() or path.read_text() != value:
                outdated.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
    if outdated:
        raise SystemExit("Regenerate maker pages: " + ", ".join(outdated))
    print(f"{'Checked' if check else 'Rendered'} {len(data['makers'])} maker profiles and directory; sources validated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated files without modifying them")
    render(parser.parse_args().check)
