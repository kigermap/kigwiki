---
hide:
  - toc
---

<section class="archive-hero">
  <div class="archive-hero__copy">
    <p class="archive-kicker">Community Chronicle · Kigurumi Archive</p>
    <h1>Kigurumi 编年志</h1>
    <p class="archive-lede">记录活动、制作、展陈、访谈和社群礼仪的长期资料馆。这里不只是把页面堆起来，而是把每一次相遇、每一份工艺、每一条来源都放回可追溯的时间脉络里。</p>
    <div class="archive-actions">
      <a class="md-button md-button--primary" href="generated/events/">查看大事记</a>
      <a class="md-button" href="places/county-seat/">进入星绸会馆</a>
    </div>
  </div>
  <div class="archive-hero__meta">
    <span>公开阅读</span>
    <span>协作者编辑</span>
    <span>来源可追溯</span>
  </div>
</section>

<section class="archive-stats" aria-label="资料库概览">
  <div>
    <strong>5</strong>
    <span>已编目事件</span>
  </div>
  <div>
    <strong>3</strong>
    <span>空间与据点</span>
  </div>
  <div>
    <strong>4</strong>
    <span>来源类型</span>
  </div>
  <div>
    <strong>2014-2024</strong>
    <span>当前年表范围</span>
  </div>
</section>

<section class="archive-section" markdown>
  <p class="archive-kicker">Archive Structure</p>
  <h2>按修志方式组织社群记忆</h2>
  <p>站点保留普通读者的阅读体验，也给整理者留下结构化资料入口。事件、人物、地点和来源互相连接，后续可以继续扩展成年表、活动谱系、访谈索引和工艺档案。</p>

  <div class="archive-feature-grid">
    <article class="archive-feature">
      <span class="archive-feature__icon">年</span>
      <h3>编年</h3>
      <p>按时间记录社群活动、制作规范、展陈节点和线上资料馆更新。</p>
      <a href="chronicle/">打开编年</a>
    </article>
    <article class="archive-feature">
      <span class="archive-feature__icon">志</span>
      <h3>志书</h3>
      <p>以章节方式整理社群沿革、空间、工艺、风俗和术语。</p>
      <a href="gazetteer/">阅读志书</a>
    </article>
    <article class="archive-feature">
      <span class="archive-feature__icon">点</span>
      <h3>据点</h3>
      <p>记录线下会馆、工坊、展陈空间与线上资料馆的功能变化。</p>
      <a href="places/">查看地点</a>
    </article>
    <article class="archive-feature">
      <span class="archive-feature__icon">源</span>
      <h3>来源</h3>
      <p>把活动手册、访谈稿、照片册和维护规范纳入统一引用体系。</p>
      <a href="sources/">核对来源</a>
    </article>
  </div>
</section>

<section class="archive-section archive-section--split">
  <div>
    <p class="archive-kicker">Editorial Workflow</p>
    <h2>适合长期维护的资料流程</h2>
    <p>正文负责讲述，<code>data/*.yml</code> 负责索引。每次新增事件，都建议同时绑定人物、地点和来源，避免资料在几年后变成无法考证的散点。</p>
  </div>
  <ol class="archive-steps">
    <li><strong>采集</strong><span>活动照片、访谈、手册、制作记录</span></li>
    <li><strong>编目</strong><span>拆成事件、人物、地点、来源</span></li>
    <li><strong>校对</strong><span>确认时间、署名、公开范围和可信度</span></li>
    <li><strong>发布</strong><span>自动生成索引并部署到静态站</span></li>
  </ol>
</section>
