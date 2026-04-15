import json
import sys
import os
import uuid
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.research import ResearchMessage, ResearchMessageRead

MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

SEED_MESSAGES = [
    {
        "title": "2026年二季度宏观经济展望：政策宽松预期升温",
        "summary": "央行降准预期增强，财政政策加码基建投资，GDP增速目标维持5%左右。",
        "body": "# 2026年二季度宏观经济展望\n\n## 核心观点\n\n1. **货币政策**：央行降准预期增强，市场流动性保持合理充裕\n2. **财政政策**：专项债发行提速，基建投资成为稳增长重要抓手\n3. **GDP展望**：全年增速目标维持5%左右，二季度环比有望回升\n\n## 风险提示\n\n- 海外通胀反复可能制约国内政策空间\n- 房地产市场恢复节奏仍有不确定性",
        "content_format": "markdown",
        "category": "宏观经济",
        "source_type": "manual",
        "source_name": "宏观研究部",
        "published_at": datetime(2026, 4, 14, 8, 0, 0),
        "links": json.dumps([{"label": "完整报告PDF", "url": "https://example.com/macro-q2-2026.pdf"}]),
    },
    {
        "title": "4月MLF操作点评：释放积极信号",
        "summary": "央行4月MLF操作利率下调10bp，释放货币宽松信号。",
        "body": "# 4月MLF操作点评\n\n央行4月15日开展MLF操作，中标利率下调10bp至2.35%。本次降息释放了明确的货币宽松信号，有助于降低实体经济融资成本。\n\n## 影响分析\n\n- 债券市场：利好长端利率下行\n- 股票市场：有利于成长股估值修复\n- 银行板块：净息差压力短期承压",
        "content_format": "markdown",
        "category": "宏观经济",
        "source_type": "manual",
        "source_name": "固收研究部",
        "published_at": datetime(2026, 4, 13, 14, 30, 0),
        "links": json.dumps([]),
    },
    {
        "title": "CPI与PPI月度跟踪：通胀温和回升",
        "summary": "3月CPI同比上涨1.2%，PPI同比下降0.5%，通胀整体温和。",
        "body": "# 3月通胀数据点评\n\n- CPI同比+1.2%（前值+0.8%），食品价格是主要推动力\n- PPI同比-0.5%（前值-1.1%），工业品价格降幅收窄\n- 核心CPI同比+0.9%，内需温和修复",
        "content_format": "markdown",
        "category": "宏观经济",
        "source_type": "feed",
        "source_name": "数据速递",
        "published_at": datetime(2026, 4, 13, 9, 0, 0),
        "links": json.dumps([{"label": "统计局原文", "url": "https://example.com/stats-cpi"}]),
    },
    {
        "title": "新能源汽车产业链4月跟踪：锂电排产环比回升",
        "summary": "4月电池排产环比增长15%，碳酸锂价格企稳回升。",
        "body": "# 新能源产业链跟踪\n\n## 电池排产\n\n4月主要电池厂排产环比增长15%，其中方形电池增长18%，圆柱电池增长12%。\n\n## 上游材料\n\n- 碳酸锂价格企稳在8.5万元/吨\n- 正极材料需求回暖\n- 负极材料产能利用率提升至75%\n\n## 投资建议\n\n关注电池龙头及上游材料供应商的业绩弹性。",
        "content_format": "markdown",
        "category": "行业研究",
        "source_type": "feed",
        "source_name": "行业研究部",
        "published_at": datetime(2026, 4, 12, 10, 0, 0),
        "links": json.dumps([{"label": "产业链数据", "url": "https://example.com/ev-chain"}]),
        "metadata_": json.dumps({"sector": "新能源"}),
    },
    {
        "title": "半导体行业深度：AI芯片需求持续高增",
        "summary": "AI算力需求驱动高端芯片出货量增长，国产替代加速。",
        "body": "# 半导体行业深度报告\n\n## AI芯片市场\n\n全球AI芯片市场规模预计2026年达到800亿美元，同比增长45%。\n\n## 国产替代进展\n\n- 先进制程：14nm量产稳定，7nm研发推进\n- EDA工具：国产EDA覆盖率提升至30%\n- 设备：刻蚀、薄膜设备国产化率超40%",
        "content_format": "markdown",
        "category": "行业研究",
        "source_type": "feed",
        "source_name": "科技研究部",
        "published_at": datetime(2026, 4, 11, 16, 0, 0),
        "links": json.dumps([]),
        "metadata_": json.dumps({"sector": "半导体"}),
    },
    {
        "title": "医药行业周报：创新药出海再获突破",
        "summary": "国内药企FDA获批数量创新高，CXO订单回暖。",
        "body": "# 医药行业周报（4月第2周）\n\n## 本周要闻\n\n1. XX药业PD-1单抗获FDA批准上市\n2. CXO行业订单环比增长20%\n3. 集采续约政策温和，利好仿制药企业\n\n## 投资建议\n\n重点关注创新药出海龙头及CXO行业回暖标的。",
        "content_format": "markdown",
        "category": "行业研究",
        "source_type": "manual",
        "source_name": "医药研究部",
        "published_at": datetime(2026, 4, 11, 9, 0, 0),
        "links": json.dumps([]),
        "metadata_": json.dumps({"sector": "医药"}),
    },
    {
        "title": "XX银行2025年报点评：资产质量持续改善",
        "summary": "不良率降至1.05%，拨备覆盖率提升至320%，分红比例提高。",
        "body": "<h1>XX银行2025年报点评</h1><h2>业绩概要</h2><ul><li>营收同比+8.2%，归母净利润+12.5%</li><li>不良贷款率1.05%，较年初下降15bp</li><li>拨备覆盖率320.5%，安全边际充足</li><li>每股分红0.85元，分红比例提升至32%</li></ul><h2>核心看点</h2><p>零售转型成效显著，财富管理AUM突破5万亿。对公贷款结构优化，制造业和绿色贷款占比提升。</p>",
        "content_format": "html",
        "category": "个股分析",
        "source_type": "mock",
        "source_name": "金融研究部",
        "published_at": datetime(2026, 4, 10, 8, 30, 0),
        "links": json.dumps([]),
        "metadata_": json.dumps({"ticker": "600000.SH"}),
    },
    {
        "title": "YY科技一季报前瞻：业绩有望超预期",
        "summary": "云计算业务高增，预计一季度收入同比增长35%。",
        "body": "<h1>YY科技一季报前瞻</h1><p>基于产业链调研，我们预计YY科技2026年一季度：</p><ul><li>收入：约450亿元，同比+35%</li><li>净利润：约80亿元，同比+42%</li><li>云计算收入：约180亿元，占比40%</li></ul><p><strong>投资评级</strong>：维持「买入」评级，目标价350元。</p>",
        "content_format": "html",
        "category": "个股分析",
        "source_type": "mock",
        "source_name": "科技研究部",
        "published_at": datetime(2026, 4, 9, 15, 0, 0),
        "links": json.dumps([{"label": "估值模型", "url": "https://example.com/yy-model.xlsx"}]),
        "metadata_": json.dumps({"ticker": "YYYY.HK"}),
    },
    {
        "title": "ZZ新能源季度经营数据：交付量创新高",
        "summary": "一季度交付12万辆，同比增长60%，海外占比提升。",
        "body": "<h1>ZZ新能源经营数据</h1><p>2026Q1交付量12万辆（YoY+60%），其中海外交付3.5万辆，占比29%。新车型Z9于3月上市，首月订单超2万。</p>",
        "content_format": "html",
        "category": "个股分析",
        "source_type": "mock",
        "source_name": "汽车研究部",
        "published_at": datetime(2026, 4, 8, 10, 0, 0),
        "links": json.dumps([]),
    },
    {
        "title": "利率债周策略：配置价值凸显",
        "summary": "10Y国债收益率降至2.6%，建议逢低加配长久期利率债。",
        "body": "利率债周度策略报告\n\n本周10年期国债收益率下行5bp至2.60%，30年期下行3bp至2.85%。\n\n策略建议：\n1. 利率债配置价值凸显，建议加配长久期品种\n2. 关注4月税期对资金面的扰动\n3. 信用债利差继续压缩空间有限，建议保持中性",
        "content_format": "plain",
        "category": "固收债券",
        "source_type": "manual",
        "source_name": "固收研究部",
        "published_at": datetime(2026, 4, 7, 8, 0, 0),
        "links": json.dumps([{"label": "收益率曲线", "url": "https://example.com/yield-curve"}]),
    },
    {
        "title": "信用债市场周报：城投债利差分化",
        "summary": "高等级城投利差压缩，弱区域城投估值承压。",
        "body": "信用债市场周报\n\n本周信用债成交活跃，高等级城投利差继续压缩。但弱区域城投债（如贵州、云南）利差走阔10-20bp。\n\n建议：聚焦经济强省城投平台，回避弱资质主体。",
        "content_format": "plain",
        "category": "固收债券",
        "source_type": "manual",
        "source_name": "固收研究部",
        "published_at": datetime(2026, 4, 6, 14, 0, 0),
        "links": json.dumps([]),
    },
    {
        "title": "可转债投资策略：关注低价转债修复机会",
        "summary": "低价转债组合近一周上涨2.3%，转股溢价率合理。",
        "body": "可转债投资策略更新\n\n近期低价转债表现活跃，建议关注：\n1. 价格在100-110元的低价转债\n2. 正股基本面改善的品种\n3. 转股溢价率低于30%的标的",
        "content_format": "plain",
        "category": "固收债券",
        "source_type": "feed",
        "source_name": "量化研究部",
        "published_at": datetime(2026, 4, 5, 9, 30, 0),
        "links": json.dumps([]),
    },
    {
        "title": "南方成长先锋混合基金月报",
        "summary": "3月净值增长4.2%，跑赢基准1.8个百分点。",
        "body": "# 南方成长先锋混合基金月报（2026年3月）\n\n## 业绩表现\n\n- 本月净值增长：**4.2%**\n- 业绩基准收益：2.4%\n- 超额收益：+1.8%\n\n## 持仓调整\n\n- 增持：新能源、半导体\n- 减持：消费、地产\n- 前十大持仓集中度：45%\n\n## 展望\n\n看好科技成长方向，维持较高仓位运作。",
        "content_format": "markdown",
        "category": "基金产品",
        "source_type": "glue",
        "source_name": "产品运营部",
        "published_at": datetime(2026, 4, 4, 10, 0, 0),
        "links": json.dumps([{"label": "完整月报", "url": "https://example.com/fund-monthly"}]),
        "metadata_": json.dumps({"fundCode": "000001"}),
    },
    {
        "title": "南方稳健收益债券基金季报摘要",
        "summary": "一季度年化收益5.8%，最大回撤0.3%。",
        "body": "# 南方稳健收益债券基金2026Q1季报\n\n## 业绩\n\n- 一季度收益：1.45%（年化5.8%）\n- 最大回撤：0.3%\n- 夏普比率：3.2\n\n## 策略回顾\n\n以中高等级信用债为底仓，适度参与利率波段。转债增强贡献约0.3%的收益。",
        "content_format": "markdown",
        "category": "基金产品",
        "source_type": "glue",
        "source_name": "产品运营部",
        "published_at": datetime(2026, 4, 2, 16, 0, 0),
        "links": json.dumps([]),
        "metadata_": json.dumps({"fundCode": "000002"}),
    },
    {
        "title": "新发基金预告：南方数字经济主题基金",
        "summary": "聚焦数字经济核心赛道，4月15日起发行。",
        "body": "# 新发基金预告\n\n**南方数字经济主题混合基金**将于2026年4月15日起公开发行。\n\n## 产品亮点\n\n- 聚焦AI、云计算、大数据等数字经济核心赛道\n- 拟任基金经理：XX（10年投研经验）\n- 认购费率优惠：1折起\n\n*本基金为混合型基金，其预期收益及预期风险水平高于货币基金和债券基金，低于股票基金。*",
        "content_format": "markdown",
        "category": "基金产品",
        "source_type": "glue",
        "source_name": "产品运营部",
        "published_at": datetime(2026, 4, 1, 9, 0, 0),
        "links": json.dumps([{"label": "产品说明书", "url": "https://example.com/fund-prospectus"}]),
        "metadata_": json.dumps({"fundCode": "000003"}),
    },
]

PRE_READ_INDICES = [0, 3, 6]


def seed():
    app = create_app("dev")
    with app.app_context():
        db.create_all()

        if ResearchMessage.query.first() is not None:
            print("Database already has data. Skipping seed.")
            return

        for i, data in enumerate(SEED_MESSAGES):
            msg = ResearchMessage(
                id=str(uuid.uuid4()),
                title=data["title"],
                summary=data.get("summary"),
                body=data["body"],
                content_format=data.get("content_format", "markdown"),
                published_at=data["published_at"],
                category=data.get("category"),
                source_type=data.get("source_type"),
                source_name=data.get("source_name"),
                links=data.get("links"),
                metadata_=data.get("metadata_"),
            )
            db.session.add(msg)
            db.session.flush()

            if i in PRE_READ_INDICES:
                read_record = ResearchMessageRead(
                    user_id=MOCK_USER_ID,
                    message_id=msg.id,
                )
                db.session.add(read_record)

        db.session.commit()
        total = ResearchMessage.query.count()
        read_count = ResearchMessageRead.query.filter_by(user_id=MOCK_USER_ID).count()
        print(f"Seeded {total} messages, {read_count} pre-marked as read.")


if __name__ == "__main__":
    seed()
