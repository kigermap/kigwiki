"""Shared, accessible presentation for maker cards and original artwork."""
from html import escape


def esc(value):
    return escape(str(value), quote=True)


def chips(values):
    return '<div class="maker-tags">' + ''.join(f'<span>{esc(v)}</span>' for v in values if v) + '</div>'


def cover(images, name, logo=None):
    if images:
        image = images[0]
        return (f'<div class="maker-card-media"><img src="{esc(image["src"])}" alt="{esc(image["caption"])}" '
                'loading="lazy" decoding="async" width="640" height="480">'
                f'<span class="maker-image-count">{len(images)} 张配图</span></div>')
    identity = f'<img src="{esc(logo)}" alt="{esc(name)} 品牌标识" loading="lazy">' if logo else f'<span class="maker-monogram">{esc(name[:2])}</span>'
    return f'<div class="maker-card-media maker-card-media--identity">{identity}<span class="maker-image-count">作品图待补充</span></div>'


def gallery(images, name, logo=None):
    if not images:
        return '<div class="maker-gallery maker-gallery--empty">' + cover([], name, logo) + '<p class="maker-caption">可通过店铺公开入口浏览更多作品。</p></div>'
    first = images[0]
    lines = ['<div class="maker-gallery" data-maker-gallery>', '<figure class="maker-gallery-main">',
             f'<a data-gallery-open href="{esc(first["src"])}" target="_blank" rel="noopener" aria-label="打开完整配图">',
             f'<img data-gallery-image src="{esc(first["src"])}" alt="{esc(first["caption"])}" width="1200" height="1200" decoding="async"></a>',
             f'<figcaption><span data-gallery-caption>{esc(first["caption"])}</span> <a data-gallery-credit href="{esc(first["credit"])}">来源 ↗</a></figcaption>', '</figure>']
    if len(images) > 1:
        lines.append('<div class="maker-gallery-thumbs" role="group" aria-label="切换作品图片">')
        for n, image in enumerate(images):
            lines.append(f'<button type="button" data-gallery-thumb data-src="{esc(image["src"])}" data-caption="{esc(image["caption"])}" data-credit="{esc(image["credit"])}" aria-label="查看配图 {n+1}：{esc(image["caption"])}" aria-pressed="{"true" if n==0 else "false"}"><img src="{esc(image["src"])}" alt="" width="72" height="72" loading="lazy" decoding="async"></button>')
        lines.append('</div>')
    lines.append('</div>')
    return '\n'.join(lines)


def fact(label, value):
    return f'<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>'
