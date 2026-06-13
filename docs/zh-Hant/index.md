---
hide:
  - toc
---

<section class="archive-hero">
  <div class="archive-hero__copy">
    <p class="archive-kicker">Community Chronicle · Kigurumi Archive</p>
    <h1>Kigurumi 編年志</h1>
    <p class="archive-lede">一個面向 kigurumi 社群的輕量資料館，用清晰、可追溯、可長期維護的方式整理公開介紹、協作說明和貢獻入口。</p>
    <div class="archive-actions">
      <a class="md-button md-button--primary" href="about/">了解項目</a>
      <a class="md-button" href="support/">參與貢獻</a>
    </div>
  </div>
  <div class="archive-hero__meta">
    <span>靜態站點</span>
    <span>多語言結構</span>
    <span>協作友好</span>
  </div>
</section>

<section class="archive-section" markdown>
  <p class="archive-kicker">Site Focus</p>
  <h2>先把核心資訊講清楚</h2>
  <p>目前版本保留首頁、關於介紹、貢獻與支持三個頁面，避免開發期資訊架構過早變複雜。後續需要擴展編年、資料索引或專題頁時，可以繼續沿用同一套國際化目錄結構。</p>

  <div class="archive-feature-grid archive-feature-grid--compact">
    <article class="archive-feature">
      <span class="archive-feature__icon">首</span>
      <h3>首頁</h3>
      <p>展示項目定位、主要入口和目前維護方向。</p>
      <a href="./">返回首頁</a>
    </article>
    <article class="archive-feature">
      <span class="archive-feature__icon">介</span>
      <h3>關於介紹</h3>
      <p>說明資料館的目標、邊界、內容原則和長期維護方式。</p>
      <a href="about/">查看介紹</a>
    </article>
    <article class="archive-feature">
      <span class="archive-feature__icon">助</span>
      <h3>貢獻支持</h3>
      <p>提供參與翻譯、校對、頁面維護和資料授權的協作說明。</p>
      <a href="support/">查看支持方式</a>
    </article>
  </div>
</section>

<section class="archive-section archive-section--split">
  <div markdown>
    <p class="archive-kicker">Development Principle</p>
    <h2>輕量，但不臨時</h2>
    <p>頁面數量減少後，項目仍然保留 MkDocs Material、多語言目錄、統一視覺樣式和自動部署流程。它適合在開發期快速迭代，也能在內容成長後平滑擴展。</p>
  </div>
  <ol class="archive-steps">
    <li><strong>資訊收斂</strong><span>只保留目前必要頁面</span></li>
    <li><strong>結構穩定</strong><span>多語言頁面保持同一路徑</span></li>
    <li><strong>樣式一致</strong><span>複用 archive 元件體系</span></li>
    <li><strong>部署自動化</strong><span>推送後由 GitHub Actions 發布</span></li>
  </ol>
</section>
