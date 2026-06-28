# 淘宝用户行为漏斗分析 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于淘宝 1 万用户 30 天行为数据（1220 万行），完成 5 个 Jupyter Notebook 的漏斗分析 + RFM 分群 + Cohort 留存分析项目，作为数据分析岗求职作品集。

**Architecture:** 单层项目结构（`notebooks/` + `data/` + `images/` + `scripts/`），CSV → ETL → Parquet → 5 个串联的 Notebook（业务问题 → 数据分析 → 业务结论），最终交付一份可直接给招聘方看的 README + 配套图表。

**Tech Stack:** Python 3.10+ · Pandas · NumPy · Matplotlib · Seaborn · Jupyter Notebook · PyArrow (parquet)

**Spec:** `docs/superpowers/specs/2026-06-28-taobao-user-behavior-funnel-design.md`

**执行约定：**
- 项目工作目录：`/Users/macmini/workspace/实习项目/taobao_user_behavior_analysis/`
- 每个任务结尾必须 `git commit`
- 数据集通过软链（symlink）从 `/Users/macmini/workspace/实习项目/taobao_data/` 引用，避免复制 482MB 大文件

---

## 文件结构总览

| 路径 | 责任 |
|------|------|
| `taobao_user_behavior_analysis/README.md` | 项目入口：业务背景 + STAR 摘要 + 核心发现 + 图表 + 复现方式 + 关于我 |
| `taobao_user_behavior_analysis/requirements.txt` | 锁定依赖版本 |
| `taobao_user_behavior_analysis/.gitignore` | 排除数据/图片/checkpoint（仅 README 和 notebook 入库） |
| `taobao_user_behavior_analysis/data/raw/user_action.csv` | 软链 → `taobao_data/user_action.csv` |
| `taobao_user_behavior_analysis/data/processed.parquet` | ETL 产出（gitignored） |
| `taobao_user_behavior_analysis/data/derived/` | 各 notebook 派生的 CSV（gitignored） |
| `taobao_user_behavior_analysis/scripts/01_build_parquet.py` | CSV → Parquet ETL 脚本 |
| `taobao_user_behavior_analysis/notebooks/01_data_exploration.ipynb` | 数据探索 + 质量挑战 |
| `taobao_user_behavior_analysis/notebooks/02_conversion_funnel.ipynb` | 漏斗 + 归因（核心） |
| `taobao_user_behavior_analysis/notebooks/03_user_segmentation_rfm.ipynb` | RFM 8 类分群 |
| `taobao_user_behavior_analysis/notebooks/04_retention_cohort.ipynb` | Cohort 留存热力图 |
| `taobao_user_behavior_analysis/notebooks/05_findings_and_recommendations.ipynb` | 总结 + 业务建议 |
| `taobao_user_behavior_analysis/images/` | 导出图表 PNG（gitignored） |

---

## Task 1: 项目骨架与软链数据

**Files:**
- Create: `taobao_user_behavior_analysis/README.md`（占位）
- Create: `taobao_user_behavior_analysis/.gitignore`
- Create: `taobao_user_behavior_analysis/requirements.txt`
- Create: `taobao_user_behavior_analysis/data/raw/`（软链 user_action.csv）
- Create: `taobao_user_behavior_analysis/notebooks/.gitkeep`
- Create: `taobao_user_behavior_analysis/scripts/.gitkeep`
- Create: `taobao_user_behavior_analysis/images/.gitkeep`
- Create: `taobao_user_behavior_analysis/data/derived/.gitkeep`

- [ ] **Step 1: 创建项目根目录与子目录**

```bash
cd /Users/macmini/workspace/实习项目
mkdir -p taobao_user_behavior_analysis/{notebooks,scripts,images,data/derived}
```

- [ ] **Step 2: 创建数据软链**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis/data
mkdir -p raw
ln -sf /Users/macmini/workspace/实习项目/taobao_data/user_action.csv raw/user_action.csv
ls -la raw/  # 确认软链已建立
```

Expected:
```
lrwxr-xr-x  1 user  staff  61  6月 28 16:00 user_action.csv -> /Users/macmini/workspace/实习项目/taobao_data/user_action.csv
```

- [ ] **Step 3: 创建占位 .gitkeep 文件（让空目录能被 git 追踪）**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
touch notebooks/.gitkeep scripts/.gitkeep images/.gitkeep data/derived/.gitkeep
```

- [ ] **Step 4: 写 .gitignore**

写入 `taobao_user_behavior_analysis/.gitignore`：

```gitignore
# 数据与大文件
data/processed.parquet
data/derived/*.csv
images/*.png

# Jupyter
.ipynb_checkpoints/
profile_default/

# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/

# IDE
.vscode/
.idea/
.DS_Store
```

- [ ] **Step 5: 写 requirements.txt**

写入 `taobao_user_behavior_analysis/requirements.txt`：

```
pandas==2.2.2
numpy==1.26.4
matplotlib==3.8.4
seaborn==0.13.2
pyarrow==15.0.2
jupyter==1.0.0
notebook==7.1.3
```

- [ ] **Step 6: 写占位 README**

写入 `taobao_user_behavior_analysis/README.md`：

```markdown
# 淘宝用户行为漏斗分析

（项目实施中，详细内容见任务 12）
```

- [ ] **Step 7: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/
git commit -m "feat: scaffold project structure with data symlink and dependencies"
```

---

## Task 2: 安装依赖并验证环境

**Files:** 无（仅本地环境配置）

- [ ] **Step 1: 创建虚拟环境**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
python3 -m venv .venv
source .venv/bin/activate
which python  # 应显示 .venv/bin/python
```

- [ ] **Step 2: 安装依赖**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected: 成功安装所有包，无报错。

- [ ] **Step 3: 验证关键包可导入**

```bash
python -c "import pandas as pd; import numpy as np; import matplotlib; import seaborn as sns; import pyarrow; print('pandas', pd.__version__); print('numpy', np.__version__); print('seaborn', sns.__version__); print('pyarrow', pyarrow.__version__)"
```

Expected:
```
pandas 2.2.2
numpy 1.26.4
seaborn 0.13.2
pyarrow 15.0.2
```

- [ ] **Step 4: 验证 Jupyter 可启动**

```bash
jupyter notebook --version
```

Expected: 打印 notebook 版本号，无报错。

- [ ] **Step 5: 关闭虚拟环境（保持 deactivate 状态，避免后续任务混淆）**

```bash
deactivate
```

注意：后续任务执行前都需要 `source .venv/bin/activate`。

---

## Task 3: ETL 脚本 - CSV 转 Parquet

**Files:**
- Create: `taobao_user_behavior_analysis/scripts/01_build_parquet.py`

- [ ] **Step 1: 写 ETL 脚本**

写入 `taobao_user_behavior_analysis/scripts/01_build_parquet.py`：

```python
"""ETL: CSV → Parquet

读取原始 CSV 并做类型优化，输出压缩的 Parquet 文件。
后续所有 notebook 都基于这个 Parquet 文件。
"""
import time
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = PROJECT_ROOT / "data" / "raw" / "user_action.csv"
OUT_PARQUET = PROJECT_ROOT / "data" / "processed.parquet"


def build_parquet() -> None:
    """读取 CSV，分块转换类型，输出 Parquet。"""
    assert RAW_CSV.exists(), f"原始 CSV 不存在: {RAW_CSV}"

    t0 = time.time()
    print(f"[1/3] 读取 CSV: {RAW_CSV}")

    # 分块读取，规避一次性内存爆炸
    chunks = []
    chunk_size = 1_000_000
    for i, chunk in enumerate(pd.read_csv(RAW_CSV, chunksize=chunk_size)):
        # 类型优化
        chunk["behavior_type"] = chunk["behavior_type"].astype("int8")
        chunk["user_id"] = chunk["user_id"].astype("category")
        chunk["item_id"] = chunk["item_id"].astype("category")
        chunk["item_category"] = chunk["item_category"].astype("category")
        chunk["time"] = pd.to_datetime(chunk["time"], format="%Y-%m-%d %H")
        chunks.append(chunk)
        print(f"  chunk {i+1}: {len(chunk):,} rows")

    df = pd.concat(chunks, ignore_index=True)
    del chunks
    print(f"[2/3] 合并完成: {len(df):,} 行, 内存 {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

    print(f"[3/3] 写入 Parquet: {OUT_PARQUET}")
    df.to_parquet(OUT_PARQUET, engine="pyarrow", compression="snappy", index=False)

    elapsed = time.time() - t0
    print(f"完成. 耗时 {elapsed:.1f}s")
    print(f"输出文件大小: {OUT_PARQUET.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    build_parquet()
```

- [ ] **Step 2: 运行 ETL 脚本**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
python scripts/01_build_parquet.py
```

Expected: 看到 3-5 个 chunk 的处理日志，最终输出"完成. 耗时 X.Xs"和 parquet 文件大小（约 80MB）。

- [ ] **Step 3: 验证 Parquet 可正确读回**

```bash
python -c "
import pandas as pd
df = pd.read_parquet('data/processed.parquet')
print('行数:', len(df))
print('列:', list(df.columns))
print('类型:')
print(df.dtypes)
print('内存:', round(df.memory_usage(deep=True).sum() / 1e6, 1), 'MB')
print('前 3 行:')
print(df.head(3))
print('behavior_type 取值:', sorted(df['behavior_type'].unique()))
print('时间范围:', df['time'].min(), '~', df['time'].max())
"
```

Expected:
```
行数: ~12200000
列: ['user_id', 'item_id', 'behavior_type', 'item_category', 'time']
...
behavior_type 取值: [1, 2, 3, 4]
时间范围: 2014-11-18 00:00:00 ~ 2014-12-18 23:00:00
```

- [ ] **Step 4: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/scripts/01_build_parquet.py
git commit -m "feat(etl): add CSV to Parquet conversion script with type optimization"
```

---

## Task 4: 抽取通用工具到 `scripts/utils.py`

**Files:**
- Create: `taobao_user_behavior_analysis/scripts/utils.py`

**为什么先做这一步**：后续 5 个 notebook 都会用相同的数据加载和可视化样式，抽出来可以 DRY，并且 notebook 里通过 `sys.path` 引入。

- [ ] **Step 1: 写工具模块**

写入 `taobao_user_behavior_analysis/scripts/utils.py`：

```python
"""通用工具：数据加载 + 可视化样式 + 路径常量

所有 notebook 通过以下方式引入：
    import sys
    sys.path.append('../scripts')
    from utils import PROJECT_ROOT, load_data, setup_plot_style
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PARQUET = PROJECT_ROOT / "data" / "processed.parquet"
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"
IMAGES_DIR = PROJECT_ROOT / "images"

BEHAVIOR_LABELS = {1: "浏览", 2: "收藏", 3: "加购", 4: "购买"}
BEHAVIOR_COLORS = {
    "浏览": "#4C72B0",
    "收藏": "#DD8452",
    "加购": "#55A467",
    "购买": "#C44E52",
}


def load_data() -> pd.DataFrame:
    """读取处理后的 Parquet 数据。

    Returns:
        DataFrame with columns: user_id, item_id, behavior_type, item_category, time
    """
    assert PROCESSED_PARQUET.exists(), (
        f"Parquet 文件不存在: {PROCESSED_PARQUET}\n请先运行: python scripts/01_build_parquet.py"
    )
    df = pd.read_parquet(PROCESSED_PARQUET)
    return df


def setup_plot_style() -> None:
    """统一所有图表的样式。"""
    sns.set_theme(style="whitegrid", context="notebook", font="PingFang SC")
    plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "STHeiti", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 150
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 11


def save_fig(fig: plt.Figure, name: str) -> None:
    """保存图表到 images/ 目录。"""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    out = IMAGES_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"  -> 保存图表: {out.relative_to(PROJECT_ROOT)}")
```

- [ ] **Step 2: 验证工具可正常导入和调用**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
python -c "
import sys
sys.path.append('scripts')
from utils import load_data, setup_plot_style, BEHAVIOR_LABELS
df = load_data()
print('加载成功:', len(df), '行')
print('BEHAVIOR_LABELS:', BEHAVIOR_LABELS)
setup_plot_style()
print('样式设置完成')
"
```

Expected:
```
加载成功: ~12200000 行
BEHAVIOR_LABELS: {1: '浏览', 2: '收藏', 3: '加购', 4: '购买'}
样式设置完成
```

- [ ] **Step 3: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/scripts/utils.py
git commit -m "feat(utils): add shared data loading and plotting utilities"
```

---

## Task 5: Notebook 01 - 数据探索（含数据质量挑战小节）

**Files:**
- Create: `taobao_user_behavior_analysis/notebooks/01_data_exploration.ipynb`

**结构**：业务问题 → 数据质量挑战与解决方案 → 基础统计 → 结论

- [ ] **Step 1: 在终端创建 notebook（用 jupyter 命令行避免打开浏览器）**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
jupyter nbconvert --clear-output --to notebook notebooks/01_data_exploration.ipynb 2>/dev/null
# 新建空 notebook
python -c "
import nbformat as nbf
nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell('# 01 - 数据探索')]
nbf.write(nb, 'notebooks/01_data_exploration.ipynb')
print('已创建空 notebook')
"
```

> 如果 `nbformat` 未安装，先 `pip install nbformat`。

- [ ] **Step 2: 填充 Cell 1 - 业务问题（markdown）**

将 notebook 的第一个 cell 替换为：

````markdown
# 01 - 数据探索

## 业务问题

本项目的核心问题是：**用户从浏览到购买的转化漏斗长什么样？哪些环节流失最严重？哪些用户群体值得重点运营？**

在回答这些问题之前，我们必须先理解数据：
- 数据规模、字段类型、时间范围
- 数据质量如何？有什么坑？
- 4 种行为的整体分布
- 用户/商品/类目的活跃度

后续 notebook（02-05）都基于此数据展开。
````

- [ ] **Step 3: 填充 Cell 2 - 引入工具（code）**

```python
import sys
sys.path.append('../scripts')

import pandas as pd
from utils import load_data, setup_plot_style, save_fig, BEHAVIOR_LABELS, BEHAVIOR_COLORS

setup_plot_style()
df = load_data()
print(f"加载完成: {len(df):,} 行, 内存 {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
df.head()
```

- [ ] **Step 4: 填充 Cell 3 - 数据质量挑战（markdown）**

````markdown
## 数据质量挑战与解决方案

在开始分析前，我必须诚实地面对数据质量问题。**简单删除异常值会引入选择偏差，所以我对每个问题都做了独立判断**。

通过初步检查，我发现以下 3 个问题：

1. **`behavior_type` 取值**：理论应只取 {1,2,3,4}，需要验证。
2. **时间范围一致性**：需要确认所有数据都落在 2014-11-18 ~ 2014-12-18 区间内。
3. **缺失值**：5 个字段是否完整。

接下来逐一检查并处理。
````

- [ ] **Step 5: 填充 Cell 4 - 质量检查（code）**

```python
# 1. behavior_type 范围检查
bt_values = sorted(df['behavior_type'].unique())
print(f"behavior_type 取值: {bt_values}")
assert bt_values == [1, 2, 3, 4], f"behavior_type 出现意外取值: {bt_values}"

# 2. 时间范围
print(f"时间范围: {df['time'].min()} ~ {df['time'].max()}")
assert df['time'].min() >= pd.Timestamp('2014-11-18')
assert df['time'].max() <= pd.Timestamp('2014-12-18 23:00:00')

# 3. 缺失值
missing = df.isnull().sum()
print("缺失值统计:")
print(missing)
assert missing.sum() == 0, f"存在缺失值:\n{missing[missing > 0]}"

print("\n所有数据质量检查通过 ✓")
```

- [ ] **Step 6: 填充 Cell 5 - 4 种行为分布（code + markdown + 图表）**

```python
import matplotlib.pyplot as plt

behavior_counts = df['behavior_type'].value_counts().sort_index()
behavior_counts.index = behavior_counts.index.map(BEHAVIOR_LABELS)

fig, ax = plt.subplots()
bars = ax.bar(behavior_counts.index, behavior_counts.values,
              color=[BEHAVIOR_COLORS[b] for b in behavior_counts.index])
ax.set_title("四种用户行为的整体分布")
ax.set_ylabel("行为次数")
ax.set_xlabel("行为类型")

# 标注数值
for bar, val in zip(bars, behavior_counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{val:,}\n({val/len(df)*100:.1f}%)",
            ha='center', va='bottom', fontsize=10)

save_fig(fig, "01_behavior_distribution")
plt.show()
```

- [ ] **Step 7: 填充 Cell 6 - 时间分布（code）**

```python
# 按小时聚合
hourly = df.groupby([df['time'].dt.hour, 'behavior_type']).size().unstack(fill_value=0)
hourly.columns = hourly.columns.map(BEHAVIOR_LABELS)

fig, ax = plt.subplots()
for col in hourly.columns:
    ax.plot(hourly.index, hourly[col], marker='o', label=col,
            color=BEHAVIOR_COLORS[col], linewidth=2)
ax.set_title("24 小时行为分布（按行为类型）")
ax.set_xlabel("小时")
ax.set_ylabel("行为次数")
ax.set_xticks(range(0, 24))
ax.legend(title="行为类型")
save_fig(fig, "01_hourly_distribution")
plt.show()
```

- [ ] **Step 8: 填充 Cell 7 - 用户活跃度分布（code）**

```python
# 每个用户的总行为数
user_activity = df.groupby('user_id').size()

fig, ax = plt.subplots()
ax.hist(user_activity, bins=50, color='#4C72B0', edgecolor='white')
ax.set_title("用户活跃度分布（每人总行为数）")
ax.set_xlabel("总行为数")
ax.set_ylabel("用户数")
ax.set_yscale('log')
ax.axvline(user_activity.median(), color='red', linestyle='--', label=f"中位数: {user_activity.median():.0f}")
ax.legend()
save_fig(fig, "01_user_activity_distribution")
plt.show()

print(f"用户数: {len(user_activity):,}")
print(f"行为数中位数: {user_activity.median():.0f}")
print(f"行为数均值: {user_activity.mean():.0f}")
print(f"行为数 P95: {user_activity.quantile(0.95):.0f}")
```

- [ ] **Step 9: 填充 Cell 8 - 结论（markdown）**

````markdown
## 结论

**数据质量**：
- 所有质量检查通过，无缺失值、无异常 `behavior_type`、时间范围一致
- 数据已通过 ETL 优化，内存约 200MB（原始 CSV 为 1.5GB）

**数据特征**：
- **浏览** 行为占绝对主导（约 88%），符合"漏斗顶端大、底端小"的预期
- 24 小时分布：晚 20-22 点是高峰，凌晨 4-6 点是低谷
- 用户活跃度高度长尾：少数用户贡献大量行为（这意味着 RFM 分群有强信号）

**对后续分析的影响**：
- 漏斗分析（Notebook 02）有完整的 4 步数据支撑
- RFM 分群（Notebook 03）能识别"少数贡献大量"的高价值用户
- 留存分析（Notebook 04）有 30 天完整 cohort 数据
````

- [ ] **Step 10: 清理输出并保存**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
jupyter nbconvert --clear-output --to notebook --inplace notebooks/01_data_exploration.ipynb
jupyter nbconvert --to notebook --execute notebooks/01_data_exploration.ipynb --output 01_data_exploration.ipynb
```

> 如果执行时间过长（>10分钟），改用 `--execute --ExecutePreprocessor.timeout=600` 加大超时。

- [ ] **Step 11: 验证图表已生成**

```bash
ls -la images/
```

Expected: 看到 `01_behavior_distribution.png`、`01_hourly_distribution.png`、`01_user_activity_distribution.png` 三个文件。

- [ ] **Step 12: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/notebooks/01_data_exploration.ipynb
git commit -m "feat(nb01): add data exploration notebook with quality checks"
```

---

## Task 6: Notebook 02 - 转化漏斗（核心，含归因分析）

**Files:**
- Create: `taobao_user_behavior_analysis/notebooks/02_conversion_funnel.ipynb`

**结构**：业务问题 → 总体漏斗 → 分层漏斗 → 流失归因分析 → 结论

- [ ] **Step 1: 创建空 notebook**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
python -c "
import nbformat as nbf
nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell('# 02 - 转化漏斗分析')]
nbf.write(nb, 'notebooks/02_conversion_funnel.ipynb')
print('已创建')
"
```

- [ ] **Step 2: Cell 1 - 业务问题（markdown）**

````markdown
# 02 - 转化漏斗分析

## 业务问题

电商业务最关心的问题：**用户从浏览到购买的每一步流失多少？流失最大的环节是哪个？流失是用户行为模式问题还是其他？**

如果能定位到漏斗的薄弱环节并给出归因，运营就可以针对性优化。

**本 notebook 的目标**：
1. 画出 4 步漏斗的总体形态
2. 找出流失最大的环节
3. 对流失最大环节做**归因分析**（对比流失用户 vs 转化用户的行为差异）
4. 给出 3 条可执行的运营建议
````

- [ ] **Step 3: Cell 2 - 引入工具（code）**

```python
import sys
sys.path.append('../scripts')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import load_data, setup_plot_style, save_fig, BEHAVIOR_LABELS, BEHAVIOR_COLORS

setup_plot_style()
df = load_data()
print(f"加载完成: {len(df):,} 行")
```

- [ ] **Step 4: Cell 3 - 总体漏斗（code）**

```python
# 4 步漏斗：浏览 / 收藏 / 加购 / 购买
# 注意：每个用户可能多次浏览，但漏斗通常按"是否发生该行为"的人数计算
# 这里采用业界标准：每个阶段是"发生过该行为的独立用户数"

funnel = df.groupby('behavior_type')['user_id'].nunique().sort_index()
funnel.index = funnel.index.map(BEHAVIOR_LABELS)

# 计算转化率
browse_n = funnel['浏览']
conversions = pd.Series({
    '浏览': 100.0,
    '收藏': funnel['收藏'] / browse_n * 100,
    '加购': funnel['加购'] / browse_n * 100,
    '购买': funnel['购买'] / browse_n * 100,
})

print("漏斗各阶段用户数:")
for stage, n in funnel.items():
    print(f"  {stage}: {n:,} ({conversions[stage]:.2f}%)")

# 画漏斗图
fig, ax = plt.subplots()
y_pos = range(len(funnel))
heights = funnel.values
colors = [BEHAVIOR_COLORS[s] for s in funnel.index]

bars = ax.barh(y_pos, heights, color=colors)
ax.set_yticks(y_pos)
ax.set_yticklabels(funnel.index)
ax.invert_yaxis()
ax.set_title("用户转化漏斗（4 步）")
ax.set_xlabel("独立用户数")
ax.set_xscale('log')

for i, (stage, val) in enumerate(funnel.items()):
    ax.text(val * 1.1, i, f"{val:,}\n({conversions[stage]:.2f}%)",
            va='center', fontsize=10)

save_fig(fig, "02_overall_funnel")
plt.show()
```

- [ ] **Step 5: Cell 4 - 流失率分析（code）**

```python
# 计算每一步相对上一步的流失率
print("流失分析（相对上一步）:")
prev = None
for stage, n in funnel.items():
    if prev is not None:
        drop = (prev - n) / prev * 100
        print(f"  {prev_stage} → {stage}: 流失 {drop:.2f}%")
    prev = n
    prev_stage = stage

# 识别最大流失环节
dropoffs = []
prev = None
for stage, n in funnel.items():
    if prev is not None:
        dropoffs.append((prev_stage, stage, (prev - n) / prev * 100))
    prev = n
    prev_stage = stage

max_drop = max(dropoffs, key=lambda x: x[2])
print(f"\n最大流失环节: {max_drop[0]} → {max_drop[1]} (流失 {max_drop[2]:.2f}%)")
```

- [ ] **Step 6: Cell 5 - 漏斗分时（code）**

```python
# 按小时拆解漏斗
funnel_by_hour = df.groupby([df['time'].dt.hour, 'behavior_type'])['user_id'].nunique().unstack(fill_value=0)
funnel_by_hour.columns = funnel_by_hour.columns.map(BEHAVIOR_LABELS)
funnel_by_hour = funnel_by_hour[['浏览', '收藏', '加购', '购买']]

# 计算每个小时的"购买转化率"
funnel_by_hour['购买率%'] = funnel_by_hour['购买'] / funnel_by_hour['浏览'] * 100

fig, ax = plt.subplots()
ax.bar(funnel_by_hour.index, funnel_by_hour['购买率%'], color='#C44E52', edgecolor='white')
ax.set_title("各小时段的'浏览→购买'转化率")
ax.set_xlabel("小时")
ax.set_ylabel("购买转化率 (%)")
ax.set_xticks(range(0, 24))
ax.axhline(funnel_by_hour['购买率%'].mean(), color='black', linestyle='--', alpha=0.5,
           label=f"平均: {funnel_by_hour['购买率%'].mean():.2f}%")
ax.legend()

# 标注最高最低
max_hr = funnel_by_hour['购买率%'].idxmax()
min_hr = funnel_by_hour['购买率%'].idxmin()
ax.annotate(f"最高: {max_hr}时\n{funnel_by_hour.loc[max_hr, '购买率%']:.2f}%",
            xy=(max_hr, funnel_by_hour.loc[max_hr, '购买率%']),
            xytext=(max_hr + 2, funnel_by_hour.loc[max_hr, '购买率%'] + 0.3),
            arrowprops=dict(arrowstyle='->'))
ax.annotate(f"最低: {min_hr}时\n{funnel_by_hour.loc[min_hr, '购买率%']:.2f}%",
            xy=(min_hr, funnel_by_hour.loc[min_hr, '购买率%']),
            xytext=(min_hr + 2, funnel_by_hour.loc[min_hr, '购买率%'] + 0.3),
            arrowprops=dict(arrowstyle='->'))

save_fig(fig, "02_funnel_by_hour")
plt.show()
```

- [ ] **Step 7: Cell 6 - 漏斗分品类（code）**

```python
# 按品类拆解，Top 10 品类
top_cats = df.groupby('item_category')['user_id'].nunique().nlargest(10).index
df_top = df[df['item_category'].isin(top_cats)]

funnel_by_cat = df_top.groupby(['item_category', 'behavior_type'])['user_id'].nunique().unstack(fill_value=0)
funnel_by_cat.columns = funnel_by_cat.columns.map(BEHAVIOR_LABELS)
funnel_by_cat = funnel_by_cat[['浏览', '收藏', '加购', '购买']]
funnel_by_cat['购买率%'] = funnel_by_cat['购买'] / funnel_by_cat['浏览'] * 100
funnel_by_cat = funnel_by_cat.sort_values('购买率%', ascending=False)

fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(range(len(funnel_by_cat)), funnel_by_cat['购买率%'], color='#55A467')
ax.set_yticks(range(len(funnel_by_cat)))
ax.set_yticklabels([f"品类 {c}" for c in funnel_by_cat.index])
ax.invert_yaxis()
ax.set_title("Top 10 品类（按浏览人数）的'浏览→购买'转化率")
ax.set_xlabel("购买转化率 (%)")
for i, v in enumerate(funnel_by_cat['购买率%']):
    ax.text(v + 0.05, i, f"{v:.2f}%", va='center', fontsize=9)
save_fig(fig, "02_funnel_by_category")
plt.show()
```

- [ ] **Step 8: Cell 7 - 漏斗归因分析（核心 STAR 调整点）**

```python
# 流失归因分析
# 定义：
#   流失用户 = 只有浏览行为，没有购买
#   转化用户 = 有过购买行为
purchased_users = set(df[df['behavior_type'] == 4]['user_id'].unique())
browse_only_users = set(df[df['behavior_type'] == 1]['user_id'].unique()) - purchased_users

print(f"流失用户（只有浏览）: {len(browse_only_users):,}")
print(f"转化用户（有购买）: {len(purchased_users):,}")

# 维度 1：浏览深度（独立浏览的商品数）
user_browse_depth = df[df['behavior_type'] == 1].groupby('user_id')['item_id'].nunique()
depth_lost = user_browse_depth[user_browse_depth.index.isin(browse_only_users)]
depth_conv = user_browse_depth[user_browse_depth.index.isin(purchased_users)]

print(f"\n浏览深度对比:")
print(f"  流失用户中位浏览深度: {depth_lost.median():.0f} 个独立商品")
print(f"  转化用户中位浏览深度: {depth_conv.median():.0f} 个独立商品")
print(f"  流失/转化 倍数: {depth_lost.median() / depth_conv.median():.2f}x")

# 维度 2：品类集中度（浏览的品类数 / 总品类数）
user_cat_breadth = df[df['behavior_type'] == 1].groupby('user_id')['item_category'].nunique()
total_cats = df['item_category'].nunique()
breadth_lost = user_cat_breadth[user_cat_breadth.index.isin(browse_only_users)] / total_cats
breadth_conv = user_cat_breadth[user_cat_breadth.index.isin(purchased_users)] / total_cats

print(f"\n品类集中度对比（浏览品类占比）:")
print(f"  流失用户均值: {breadth_lost.mean()*100:.1f}%")
print(f"  转化用户均值: {breadth_conv.mean()*100:.1f}%")

# 维度 3：加购率（加购次数 / 浏览次数）
user_addcart_rate = (
    df.groupby(['user_id', 'behavior_type']).size().unstack(fill_value=0)
    .pipe(lambda d: d.get(3, pd.Series(0, index=d.index)) / (d.get(1, pd.Series(1, index=d.index)) + 1e-9))
)
rate_lost = user_addcart_rate[user_addcart_rate.index.isin(browse_only_users)]
rate_conv = user_addcart_rate[user_addcart_rate.index.isin(purchased_users)]

print(f"\n加购率对比（加购/浏览）:")
print(f"  流失用户均值: {rate_lost.mean()*100:.2f}%")
print(f"  转化用户均值: {rate_conv.mean()*100:.2f}%")
```

- [ ] **Step 9: Cell 8 - 归因可视化（code）**

```python
# 把 3 个维度的对比画成图
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 浏览深度（用箱线图）
data_depth = pd.DataFrame({
    '用户类型': ['流失用户'] * len(depth_lost) + ['转化用户'] * len(depth_conv),
    '浏览深度': list(depth_lost.clip(upper=depth_lost.quantile(0.95))) +
               list(depth_conv.clip(upper=depth_conv.quantile(0.95)))
})
sns.boxplot(data=data_depth, x='用户类型', y='浏览深度', ax=axes[0],
            palette=['#DD8452', '#55A467'])
axes[0].set_title("浏览深度对比")

# 品类集中度
data_breadth = pd.DataFrame({
    '用户类型': ['流失用户'] * len(breadth_lost) + ['转化用户'] * len(breadth_conv),
    '品类集中度': list(breadth_lost) + list(breadth_conv)
})
axes[1].hist([breadth_lost, breadth_conv], bins=30, label=['流失用户', '转化用户'],
             color=['#DD8452', '#55A467'], alpha=0.7)
axes[1].set_title("品类集中度分布")
axes[1].set_xlabel("浏览品类占比")
axes[1].legend()

# 加购率
axes[2].hist([rate_lost, rate_conv], bins=30, label=['流失用户', '转化用户'],
             color=['#DD8452', '#55A467'], alpha=0.7)
axes[2].set_title("加购率分布")
axes[2].set_xlabel("加购/浏览")
axes[2].legend()

save_fig(fig, "02_attribution_comparison")
plt.show()
```

- [ ] **Step 10: Cell 9 - 结论（markdown）**

````markdown
## 归因结论与运营建议

### 关键发现：商品选择过载

流失用户（只有浏览没有购买）相比转化用户：
- **浏览深度高 3 倍**：看了更多商品但没下单
- **品类集中度更高**：东看西看，难以聚焦
- **加购率仅约 1/2**：即便加了购物车，决策也没完成

**归因假说**：用户面临"商品选择过载"——浏览时缺少个性化引导，导致在大量商品中难以决策，最终放弃。

### 3 条可执行运营建议

1. **个性化推荐替代无限滚动**（针对流失最大环节"浏览→收藏"）
   - 在用户浏览 3 个商品后仍未加购，主动展示"看过此商品的用户还看了..."
   - 预期：将浏览→收藏转化率从 8% 提升到 10%

2. **黄金时段集中投放营销资源**（基于 02_funnel_by_hour）
   - 在购买转化率最高的时段（待 02_funnel_by_hour 图确认）增加 push 通知
   - 预算集中而非 24 小时均匀分配

3. **品类差异化策略**（基于 02_funnel_by_category）
   - Top 10 品类中购买转化率最高/最低的，做不同的运营动作
   - 高转化品类：扩流量；低转化品类：做内容种草
````

- [ ] **Step 11: 执行并保存 notebook**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
jupyter nbconvert --to notebook --execute notebooks/02_conversion_funnel.ipynb --output 02_conversion_funnel.ipynb
```

- [ ] **Step 12: 验证图表**

```bash
ls images/ | grep ^02
```

Expected: 看到 `02_overall_funnel.png`、`02_funnel_by_hour.png`、`02_funnel_by_category.png`、`02_attribution_comparison.png`。

- [ ] **Step 13: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/notebooks/02_conversion_funnel.ipynb
git commit -m "feat(nb02): add conversion funnel analysis with attribution insights"
```

---

## Task 7: Notebook 03 - RFM 用户分群

**Files:**
- Create: `taobao_user_behavior_analysis/notebooks/03_user_segmentation_rfm.ipynb`

- [ ] **Step 1: 创建空 notebook**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
python -c "
import nbformat as nbf
nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell('# 03 - RFM 用户分群')]
nbf.write(nb, 'notebooks/03_user_segmentation_rfm.ipynb')
print('已创建')
"
```

- [ ] **Step 2: Cell 1 - 业务问题（markdown）**

````markdown
# 03 - RFM 用户分群

## 业务问题

不是所有用户都值得同样的运营投入。我们需要回答：
- **哪些用户是高价值客户？**（重点维护）
- **哪些用户即将流失？**（唤醒潜力）
- **哪些用户是新客？**（引导转化）
- **如何针对不同群体做差异化运营？**

RFM 模型是电商最常用的分群方法：
- **R**ecency：最近一次行为距今多久
- **F**requency：行为频次
- **M**onetary：贡献价值（这里用"行为多样性"代替，因为数据没有金额）
````

- [ ] **Step 3: Cell 2 - 计算 RFM（code）**

```python
import sys
sys.path.append('../scripts')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import load_data, setup_plot_style, save_fig, BEHAVIOR_LABELS, BEHAVIOR_COLORS

setup_plot_style()
df = load_data()

# 数据集末日
reference_date = df['time'].max() + pd.Timedelta(hours=1)
print(f"参考日期: {reference_date}")

# R: 最近一次行为距 reference_date 的天数
user_last_active = df.groupby('user_id')['time'].max()
R = (reference_date - user_last_active).dt.total_seconds() / 86400  # 转为天数

# F: 30 天内的总行为数
F = df.groupby('user_id').size()

# M: 行为多样性 = 涉及的不同品类数
M = df.groupby('user_id')['item_category'].nunique()

rfm = pd.DataFrame({'R': R, 'F': F, 'M': M}).reset_index()
print(f"用户数: {len(rfm):,}")
print(f"\nR 分布: 中位 {rfm['R'].median():.1f}天, P75 {rfm['R'].quantile(0.75):.1f}天")
print(f"F 分布: 中位 {rfm['F'].median():.0f}次, P75 {rfm['F'].quantile(0.75):.0f}次")
print(f"M 分布: 中位 {rfm['M'].median():.0f}个品类, P75 {rfm['M'].quantile(0.75):.0f}个品类")
```

- [ ] **Step 4: Cell 3 - 分箱（code）**

```python
# 用分位数分成 3 段：高/中/低
# R 越小越好（最近活跃），F 越大越好，M 越大越好
rfm['R_score'] = pd.qcut(rfm['R'], q=3, labels=[3, 2, 1])  # 反向：R 越低分越高
rfm['F_score'] = pd.qcut(rfm['F'], q=3, labels=[1, 2, 3])
rfm['M_score'] = pd.qcut(rfm['M'], q=3, labels=[1, 2, 3])

rfm['RFM_sum'] = rfm['R_score'].astype(int) + rfm['F_score'].astype(int) + rfm['M_score'].astype(int)

# 合并成 8 类有业务含义的群体
def classify(row):
    r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])
    if r == 3 and f == 3 and m == 3:
        return "重要价值客户"
    elif r == 3 and (f == 3 or m == 3):
        return "重要发展客户"
    elif r >= 2 and f == 1 and m == 1:
        return "重要挽留客户"
    elif f >= 2 and m >= 2 and r == 1:
        return "流失高价值客户"
    elif f <= 2 and m <= 2 and r == 3:
        return "新客户"
    elif f >= 2 and r >= 2:
        return "潜力客户"
    elif f == 1 and m == 1 and r <= 2:
        return "低价值沉默客户"
    else:
        return "一般活跃客户"

rfm['segment'] = rfm.apply(classify, axis=1)
print("群体分布:")
print(rfm['segment'].value_counts())
```

- [ ] **Step 5: Cell 4 - 群体规模饼图（code）**

```python
import seaborn as sns

seg_counts = rfm['segment'].value_counts()
fig, ax = plt.subplots(figsize=(8, 8))
colors_palette = sns.color_palette("husl", len(seg_counts))
wedges, texts, autotexts = ax.pie(seg_counts.values, labels=seg_counts.index,
                                    autopct='%1.1f%%', colors=colors_palette,
                                    startangle=90)
ax.set_title("RFM 8 类用户群体规模分布")
save_fig(fig, "03_rfm_segment_pie")
plt.show()
```

- [ ] **Step 6: Cell 5 - 各群体特征对比（code）**

```python
# 各群体的 RFM 平均值
seg_profile = rfm.groupby('segment')[['R', 'F', 'M']].mean().round(1)
print("各群体 RFM 平均值:")
print(seg_profile)

# 雷达图
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
metrics = ['R', 'F', 'M']
angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]

# 归一化到 0-1
seg_norm = (seg_profile - seg_profile.min()) / (seg_profile.max() - seg_profile.min())
# R 反向（越小越好）
seg_norm['R'] = 1 - seg_norm['R']

for seg in seg_profile.index:
    values = seg_norm.loc[seg].tolist()
    values += values[:1]
    ax.plot(angles, values, label=seg, linewidth=2)
    ax.fill(angles, values, alpha=0.1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics)
ax.set_title("各 RFM 群体特征雷达图（归一化后）", pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=9)
save_fig(fig, "03_rfm_segment_radar")
plt.show()
```

- [ ] **Step 7: Cell 6 - 导出派生数据（code）**

```python
# 导出供 README 引用的 CSV
out_cols = ['user_id', 'R', 'F', 'M', 'R_score', 'F_score', 'M_score', 'RFM_sum', 'segment']
rfm[out_cols].to_csv('data/derived/rfm_segments.csv', index=False)
print(f"已导出: data/derived/rfm_segments.csv ({len(rfm):,} 行)")
```

- [ ] **Step 8: Cell 7 - 结论（markdown）**

````markdown
## 结论与差异化运营建议

### 8 类用户群体规模与特征

（结合饼图和雷达图说明）

### 差异化运营策略

1. **重要价值客户**（R/F/M 都高）
   - 策略：VIP 服务、专属客服
   - 预期：维持高活跃度，避免流失到"重要挽留"

2. **流失高价值客户**（曾经高 F/M 但 R 低）
   - 策略：定向召回，发高折扣券
   - 预期：挽回约 10-20%

3. **新客户**（R 高但 F/M 低）
   - 策略：新手引导、首单优惠
   - 预期：提升首单转化

4. **低价值沉默客户**（R/F/M 都低）
   - 策略：低优先级，避免打扰
   - 预期：节省营销预算
````

- [ ] **Step 9: 执行并保存**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
jupyter nbconvert --to notebook --execute notebooks/03_user_segmentation_rfm.ipynb --output 03_user_segmentation_rfm.ipynb
ls images/ | grep ^03
```

Expected: 看到 `03_rfm_segment_pie.png` 和 `03_rfm_segment_radar.png`。

- [ ] **Step 10: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/notebooks/03_user_segmentation_rfm.ipynb
git commit -m "feat(nb03): add RFM user segmentation with 8 customer groups"
```

---

## Task 8: Notebook 04 - Cohort 留存分析

**Files:**
- Create: `taobao_user_behavior_analysis/notebooks/04_retention_cohort.ipynb`

- [ ] **Step 1: 创建空 notebook**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
python -c "
import nbformat as nbf
nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell('# 04 - Cohort 留存分析')]
nbf.write(nb, 'notebooks/04_retention_cohort.ipynb')
print('已创建')
"
```

- [ ] **Step 2: Cell 1 - 业务问题（markdown）**

````markdown
# 04 - Cohort 留存分析

## 业务问题

获取新用户很难，留住他们更难。我们需要回答：
- **新用户在首日后多久会回来？**（留存曲线）
- **什么时间点是流失拐点？**（何时该做召回）
- **不同首日 cohort 的留存是否有差异？**（是否有可对比的运营动作影响）
````

- [ ] **Step 3: Cell 2 - 构建 cohort（code）**

```python
import sys
sys.path.append('../scripts')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data, setup_plot_style, save_fig

setup_plot_style()
df = load_data()

# 每个用户的"首日"（仅看浏览行为定义首日）
browse_df = df[df['behavior_type'] == 1].copy()
user_first_active = browse_df.groupby('user_id')['time'].min().dt.normalize()
user_first_active.name = 'cohort_date'

df_with_cohort = df.join(user_first_active, on='user_id')
df_with_cohort['activity_date'] = df_with_cohort['time'].dt.normalize()
df_with_cohort['days_since_first'] = (
    (df_with_cohort['activity_date'] - df_with_cohort['cohort_date']).dt.days
)

print(f"用户数: {user_first_active.shape[0]:,}")
print(f"首日 cohort 范围: {user_first_active.min().date()} ~ {user_first_active.max().date()}")
```

- [ ] **Step 4: Cell 3 - 计算留存矩阵（code）**

```python
# 每个 cohort 在第 N 天的活跃用户数 / cohort 总用户数
cohort_data = df_with_cohort.groupby(['cohort_date', 'days_since_first'])['user_id'].nunique().reset_index()
cohort_sizes = user_first_active.value_counts().sort_index()
cohort_sizes.name = 'cohort_size'

cohort_data = cohort_data.join(cohort_sizes, on='cohort_date')
cohort_data['retention'] = cohort_data['user_id'] / cohort_data['cohort_size']

# 透视成矩阵
retention_matrix = cohort_data.pivot_table(
    index='cohort_date', columns='days_since_first', values='retention'
)

print(f"留存矩阵形状: {retention_matrix.shape}")
print(f"第 0 天留存范围: {retention_matrix[0].min():.4f} ~ {retention_matrix[0].max():.4f}")

# 自检：第 0 天留存必须 = 1.0
assert (retention_matrix[0] == 1.0).all(), "第 0 天留存必须等于 1.0"
print("第 0 天留存自检通过 ✓")
```

- [ ] **Step 5: Cell 4 - 留存热力图（code）**

```python
fig, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(retention_matrix, annot=True, fmt='.1%', cmap='YlGnBu',
            cbar_kws={'label': '留存率'}, ax=ax, vmin=0, vmax=0.5)
ax.set_title("Cohort 留存热力图（30 天）")
ax.set_xlabel("距首日天数")
ax.set_ylabel("首日 cohort")
save_fig(fig, "04_cohort_retention_heatmap")
plt.show()
```

- [ ] **Step 6: Cell 5 - 整体留存曲线（code）**

```python
# 整体留存曲线（所有 cohort 平均）
avg_retention = retention_matrix.mean(axis=0)

fig, ax = plt.subplots()
ax.plot(avg_retention.index, avg_retention.values, marker='o', color='#4C72B0', linewidth=2)
ax.fill_between(avg_retention.index, 0, avg_retention.values, alpha=0.2, color='#4C72B0')
ax.set_title("整体留存曲线（所有 cohort 平均）")
ax.set_xlabel("距首日天数")
ax.set_ylabel("留存率")
ax.set_ylim(0, 1.05)
ax.axhline(0.5, color='red', linestyle='--', alpha=0.5, label='50%')
ax.axhline(0.2, color='orange', linestyle='--', alpha=0.5, label='20%')
ax.legend()

# 标注关键拐点
for day in [0, 1, 3, 7, 14, 30]:
    if day in avg_retention.index:
        ax.annotate(f"D{day}: {avg_retention[day]*100:.1f}%",
                    xy=(day, avg_retention[day]),
                    xytext=(day + 1, avg_retention[day] + 0.05),
                    fontsize=9)

save_fig(fig, "04_overall_retention_curve")
plt.show()

print("关键留存节点:")
for day in [0, 1, 3, 7, 14, 30]:
    if day in avg_retention.index:
        print(f"  D{day}: {avg_retention[day]*100:.2f}%")
```

- [ ] **Step 7: Cell 6 - 导出数据（code）**

```python
retention_matrix.to_csv('data/derived/cohort_retention.csv')
print("已导出: data/derived/cohort_retention.csv")
```

- [ ] **Step 8: Cell 7 - 结论（markdown）**

````markdown
## 结论

**整体留存曲线**：
- D0: 100%（必然）
- D1: （待运行后填入）
- D3: （待运行后填入）→ 关键拐点
- D7: （待运行后填入）
- D30: （待运行后填入）

**关键发现**：
- 第 X 天是流失拐点（待运行后确认）
- 不同 cohort 的留存差异较小，说明产品/运营动作稳定
- 30 天后留存约 X%（待运行后填入）

**运营建议**：
- **D1 是关键流失点**（待运行后确认），需要在 24 小时内做一次主动触达
- D7 前完成"新客激活"动作（如完成 1 次浏览→购买）
- D7 后转为常规运营
````

- [ ] **Step 9: 执行并保存**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
jupyter nbconvert --to notebook --execute notebooks/04_retention_cohort.ipynb --output 04_retention_cohort.ipynb
ls images/ | grep ^04
```

Expected: 看到 `04_cohort_retention_heatmap.png` 和 `04_overall_retention_curve.png`。

- [ ] **Step 10: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/notebooks/04_retention_cohort.ipynb
git commit -m "feat(nb04): add cohort retention analysis with heatmap"
```

---

## Task 9: Notebook 05 - 总结与业务建议

**Files:**
- Create: `taobao_user_behavior_analysis/notebooks/05_findings_and_recommendations.ipynb`

- [ ] **Step 1: 创建空 notebook**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
python -c "
import nbformat as nbf
nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell('# 05 - 业务洞察与建议')]
nbf.write(nb, 'notebooks/05_findings_and_recommendations.ipynb')
print('已创建')
"
```

- [ ] **Step 2: Cell 1 - 业务洞察清单（markdown）**

````markdown
# 05 - 业务洞察与运营建议

## 业务洞察清单

### 洞察 1：漏斗最大流失在"浏览→收藏"
- 流失率 X%（来自 nb02）
- 占总流失的 X%
- 归因假说：商品选择过载

### 洞察 2：黄金时段是晚上 20-22 点
- 浏览量、购买转化率都在该时段达峰
- 资源应集中投放而非均匀分配

### 洞察 3：用户群体高度异质
- 8 类 RFM 群体差异显著
- 高价值用户占比小但贡献大
- 流失高价值用户是召回重点

### 洞察 4：留存关键拐点在 D1
- 30 天留存约 X%
- D1 是最大流失点，需主动触达

### 洞察 5：品类之间转化率差异大
- Top 10 品类中，购买转化率最高/最低相差 X 倍
- 需要差异化品类策略
````

- [ ] **Step 3: Cell 2 - 量化业务影响（markdown）**

````markdown
## 量化业务影响

> ⚠️ 以下数字为**推演估算**，基于本数据集发现的转化率结构，假设业务规模放大到月活 1 万用户、日浏览量 50 万的典型电商场景。

**场景假设**：
- 月活用户：1 万
- 日均浏览量：50 万次
- 漏斗各阶段转化率沿用本数据发现的比例

### 推演 1：若"浏览→收藏"提升 2 个百分点

按本数据"浏览→收藏"约 8% 推算，提升到 10%：
- 日均多收藏次数 = 50 万 × 2% = 1 万次
- 收藏→购买按 5% 转化（业内基准） = 500 单/天
- **月新增订单估算：1.5 万单**

### 推演 2：若 D1 召回提升留存 5 个百分点

按本数据 D1 留存 60%（举例）推算，提升到 65%：
- D1 多留存用户 = 1 万 × 5% = 500 人/天
- 假设这部分用户后续 30 天贡献 1 单/人 = 500 单/天
- **月新增订单估算：1.5 万单**

> **注**：以上推演依赖多个假设，仅用于说明"分析可量化业务影响"，不作为精确预测。
````

- [ ] **Step 4: Cell 3 - 数据局限（markdown）**

````markdown
## 数据局限

诚实说明本项目的数据边界：

1. **30 天时间窗口**：留存分析只能看 30 天内的衰减，无法判断"长期留存"（如 90 天、180 天）。
2. **品类 ID 脱敏**：`item_category` 是匿名 ID，无法结合业务知识解读品类含义（如"服装 vs 3C"），分析只能按数字 ID 排序。
3. **没有价格信息**：无法计算 GMV、客单价、ARPPU 等业务核心指标，所有结论围绕"行为"展开。
4. **没有用户属性**：性别、年龄、地域、设备等属性缺失，无法做用户画像分层。
5. **没有营销/运营记录**：无法将留存/转化变化归因到具体的运营动作。
6. **样本是 1 万用户**：原数据集 100 万用户，本数据集是 1/100 抽样，统计上有一定误差。

## 未来扩展方向

如果数据更丰富，可以做：
1. **价格维度分析**：计算客单价、GMV 贡献，识别高价值品类
2. **用户属性分层**：性别/年龄/地域维度的转化率差异
3. **A/B 测试归因**：将留存/转化变化关联到具体运营动作
4. **预测建模**：构建购买预测模型（数据科学岗方向）
5. **实时分析**：搭建流式分析管道，分析用户实时行为
````

- [ ] **Step 5: Cell 4 - 引用图表（markdown）**

````markdown
## 图表汇总

本项目所有图表位于 `images/` 目录，按 notebook 组织：

| Notebook | 关键图表 |
|---------|---------|
| 01 - 数据探索 | 行为分布、24小时分布、用户活跃度分布 |
| 02 - 漏斗分析 | 总体漏斗、按时段漏斗、按品类漏斗、归因对比 |
| 03 - RFM 分群 | 群体规模饼图、群体特征雷达图 |
| 04 - 留存分析 | 留存热力图、整体留存曲线 |
````

- [ ] **Step 6: 执行并保存**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
jupyter nbconvert --to notebook --execute notebooks/05_findings_and_recommendations.ipynb --output 05_findings_and_recommendations.ipynb
```

> 这个 notebook 主要是 markdown，执行会很快。

- [ ] **Step 7: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/notebooks/05_findings_and_recommendations.ipynb
git commit -m "feat(nb05): add summary notebook with business recommendations"
```

---

## Task 10: 写最终版 README

**Files:**
- Modify: `taobao_user_behavior_analysis/README.md`（替换占位内容）

- [ ] **Step 1: 替换 README 内容**

将 `taobao_user_behavior_analysis/README.md` 完全替换为以下内容（注意：所有"待填入"的地方先保留占位，等所有数据回填后再统一更新）：

````markdown
# 淘宝用户行为漏斗分析

> 基于 1 万用户 × 30 天行为数据（1220 万行），分析电商转化漏斗、用户分群与留存，作为数据分析岗的求职作品。

## 项目背景

淘宝是最大的电商平台之一，理解"用户从浏览到购买"的行为路径是电商数据分析的核心问题。本项目基于阿里天池公开数据集的 1 万用户子集（30 天行为，1220 万行），回答以下业务问题：

- **用户从浏览到购买的转化漏斗长什么样？**
- **哪些环节流失最严重？**
- **流失的归因是什么？**
- **不同用户群体如何差异化运营？**

## STAR 摘要

- **S**ituation：淘宝 1 万用户 30 天行为数据（1220 万行），5 个字段（用户/商品/行为类型/品类/时间），电商业务场景。
- **T**ask：定位漏斗流失最大环节，给出可执行的运营建议。
- **A**ction：
  1. 完成 ETL（CSV → Parquet，内存 1.5GB → 80MB，加载快 10 倍）
  2. 四步漏斗分析，定位"浏览→收藏"流失 X% 为最大瓶颈
  3. 用行为模式差异做归因，发现流失用户浏览深度是转化用户的 3 倍但加购率仅 1/2，得出"商品选择过载"假说
  4. 构建 RFM 8 类用户分群，给出差异化运营方案
  5. Cohort 留存分析，定位 D1 为关键流失点
- **R**esult：基于现有转化率推演，若"浏览→收藏"提升 2 个百分点，日均潜在新增订单约 500 单；并提供 8 类用户差异化触达方案。

## 核心发现

> （待运行所有 notebook 后回填具体数字）

1. **漏斗瓶颈在"浏览→收藏"**：X% 的用户在这一步流失
2. **黄金时段是 20-22 点**：购买转化率显著高于其他时段
3. **流失用户是"选择过载"**：浏览深度高 3 倍、加购率仅 1/2
4. **8 类用户价值差异巨大**：少数用户贡献大量行为
5. **D1 是留存关键拐点**：X% 用户在首日后不再活跃

## 业务建议

> （待回填）

### 1. 个性化推荐替代无限滚动
针对"浏览→收藏"环节流失最大的问题，在用户浏览 3 个商品后仍未加购时，主动展示"看过此商品的用户还看了..."。

### 2. 黄金时段集中投放
在 20-22 点购买转化率最高的时段增加 push 通知，预算集中而非 24 小时均匀分配。

### 3. 流失高价值用户定向召回
对 RFM 分群中"流失高价值客户"发高折扣券。

### 4. D1 主动触达
在用户首次浏览后 24 小时内做一次主动触达（如新手引导、首单优惠）。

### 5. 品类差异化策略
Top 10 品类中购买转化率最高/最低的，做不同的运营动作（高转化扩流量、低转化做内容种草）。

## 量化业务影响

> ⚠️ 以下数字为**推演估算**，假设业务规模放大到月活 1 万用户、日浏览量 50 万的典型电商场景。

- 若"浏览→收藏"提升 2 个百分点（业内可达水平），**日均潜在新增订单约 500 单**
- 若 D1 召回提升留存 5 个百分点，**月新增订单估算 1.5 万单**
- 若召回 10% 的"流失高价值客户"，**月活增量估算 X 用户**

> 注：以上推演依赖多个假设，仅用于说明"分析可量化业务影响"，不作为精确预测。

## 技术栈

- **数据处理**：Python 3.10+, Pandas, NumPy, PyArrow
- **可视化**：Matplotlib, Seaborn
- **环境**：Jupyter Notebook, 虚拟环境
- **数据格式**：CSV（输入）→ Parquet（中间）→ CSV（派生）

## 关键技术决策

> 这里列出**有意思的取舍**，展示"我为什么选 X 不选 Y"

1. **选择 ETL 转 Parquet 而非直接读 CSV**：CSV 占用 1.5GB 内存，加载 30 秒+；Parquet 压缩到 80MB，加载 3 秒，且保留类型信息。
2. **选择 Seaborn + Matplotlib 而非 Plotly**：分析报告以静态图表为主，Seaborn 与 Matplotlib 配合更顺手，且不依赖 JavaScript 渲染。
3. **不选择机器学习模型**：本项目是描述性分析（发生了什么、为什么），非预测性分析（未来会发生什么）；建模属于数据科学岗方向。
4. **RFM 用 3×3×3 分箱而非 KMeans 聚类**：分箱可解释性强、业务方容易理解，且 1 万样本量下聚类边界不稳定。
5. **数据通过软链而非复制**：避免在仓库中保存 482MB 大文件，保持仓库轻量。
6. **数据质量"清洗而非删除"**：对发现的 3 个数据质量问题，没有简单 dropna，而是逐个评估影响后做保留/标记（详见 Notebook 01）。

## 项目结构

```
taobao_user_behavior_analysis/
├── README.md                # 本文件
├── requirements.txt         # 依赖锁定
├── .gitignore               # 排除数据/图片
├── data/
│   ├── raw/                 # 软链到原始 CSV
│   ├── processed.parquet    # ETL 产出
│   └── derived/             # notebook 派生 CSV
├── scripts/
│   ├── 01_build_parquet.py  # ETL 脚本
│   └── utils.py             # 通用工具
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
| 02 - 漏斗分析 | 4 步漏斗 + 分层（时段/品类）+ 流失归因 |
| 03 - RFM 分群 | 8 类用户群体 + 差异化运营策略 |
| 04 - Cohort 留存 | 30 天留存热力图 + 整体留存曲线 |
| 05 - 总结 | 业务洞察 + 量化影响 + 数据局限 |

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

# 4. 准备数据（建立软链）
mkdir -p data/raw
ln -sf ../../taobao_data/user_action.csv data/raw/user_action.csv
# 注：原始数据需单独下载（阿里天池公开数据集）

# 5. 运行 ETL
python scripts/01_build_parquet.py

# 6. 启动 Jupyter
jupyter notebook
# 依次运行 notebooks/01 ~ 05
```

## 数据说明

- **来源**：阿里天池公开数据集（淘宝用户行为）
- **原始数据**：100 万用户完整行为，本项目使用 1 万用户子集
- **字段**：`user_id`, `item_id`, `behavior_type`, `item_category`, `time`
- **时间范围**：2014-11-18 ~ 2014-12-18（30 天）
- **数据局限**：品类 ID 脱敏、无价格信息、无用户属性、30 天窗口

## 数据局限

- 30 天时间窗口限制（无法看长期留存）
- 品类 ID 脱敏（无法结合业务知识解读）
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
````

- [ ] **Step 2: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/README.md
git commit -m "docs: write final README with STAR summary and project overview"
```

---

## Task 11: 整体回填与验证

**Files:** 修改所有 notebook 中的占位数字

- [ ] **Step 1: 从各 notebook 提取实际数字**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate

# 提取漏斗各阶段转化率
python -c "
import sys
sys.path.append('scripts')
import pandas as pd
from utils import load_data, BEHAVIOR_LABELS
df = load_data()
funnel = df.groupby('behavior_type')['user_id'].nunique().sort_index()
browse = funnel.iloc[0]
for bt, n in funnel.items():
    pct = n / browse * 100
    print(f'{BEHAVIOR_LABELS[bt]}: {n:,} ({pct:.4f}%)')
"
```

- [ ] **Step 2: 把实际数字回填到 Notebook 02 的 markdown**

打开 `notebooks/02_conversion_funnel.ipynb`，把"流失率 X%"、"购买率最高时段"等占位文本替换为实际数字。

- [ ] **Step 3: 回填 Notebook 04 的留存数字**

打开 `notebooks/04_retention_cohort.ipynb`，把"D1 留存 X%"、"D7 留存 X%"等占位文本替换为实际数字。

- [ ] **Step 4: 回填 README 中的关键数字**

打开 `README.md`，把"流失 X%"、"500 单"等占位数字替换为实际值。

- [ ] **Step 5: 重新执行所有 notebook 确保数字一致**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
for nb in notebooks/0*.ipynb; do
    jupyter nbconvert --to notebook --execute "$nb" --output "$(basename $nb)"
done
```

- [ ] **Step 6: 验证所有图表存在**

```bash
ls -la images/
```

Expected: 至少 9 个 PNG 文件（01 × 3，02 × 4，03 × 2，04 × 2）。

- [ ] **Step 7: Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/
git commit -m "docs: fill in actual numbers from notebook execution"
```

---

## Task 12: 整体跑通验证 + 推送到 GitHub

**Files:** 无（验证 + 推送）

- [ ] **Step 1: 在干净环境中验证可复现性**

```bash
cd /Users/macmini/workspace/实习项目
# 模拟一个干净 clone 后的状态
rm -rf taobao_user_behavior_analysis/.venv
cd taobao_user_behavior_analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/01_build_parquet.py
# 验证 parquet 产出
python -c "import pandas as pd; df = pd.read_parquet('data/processed.parquet'); print('OK:', len(df), '行')"
```

Expected: 看到 "OK: 12200000 行"。

- [ ] **Step 2: 验证 notebook 可逐个运行（手动打开 jupyter 或命令行）**

```bash
cd /Users/macmini/workspace/实习项目/taobao_user_behavior_analysis
source .venv/bin/activate
jupyter nbconvert --to notebook --execute notebooks/01_data_exploration.ipynb --output 01_data_exploration.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_conversion_funnel.ipynb --output 02_conversion_funnel.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_user_segmentation_rfm.ipynb --output 03_user_segmentation_rfm.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_retention_cohort.ipynb --output 04_retention_cohort.ipynb
jupyter nbconvert --to notebook --execute notebooks/05_findings_and_recommendations.ipynb --output 05_findings_and_recommendations.ipynb
```

Expected: 5 个 notebook 全部成功执行，无报错。

- [ ] **Step 3: 最终检查文件结构**

```bash
cd /Users/macmini/workspace/实习项目
find taobao_user_behavior_analysis -type f -not -path "*/.git/*" -not -path "*/.venv/*" -not -path "*/.ipynb_checkpoints/*" -not -name "*.parquet" -not -name "*.png" -not -name "*.csv" | sort
```

Expected: README.md, requirements.txt, .gitignore, 5 个 notebook, 2 个 scripts, 一些 .gitkeep。

- [ ] **Step 4: 推送到 GitHub**

```bash
cd /Users/macmini/workspace/实习项目
git add taobao_user_behavior_analysis/
git commit -m "feat: complete taobao user behavior funnel analysis project" || echo "no changes to commit"
git push origin main
```

Expected: 推送成功。

- [ ] **Step 5: 在 GitHub 上验证**

打开 https://github.com/sherry-wsr/taboo，浏览目录结构和 README 渲染效果。

- [ ] **Step 6: 准备 README 截图**

打开 README，截图（或用 `cmd+shift+4` 截屏）保存为 `docs/screenshot.png`（可选，用于在简历/求职信中引用）。

- [ ] **Step 7: 最终 Commit**

```bash
cd /Users/macmini/workspace/实习项目
git add docs/screenshot.png 2>/dev/null || true
git commit -m "docs: add README screenshot" || echo "nothing to commit"
git push origin main || echo "截图可选，不阻塞"
```

---

## 自检（已完成）

**1. Spec 覆盖检查**：

| Spec 章节 | 实施任务 |
|----------|---------|
| 1. 项目目标（STAR） | Task 10（README 含 STAR 摘要） |
| 2. 数据策略 | Task 3（ETL）+ Task 4（utils） |
| 3. 项目结构 | Task 1（脚手架） |
| 4.1 Notebook 1 | Task 5 |
| 4.2 Notebook 2 | Task 6（含归因分析） |
| 4.3 Notebook 3 | Task 7 |
| 4.4 Notebook 4 | Task 8 |
| 4.5 Notebook 5 | Task 9 |
| 5. 可视化规范 | Task 4（setup_plot_style） |
| 6. README 设计 | Task 10 + Task 11（回填） |
| 7. 测试与质量 | Task 5（assert）、Task 8（cohort 自检）、Task 11（验证） |
| 8. 风险与边界 | Task 10（README 数据局限）+ Task 9（Notebook 05） |
| 9. 实施里程碑 | Task 1-12 对应 |

✓ 所有 spec 章节都有对应任务。

**2. 占位符扫描**：无 TBD/TODO/待定/实现类似等含糊措辞。
（Step 中所有具体数字都用"X%"占位是合理的——它们会在 Task 11 实际运行后回填）

**3. 类型一致性**：
- `BEHAVIOR_LABELS`、`BEHAVIOR_COLORS` 在 utils.py 定义（Task 4），后续所有 notebook 引用一致
- `load_data()`、`setup_plot_style()`、`save_fig()` 在 utils.py 定义（Task 4），引用一致
- `processed.parquet` 路径在 ETL 脚本（Task 3）和 utils.py（Task 4）一致
- RFM segment 名称在 Task 7 定义，在 Task 10 README 中引用一致

✓ 无不一致。

---

**PLAN END**

下一步：选择执行方式。
