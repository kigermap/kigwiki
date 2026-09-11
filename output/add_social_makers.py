"""Import manually reviewed public business-profile evidence into the maker dataset."""
import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/assets/data/makers.yml"
EVIDENCE = ROOT / "output/shop-evidence"
DIRECTORY = "https://makers.kig-o.com/"
old_directory = json.loads((EVIDENCE / "makerlist20251210.json").read_text())


def evidence(account):
    url = f"https://x.com/{account}"
    path = EVIDENCE / (hashlib.sha256(url.encode()).hexdigest()[:12] + ".json")
    data = json.loads(path.read_text())
    assert data["status"] == 200 and account.lower() in data["text"].lower()
    return data


def post(account, label):
    return next("https://x.com" + x["url"] for x in evidence(account)["links"]
                if x["text"] == label and "/status/" in x["url"])


def declaration(platform, name, account):
    return [platform, f"店名声明：{name}", f"https://x.com/{account}",
            "官方简介明确声明；链接为声明出处，未取得店铺直链或平台 UID", "profile"]


def direct(platform, name, url):
    return [platform, name, url, "官方账号公开链接；未核实平台库存和排期", "profile"]


def product(name, note="公开作品展示，不代表现货；当前报价需询问制作方"):
    return [name, "成品展示", "", "", "未公开价格", note, "profile"]


def maker(key, name, account, summary, description, *, legacy=None, aliases=(),
          location=None, status="inquiry", note=None, channels=(), qq=(),
          products=(), categories=("全定制",), merge="", terms=None):
    source = evidence(account)
    url = source["url"]
    entry = {
        "id": key, "name": name, "aliases": list(aliases), "region": "中国大陆",
        "location": location or "中国；具体城市与制作地址未核实（国家线索来自社群目录）",
        "status": status,
        "status_note": note or "当前可访问的第一方业务简介提供制作或店铺联系入口；平台商品、价格及即时接单名额尚未核实。",
        "summary": summary, "description": description, "categories": list(categories),
        "price_summary": "头壳按需求询价；无已核实当前价目表",
        "contacts": [["X 业务联系", "@" + account, url, "profile"]],
        "channels": [["X", "制作方公开业务账号", url, "第一方业务说明", "profile"], *channels],
        "merge_note": merge + " 未取得新渠道的官方归属证据时，不按同名、同图自动合并。",
        "terms": terms or "当前报价、材料、尺寸、排期、支付、配送及售后须向制作方确认；公开作品不是在售库存。",
        "products": list(products) or [["Kigurumi 人脸头壳制作", "定制服务", "", "", "询价", "仅记录公开制作业务；规格及新单受理需确认", "profile"]],
        "sources": {"profile": ["制作方 X 公开简介、渠道与作品；访问于 2026-09-09", url]},
    }
    for label, value in qq:
        assert value in source["text"], (key, value)
        entry["contacts"].append([label + "（出处）", value, url, "profile"])
    avatars = [i["src"] for i in source["images"] if "/profile_images/" in (i.get("src") or "") and "400x400" in i["src"]]
    if avatars:
        entry.update(logo=avatars[0], logo_source="profile",
                     logo_note="识别图为制作方公开业务账号头像，不宣称是注册商标；未收录私人照片或私人联系方式。")
    if legacy:
        old = next(x for x in old_directory if x["Name"] == legacy and any("taobao.com" in x[k] for k in ["Website1Link", "Website2Link"]))
        entry["sources"]["directory"] = ["2025-12-10 制作者目录；仅用于历史渠道线索", DIRECTORY]
        for k in ["Website1Link", "Website2Link"]:
            candidate = old[k]
            if "taobao.com" not in candidate:
                continue
            ids = re.findall(r"shop(\d+)", candidate)
            if any(candidate.rstrip("/") == c[2].rstrip("/") or (ids and ids[0] in c[2]) for c in channels):
                continue
            entry["channels"].append(["淘宝", "历史店铺 URL（归属待复核）", candidate, "第三方历史 URL；不是本次核实的店铺直链", "directory"])
    return entry


records = [
    maker("raigeki", "雷击工坊 Raigeki", "RAIGEKI_Li",
          "提供着ぐるみ头壳制作，官方简介公开淘宝入口及广东英德所在地。",
          "官方账号自称雷击工坊，说明制作着ぐるみ面具并接受需求与订单咨询。网页直接标示 raigeki.taobao.com；本次没有取得淘宝商品价格，不沿用早期手册与新颜玩偶重复的 QQ 号。",
          aliases=["雷撃工房", "Raigeki", "KIGURUMI雷击工坊"],
          location="中国广东清远英德（官方业务账号自述）；具体工作室地址未公开",
          channels=[direct("淘宝", "雷击工坊", "https://raigeki.taobao.com/")],
          merge="雷击、雷撃工房与 Raigeki 在同一官方简介对应。与新颜玩偶分开建档；邮箱在此次文本中被遮蔽，不补写。"),
    maker("nekotofu", "猫豆腐 NekoToufu", "nekotoufufu",
          "提供 kigurumi 全流程定制，官方声明淘宝、闲鱼同名，并设国际业务账号。",
          "中文官方账号明确写明全流程定制和淘宝／闲鱼店铺同名，并直接关联国际账号。公开作品包括洛天依、明日方舟终末地管理员及鸣潮达妮娅；肤色衣业务与整头分开记录。",
          legacy="Nekotofu", aliases=["猫豆腐NekoToufu", "Nekotofu", "NEKOTOUFU"],
          channels=[declaration("淘宝", "猫豆腐NekoToufu", "nekotoufufu"), declaration("闲鱼", "猫豆腐NekoToufu", "nekotoufufu")],
          qq=[("官方 QQ 群", "915979496")], categories=["全定制", "肤色衣"],
          products=[product("洛天依头壳"), product("明日方舟：终末地 女管理员头壳"), product("鸣潮 达妮娅头壳")],
          merge="中文号直接关联 @NEKOTOUFU_shop，归为同一店铺的国际渠道；淘宝与闲鱼名称有第一方声明，但具体平台 UID 未核实。"),
    maker("haagaau", "虾饺工房 Haagaau", "haagaau_GF",
          "制作 kigurumi 头壳，公开淘宝与闲鱼店名，并区分国内和国际业务入口。",
          "官方中文账号标示 kigurumi 虾饺工房、淘宝及闲鱼同名和 QQ 联系方式，关联国际业务号及分店虾饺糖水铺。国际账号展示丹瑾、阿妮斯、桔梗和风华委托成果；本次订单表需要登录，不能验证是否仍接受提交。",
          aliases=["Kigurumi虾饺工房", "Haagaau Kigurumi Workshop", "虾饺糖水铺"],
          channels=[declaration("淘宝", "kigurumi虾饺工房", "haagaau_GF"), declaration("闲鱼", "kigurumi虾饺工房", "haagaau_GF")],
          qq=[("业务 QQ", "3792059014"), ("QQ 群", "195721304")],
          merge="中文号直接关联 @Haagaau_GF_EN 和新分店 @haagaau_TSP，按主品牌保留关系；糖水铺商品、价格和经营主体未独立核实，不重复建店。",
          terms="国际账号有下单表和海外业务说明；此次表单需登录、shop.haagaau-kig.com 连接失败，暂不推定可下单。邮箱文本被遮蔽，未抄作有效联系方式。"),
    maker("4uuone", "底层人员 4uuone", "4uuone",
          "公开业务账号写明淘宝、闲鱼均为 kigurumi底层人员，亦使用 4u 名称。",
          "账号公开店名为 kigurumi底层人员，简介包含 4u 及淘宝／闲鱼同名声明。没有公开可核实的统一价目表、城市或当前排期，需从业务账号进一步询问。",
          legacy="kigurumi底层人员 (aka 4u and 4uuone)", aliases=["kigurumi底层人员", "4u", "4uuone"],
          channels=[declaration("淘宝", "kigurumi底层人员", "4uuone"), declaration("闲鱼", "kigurumi底层人员", "4uuone")],
          merge="2025 制作者目录明确纠正此前将 4uuone 与 Power_9567 合并的错误；二者当前简介也给出不同店名，分别建档。"),
    maker("power", "速趴抛瓦 Power Kigurumi", "Power_9567",
          "淘宝与闲鱼公开店名为速趴抛瓦kigurumi，提供业务 QQ 联系。",
          "官方公开账号使用 power kigurumi抛瓦，明确列出淘宝／闲鱼名称与 QQ。两平台归属于同一品牌的声明已取得；商品规格、平台店铺 UID 与当前整头价仍待核实。",
          legacy="Power Kigurumi (aka Power_9567 and 抛瓦)", aliases=["抛瓦", "Power_9567", "速趴抛瓦kigurumi"],
          channels=[declaration("淘宝", "速趴抛瓦kigurumi", "Power_9567"), declaration("闲鱼", "速趴抛瓦kigurumi", "Power_9567")],
          qq=[("业务 QQ", "1113132445")], merge="与 4uuone 是不同制作者，互相提及或合影不构成合并依据。"),
    maker("akg", "AKG / Alice Kig Garden", "Alicekigsale",
          "设计制作 kigurumi 头壳，公开淘宝名 AKG工坊及亚马逊店铺链接。",
          "官方英文简介明确制作 kigurumi 面具、淘宝店名与 PayPal 支付，并公开亚马逊商店入口。作品包含芙宁娜、可替换脸部及可拆刘海展示，也提供不同颜色肤色衣。",
          legacy="Alice Kig Garden", aliases=["AKG工坊", "Alice Kig Garden", "AKG-Alice Kig Garden"],
          channels=[declaration("淘宝", "AKG工坊", "Alicekigsale"), direct("Amazon", "官方简介中的亚马逊店铺短链", "https://t.co/WieT44t4AG")],
          categories=["全定制", "肤色衣", "配件"], products=[product("芙宁娜头壳"), product("可替换脸部头壳"), product("可拆刘海头壳")],
          terms="官方简介声明接受 PayPal。未取得亚马逊商品清单与售价；不把账号中的质量宣传视为本站验证结果。",
          merge="AKG、Alice Kig Garden 与淘宝名 AKG工坊由同一账号声明；不与兔子工坊的历史 Etsy 名 AliceKigWorkshop 合并。"),
    maker("beadoll", "偶形记 BEADOLL", "BEADOLL_OS",
          "官方公开淘宝编号 247990779，支持 PayPal 与海外发货。",
          "公开业务简介写明淘宝同名，直接标示 shop247990779.m.taobao.com。账号发布月城、DOLL 等造型以及肤色衣内容；无面产品等未能确认属于人脸头壳的商品不纳入价目表。",
          legacy="BEADOLL", aliases=["偶形记BEADOLL"], channels=[direct("淘宝", "偶形记BEADOLL", "https://shop247990779.m.taobao.com/")],
          categories=["半定制", "肤色衣"], products=[product("月城头壳")],
          terms="官方简介支持 PayPal 支付和海外发货；半壳、全壳配置仅有历史目录描述，实际规格与当前报价需确认。",
          merge="官网外的官方业务账号直接展示淘宝店铺编号，与历史目录相同编号对应为同一渠道。"),
    maker("dora", "哆啦工坊 Dora Studio", "DoraKigStudio",
          "营业账号公开淘宝店名及 QQ 群，能读取的作品记录主要停留在 2024 年。",
          "账号自称哆啦工坊营业号，要求在淘宝搜索 Kigurumi哆啦工坊。公开作品包括布丽姬、雷电将军、流萤和春日野穹；此次没有取得近期接单或商品页面，因此先保留待核实。",
          legacy="哆啦工坊 / Dora Studio", aliases=["Kigurumi哆啦工坊", "Dora Studio"], status="unverified",
          note="官方账号身份与淘宝店名已确认，但可读取作品主要为 2024-09，缺少当前接单证据。",
          channels=[declaration("淘宝", "Kigurumi哆啦工坊", "DoraKigStudio")], qq=[("QQ 交流群", "539704355")],
          products=[product("布丽姬头壳", "2024-09 客户返图／内测单，不代表在售"), product("雷电将军／流萤／春日野穹头壳", "2024-09 作品展示，当前业务待复核")],
          merge="Dora Studio 与哆啦工坊为同一业务账号名称；淘宝店名已声明，历史 URL 的当前归属仍需验证。"),
    maker("fantasymasks", "绮幻坊 FantasyMasks", "FantasyMasks_",
          "官方简介明确接受头壳定制，公开 QQ、交流群和淘宝同名店铺。",
          "工坊自述为 kigurumi 头壳店，提供 QQ 与淘宝咨询方式。公开视频展示鹿目圆、藿藿、和实由依等人脸动漫角色；没有公开统一售价和交期。",
          legacy="FantasyMasks绮幻坊", aliases=["FantasyMasks绮幻坊", "绮幻坊"],
          channels=[declaration("淘宝", "FantasyMasks绮幻坊", "FantasyMasks_")], qq=[("定制 QQ", "1487499638"), ("QQ 群", "936351202")],
          products=[product("鹿目圆头壳"), product("藿藿头壳"), product("和实由依头壳")],
          note="当前公开简介与置顶明确提供定制询价；可见作品主要为 2025 年，最新排期必须再确认。",
          merge="简介称全平台同名，但只明确点名淘宝；不据此自动确认闲鱼、拼多多或其他平台。"),
    maker("newfacedoll", "新颜玩偶 New Face Doll", "NewfacedolL",
          "公开账号确认 NFD 制作者名称；本次可见 X 作品主要为 2023 年，接单待核实。",
          "账号以 Kigurumi Maker NFD - New Face Doll 自我介绍，展示刑部姬、妮娅、摩根等头壳。旧目录关联淘宝及 Bilibili，但本次未取得有效的当前接单条款，不使用多年以前的 QQ 作为有效客服。",
          legacy="New Face Doll", aliases=["NFD", "NFD新颜玩偶", "New Face Doll"], status="unverified",
          note="制作方公开身份已确认；可见 X 更新停留于 2023-12，当前淘宝归属和接单状况待复核。",
          products=[product("刑部姬／妮娅／摩根头壳", "2023 年制作展示，不代表现货或当前委托入口")],
          merge="不与雷击工坊合并，早期手册的重复 QQ 不能作为身份依据。"),
    maker("shinkai", "深海工坊 Shinkai Workshop", "ShinkaiWorkshop",
          "青岛头壳手作工坊，公开接受国内外私信委托；2026 夏季促销已结束。",
          "官方简介写明位于 Qingdao,CN，承接 kigurumi 面具制作和海外订单。2026-06-29 至 07-31 的促销区分全头、3/4 壳及半定制，按已结束活动记录，不作为当前最低价。",
          legacy="Shinkai Workshop", aliases=["深海工房", "ShinkaiWorkshop"], location="中国山东青岛（官方业务账号自述）；详细地址未公开",
          categories=["全定制", "半定制"],
          products=[["Full-head Mask", "全头", "USD", "700", "历史促销／已结束", "2026-06-29 至 07-31；不含 PayPal 手续费与运费", "promotion"], ["3/4 Mask", "3/4 壳", "USD", "525", "历史促销／已结束", "同一活动期限；非当前报价", "promotion"], ["Semi-customized Mask", "半定制", "USD", "450", "历史促销／已结束", "同一活动期限；非当前报价", "promotion"]],
          merge="英文与中文工坊名称由同一官方简介对应；淘宝历史地址尚未取得第一方直链。",
          terms="通过 X 私信询价，接受海外订单。2026 夏季促销已经结束，活动价不含 PayPal 手续费和运费。"),
    maker("samon", "厚切三文鱼工坊 Samon", "samon_ii",
          "官方简介提供淘宝头壳定制入口及 QQ 群，并展示角色定制成果。",
          "工坊明确自述为 kigurumi 头壳制作者，要求定制需求从淘宝店咨询。作品包括祐天寺若麦、可可萝等；不将历史代理渠道的美元报价作为制作方本店报价。",
          legacy="厚切三文鱼工坊 / Samon", aliases=["KIGURUMI厚切三文鱼工坊", "Samon"],
          channels=[direct("淘宝", "厚切三文鱼工坊", "https://shop116489042.m.taobao.com/")], qq=[("QQ 群", "1025833372")],
          products=[product("祐天寺若麦头壳"), product("可可萝头壳")],
          merge="官方账号中的淘宝编号与历史目录一致；Lucky Larus 仅有历史代理关系，不能与 Samon 或 BHY 合为一家。"),
    maker("aniplus", "壳反应 Aniplus", "KFY_Aniplus",
          "制作 kigurumi 头壳，官方公开淘宝编号及海外业务账号。",
          "官方账号写明头壳、面具制作与合作私信，链接淘宝，并把海外业务指向日语账号。公开作品包含火花 lite、爱弥斯及洛天依客户定制；lite 名称不直接等同于统一量产规格。",
          legacy="壳反应Aniplus", aliases=["壳反应Aniplus", "KFY Aniplus"],
          channels=[direct("淘宝", "壳反应Aniplus", "https://shop567949612.taobao.com/")],
          products=[product("火花 lite 版头壳"), product("爱弥斯头壳"), product("洛天依客户定制头壳")],
          merge="@KFY_aniplus_JP 由主账号直接指定为海外订单入口，归为同品牌渠道。全平台同名声明不自动确认未点名的平台。"),
    maker("nm", "NM工坊 Nonhumanmasque", "nonhumanmasque",
          "中国头壳工作室，公开淘宝名称 nonhumanmasque 与店铺编号。",
          "官方中英简介直接说明中国头壳工作室身份及淘宝入口。页面能见到伊芙琳作品和此前定制名额活动。2025 年尾款减免、样品出售与抽奖都不是当前常规价格。",
          legacy="NM工坊", aliases=["nonhumanmasque", "NM工坊"], location="中国（官方业务简介）；具体城市未公开",
          channels=[direct("淘宝", "nonhumanmasque / NM工坊", "https://shop413645462.taobao.com/")],
          products=[product("伊芙琳头壳", "2025 年公开作品；当前规格与报价待询")],
          merge="英文名、NM 工坊与淘宝编号在官方简介直接对应。旧目录 QQ 群未在本次页面明文出现，不复制为当前号码。"),
    maker("xingyueqi", "星玥琦工坊", "xyq_kig",
          "公开淘宝同名店、角色定制及全球配送；过往单日促销与当前询价分开。",
          "公开业务简介写明 kigurumi mask maker、淘宝店名和全球配送。页面有多次单日现货促销，但未给出可核实的型号名称，也未在文本中明确美元币种；保留原文金额，不作为当前价目表。",
          legacy="星玥琦工坊", aliases=["XYQ", "xingyueqi"],
          channels=[declaration("淘宝", "星玥琦工坊", "xyq_kig")], categories=["全定制", "现货成品"],
          products=[["单日促销头壳（型号未标）", "历史现货", "", "459", "原文 $459；单日促销已过", "6 月 24 日帖子；称全球包邮，币种与当前库存未核实", "sale"]],
          merge="2025 目录重复两次列出星玥琦，合并为一份档案。此次邮箱显示被遮蔽，不将旧目录邮箱写成新核实联系方式。"),
    maker("sakurano", "乃粉罐头 Sakurano", "sakura_ingnai",
          "武汉头壳店，店主公开接受头壳定制和摄影委托，并提供业务群。",
          "店主公开业务简介明确店铺名乃粉罐头、坐标武汉、头壳定制及正片拍摄。账号兼有个人出勤内容，不能把每一张角色照片都当作该店商品；因此不据照片猜测型号和价格。",
          legacy="乃粉罐头 / Sakurano", aliases=["乃粉罐头", "Sakurano"], location="中国湖北武汉（公开业务简介）；不收录私人地址",
          qq=[("公开业务群", "549065952")], merge="店主账号明确声明乃粉罐头业务身份；淘宝 URL 仍仅为第三方历史关联。"),
    maker("rabbit", "兔子 Kigurumi 工坊", "Scarlet0rabbit",
          "公开接受国内外头壳定制，第一方提供淘宝编号与当前客户 QQ 群。",
          "店主公开介绍承接 kigurumi 定制及海外订单，近期作品帖重复链接国内淘宝店。此次简介客户群为 123280522，与旧目录不同，保留本轮第一方号码。",
          legacy="兔子kigurumi工坊", aliases=["兔子kigurumi工坊", "幻胧挽歌", "AliceKigWorkshop（历史渠道名）"],
          channels=[direct("淘宝", "兔子kigurumi工坊", "https://shop236878671.taobao.com/")], qq=[("客户 QQ 群", "123280522")],
          merge="历史 Etsy 名 AliceKigWorkshop 不等于 AKG / Alice Kig Garden。旧目录 Etsy 暂停的结论不推及当前淘宝；当前群号优先于旧目录。"),
    maker("beartech", "熊熊工业技研中心", "BearTechCenter",
          "以熊熊家kigurumi发布制作业务，接受成品与角色定制，公开淘宝名称。",
          "公开简介明确头壳成品可售、接受角色定制并指向淘宝熊熊技研，置顶另写完整名称熊熊工业技研中心。作品中有原神优菈人脸头壳；店名含熊不代表制作 furry 兽头，其他肤色衣业务单列。",
          legacy="熊熊工业技研中心", aliases=["熊熊家kigurumi", "熊熊技研", "BearTechCenter"],
          channels=[declaration("淘宝", "熊熊工业技研中心 / 熊熊技研", "BearTechCenter"), direct("淘宝", "官方简介中的店铺短链", "https://t.co/1z4JuoEySr")],
          categories=["全定制", "现货成品", "肤色衣"], products=[product("浪花骑士优菈头壳")],
          merge="简介与置顶将熊熊家、熊熊技研及完整淘宝名称对应；旧目录的长地址与短链尚未核实为同一 UID，分别标注证据。"),
    maker("magicdoll", "魔界工坊 MagicDoll", "MagicDoll1208",
          "官方账号提供角色定制、淘宝短链和 QQ 群；2026 暑期优惠已结束。",
          "工坊中英简介明确接受 kigurumi 角色委托。2026 年暑期活动为 7 月 20 日至 8 月 30 日，帖子中的四百元是优惠金额，不是头壳售价。公开角色作品包括耀嘉音和卡芙卡。",
          legacy="魔界工坊MagicDoll", aliases=["魔界工坊MagicDoll", "MagicDoll"],
          channels=[direct("淘宝", "魔界工坊官方公开短链", "https://m.tb.cn/h.73BDiObX12auhmW")], qq=[("QQ 群", "793242071")],
          products=[product("耀嘉音头壳"), product("卡芙卡头壳")],
          merge="原目录重复的魔界工坊记录合并。官方短链与第三方长地址的 UID 对应未实测，不借此伪造平台商品价格。"),
    maker("haka", "哈卡人形 Kigurumi", "hakarenxin99",
          "公开自制与定制建模说明，保留 2025 年历史均价；当前接单状态待核实。",
          "2025-05-20 置顶明确称头壳自制、定制建模，支持全球配送及 PayPal，并写出淘宝店名、QQ 群和平均价格范围。此次可读取帖子仍集中于 2025 年，历史报价不作为当前可下单价格。",
          legacy="哈卡人形kigurumi", aliases=["哈卡人形kigurumi", "Haka"], status="unverified",
          note="制作与店名声明来自 2025-05-20 置顶；当前报价、库存和新单受理缺少新证据。",
          channels=[declaration("淘宝", "哈卡人形kigurumi", "hakarenxin99")], qq=[("QQ 群", "1041285347")],
          products=[["自制头壳／定制建模", "定制服务", "CNY", "2500–3500", "2025 年店主自述均价", "非统一商品价；原帖另作约 USD350–500 的估算，不自行按汇率换算", "announcement"]],
          merge="淘宝名称由制作方置顶明确公开；历史店铺编号尚未获本次第一方直链验证。",
          terms="2025 年置顶称支持全球配送和 PayPal；当前付款方式、税费、工期及售后均待确认。"),
    maker("2dfantasy", "二维幻想 2D Fantasy", "2DFantasy111",
          "公开角色头壳定制、业务 QQ 与 2dfantasy 淘宝域名。",
          "业务简介明确 Kigurumi 头壳定制，要求带角色图通过 QQ 询价，直接标示淘宝域名。公开作品包括重音、可琳、明日香和休比；未公开统一整头售价。",
          legacy="二维幻想 / 2D Fantasy", aliases=["二维幻想", "2D Fantasy"],
          channels=[direct("淘宝", "二维幻想", "https://2dfantasy.taobao.com/")], qq=[("定制 QQ", "3983453230")],
          products=[product("重音／可琳／明日香／休比头壳")],
          merge="官方简介确认域名及名称。QQ 用途为带图定制联系，不把它误写为 QQ 群。"),
    maker("aria", "Haruka 的道具屋 ARIA", "mitsukiriya",
          "店主公开声明经营 ARIA、制作头壳，并直接提供淘宝链接。",
          "公开业务简介说明经营 haruka的道具屋ARIA，从事头壳制作；店铺相关内容通过私信联系。2025 年商品展示帖也重复指向同一淘宝编号，不将个人摄影、绘画或 AI 图片混入商品。",
          legacy="haruka的道具屋ARIA", aliases=["haruka的道具屋ARIA", "ARIA", "Haruka"], location="中国（业务简介）；具体城市未公开",
          channels=[direct("淘宝", "haruka的道具屋ARIA", "https://shop280538250.taobao.com/")],
          merge="官方简介与商品帖的淘宝编号一致；店主账号仅记录公开业务身份，不收录其他私人信息。"),
    maker("hideyoshi", "秀吉姬 Kigurumi 工坊", "lightning520",
          "手工头壳制作者，公开淘宝店名和私信定制入口。",
          "公开简介说明做头壳、私聊定制和淘宝名秀吉姬kigurumi，作品帖子提到妆容与模型改进及硬质造型。缺少具体型号、材料参数和售价时不补写。",
          legacy="秀吉姬kigurumi工坊", aliases=["秀吉姬kigurumi", "秀吉姬工坊"], location="中国（公开业务账号地区）；具体城市未公开",
          channels=[declaration("淘宝", "秀吉姬kigurumi", "lightning520")],
          merge="同一业务简介对应工坊名与淘宝名；历史店铺编号仍待第一方核实。"),
    maker("huyao", "狐妖手作 Kigurumi", "Huyaoshouzuo",
          "官方账号仍公开头壳来图定制与淘宝域名，独立官网处于维护状态。",
          "虽然 huyaoshouzuo.com 只显示维护和测量工具，官方 X 简介明确写头壳来图定做及淘宝 huyaoshouzuo.taobao.com。公开头壳作品包括古明地觉与赛马娘角色；同店服装和乳胶用品不计入头壳价格。",
          legacy="Kigurumi狐妖手作", aliases=["Kigurumi狐妖手作", "Huyaoshouzuo"],
          channels=[direct("淘宝", "kigurumi狐妖手作", "https://huyaoshouzuo.taobao.com/"), ["官网", "狐妖手作（维护中）", "https://huyaoshouzuo.com/", "官方简介关联；当前主要为测量工具", "profile"]],
          products=[product("古明地觉全头软支撑反重力造型"), product("赛马娘角色全头可拆卸反重力造型")],
          merge="官方账号直接关联品牌官网和淘宝域名；官网维护不等于整家业务停业。服装现货价不能冒充头壳售价。"),
]

# Additional sources are attached only after individual statements were reviewed.
by_id = {m["id"]: m for m in records}
for key, account, label, source_key, title in [
    ("shinkai", "ShinkaiWorkshop", "Jun 28", "promotion", "2026 夏季促销，已于 7 月 31 日结束"),
    ("xingyueqi", "xyq_kig", "Jun 24", "sale", "单日促销原帖；金额币种与现库存待核"),
    ("haka", "hakarenxin99", "May 20, 2025", "announcement", "2025-05-20 自制、店名与历史均价声明"),
]:
    by_id[key]["sources"][source_key] = [title, post(account, label)]
by_id["shinkai"]["price_summary"] = "现价询问；USD 450–700 为已结束活动价"
by_id["xingyueqi"]["price_summary"] = "现价询问；原文 $459 为过往单日促销"
by_id["haka"]["price_summary"] = "历史均价 CNY 2500–3500；现价待核"
for key, account in [("nekotofu", "NEKOTOUFU_shop"), ("haagaau", "haagaau_GF_EN")]:
    entry = by_id[key]
    entry["sources"]["international"] = ["官方关联的国际业务号", "https://x.com/" + account]
    entry["contacts"].append(["X 国际业务", "@" + account, "https://x.com/" + account, "international"])
by_id["nekotofu"]["contacts"].append(["Discord（肤色衣订购，出处）", "@VANGDE3293", "https://x.com/NEKOTOUFU_shop", "international"])
by_id["haagaau"]["sources"]["form"] = ["旧下单表本次需登录，未验证可提交", "https://docs.google.com/forms/d/e/1FAIpQLScgAfIOdUWjB1GRJr7OK_x6feWYJTZTnm6Arf4Y1GgMlMpL3g/viewform"]
by_id["haagaau"]["contacts"].append(["官方提及分店（未独立复核）", "@haagaau_TSP", "https://x.com/haagaau_TSP", "profile"])
by_id["aniplus"]["contacts"].append(["官方指定海外业务", "@KFY_aniplus_JP", "https://x.com/KFY_aniplus_JP", "profile"])

data = yaml.safe_load(DATA.read_text())
existing = {m["id"] for m in data["makers"]}
assert not existing.intersection(by_id), "Import is intentionally one-time; edit makers.yml for subsequent revisions"
with DATA.open("a") as target:
    target.write("\n  # 2026-09-09: reviewed public business profiles; marketplace inventory not accessed.\n")
    dumped = yaml.safe_dump(records, allow_unicode=True, sort_keys=False, width=110)
    target.write("\n".join("  " + line if line else "" for line in dumped.splitlines()) + "\n")
print(f"Imported {len(records)} reviewed business profiles")
