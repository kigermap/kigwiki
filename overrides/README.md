# Chronicle Museum Theme

The September 2026 redesign keeps MkDocs Material, its search, language routing,
palette switch, Markdown content, and build hooks. The public content remains in
`docs/<locale>/`; presentation is shared across all five languages.

- `partials/nav.html` builds the flat catalogue from MkDocs navigation pages.
- `partials/path.html` renders breadcrumbs from the current page ancestry.
- `main.html` exposes Material's existing SVG icons for progressive enhancement.
- `docs/assets/stylesheets/extra.css` owns the complete light/dark responsive theme.
- `docs/assets/javascripts/archive-ui.js` enhances the existing catalogue, year
  filters, mobile contents, table scrolling, and reading progress.

The catalogue enhancement reorders existing sections and keeps their text and
links. Year filters use the actual entries in the page, including future additions.
Without JavaScript, the complete content and navigation remain readable.

## Visual Reference

- Mockup: `docs/assets/design/chronicle-redesign-20260909.png`
- Generation prompts: `docs/assets/design/chronicle-redesign-20260909.json`
- Original themed image: `docs/assets/images/chronicle-studio-20260909.png`
- Browser asset: `docs/assets/images/chronicle-studio-20260909.webp`
- Provider: imagegen MCP / sub2api, `gpt-image-2`, interactive SSE, 2 partial images.
- Palette: white, neutral charcoal, vermilion `#b84033`, teal `#386d65`.
- UI font: local system sans-serif; headings: local Chinese serif with Georgia fallback.

The generated studio still life is a decorative theme asset, not a historical
photograph or archival source. Existing documentary images were not changed.

## Verification

```sh
.venv/bin/mkdocs build --strict --clean
node --check docs/assets/javascripts/archive-ui.js
git diff --check
```

Browser coverage should include home, year catalogue, annual article, monthly
digest, survey report, source directory, and join page; all five locales; desktop,
tablet, 390px and 320px widths; dark mode; search; drawer; language menu; year
filters; sorting; mobile contents; and keyboard scrolling of wide tables.

Update the asset query strings in `mkdocs.yml` when changing the shared CSS or JS.
