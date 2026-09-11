"""Prepare the final directory and residual-section cleanup patch."""
import difflib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARIES = {
    1997: "东京电玩展春秋两届的日程、主题与整体来场统计。",
    1998: "东京电玩展两次会期、宣传主题和春季入场纪念品安排。",
    1999: "SIGMA 创立记载、Multi 眼睑与手腕附件，以及参照插画的角色摄影。",
    2000: "双叶萤与来栖川绫香制作、Multi 可替换眼部部件及表情原理说明图。",
    2001: "芹香场景与灯光、Multi 户外摄影，以及绫香和奈留的有日期图集。",
    2002: "明日香新造型、前原忍与御剑凉子的角色图集，以及展会闭幕统计。",
    2003: "水原历、爱泽友美、桃宫莓与风见瑞穗的作品档案，及 Inside Doll 的网站更新。",
    2004: "春丽动作摄影、国分寺小依与爱德华角色展示，以及当届公共展会参与条件。",
    2005: "琥珀与翡翠成对制作、《拜托了双子星》角色、希耶尔与千代图集，以及展会规模。",
    2006: "白蔷薇姐妹的成对角色制作，以及东京电玩展日程、主题与闭幕结果。",
    2007: "东京电玩展四日会期与闭幕统计；专题活动记录仍待更多原始资料。",
    2008: "东京电玩展当届日程、主题与来场统计，以及公共活动的档案入口。",
    2009: "东京电玩展行李检查、现场缝纫工具、更衣时限及当届规模。",
    2010: "秋叶原青风亭 kigurumi 咖啡馆预告，以及电玩展的 cosplay 专门企划。",
    2011: "东京电玩展本届更衣与寄存场地、公共参与安排及整体来场统计。",
    2012: "东京电玩展早间换装、指定摄影区和影像使用限制，以及本届统计。",
    2013: "河妖开始制作面具的自述，以及东京电玩展本届参与与摄影条件。",
    2014: "Laurie Simmons 的 Kigurumi 摄影系列，以及 AnimeJapan 官方角色互动。",
    2015: "Teitoku Workshop 与 Hyokkame 的创立记录，以及 AnimeJapan 活动空间。",
    2016: "AnimeJapan 本届着ぐるみ参与区域、更衣寄存和公共摄影服务。",
    2017: "FGO Fes. 着ぐるみ舞台、SIGMA Twin Angel 图集，以及 220 份社群问卷。",
    2018: "SIGMA 新面具展售与量产接单，以及面具制作匹配服务的学位研究。",
    2019: "SIGMA 二十周年公告，以及 AnimeJapan 的 FGO 官方角色节目。",
    2020: "Hyokkame 面具展与讲座、取消的展会计划，以及 WCS 线上活动。",
    2021: "WCS 混合活动与官方手册，以及第 18 回キグルミwasshoi! 酒店活动。",
    2022: "专门活动恢复、着ぐFesta 首回、DW5–8 影像发表与入门面具设计。",
    2023: "着ぐFesta 的不同活动形态、DW9 舞台展示与 DW10 国际参与。",
    2024: "DW11 才艺影像、制面工作坊设计、Advent Calendar 写作与社群调查。",
    2025: "多伦多制面工作坊、DW12 河源活动、国际合作及制作方名录更新。",
}


def patch(path, old, new):
    if old == new:
        return
    print("*** Update File: " + str(path.relative_to(ROOT)))
    for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3, lineterm=""))[2:]:
        print("@@" if line.startswith("@@") else line)


print("*** Begin Patch")
for name in ("years", "chronicle"):
    path = ROOT / f"docs/zh-Hans/{name}/index.md"
    old = path.read_text()
    def update_card(match):
        card = match.group()
        year = re.search(r"<h3>(\d{4}) 年", card)
        if year and int(year[1]) in SUMMARIES:
            return re.sub(r"<p>.*?</p>", "<p>" + SUMMARIES[int(year[1])] + "</p>", card, count=1, flags=re.S)
        return card
    new = re.sub(r'<article class="archive-feature">.*?</article>', update_card, old, flags=re.S)
    patch(path, old, new)

for locale, year, title in (
    ("ru", 2000, "## 4. Исключение повторов с 2001-2025 годами"),
    ("ja", 2023, "## 8. 2024年、2025年の記事との関係：重複表"),
):
    path = ROOT / f"docs/{locale}/years/{year}/index.md"
    old = path.read_text()
    new = re.sub(re.escape(title) + r"\n.*?(?=^## |\Z)", "", old, flags=re.S | re.M)
    patch(path, old, new)
print("*** End Patch")
