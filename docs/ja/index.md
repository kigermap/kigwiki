---
hide:
  - toc
---

<section class="archive-hero">
  <div class="archive-hero__copy">
    <p class="archive-kicker">Community Chronicle · Kigurumi Archive</p>
    <h1>Kigurumi 編年誌</h1>
    <p class="archive-lede">kigurumi コミュニティのための軽量な資料アーカイブです。公開紹介、協力方法、貢献入口を、明確で検証しやすく、長期維持しやすい形で整理します。</p>
    <div class="archive-actions">
      <a class="md-button md-button--primary" href="about/">プロジェクト紹介</a>
      <a class="md-button" href="support/">貢献する</a>
    </div>
  </div>
  <div class="archive-hero__meta">
    <span>静的サイト</span>
    <span>多言語構成</span>
    <span>協作しやすい</span>
  </div>
</section>

<section class="archive-section" markdown>
  <p class="archive-kicker">Site Focus</p>
  <h2>まず中核情報を明確に</h2>
  <p>現在の開発版では、ホーム、紹介、貢献と支援の 3 ページだけを残しています。開発初期に情報構造を複雑にしすぎず、将来必要になった編年、索引、特集ページは同じ国際化ディレクトリ構造で追加できます。</p>

  <div class="archive-feature-grid archive-feature-grid--compact">
    <article class="archive-feature">
      <span class="archive-feature__icon">首</span>
      <h3>ホーム</h3>
      <p>プロジェクトの位置づけ、主な入口、現在の保守方針を示します。</p>
      <a href="./">ホームへ戻る</a>
    </article>
    <article class="archive-feature">
      <span class="archive-feature__icon">紹</span>
      <h3>紹介</h3>
      <p>アーカイブの目標、範囲、内容原則、長期保守の方法を説明します。</p>
      <a href="about/">紹介を読む</a>
    </article>
    <article class="archive-feature">
      <span class="archive-feature__icon">助</span>
      <h3>貢献と支援</h3>
      <p>翻訳、確認、ページ保守、許諾、支援方法を説明します。</p>
      <a href="support/">支援方法を見る</a>
    </article>
  </div>
</section>

<section class="archive-section archive-section--split">
  <div markdown>
    <p class="archive-kicker">Development Principle</p>
    <h2>軽量だが、一時的ではない</h2>
    <p>ページ数を減らしても、MkDocs Material、多言語ディレクトリ、統一されたビジュアル部品、自動デプロイは残しています。今は素早く改善でき、内容が増えた後も自然に拡張できます。</p>
  </div>
  <ol class="archive-steps">
    <li><strong>情報を絞る</strong><span>今必要なページだけを残す</span></li>
    <li><strong>構造を安定させる</strong><span>言語間で同じパスを使う</span></li>
    <li><strong>見た目をそろえる</strong><span>archive コンポーネントを再利用する</span></li>
    <li><strong>公開を自動化する</strong><span>push 後に GitHub Actions で公開する</span></li>
  </ol>
</section>
