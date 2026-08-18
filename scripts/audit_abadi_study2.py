from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "abadi_study2_2020" / "abadi_2023_four_country_study2.csv"
OUT = ROOT / "new_computations" / "abadi_study2_audit"
OUT.mkdir(parents=True, exist_ok=True)

raw = pd.read_csv(DATA, encoding="utf-8-sig")
raw.columns = [str(column).strip() for column in raw.columns]

required = {
    "country": ["Country"],
    "demographics": ["A3.1", "A3.2", "A3.7", "A3.8", "A3.9", "A3.10"],
    "threat": ["A9.1", "A9.2", "A9.3*", "A9.4", "A9.5", "A9.6", "A9.7", "A9.8*"],
    "attention_check": ["A18.1"],
    "populist_attitudes": ["A20.1", "A20.2", "A20.3", "A21.1", "A21.2*", "A22.1", "A22.2"],
    "nativism": ["A23.1", "A23.2", "A23.3"],
    "conspiracy_mentality": [f"A24.{number}" for number in range(1, 6)],
}

availability = []
for family, variables in required.items():
    for variable in variables:
        availability.append({
            "family": family,
            "variable": variable,
            "available": variable in raw.columns,
            "missing_n": int(raw[variable].isna().sum()) if variable in raw.columns else None,
            "unique_values": int(raw[variable].nunique(dropna=True)) if variable in raw.columns else None,
            "min": float(pd.to_numeric(raw[variable], errors="coerce").min()) if variable in raw.columns else None,
            "max": float(pd.to_numeric(raw[variable], errors="coerce").max()) if variable in raw.columns else None,
        })
availability_df = pd.DataFrame(availability)
availability_df.to_csv(OUT / "required_variable_availability.csv", index=False)

country_counts = raw["Country"].value_counts(dropna=False).rename_axis("country_code").reset_index(name="n")
country_counts.to_csv(OUT / "country_counts_raw.csv", index=False)

attention = raw["A18.1"].value_counts(dropna=False).rename_axis("attention_response").reset_index(name="n")
attention.to_csv(OUT / "attention_check_distribution.csv", index=False)

study2_nodes = sum((items for family, items in required.items() if family not in {"country", "attention_check"}), [])
node_frame = raw.loc[:, study2_nodes].apply(pd.to_numeric, errors="coerce")

summary = {
    "raw_rows": int(raw.shape[0]),
    "raw_columns": int(raw.shape[1]),
    "study2_core_nodes": int(len(study2_nodes)),
    "complete_cases_all_core_nodes": int(node_frame.dropna().shape[0]),
    "attention_pass_code": 5,
    "attention_pass_rows": int((pd.to_numeric(raw["A18.1"], errors="coerce") == 5).sum()),
    "attention_pass_complete_cases": int(node_frame.loc[pd.to_numeric(raw["A18.1"], errors="coerce") == 5].dropna().shape[0]),
    "all_required_variables_available": bool(availability_df["available"].all()),
}
(OUT / "study2_audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
print("\nCountry counts:\n", country_counts.to_string(index=False))
print("\nAttention-check distribution:\n", attention.to_string(index=False))
print("\nUnavailable variables:\n", availability_df.loc[~availability_df["available"], ["family", "variable"]].to_string(index=False))
