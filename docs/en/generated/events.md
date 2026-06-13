---
hide:
  - toc
---

<section class="archive-page-intro" markdown>
  <p class="archive-kicker">Chronicle Index</p>
  <h1>Event Index</h1>
  <p>Generated from `data/events.yml`, this page lists cataloged events with dates, people, places, sources, and confidence notes.</p>
</section>
<section class="archive-index-panel" data-archive-filter>
  <div class="archive-index-panel__summary">
    <span class="archive-index-panel__label">Structured events</span>
    <strong>5</strong>
    <p>Scan every record by date, category, place, source, and confidence.</p>
  </div>
  <div class="archive-index-panel__tools">
    <label class="archive-index-search"><span>Search this page</span><input type="search" data-archive-filter-input placeholder="Filter by date, event, person, place, or source"></label>
    <div class="archive-chip-list" aria-label="Quick filters">
    <button type="button" class="archive-chip archive-chip--active" data-archive-filter-reset>All</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="口述史">口述史</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="场地沿革">场地沿革</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="工艺维护">工艺维护</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="数字资料馆">数字资料馆</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="社群治理">社群治理</button>
    </div>
  </div>
</section>

<p class="archive-update-note">After editing structured events, run <code>python scripts/build_indexes.py</code> to refresh these pages.</p>

| Date | Event | Category | People | Places | Sources | Confidence | Summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2014-05-18 | 星绸会馆首次开放社群整理日 | 场地沿革 | [档案整理员 A](../people/zhang-san.md) | [星绸会馆](../places/county-seat.md) | 整理日记录 | 高 | 成员集中整理活动照片、制作记录和服装维护笔记，形成最早的可检索社群资料。 |
| 2016-08-07 | 夏季见面会建立活动编号规则 | 社群治理 |  | [星绸会馆](../places/county-seat.md) | 2016活动手册 | 高 | 以年份、城市、活动类型组合编号，方便后续照片、访谈和物料归档。 |
| 2019-11-23 | 完成第一批口述访谈转写 | 口述史 | 访谈协作者 B | [星绸会馆](../places/county-seat.md) | 整理日记录 | 高 | 围绕入坑契机、制作分工、线下礼仪和早期活动记忆完成访谈转写。 |
| 2021-04-10 | 建立面具维护与收纳规范 | 工艺维护 |  | 制作工坊 | 维护规范 | 高 | 形成清洁、运输、展示和修复记录模板，降低活动后资料和实物散失风险。 |
| 2024-10-06 | 社群年表公开试运行 | 数字资料馆 |  | 线上资料馆 | 发布记录 | 高 | 将活动、人物、地点和来源拆分为结构化资料，开放公众阅读并保留协作者编辑权限。 |
