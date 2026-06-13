---
hide:
  - toc
---

<section class="archive-page-intro" markdown>
  <p class="archive-kicker">Chronicle Index</p>
  <h1>事件索引</h1>
  <p>`data/events.yml` から自動生成され、編目済みの事件を日時、人物、場所、出典、信頼度とともに一覧します。</p>
</section>
<section class="archive-index-panel" data-archive-filter>
  <div class="archive-index-panel__summary">
    <span class="archive-index-panel__label">構造化イベント</span>
    <strong>5</strong>
    <p>日時、分類、場所、出典、信頼度で全記録を確認できます。</p>
  </div>
  <div class="archive-index-panel__tools">
    <label class="archive-index-search"><span>このページを検索</span><input type="search" data-archive-filter-input placeholder="日時、事件、人物、場所、出典で絞り込み"></label>
    <div class="archive-chip-list" aria-label="クイックフィルター">
    <button type="button" class="archive-chip archive-chip--active" data-archive-filter-reset>すべて</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="口述史">口述史</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="场地沿革">场地沿革</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="工艺维护">工艺维护</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="数字资料馆">数字资料馆</button>
    <button type="button" class="archive-chip" data-archive-filter-chip="社群治理">社群治理</button>
    </div>
  </div>
</section>

<p class="archive-update-note">構造化イベントを編集した後は、<code>python scripts/build_indexes.py</code> を実行して更新してください。</p>

| 日時 | 事件 | 分類 | 人物 | 場所 | 出典 | 信頼度 | 概要 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2014-05-18 | 星绸会馆首次开放社群整理日 | 场地沿革 | [档案整理员 A](../people/zhang-san.md) | [星绸会馆](../places/county-seat.md) | 整理日记录 | 高 | 成员集中整理活动照片、制作记录和服装维护笔记，形成最早的可检索社群资料。 |
| 2016-08-07 | 夏季见面会建立活动编号规则 | 社群治理 |  | [星绸会馆](../places/county-seat.md) | 2016活动手册 | 高 | 以年份、城市、活动类型组合编号，方便后续照片、访谈和物料归档。 |
| 2019-11-23 | 完成第一批口述访谈转写 | 口述史 | 访谈协作者 B | [星绸会馆](../places/county-seat.md) | 整理日记录 | 高 | 围绕入坑契机、制作分工、线下礼仪和早期活动记忆完成访谈转写。 |
| 2021-04-10 | 建立面具维护与收纳规范 | 工艺维护 |  | 制作工坊 | 维护规范 | 高 | 形成清洁、运输、展示和修复记录模板，降低活动后资料和实物散失风险。 |
| 2024-10-06 | 社群年表公开试运行 | 数字资料馆 |  | 线上资料馆 | 发布记录 | 高 | 将活动、人物、地点和来源拆分为结构化资料，开放公众阅读并保留协作者编辑权限。 |
