"""ETL: CSV -> Parquet

Reads the original CSV and optimizes dtypes, outputs a compressed Parquet file.
All subsequent notebooks load from this Parquet file.
"""
import time
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = PROJECT_ROOT / "data" / "raw" / "user_action.csv"
OUT_PARQUET = PROJECT_ROOT / "data" / "processed.parquet"


def build_parquet() -> None:
    """Read CSV in chunks, optimize dtypes, write Parquet."""
    assert RAW_CSV.exists(), f"原始 CSV 不存在: {RAW_CSV}"

    t0 = time.time()
    print(f"[1/3] 读取 CSV: {RAW_CSV}")

    chunks = []
    chunk_size = 1_000_000
    for i, chunk in enumerate(pd.read_csv(RAW_CSV, chunksize=chunk_size)):
        chunk["behavior_type"] = chunk["behavior_type"].astype("int8")
        chunk["user_id"] = chunk["user_id"].astype("category")
        chunk["item_id"] = chunk["item_id"].astype("category")
        chunk["item_category"] = chunk["item_category"].astype("category")
        chunk["time"] = pd.to_datetime(chunk["time"], format="%Y-%m-%d %H")
        chunks.append(chunk)
        print(f"  chunk {i + 1}: {len(chunk):,} rows")

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
