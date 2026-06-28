"""Common utilities: data loading + plot styling + path constants.

All notebooks import via:
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
    """Load the processed Parquet data.

    Returns:
        DataFrame with columns: user_id, item_id, behavior_type, item_category, time
    """
    assert PROCESSED_PARQUET.exists(), (
        f"Parquet 文件不存在: {PROCESSED_PARQUET}\n请先运行: python scripts/01_build_parquet.py"
    )
    df = pd.read_parquet(PROCESSED_PARQUET)
    return df


def setup_plot_style() -> None:
    """Unify plot styling across all notebooks."""
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["font.sans-serif"] = ["STHeiti", "Heiti SC", "PingFang SC", "STSong", "Arial Unicode MS"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 150
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 11


def save_fig(fig: plt.Figure, name: str) -> None:
    """Save figure to images/ directory."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    out = IMAGES_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"  -> saved: {out.relative_to(PROJECT_ROOT)}")
