from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "abadi_study2_2020" / "abadi_2023_four_country_study2.csv"
OUT = ROOT / "new_computations" / "abadi_study2_audit"
OUT.mkdir(parents=True, exist_ok=True)

nodes = [
    "Country", "A3.1", "A3.2", "A3.7", "A3.8", "A3.10",
    "A9.1", "A9.2", "A9.3*", "A9.4", "A9.5", "A9.6", "A9.7", "A9.8*",
    "A20.1", "A20.2", "A20.3", "A21.1", "A21.2*", "A22.1", "A22.2",
    "A23.1", "A23.2", "A23.3", "A24.1", "A24.2", "A24.3", "A24.4", "A24.5",
]

raw = pd.read_csv(DATA, encoding="utf-8-sig")
raw = raw.loc[raw["A3.1"] != 3, nodes]
records = []
for variable in nodes:
    counts = raw[variable].value_counts(dropna=False).sort_index()
    for value, count in counts.items():
        records.append({"variable": variable, "value": value, "n": int(count), "sparse_under_2": bool(count < 2), "sparse_under_5": bool(count < 5), "sparse_under_10": bool(count < 10)})
result = pd.DataFrame(records)
result.to_csv(OUT / "node_category_frequencies_after_gender_exclusion.csv", index=False)
summary = result.groupby("variable", as_index=False).agg(minimum_n=("n", "min"), categories=("value", "count"), sparse_categories_under_2=("sparse_under_2", "sum"), sparse_categories_under_5=("sparse_under_5", "sum"))
summary.to_csv(OUT / "node_category_frequency_summary.csv", index=False)
print(summary.to_string(index=False))
print("\nSparse categories (< 2):")
print(result.loc[result["sparse_under_2"], ["variable", "value", "n"]].to_string(index=False))
