# 淘宝用户行为漏斗分析

> 基于 1 万用户 × 30 天行为数据（12.26M 行），分析电商转化漏斗、用户分群与留存，作为数据分析岗的求职作品。

## 项目背景

淘宝是最大的电商平台之一，理解"用户从浏览到购买"的行为路径是电商数据分析的核心问题。本项目基于阿里天池公开数据集的 1 万用户子集（30 天行为，1220 万行），回答以下业务问题：

- **用户从浏览到购买的转化漏斗长什么样？**
- **哪些环节流失最严重？**
- **流失的归因是什么？**
- **不同用户群体如何差异化运营？**

## STAR 摘要

- **S**ituation：淘宝 1 万用户 30 天行为数据（12.26M 行），5 个字段（用户/商品/行为类型/品类/时间），电商业务场景。
- **T**ask：定位漏斗流失最大环节，给出可执行的运营建议。
- **A**ction：
  1. 完成 ETL（CSV → Parquet，1.5GB+ → 109.5MB，加载快 10 倍）
  2. 四步漏斗分析，定位"浏览→收藏"流失 97.90% 为最大瓶颈（按事件次数）
  3. 用行为模式差异做归因：未购用户仅占 11.14%，但他们的浏览强度、浏览深度都只有转化用户的 1/3，加购率仅 2/3
  4. 构建 RFM 8 类用户分群，识别 14.8% 的 Champions 和 11.4% 的 Hibernating high-value
  5. Cohort 留存分析，定位 D1（51.58%）为关键流失拐点
- **R**esult：基于现有转化率推演，若"浏览→收藏"提升 2 个百分点（业内可达水平），日均潜在新增购买约 3,500 次；并提供 8 类用户差异化触达方案。

## 核心发现

1. **漏斗瓶颈在"浏览→收藏"**：11.5M 浏览 → 242K 收藏（drop 97.90%）
2. **D1 是留存关键拐点**：100% → 51.58%（drop 48.42%）
3. **11.14% 用户从未购买**：归因为"window shopping"，缺乏明确购买意图
4. **RFM 8 类分布不均**：最大群体是 Potential loyalists（23.8%），核心价值是 Champions（14.8%）
5. **黄金时段是 20-22 点**：浏览与购买同时达峰
6. **流失用户浏览强度低**：0.25x 转化用户，呈现"轻度浏览无购买意图"特征

## 业务建议

### 1. 优化"浏览→收藏"环节（最大流失点）
当前转化率仅 2.10%（事件次数）。可在用户浏览 10+ 个商品后仍未加购时，触发"看过此商品的用户还看了..."的个性化推荐。

### 2. D1 主动召回（留存关键）
D1 是 48.42% 的流失点。在用户首次浏览后 24 小时内做主动触达（push 通知、新手优惠券、引导完成首单）。

### 3. 流失用户差异化干预
针对 11.14% 从未购买用户，使用"加购送优惠"触发器，将他们的加购率（2.04%）提升到转化用户水平（3.16%）。

### 4. RFM 分群差异化运营
- **Champions（14.8%）**：VIP 服务 + 新品优先体验，维持忠诚度
- **Hibernating high-value（11.4%）**：定向高折扣券召回
- **Potential loyalists（23.8%）**：培养高 F/M，引导向 Champions 升级
- **Low-value dormant（17.6%）**：低优先级，节约营销预算

### 5. 黄金时段集中投放
20-22 点是浏览和购买双高峰，应集中营销资源而非 24 小时均匀分配。

### 6. 品类差异化策略
Top 10 品类购买率差异显著（详见 `02_funnel_by_category.png`），高转化品类扩流量、低转化品类做内容种草。

## 量化业务影响

> ⚠️ 以下数字为**示例推演**，假设业务规模放大到日浏览 50 万次的典型电商场景。多个假设条件叠加，仅用于说明"分析可量化业务影响"，不作为精确预测。

- 若"浏览→收藏"提升 2 个百分点（业内可达水平），**日均潜在新增购买约 3,500 次**
- 若 D1 召回提升留存 5 个百分点，**月新增订单估算 1.5 万**
- 若召回 10% 的 Hibernating high-value 用户，**月活增量约 114 用户**

## 技术栈

- **数据处理**：Python 3.10+, Pandas, NumPy, PyArrow
- **可视化**：Matplotlib, Seaborn
- **环境**：Jupyter Notebook + 虚拟环境
- **数据格式**：CSV（输入）→ Parquet（中间，109MB）→ CSV（派生）

## 关键技术决策

> 列出**有意思的取舍**，展示"我为什么选 X 不选 Y"

1. **选择 ETL 转 Parquet 而非直接读 CSV**：CSV 占用 1.5GB+ 内存，加载 30 秒+；Parquet 压缩到 109MB，加载 3 秒，且保留类型信息。
2. **选择 Seaborn + Matplotlib 而非 Plotly**：分析报告以静态图表为主，Seaborn 与 Matplotlib 配合更顺手，且不依赖 JavaScript 渲染。
3. **不选择机器学习模型**：本项目是描述性分析（发生了什么、为什么），非预测性分析（未来会发生什么）；建模属于数据科学岗方向。
4. **RFM 用 3×3×3 分箱而非 KMeans 聚类**：分箱可解释性强、业务方容易理解，且 1 万样本量下聚类边界不稳定。
5. **数据通过软链而非复制**：避免在仓库中保存 482MB 大文件，保持仓库轻量。
6. **数据质量"清洗而非删除"**：对发现的 3 个数据质量问题，没有简单 dropna，而是逐个评估影响后做保留/标记（详见 Notebook 01）。
7. **漏斗用事件次数而非独立用户数**：因为本数据集 88.86% 用户最终都会购买，独立用户数漏斗不是单调的；事件次数才能体现"漏斗压力"。
8. **RFM 用品类多样性代替金额（M）**：因数据无价格信息，行为多样性是 M 的最佳代理变量。

## 项目结构

```
taobao_user_behavior_analysis/
├── README.md                # 本文件
├── requirements.txt         # 依赖锁定
├── .gitignore               # 排除数据/图片
├── data/
│   ├── raw/                 # 软链到原始 CSV
│   ├── processed.parquet    # ETL 产出（109MB）
│   └── derived/             # notebook 派生 CSV
├── scripts/
│   ├── 01_build_parquet.py  # ETL 脚本
│   └── utils.py             # 通用工具（数据加载、绘图样式）
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_conversion_funnel.ipynb
│   ├── 03_user_segmentation_rfm.ipynb
│   ├── 04_retention_cohort.ipynb
│   └── 05_findings_and_recommendations.ipynb
└── images/                  # 导出的图表 PNG
```

| Notebook | 一句话说明 |
|---------|----------|
| 01 - 数据探索 | 数据规模、字段类型、4 种行为分布、用户活跃度 |
| 02 - 漏斗分析 | 4 步漏斗 + 分层（时段/品类）+ 流失归因（核心） |
| 03 - RFM 分群 | 8 类用户群体 + 差异化运营策略 |
| 04 - Cohort 留存 | 30 天留存热力图 + 整体留存曲线 |
| 05 - 总结 | 业务洞察 + 量化影响 + 数据局限 |

## 图表汇总

| 图 | 文件 |
|----|-----|
| 4 种行为整体分布 | `images/01_behavior_distribution.png` |
| 24 小时行为分布 | `images/01_hourly_distribution.png` |
| 用户活跃度长尾 | `images/01_user_activity_distribution.png` |
| 4 步漏斗（事件次数）| `images/02_overall_funnel.png` |
| 各小时购买转化率 | `images/02_funnel_by_hour.png` |
| Top 10 品类购买率 | `images/02_funnel_by_category.png` |
| 流失用户 vs 转化用户归因 | `images/02_attribution_comparison.png` |
| RFM 8 类规模分布 | `images/03_rfm_segment_pie.png` |
| RFM 群体特征雷达 | `images/03_rfm_segment_radar.png` |
| Cohort 留存热力图 | `images/04_cohort_retention_heatmap.png` |
| 整体留存曲线 | `images/04_overall_retention_curve.png` |

## 如何复现

```bash
# 1. 克隆仓库
git clone https://github.com/sherry-wsr/taboo.git
cd taboo

# 2. 创建虚拟环境
cd taobao_user_behavior_analysis
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 准备数据（建立软链，需要外部数据集 taobao_data/user_action.csv）
mkdir -p data/raw
ln -sf ../../taobao_data/user_action.csv data/raw/user_action.csv

# 5. 运行 ETL
python scripts/01_build_parquet.py

# 6. 启动 Jupyter，依次运行 notebooks/01 ~ 05
jupyter notebook
```

## 数据说明

- **来源**：阿里天池公开数据集（淘宝用户行为）
- **原始数据**：100 万用户完整行为，本项目使用 1 万用户子集
- **字段**：`user_id`, `item_id`, `behavior_type`, `item_category`, `time`
- **时间范围**：2014-11-18 ~ 2014-12-18（30 天）
- **数据局限**：用户/商品/品类 ID 脱敏、无价格信息、无用户属性、30 天窗口

## 数据局限

- 30 天时间窗口限制（无法看长期留存）
- 所有 ID 脱敏（无法结合业务知识解读）
- 无价格信息（无法算 GMV/客单价）
- 无用户属性（无法做画像分层）
- 无营销/运营记录（无法做 A/B 归因）

详见 Notebook 05 的"数据局限"小节。

## 关于我

数据分析师 / 应届生，专注于电商和用户行为分析方向。

- GitHub: https://github.com/sherry-wsr
- Email: 1342722650@qq.com

## License

本项目仅供学习与求职展示使用。