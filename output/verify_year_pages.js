async (page) => {
  const results = [];
  for (const viewport of [{width: 1440, height: 1000}, {width: 390, height: 844}]) {
    await page.setViewportSize(viewport);
    for (const route of ["years/", "years/2000/", "years/2024/", "years/2025/"]) {
      await page.goto("http://127.0.0.1:8023/" + route);
      await page.waitForLoadState("networkidle");
      const result = await page.evaluate(() => {
        const content = document.querySelector("article.md-content__inner");
        return {
          title: document.title,
          width: window.innerWidth,
          overflow: document.documentElement.scrollWidth > window.innerWidth,
          brokenImages: [...content.querySelectorAll("img")].filter(i => !i.complete || !i.naturalWidth).map(i => i.src),
          headings: [...content.querySelectorAll("h2")].map(h => h.textContent.replace("¶", "").trim()),
          missingSourceAnchors: [...content.querySelectorAll('a[href^="#s"], a.footnote-ref')].filter(a => !document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a => a.hash),
        };
      });
      results.push({route, ...result});
      const slug = route.replaceAll("/", "-").replace(/-$/, "");
      await page.screenshot({path: "output/playwright/annual-" + slug + "-" + viewport.width + ".png", fullPage: false});
      if (route === "years/2000/" || route === "years/2025/") {
        await page.locator('img[src*="explainer.webp"]').scrollIntoViewIfNeeded();
        await page.screenshot({path: "output/playwright/annual-" + slug + "-illustration-" + viewport.width + ".png"});
      }
    }
  }
  return results;
}
