"""Evidence-aware worked example using the Ravšelj et al. public ChatGPT survey."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "app" / "assets" / "chatgpt_ravselj_2025"
MODEL_DIR = ASSET_DIR / "focused_model"
INITIAL_DIR = ASSET_DIR / "initial_31node_diagnostic"
DATA_DIR = ROOT / "data" / "raw" / "chatgpt_ravselj_2025"


@st.cache_data(show_spinner=False)
def table(directory: Path, filename: str) -> pd.DataFrame:
    return pd.read_csv(directory / filename)


def download(label: str, path: Path, filename: str, mime: str, key: str) -> None:
    st.download_button(label, data=path.read_bytes(), file_name=filename, mime=mime, key=key)


def render_chatgpt_ravselj_example() -> None:
    st.header("Ravšelj et al.: ChatGPT perceptions worked example")
    st.write(
        "This is a **second worked example**, not an Abadi et al. replication. It uses the public global survey of higher-education students’ early perceptions of ChatGPT and demonstrates how the reusable CAN workflow responds when a large cross-sectional perception survey produces a dense network."
    )
    st.warning(
        "The completed 31-node network is a diagnostic result, not a publication-ready substantive network: all 465 possible edges were retained. The example therefore displays that result transparently and does not make centrality, bridge, causal, or intervention claims from it."
    )

    flow = table(MODEL_DIR, "sample_flow.csv").set_index("statistic")["value"]
    mgm_summary = table(MODEL_DIR, "mgm_network_summary.csv").iloc[0]
    metrics = st.columns(4)
    metrics[0].metric("Public records", f"{int(flow['raw_rows']):,}")
    metrics[1].metric("Prior ChatGPT users", f"{int(flow['filtered_rows']):,}")
    metrics[2].metric("Focused complete cases", f"{int(flow['primary_network_rows']):,}")
    metrics[3].metric("Focused nodes", int(mgm_summary["p"]))

    overview_tab, diagnostic_tab, focused_tab, assessment_tab, data_tab = st.tabs(
        [
            "Data and design",
            "Initial 31-node diagnostic",
            "Focused-model sensitivity",
            "Assessment and publication readiness",
            "Data and code",
        ]
    )

    with overview_tab:
        st.subheader("Source and analytical scope")
        st.write(
            "The source dataset contains 23,218 student responses. The worked example filters to participants reporting prior ChatGPT use (`Q13 = 1`) and uses 16,010 respondents before complete-case handling. The focused configuration contains 16 labelled item-level nodes spanning behaviour, capability beliefs, governance, risk appraisal, evaluations, expected outcomes, and feelings."
        )
        st.dataframe(
            table(MODEL_DIR, "node_map.csv").rename(
                columns={
                    "source_variable": "Questionnaire item",
                    "label": "Node label",
                    "domain": "CAN domain",
                    "levels": "Observed response levels",
                }
            ),
            width="stretch",
            hide_index=True,
        )
        st.info(
            "This is a single cross-sectional survey. Its undirected network edges are conditional associations, not verified directional causal effects or within-person processes."
        )
        st.markdown(
            "**Cite the sources:** Ravšelj et al. (2025), *Higher education students’ perceptions of ChatGPT: A global study of early reactions*, PLOS ONE, [10.1371/journal.pone.0315011](https://doi.org/10.1371/journal.pone.0315011); and the public data deposit, [10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2)."
        )

    with diagnostic_tab:
        st.subheader("The completed 31-node BYOD run")
        initial_summary = table(INITIAL_DIR, "network_summary.csv").iloc[0]
        st.error(
            f"Diagnostic result: {int(initial_summary['nonzero_edges'])} of {int(initial_summary['p']) * (int(initial_summary['p']) - 1) // 2} possible edges were non-zero (density = {initial_summary['density']:.2f}). This network is fully connected and should not be interpreted as a sparse CAN structure."
        )
        st.image(
            str(INITIAL_DIR / "primary_mgm_network.png"),
            caption="Initial 31-node MGM diagnostic. The edge overlap and generic labels make this a technical demonstration, not a publication figure.",
            width="stretch",
        )
        st.dataframe(table(INITIAL_DIR, "network_summary.csv"), width="stretch", hide_index=True)
        st.caption("The initial BYOD YAML had blank labels and a single default domain. The current reusable workflow normalizes blank labels, but the historical output is shown here unchanged for auditability.")

    with focused_tab:
        st.subheader("Pre-specified focused-model sensitivity")
        st.write(
            "A smaller, labelled 16-node configuration was specified before rerunning the workflow. It reduces conceptual redundancy but still yields dense networks under both the ordinal MGM and Spearman EBICglasso sensitivity estimators. The output is therefore retained to document sensitivity, not to select a preferred central node."
        )
        comparison = pd.concat(
            [
                table(MODEL_DIR, "mgm_network_summary.csv").assign(model="Ordinal MGM"),
                table(MODEL_DIR, "spearman_network_summary.csv").assign(model="Spearman EBICglasso sensitivity"),
            ],
            ignore_index=True,
        )
        st.dataframe(comparison[["model", "estimator", "n", "p", "density", "nonzero_edges", "global_strength"]], width="stretch", hide_index=True)
        cols = st.columns(2)
        with cols[0]:
            st.image(str(MODEL_DIR / "primary_mgm_network.png"), caption="Focused ordinal MGM: still fully connected.", width="stretch")
        with cols[1]:
            st.image(str(MODEL_DIR / "focused_ggm_spearman_network.png"), caption="Focused Spearman sensitivity: still dense; no selective edge interpretation.", width="stretch")
        st.warning(
            "A post-hoc numerical edge threshold is not a replacement for an a priori measurement and model-specification strategy. Do not report the displayed centrality rankings as substantive findings without robustness checks and a redesigned primary model."
        )

    with assessment_tab:
        st.subheader("CAN assessment and publication readiness")
        st.markdown((ASSET_DIR / "assessment.md").read_text(encoding="utf-8"))

    with data_tab:
        st.subheader("Public source files and reproducibility artifacts")
        downloads = [
            ("Download Ravšelj survey data", DATA_DIR / "final_dataset.xlsx", "ravselj_chatgpt_final_dataset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("Download Ravšelj questionnaire", DATA_DIR / "questionnaire.pdf", "ravselj_chatgpt_questionnaire.pdf", "application/pdf"),
            ("Download focused CAN configuration", ROOT / "config" / "chatgpt_ravselj_focus.yml", "chatgpt_ravselj_focus.yml", "application/x-yaml"),
            ("Download assessment", ASSET_DIR / "assessment.md", "chatgpt_can_assessment.md", "text/markdown"),
            ("Download initial diagnostic edge table", INITIAL_DIR / "edge_table.csv", "chatgpt_initial_31node_edges.csv", "text/csv"),
            ("Download focused MGM edge table", MODEL_DIR / "mgm_edge_table.csv", "chatgpt_focused_mgm_edges.csv", "text/csv"),
        ]
        columns = st.columns(2)
        for index, (label, path, filename, mime) in enumerate(downloads):
            with columns[index % 2]:
                download(label, path, filename, mime, f"chatgpt_download_{index}")
        st.markdown(
            "**Sources:** [Ravšelj et al. companion publication](https://doi.org/10.1371/journal.pone.0315011); [public data deposit](https://doi.org/10.17632/ymg9nsn6kn.2); [Dalege et al. CAN model](https://doi.org/10.1037/a0039802); [Abadi et al. workflow reference](https://doi.org/10.1080/15366367.2024.2363718)."
        )
