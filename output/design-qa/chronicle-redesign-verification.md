# Chronicle Theme Verification

Date: 2026-09-09

## Scope

The complete shared UI theme was replaced while retaining MkDocs Material,
the five language routes, document text, source images, citations, and links.
No Markdown files under the five content locale directories were changed.

## Results

| Check | Result |
| --- | --- |
| Strict clean MkDocs build | Passed |
| JavaScript syntax and git whitespace checks | Passed |
| Generated HTML theme assets and navigation targets | 236 pages, no missing targets |
| Language navigation isolation | 47 pages per locale, plus the shared 404 |
| Browser layout checks | 235 content pages at 390px and 1536px: 470 checks |
| Runtime errors during the full browser scan | None |
| Narrow and tablet home layouts | All five locales at 320px, 768px, and 1536px |
| Year search, empty state, decade selection, sorting | Passed |
| Mobile drawer, navigation links, and page contents | Passed |
| Mobile search open, results, toolbar layout, and close | Passed |
| Search for 2025 in simplified Chinese | First result is /years/2025/ |
| Dark mode and preference persistence between pages | Passed |
| Language switching on an annual article | Preserves the annual article route |
| Shared 404 page | Renders without horizontal overflow |

The initial full scan found one mobile overflow in the Russian census report,
caused by deeply nested quote markers in the imported transcription. Nested
quote spacing was corrected in the theme, and the failing page passed a targeted
browser recheck. The report text was preserved.

## Artifacts

- Design mockup: `docs/assets/design/chronicle-redesign-20260909.png`
- Exact generation prompts: `docs/assets/design/chronicle-redesign-20260909.json`
- Theme maintenance notes: `overrides/README.md`
- Final screenshots: `output/playwright/redesign-*.png`
- Homepage, annual catalogue, annual article, monthly digest, survey report,
  join page, mobile navigation, mobile search, and dark mode were captured.
- Decorative WebP asset: 65,972 bytes, generated through imagegen MCP / sub2api.

This is a local preview. No production deployment was performed.
