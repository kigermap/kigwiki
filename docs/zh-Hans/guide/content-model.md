# 内容模型

这个工程建议把资料分成四类：事件、人物、地点、来源。

## 事件

事件写在 `data/events.yml`：

```yaml
- id: event-1949-government
  date: 1949-10-01
  sort_date: "1949-10-01"
  title: 成立人民政府
  category: 政事
  period: 现代
  people:
    - person-li-si
  places:
    - place-county-seat
  sources:
    - source-county-gazetteer-1993
  confidence: 高
  summary: 当地政权机构完成更替，人民政府成立。
```

字段说明：

| 字段 | 说明 |
| --- | --- |
| `id` | 稳定编号，建议不要改 |
| `date` | 面向读者展示的时间 |
| `sort_date` | 用于排序的 ISO 日期，可估计 |
| `title` | 事件标题 |
| `category` | 事件类别 |
| `people` | 关联人物 ID |
| `places` | 关联地点 ID |
| `sources` | 关联来源 ID |
| `confidence` | 高、中、低 |
| `summary` | 简短摘要 |

## 人物、地点、来源

人物、地点、来源分别写入：

```text
data/people.yml
data/places.yml
data/sources.yml
```

如果需要长篇介绍，可以在 `docs/people/` 或 `docs/places/` 创建 Markdown 页面，并在数据中填写 `file`。

