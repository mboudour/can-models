"""CCAM December 2024 climate-engagement CAN feasibility case.

This public workspace deliberately exposes a failed non-saturation gate. It bundles
only derived non-row-level results; the official CCAM respondent-level source is
licensed for scholarly use but must not be redistributed.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "app" / "assets" / "ccam_dec2024_climate_engagement"
CONFIG_PATH = ROOT / "config" / "ccam_dec2024_climate_engagement.yml"
CCAM_OSF_URL = "https://osf.io/jw79p/"
CCAM_DOI_URL = "https://doi.org/10.17605/OSF.IO/JW79P"


@st.cache_data(show_spinner=False)
def ccam_table(filename: str) -> pd.DataFrame:
    return pd.read_csv(ASSET_DIR / filename)


def ccam_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Analysis component": "Official CCAM source and December 2024 extraction",
                "Abadi-style counterpart": "Study 2 source preparation and node mapping",
                "Status": "Executed",
                "Evidence / boundary": "Official CCAM 2008–2024 SPSS archive was verified locally against the public SHA-256 checksum. Terms of Use prohibit redistributing respondent-level data; the app bundles derived outputs only.",
            },
            {
                "Analysis component": "RQ1: 15-node December 2024 ordinal MGM",
                "Abadi-style counterpart": "RQ1 joint Study 2 MGM",
                "Status": "Executed — fails feasibility gate",
                "Evidence / boundary": "995 complete cases; 102 of 105 possible edges; density 0.971. The primary network is nearly complete and therefore not a sparse, interpretable CAN result.",
            },
            {
                "Analysis component": "Measurement probes",
                "Abadi-style counterpart": "Scale checks before scale-level interpretation",
                "Status": "Executed",
                "Evidence / boundary": "Anticipated-harm and policy-support CFA/EFA probes are supplied as descriptive measurement checks. They do not repair the saturated joint network.",
            },
            {
                "Analysis component": "Stricter EBIC and domain-bridging sensitivities",
                "Abadi-style counterpart": "Robustness and specification checks",
                "Status": "Executed — fails feasibility gate",
                "Evidence / boundary": "Primary gamma 0.50 remains density 0.895. Smaller theory-led bridge systems are 0.964–1.000 dense. Saturation is not an artefact of a single node set.",
            },
            {
                "Analysis component": "Bootstrap, centrality, cross-wave replication, and public substantive interpretation",
                "Abadi-style counterpart": "Network robustness and replication branches",
                "Status": "Not executed after gate failure",
                "Evidence / boundary": "Further network characterisation would not make an almost complete graph a meaningful or publication-ready CAN result. No causal or substantive conclusions are offered.",
            },
        ]
    )


def render_ccam_dec2024_feasibility_case() -> None:
    summary = ccam_table("network_summary.csv").set_index("metric")["value"]
    flow = ccam_table("sample_flow.csv").set_index("statistic")["value"]

    st.header("CCAM December 2024: Climate-Engagement CAN Feasibility Case")
    st.write(
        "This third case applies the same source audit, theory-led node mapping, MGM estimation, "
        "measurement checks, and specification-sensitivity logic used in the completed cases. "
        "Unlike the Abadi Study 2 and ESS cases, it is retained as a **transparent feasibility case** because the pre-specified network fails the project’s non-saturation gate."
    )
    st.error(
        "**Feasibility result, not a substantive finding:** the primary 15-node network has 102 of 105 possible edges (density 0.971). "
        "It is nearly fully connected, so its graph, centrality, and individual edges must not be interpreted as a meaningful or publication-ready CAN architecture."
    )
    st.warning(
        "Interpretive boundary: this December 2024 survey wave is cross-sectional. Even a non-saturated network would contain undirected conditional associations, not verified directional or causal effects."
    )

    metrics = st.columns(4)
    metrics[0].metric("Official CCAM records", f"{int(flow['raw_rows']):,}")
    metrics[1].metric("December 2024 complete cases", f"{int(flow['primary_network_rows']):,}")
    metrics[2].metric("Pre-specified nodes", int(summary["Nodes"]))
    metrics[3].metric("Primary density", f"{float(summary['Network density']):.3f}")

    scope_tab, network_tab, checks_tab, ledger_tab, data_tab = st.tabs(
        [
            "CCAM scope",
            "RQ1 feasibility network",
            "Measurement and sensitivity checks",
            "Complete analysis ledger",
            "Data and code",
        ]
    )

    with scope_tab:
        st.subheader("Why this source was tested")
        st.write(
            "The public CCAM archive contains repeated national U.S. cross-sections with climate belief and attribution, affective and anticipated risk, climate-policy support, and communication/attention measures. "
            "The December 2024 wave was selected for a 15-node climate-engagement system spanning those distinct conceptual domains."
        )
        st.markdown("**Sample preparation and transformations**")
        st.dataframe(ccam_table("sample_flow.csv"), width="stretch", hide_index=True)
        st.caption("Documented CCAM code −1 is converted to missing before complete-case network estimation.")
        st.markdown("**Pre-specified 15-node mapping**")
        nodes = ccam_table("node_map.csv").rename(
            columns={"source_variable": "Official CCAM variable", "label": "Node label", "domain": "CAN domain", "node_type": "Response type", "levels": "Observed response levels"}
        )
        nodes.index = nodes.index + 1
        nodes.index.name = "Node"
        st.dataframe(nodes, width="stretch", height=570)

    with network_tab:
        st.subheader("RQ1: primary December 2024 climate-engagement MGM")
        st.image(
            ASSET_DIR / "pooled_network.png",
            caption="15-node LASSO/EBIC MGM. This graph is shown for audit transparency only: its density is too high for meaningful CAN interpretation. Edge thickness reflects estimated conditional-association magnitude.",
            width="stretch",
        )
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Network feasibility summary**")
            st.dataframe(ccam_table("network_summary.csv"), width="stretch", hide_index=True)
            st.markdown("**Highest-strength nodes — not interpreted**")
            st.dataframe(ccam_table("top_nodes.csv").head(12), width="stretch", hide_index=True)
        with cols[1]:
            st.markdown("**Largest estimated edges — not interpreted**")
            st.dataframe(ccam_table("edge_table.csv").head(15)[["from", "to", "weight", "sign"]], width="stretch", hide_index=True)
            st.markdown("**Predictability export — descriptive only**")
            st.dataframe(ccam_table("predictability.csv").head(12), width="stretch", hide_index=True)
        st.info("The displayed primary network demonstrates why the case is not treated as a publishable CAN result: 102 of 105 possible conditional associations survive selection.")

    with checks_tab:
        st.subheader("Measurement probes and non-saturation sensitivity checks")
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Anticipated climate-harm CFA probe**")
            st.dataframe(ccam_table("anticipated_harm_cfa.csv"), width="stretch", hide_index=True)
        with cols[1]:
            st.markdown("**Climate transition-policy-support CFA probe**")
            st.dataframe(ccam_table("policy_support_cfa.csv"), width="stretch", hide_index=True)
        st.markdown("**Pre-specified stricter and theory-led node-set sensitivities**")
        st.dataframe(ccam_table("sensitivity_summary.csv"), width="stretch", hide_index=True)
        st.error(
            "No tested specification meets the non-saturation gate. The stricter primary model remains density 0.895; all compact domain-bridging systems remain density 0.964–1.000. Therefore no bootstrap, centrality-stability, or cross-wave result is presented as a completed substantive CAN branch."
        )

    with ledger_tab:
        st.subheader("Complete CCAM feasibility analysis ledger")
        ledger = ccam_ledger()
        st.dataframe(ledger, width="stretch", height=520, hide_index=True)
        st.download_button(
            "Download CCAM feasibility analysis ledger",
            data=ledger.to_csv(index=False).encode("utf-8"),
            file_name="ccam_dec2024_feasibility_analysis_ledger.csv",
            mime="text/csv",
            key="download_ccam_ledger",
        )
        st.download_button(
            "Download CCAM gate assessment",
            data=(ROOT / "docs" / "ccam_dec2024_feasibility_case.md").read_bytes(),
            file_name="ccam_dec2024_feasibility_case.md",
            mime="text/markdown",
            key="download_ccam_gate_assessment",
        )

    with data_tab:
        st.subheader("Official source, access boundary, and reproducible configuration")
        st.write(
            "The official CCAM archive is openly downloadable for research use from the Yale Program on Climate Change Communication and George Mason University OSF project. "
            "Its Terms of Use prohibit redistributing or transferring the respondent-level source data. This repository and app therefore provide source links, a checksum, configuration, code, and derived non-row-level feasibility artifacts only."
        )
        st.markdown(f"- [Official CCAM OSF archive]({CCAM_OSF_URL})")
        st.markdown(f"- [Archive DOI]({CCAM_DOI_URL})")
        st.markdown("- Official source SHA-256: `db6c0d5f0f8acea6591ed4a803a85be1491aa4b0a02239b74792a636997477eb`")
        st.download_button(
            "Download CCAM feasibility configuration",
            data=CONFIG_PATH.read_bytes(),
            file_name="ccam_dec2024_climate_engagement.yml",
            mime="text/yaml",
            key="download_ccam_config",
        )
        st.code(
            "# Official CCAM data must remain outside Git and the container image\n"
            "mkdir -p data/external/ccam_2008_2024\n"
            "# Download the official SPSS archive and codebook from OSF\n"
            "Rscript --vanilla scripts/validate_config.R --config config/ccam_dec2024_climate_engagement.yml\n"
            "Rscript --vanilla scripts/run_core_analysis.R --config config/ccam_dec2024_climate_engagement.yml",
            language="bash",
        )
