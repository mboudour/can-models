"""Interactive local interface for configurable Causal Attitude Network analyses.

Run from the repository root with:
    streamlit run app/app.py
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st
import yaml

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "user_runs"
R_AVAILABLE = shutil.which("Rscript") is not None
ALLOWED_SUFFIXES = {".csv", ".xlsx", ".xls"}
DOMAIN_OPTIONS = [
    "Beliefs",
    "Evaluations",
    "Feelings",
    "Behaviour",
    "Risk appraisal",
    "Governance",
    "Context",
    "Other",
]


@st.cache_data(show_spinner=False)
def workbook_sheets(file_bytes: bytes) -> list[str]:
    return pd.ExcelFile(io.BytesIO(file_bytes)).sheet_names


@st.cache_data(show_spinner=False)
def read_uploaded_data(file_bytes: bytes, filename: str, sheet: str | None) -> pd.DataFrame:
    suffix = Path(filename).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(io.BytesIO(file_bytes))
    return pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet or 0)


def display_name(variable: str) -> str:
    return re.sub(r"[_\-.]+", " ", str(variable)).strip().title()


def profile_variables(data: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for column in data.columns:
        series = data[column]
        numeric = pd.api.types.is_numeric_dtype(series)
        nonmissing = int(series.notna().sum())
        unique = int(series.nunique(dropna=True))
        values = pd.to_numeric(series, errors="coerce") if not numeric else series
        integer_like = bool(numeric and series.dropna().map(lambda value: float(value).is_integer()).all()) if nonmissing else False
        likely_ordinal = bool(numeric and integer_like and 2 <= unique <= 7)
        records.append(
            {
                "variable": str(column),
                "dtype": str(series.dtype),
                "nonmissing": nonmissing,
                "missing_pct": round(float(series.isna().mean() * 100), 2),
                "unique": unique,
                "numeric": numeric,
                "likely_ordinal": likely_ordinal,
                "min": float(values.min()) if numeric and nonmissing else np.nan,
                "max": float(values.max()) if numeric and nonmissing else np.nan,
            }
        )
    return pd.DataFrame.from_records(records)


def candidate_labels(variables: list[str]) -> dict[str, str]:
    return {variable: display_name(variable) for variable in variables}


def parse_filter_value(value: str) -> Any:
    stripped = value.strip()
    if not stripped:
        return ""
    try:
        numeric = float(stripped)
        return int(numeric) if numeric.is_integer() else numeric
    except ValueError:
        return stripped


def build_config(
    *,
    run_dir: Path,
    data_path: Path,
    sheet: str | None,
    project_title: str,
    node_mapping: list[dict[str, str]],
    node_type: str,
    levels: int,
    filter_variable: str,
    filter_operator: str,
    filter_value: Any,
    country_variable: str,
    use_variable: str,
    categorical_variables: list[str],
    factor_items: list[str],
    country_minimum_n: int,
    quick_mode: bool,
) -> dict[str, Any]:
    node_ids = [entry["id"] for entry in node_mapping]
    factor_models: list[dict[str, Any]] = []
    if len(factor_items) >= 3:
        factor_models.append(
            {
                "id": "user_selected_scale",
                "label": "User-selected candidate scale",
                "items": factor_items,
                "estimator": "MLR",
                "minimum_cfi": 0.90,
                "maximum_rmsea": 0.08,
                "country_invariance": bool(country_variable),
            }
        )

    iterations = 25 if quick_mode else 250
    nct_iterations = 25 if quick_mode else 100
    config: dict[str, Any] = {
        "project": {
            "id": re.sub(r"[^a-z0-9_]+", "_", project_title.lower()).strip("_") or "user_can_analysis",
            "title": project_title,
            "seed": 20260818,
            "interpretive_notice": (
                "The Causal Attitude Network is a substantive theory of interacting attitude elements. "
                "With cross-sectional survey data, undirected network edges are conditional associations and do not establish directional causal effects."
            ),
        },
        "input": {
            "path": str(data_path.resolve()),
            "sheet": sheet or "Sheet1",
            "format": data_path.suffix.lower().lstrip("."),
            "questionnaire": "",
            "source_doi": "",
            "source_license": "User supplied",
        },
        "audit": {"mardia_max_n": 2000},
        "sample": {
            "filter": {
                "variable": filter_variable,
                "operator": filter_operator,
                "value": filter_value,
                "label": "User-defined analysis filter" if filter_variable else "No filter",
            },
            "complete_case_primary_network": True,
        },
        "variables": {
            "country": country_variable,
            "language": "",
            "study_field": "",
            "gender": "",
            "age": "",
            "use_frequency": use_variable,
            "use_experience": "",
        },
        "network": {
            "estimator": "mgm",
            "regularization": "LASSO",
            "model_selection": "EBIC",
            "ebic_gamma": 0.25,
            "node_type": node_type,
            "node_levels": int(levels),
            "nodes": node_mapping,
        },
        "factor_models": factor_models,
        "bootstrapping": {
            "edge_bootstrap_iterations": iterations,
            "case_drop_bootstrap_iterations": iterations,
            "case_drop_proportions": [0.05, 0.10, 0.25, 0.50, 0.75],
        },
        "community_detection": {"primary_algorithm": "walktrap", "bootstrap_consensus_iterations": 10 if quick_mode else 100},
        "comparisons": {
            "split_sample": {"enabled": True, "proportion_first_sample": 0.50, "label": "Random split-sample methodological check"},
            "use_frequency_median_split": {
                "enabled": bool(use_variable),
                "variable": use_variable,
                "exclude_from_network": True,
                "label": "User-selected median-split comparison",
            },
            "country": {
                "enabled": bool(country_variable),
                "variable": country_variable,
                "minimum_n": int(country_minimum_n),
                "network_estimator": "ggm_spearman",
                "all_pairwise_nct": True,
                "nct_iterations": nct_iterations,
                "p_adjustments": ["bonferroni", "fdr"],
            },
            "networktree": {"enabled": bool(country_variable or use_variable), "moderators": [item for item in [country_variable, use_variable] if item]},
        },
        "contextual_associations": {"categorical_variables": categorical_variables, "effect_size": "cramers_v"},
        "output": {
            "computations_dir": str((run_dir / "outputs").resolve()),
            "figures_dir": str((run_dir / "figures").resolve()),
            "report_dir": str((run_dir / "report").resolve()),
            "save_rds": True,
            "save_csv": True,
            "figure_width": 14,
            "figure_height": 11,
            "figure_dpi": 180,
        },
    }
    # The implemented high/low comparison cannot use its grouping variable as a network node.
    if use_variable in node_ids:
        config["comparisons"]["use_frequency_median_split"]["enabled"] = False
    return config


def eligibility_table(
    data: pd.DataFrame,
    profile: pd.DataFrame,
    node_ids: list[str],
    country_variable: str,
    use_variable: str,
    factor_items: list[str],
    country_minimum_n: int,
) -> pd.DataFrame:
    numeric_nodes = set(profile.loc[profile["numeric"], "variable"].astype(str))
    selected = data.loc[:, node_ids] if node_ids else pd.DataFrame(index=data.index)
    complete_n = int(selected.dropna().shape[0]) if node_ids else 0
    all_numeric = set(node_ids).issubset(numeric_nodes)
    country_groups = 0
    eligible_countries = 0
    if country_variable:
        country_counts = data[country_variable].dropna().value_counts()
        country_groups = int(country_counts.size)
        eligible_countries = int((country_counts >= country_minimum_n).sum())

    rows = [
        {
            "Abadi-style computation": "Data audit and complete-case flow",
            "Status": "Ready" if len(node_ids) >= 3 else "Placeholder",
            "Requirement / action": "Map at least three distinct item-level nodes.",
        },
        {
            "Abadi-style computation": "Abadi joint mixed graphical network (MGM, LASSO/EBIC)",
            "Status": "Ready" if len(node_ids) >= 3 and all_numeric and complete_n >= max(100, len(node_ids) * 10) else "Not yet eligible",
            "Requirement / action": f"Mapped nodes: {len(node_ids)}; complete cases: {complete_n}; numeric coding: {'yes' if all_numeric else 'no'}. Numeric coding and an adequate complete-case sample are required.",
        },
        {
            "Abadi-style computation": "Centrality, edge accuracy, case-drop stability, and Walktrap communities",
            "Status": "Ready (time-intensive)" if len(node_ids) >= 3 and all_numeric and complete_n >= max(100, len(node_ids) * 10) else "Placeholder",
            "Requirement / action": "Requires an eligible core network. Bootstrap iterations are adjustable through Quick versus Full mode.",
        },
        {
            "Abadi-style computation": "CFA, country CFA, EFA, and measurement invariance",
            "Status": "Ready" if len(factor_items) >= 3 and set(factor_items).issubset(numeric_nodes) else "Placeholder",
            "Requirement / action": "Select at least three theoretically coherent numeric items for a candidate scale. Country invariance additionally needs a country variable and adequate country samples.",
        },
        {
            "Abadi-style computation": "Two-study network comparison (original-paper design)",
            "Status": "Placeholder",
            "Requirement / action": "Requires two independent, comparable studies or waves. The current runner offers a labelled random split-sample methodological check, not a substitute for a second study.",
        },
        {
            "Abadi-style computation": "High/low group networks and NCT",
            "Status": "Ready" if use_variable and use_variable not in node_ids and len(node_ids) >= 3 and all_numeric else "Placeholder",
            "Requirement / action": "Choose a numeric grouping variable that is not included as a network node. The current generic implementation uses a median split.",
        },
        {
            "Abadi-style computation": "Country networks, pairwise NCT, and edge-matrix correlations",
            "Status": "Ready (time-intensive)" if eligible_countries >= 2 and len(node_ids) >= 3 and all_numeric else "Placeholder",
            "Requirement / action": f"Eligible country groups at n ≥ {country_minimum_n}: {eligible_countries}. At least two are needed.",
        },
        {
            "Abadi-style computation": "Country-network clustering and pooled cluster networks",
            "Status": "Ready" if eligible_countries >= 2 and len(node_ids) >= 3 and all_numeric else "Placeholder",
            "Requirement / action": "Requires at least two eligible country networks; three or more groups are preferable for meaningful clustering.",
        },
        {
            "Abadi-style computation": "NetworkTree moderation",
            "Status": "Optional placeholder",
            "Requirement / action": "Requires suitable categorical moderators and the optional R package `NetworkTree`; the app records an explicit status rather than silently omitting this module.",
        },
        {
            "Abadi-style computation": "Categorical association checks (chi-square and Cramér’s V)",
            "Status": "Ready" if len([column for column in profile["variable"].astype(str) if column not in numeric_nodes]) >= 2 else "Placeholder",
            "Requirement / action": "Requires at least two categorical variables selected for contextual checks.",
        },
    ]
    return pd.DataFrame(rows)


def write_run_bundle(uploaded_bytes: bytes, uploaded_name: str, config: dict[str, Any], data_preview: pd.DataFrame) -> tuple[Path, Path]:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_id = f"run_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    run_dir = RUNS_DIR / run_id
    raw_dir = run_dir / "raw_data"
    raw_dir.mkdir(parents=True, exist_ok=False)
    data_path = raw_dir / Path(uploaded_name).name
    data_path.write_bytes(uploaded_bytes)
    config_path = run_dir / "config.yml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    profile = profile_variables(data_preview)
    profile.to_csv(run_dir / "variable_profile.csv", index=False)
    manifest = {
        "run_id": run_id,
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_filename": Path(uploaded_name).name,
        "source_sha256": hashlib.sha256(uploaded_bytes).hexdigest(),
        "rows": int(data_preview.shape[0]),
        "columns": int(data_preview.shape[1]),
        "configuration": str(config_path),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return run_dir, config_path


def invoke_r(script_name: str, config_path: Path) -> tuple[int, str]:
    command = ["Rscript", "--vanilla", str(ROOT / "scripts" / script_name), "--config", str(config_path)]
    completed = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60 * 60)
    return completed.returncode, completed.stdout


CASE_STUDY_DIR = ROOT / "app" / "assets" / "chatgpt_case_study"
CHATGPT_DATA_DIR = ROOT / "data" / "raw" / "chatgpt_global_survey"


@st.cache_data(show_spinner=False)
def read_case_table(filename: str) -> pd.DataFrame:
    return pd.read_csv(CASE_STUDY_DIR / filename)


@st.cache_data(show_spinner=False)
def read_case_markdown(filename: str) -> str:
    return (CASE_STUDY_DIR / filename).read_text(encoding="utf-8")


def render_chatgpt_case_study() -> None:
    """Show the completed full-sample ChatGPT CAN example without requiring R at runtime."""
    st.header("ChatGPT perceptions: worked CAN case study")
    st.write(
        "This tab presents the completed example analysis bundled with the project. It uses the public global higher-education student survey, filters to respondents reporting prior ChatGPT use, and estimates the configured 30-node mixed graphical CAN. The result is a reproducible **case study**, not a causal claim from cross-sectional data."
    )

    flow = read_case_table("sample_flow.csv").set_index("statistic")["value"]
    summary = read_case_table("network_summary.csv").iloc[0]
    metric_columns = st.columns(4)
    metric_columns[0].metric("Raw survey records", f"{int(flow['raw_rows']):,}")
    metric_columns[1].metric("Prior ChatGPT users", f"{int(flow['filtered_rows']):,}")
    metric_columns[2].metric("Complete CAN cases", f"{int(flow['primary_network_rows']):,}")
    metric_columns[3].metric("CAN nodes", f"{int(summary['p'])}")

    overview_tab, network_tab, replication_tab, method_tab, conclusions_tab, download_tab = st.tabs(
        [
            "Overview",
            "Primary network",
            "Full Abadi replication",
            "Method and scope",
            "Conclusions and limits",
            "Data and code",
        ]
    )

    with overview_tab:
        st.subheader("Research object and question")
        st.write(
            "The example asks how beliefs about ChatGPT’s capability, governance and risk appraisals, satisfaction, attitudes, educational outcomes, labour-market expectations, and affect are conditionally connected among higher-education students. Nodes are item-level survey responses; colours identify theoretically defined attitude domains."
        )
        st.markdown(
            "**Configured domains:** behaviour; capability beliefs; governance evaluation; ethical and risk appraisal; satisfaction; attitude; educational outcomes; labour-market appraisal; and affect."
        )
        st.info(
            "Interpretive guardrail: the network is an undirected conditional-association model. The word ‘causal’ in CAN describes the substantive theory of linked attitude elements; these cross-sectional estimates do not verify directional causal effects."
        )
        config = yaml.safe_load((ROOT / "config" / "chatgpt_example.yml").read_text(encoding="utf-8"))
        node_map = pd.DataFrame(config["network"]["nodes"])
        node_map.index = node_map.index + 1
        node_map.index.name = "Node"
        st.dataframe(node_map.rename(columns={"id": "Source variable", "label": "Survey item", "domain": "CAN domain"}), width="stretch", height=420)

    with network_tab:
        st.subheader("Primary 30-node mixed graphical CAN")
        st.image(str(CASE_STUDY_DIR / "primary_mgm_network.png"), caption="Primary MGM/LASSO/EBIC network. Numbers correspond to the node dictionary in the Overview tab; edge width reflects conditional-association magnitude.", width="stretch")
        results_columns = st.columns(2)
        with results_columns[0]:
            st.markdown("**Network summary**")
            st.dataframe(pd.DataFrame([summary]).rename(columns={"n": "Complete cases", "p": "Nodes", "density": "Density", "global_strength": "Global strength", "nonzero_edges": "Non-zero edges"}), width="stretch", hide_index=True)
            strength = read_case_table("centrality.csv").sort_values("Strength", ascending=False).head(10)
            st.markdown("**Ten highest-strength nodes**")
            st.dataframe(strength[["node", "Strength", "ExpectedInfluence"]].rename(columns={"node": "Node"}), width="stretch", hide_index=True)
        with results_columns[1]:
            edges = read_case_table("edge_table.csv").sort_values("abs_weight", ascending=False).head(12)
            st.markdown("**Twelve strongest conditional associations**")
            st.dataframe(edges[["from", "to", "weight", "sign"]].rename(columns={"from": "From", "to": "To", "weight": "Weight", "sign": "Direction"}), width="stretch", hide_index=True)
            predictability = read_case_table("predictability.csv").sort_values("predictability", ascending=False).head(10)
            st.markdown("**Highest predictability estimates**")
            st.dataframe(predictability.rename(columns={"node": "Node", "predictability": "Predictability", "measure": "Measure"}), width="stretch", hide_index=True)

    with replication_tab:
        st.subheader("Full Abadi et al. computation-by-computation ledger")
        st.write(
            "This matrix accounts for every major computation, comparison, and conclusion path in Abadi et al. It separates executed ChatGPT results from literal replications that are impossible because the corresponding construct or research design is absent, and from implemented modules whose full offline run was runtime-deferred. Nothing is silently omitted."
        )
        ledger = read_case_table("abadi_full_replication_ledger.csv")
        ledger_columns = [
            "id",
            "paper_element",
            "Abadi_et_al_computation_or_claim",
            "literal_replication_status",
            "ChatGPT_treatment",
            "execution_status",
            "required_disclaimer",
        ]
        st.dataframe(
            ledger.loc[:, ledger_columns].rename(
                columns={
                    "id": "ID",
                    "paper_element": "Paper section",
                    "Abadi_et_al_computation_or_claim": "Abadi et al. element",
                    "literal_replication_status": "Replication status",
                    "ChatGPT_treatment": "ChatGPT treatment",
                    "execution_status": "Execution status",
                    "required_disclaimer": "Required interpretation",
                }
            ),
            width="stretch",
            height=620,
            hide_index=True,
        )
        status_counts = ledger["execution_status"].value_counts().reset_index()
        status_counts.columns = ["Execution status", "Elements"]
        st.dataframe(status_counts, width="stretch", hide_index=True)
        st.download_button(
            "Download full replication ledger",
            data=(CASE_STUDY_DIR / "abadi_full_replication_ledger.csv").read_bytes(),
            file_name="chatgpt_abadi_full_replication_ledger.csv",
            mime="text/csv",
            key="case_download_full_replication_ledger",
        )
        st.download_button(
            "Download paper-to-ChatGPT mapping",
            data=(ROOT / "docs" / "chatgpt_full_replication_mapping.md").read_bytes(),
            file_name="chatgpt_abadi_replication_mapping.md",
            mime="text/markdown",
            key="case_download_full_replication_mapping",
        )

    with method_tab:
        st.subheader("Reproducible computation")
        st.write(
            "The case study applies the reusable workflow configured in `config/chatgpt_example.yml`: numeric 1–5 item coding, complete-case primary network preparation, mixed graphical model estimation with LASSO/EBIC selection, centrality/predictability exports, bootstrap and Walktrap modules, factor-analysis modules, and configurable subgroup/country procedures."
        )
        mardia = read_case_table("mardia_multivariate_normality.csv")
        st.markdown("**Mardia diagnostic**")
        st.dataframe(mardia, width="stretch", hide_index=True)
        st.caption("The Mardia diagnostic uses a deterministic 2,000-case subsample for computational feasibility. The primary network uses all 11,964 complete cases.")
        st.markdown(
            "The network should be read as a structured description of conditional associations. For a causal or temporal test of the CAN theory, a longitudinal or experimental follow-up would be required."
        )

    with conclusions_tab:
        st.subheader("Conclusions and interpretation boundaries")
        st.warning(
            "The ChatGPT case study is not a substantive replication of Abadi et al.’s political-attitude findings. It contains no measures of populism, nativism, realistic or symbolic threat, conspiracy mentality, or left–right political orientation; it also contains no second independent study or wave."
        )
        st.markdown(read_case_markdown("case_study_conclusions.md"))
        st.divider()
        st.subheader("Explicit placeholders and reasons")
        st.markdown(read_case_markdown("limitations_and_placeholders.md"))
        st.download_button(
            "Download conclusions and limitations",
            data=(CASE_STUDY_DIR / "case_study_conclusions.md").read_bytes() + b"\n\n" + (CASE_STUDY_DIR / "limitations_and_placeholders.md").read_bytes(),
            file_name="chatgpt_can_conclusions_and_limitations.md",
            mime="text/markdown",
            key="case_download_conclusions_limitations",
        )

    with download_tab:
        st.subheader("Reuse the full case study")
        st.write("The original public dataset is released under CC BY 4.0. Download the data, questionnaire, configuration, and selected results below; cite the data source and companion article when reusing them.")
        download_columns = st.columns(2)
        downloads = [
            ("Download original survey workbook", CHATGPT_DATA_DIR / "finaldataset.xlsx", "finaldataset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("Download original questionnaire", CHATGPT_DATA_DIR / "questionnaire.pdf", "questionnaire.pdf", "application/pdf"),
            ("Download CAN configuration", ROOT / "config" / "chatgpt_example.yml", "chatgpt_example.yml", "application/x-yaml"),
            ("Download centrality results", CASE_STUDY_DIR / "centrality.csv", "chatgpt_can_centrality.csv", "text/csv"),
            ("Download edge table", CASE_STUDY_DIR / "edge_table.csv", "chatgpt_can_edges.csv", "text/csv"),
            ("Download network image", CASE_STUDY_DIR / "primary_mgm_network.png", "chatgpt_primary_can_network.png", "image/png"),
        ]
        for index, (label, path, name, mime) in enumerate(downloads):
            with download_columns[index % 2]:
                st.download_button(label, data=path.read_bytes(), file_name=name, mime=mime, key=f"case_download_{index}")
        st.markdown(
            "**Sources:** [Ravšelj et al. dataset](https://doi.org/10.17632/ymg9nsn6kn.2); [Ravšelj et al. companion article](https://doi.org/10.1371/journal.pone.0315011); [Abadi et al. CAN workflow](https://doi.org/10.1080/15366367.2024.2363718); and [Dalege et al. CAN model](https://doi.org/10.1037/a0039802)."
        )


st.set_page_config(page_title="CAN Models", page_icon="◌", layout="wide")
st.title("CAN Models")
st.caption("A reproducible Causal Attitude Network workspace with a completed ChatGPT case study and a separate bring-your-own-data workflow.")

workspace = st.radio(
    "Choose a workspace",
    ["ChatGPT case study", "Bring your own data"],
    horizontal=True,
    label_visibility="collapsed",
)
if workspace == "ChatGPT case study":
    render_chatgpt_case_study()
    st.stop()

st.header("Bring your own data")
st.caption("Upload a compatible survey, map its variable names to CAN roles, inspect the available computations, and create a reproducible run bundle.")
st.warning("Cross-sectional guardrail: estimated network edges are conditional associations. They do not, by themselves, demonstrate directional causal effects.")

with st.sidebar:
    st.header("1. Upload data")
    uploaded = st.file_uploader("CSV or Excel workbook", type=["csv", "xlsx", "xls"], help="Upload one row per participant. The file is stored only in a local run directory when you choose to create a run bundle.")
    quick_mode = st.toggle("Quick mode", value=True, help="Uses fewer bootstrap and permutation iterations for feasibility checks. Full mode retains the larger configured analysis settings.")

if uploaded is None:
    st.info("Upload a CSV or Excel file to begin mapping your variables. No fixed variable names are required.")
    st.stop()

file_bytes = uploaded.getvalue()
suffix = Path(uploaded.name).suffix.lower()
if suffix not in ALLOWED_SUFFIXES:
    st.error("Please upload a CSV, XLSX, or XLS file.")
    st.stop()

sheet = None
if suffix in {".xlsx", ".xls"}:
    sheets = workbook_sheets(file_bytes)
    sheet = st.sidebar.selectbox("Worksheet", sheets)

try:
    data = read_uploaded_data(file_bytes, uploaded.name, sheet)
except Exception as error:
    st.error(f"The file could not be read: {error}")
    st.stop()

if data.empty:
    st.error("The uploaded dataset has no rows.")
    st.stop()

data.columns = [str(column) for column in data.columns]
profile = profile_variables(data)
variables = profile["variable"].astype(str).tolist()
placeholder = "— none —"

st.subheader("Data preview")
left, right = st.columns([2, 1])
with left:
    st.dataframe(data.head(20), width="stretch", height=300)
with right:
    st.metric("Rows", f"{len(data):,}")
    st.metric("Variables", f"{len(data.columns):,}")
    st.metric("File", uploaded.name)

with st.expander("Variable profile and coding check", expanded=True):
    st.dataframe(profile, width="stretch", height=350)
    st.caption("The current R workflow expects numeric codes for network nodes. Categorical text labels should be recoded before estimation; their variable names can still be mapped here without requiring any predefined naming convention.")

st.header("2. Map your data to CAN roles")
st.write("Select item-level survey variables as network nodes. The labels and theoretical domains below are displayed in output figures and never need to match the raw column names.")
node_ids = st.multiselect("Network-node variables", variables, default=variables[: min(8, len(variables))], help="Select at least three numeric item-level variables. Avoid composite scores unless they are theoretically intended as a node.")
node_mapping: list[dict[str, str]] = []
if node_ids:
    for index, variable in enumerate(node_ids):
        columns = st.columns([3, 3, 2])
        with columns[0]:
            label = st.text_input(f"Label for {variable}", value=display_name(variable), key=f"label_{variable}")
        with columns[1]:
            domain = st.selectbox(f"CAN domain for {variable}", DOMAIN_OPTIONS, key=f"domain_{variable}")
        with columns[2]:
            st.caption(f"Source\n`{variable}`")
        node_mapping.append({"id": variable, "label": label, "domain": domain})

mapping_columns = st.columns(3)
with mapping_columns[0]:
    filter_variable = st.selectbox("Optional analysis filter", [placeholder] + variables, help="For example, select a prior-use variable and specify the response code to define the analytic sample.")
    filter_operator = st.selectbox("Filter operator", ["equals", "not_equals", "in"])
    filter_value_text = st.text_input("Filter value", value="")
with mapping_columns[1]:
    country_variable = st.selectbox("Optional country/group variable", [placeholder] + variables, help="Enables country-specific networks and country-comparison eligibility checks.")
    country_minimum_n = st.number_input("Minimum cases per country/group", min_value=50, max_value=5000, value=500, step=50)
with mapping_columns[2]:
    use_variable = st.selectbox("Optional numeric high/low grouping variable", [placeholder] + variables, help="Used for the implemented median-split comparison. It must not also remain in the compared network.")
    node_type = st.selectbox("Common node type", ["ordinal", "continuous"], index=0)
    levels = st.number_input("Ordinal response levels", min_value=2, max_value=20, value=5, step=1, disabled=node_type != "ordinal")

factor_items = st.multiselect("Optional candidate factor/CFA scale", node_ids, help="Select three or more coherent items only when a latent scale is theoretically justified. This activates CFA/EFA and, with country groups, invariance checks.")
categorical_options = profile.loc[~profile["numeric"], "variable"].astype(str).tolist()
categorical_variables = st.multiselect("Categorical variables for contextual association checks", categorical_options, help="Selecting two or more variables enables chi-square and Cramér’s V outputs.")

filter_variable = "" if filter_variable == placeholder else filter_variable
country_variable = "" if country_variable == placeholder else country_variable
use_variable = "" if use_variable == placeholder else use_variable
filter_value = parse_filter_value(filter_value_text)

st.header("3. Coverage and placeholders")
eligibility = eligibility_table(data, profile, node_ids, country_variable, use_variable, factor_items, int(country_minimum_n))
st.dataframe(eligibility, width="stretch", hide_index=True)
st.caption("A placeholder is a deliberate, documented stop: it identifies the missing design or data requirement and avoids presenting a non-applicable Abadi et al. computation as if it had been executed.")

st.header("4. Create a reproducible run bundle")
project_title = st.text_input("Run title", value="User-supplied CAN analysis")
ready_core = bool((eligibility["Abadi-style computation"] == "Abadi joint mixed graphical network (MGM, LASSO/EBIC)").any() and (eligibility.loc[eligibility["Abadi-style computation"] == "Abadi joint mixed graphical network (MGM, LASSO/EBIC)", "Status"].iloc[0] == "Ready"))

if st.button("Create configuration and run bundle", type="primary"):
    provisional_dir = RUNS_DIR / "provisional"
    provisional_data_path = provisional_dir / "raw_data" / Path(uploaded.name).name
    provisional_config = build_config(
        run_dir=provisional_dir,
        data_path=provisional_data_path,
        sheet=sheet,
        project_title=project_title,
        node_mapping=node_mapping,
        node_type=node_type,
        levels=int(levels),
        filter_variable=filter_variable,
        filter_operator=filter_operator,
        filter_value=filter_value,
        country_variable=country_variable,
        use_variable=use_variable,
        categorical_variables=categorical_variables,
        factor_items=factor_items,
        country_minimum_n=int(country_minimum_n),
        quick_mode=quick_mode,
    )
    # Write a bundle using final paths, then regenerate configuration with final locations.
    temporary_dir = RUNS_DIR / f"temporary_{uuid.uuid4().hex[:8]}"
    temporary_dir.mkdir(parents=True, exist_ok=False)
    temporary_data_path = temporary_dir / "raw_data" / Path(uploaded.name).name
    final_config = build_config(
        run_dir=temporary_dir,
        data_path=temporary_data_path,
        sheet=sheet,
        project_title=project_title,
        node_mapping=node_mapping,
        node_type=node_type,
        levels=int(levels),
        filter_variable=filter_variable,
        filter_operator=filter_operator,
        filter_value=filter_value,
        country_variable=country_variable,
        use_variable=use_variable,
        categorical_variables=categorical_variables,
        factor_items=factor_items,
        country_minimum_n=int(country_minimum_n),
        quick_mode=quick_mode,
    )
    created_dir, created_config = write_run_bundle(file_bytes, uploaded.name, final_config, data)
    # Replace temporary absolute paths with actual run-directory paths.
    actual_data_path = created_dir / "raw_data" / Path(uploaded.name).name
    actual_config = build_config(
        run_dir=created_dir,
        data_path=actual_data_path,
        sheet=sheet,
        project_title=project_title,
        node_mapping=node_mapping,
        node_type=node_type,
        levels=int(levels),
        filter_variable=filter_variable,
        filter_operator=filter_operator,
        filter_value=filter_value,
        country_variable=country_variable,
        use_variable=use_variable,
        categorical_variables=categorical_variables,
        factor_items=factor_items,
        country_minimum_n=int(country_minimum_n),
        quick_mode=quick_mode,
    )
    created_config.write_text(yaml.safe_dump(actual_config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    shutil.rmtree(temporary_dir, ignore_errors=True)
    st.session_state["run_dir"] = str(created_dir)
    st.session_state["config_path"] = str(created_config)
    st.success(f"Created run bundle: {created_dir.relative_to(ROOT)}")

if "config_path" in st.session_state:
    active_config = Path(st.session_state["config_path"])
    active_run = Path(st.session_state["run_dir"])
    st.code(str(active_config.relative_to(ROOT)), language="text")
    st.download_button("Download generated YAML configuration", data=active_config.read_bytes(), file_name="can_user_config.yml", mime="application/x-yaml")

    if not R_AVAILABLE:
        st.info("This deployment is running in mapping-only mode because no R runtime is available. You can upload data, map variables, inspect eligibility, and download a reproducible configuration. Run the analysis locally or on a container host with R and the required packages.")

    if st.button("Validate configuration with the R workflow", disabled=not R_AVAILABLE):
        with st.spinner("Running validation..."):
            return_code, output = invoke_r("validate_config.R", active_config)
        st.code(output or "No console output.", language="text")
        if return_code == 0:
            st.success("Configuration passed R-side validation.")
        else:
            st.error("R-side validation found an issue. Review the log above and adjust the mapping.")

    if ready_core:
        if st.button("Run core analysis (data audit, factor models, primary CAN network)", disabled=not R_AVAILABLE):
            with st.spinner("Running the core R workflow. Larger data and more nodes take longer."):
                return_code, output = invoke_r("run_core_analysis.R", active_config)
            (active_run / "core_analysis_console.log").write_text(output, encoding="utf-8")
            st.code(output[-12000:] or "No console output.", language="text")
            if return_code == 0:
                st.success("Core analysis completed. Outputs are inside the run bundle.")
            else:
                st.error("Core analysis did not complete. The console log and configuration remain available for debugging.")
    else:
        st.info("Core analysis is disabled until the joint-network eligibility row is Ready.")

    st.checkbox("I understand that full diagnostics and all pairwise country comparisons can be computationally intensive.", key="full_ack")
    if st.session_state.get("full_ack", False) and ready_core and st.button("Run full configured workflow", disabled=not R_AVAILABLE):
        with st.spinner("Running the complete configured workflow. This may take a substantial amount of time."):
            return_code, output = invoke_r("run_example.R", active_config)
        (active_run / "full_analysis_console.log").write_text(output, encoding="utf-8")
        st.code(output[-12000:] or "No console output.", language="text")
        if return_code == 0:
            st.success("Full configured workflow completed. Outputs are inside the run bundle.")
        else:
            st.error("The full workflow did not complete. Inspect the saved console log and module status files.")

st.divider()
st.caption("The app does not infer substantive theory from variable names. Users must map their own variables and labels to a CAN node set, and the eligibility table records every unsupported or inapplicable computational step.")
