# 编年史与方志资料库

这是一个面向长期修志的静态资料库模板。它把“可读正文”和“可计算索引”分开：正文用于叙述，结构化数据用于生成大事记、人物索引、地点索引和来源索引。

<div class="grid cards" markdown>

- :material-timeline-clock-outline: **编年**

  按时间梳理事件，保留发生日期、时期、类别、地点、人物和来源。

- :material-book-open-page-variant: **志书**

  按方志分目组织建置、地理、风俗、人物、教育、物产等正文。

- :material-account-group: **人物**

  人物专页可写传略，索引页自动统计相关事件。

- :material-map-marker-radius: **地点**

  地点专页可记录沿革、别名、坐标和空间变迁。

- :material-archive-search: **来源**

  每条事件都建议绑定来源，方便审校和回溯。

</div>

## 推荐工作流

1. 在 `data/events.yml` 录入事件。
2. 在 `data/people.yml`、`data/places.yml`、`data/sources.yml` 补齐实体。
3. 对重点人物、地点、专题在 `docs/` 下写正文。
4. 运行 `python scripts/build_indexes.py` 更新自动索引。
5. 推送到 GitHub，自动发布到 GitHub Pages。

## 示例图文

下面这张图只是占位示例。真实项目里可以把照片、地图、扫描件放在 `docs/assets/images/`。

![档案资料占位图](assets/images/sample-archive.svg)

