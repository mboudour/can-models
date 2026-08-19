"""Source-cited ESS CRONOS-3 Wave 6 SoGreen worked-case renderer.

This public view deliberately contains no respondent-level ESS data and no network
result until the pre-specified feasibility and robustness gate is satisfied.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "ess_cronos3_sogreen_w6.yml"
ESS_PORTAL_URL = "https://ess.sikt.no/en/series/a46bcac5-b030-444b-9280-441ec97e1bce"
SOGREEN_RELEASE_URL = "https://www.europeansocialsurvey.org/news/article/new-panel-survey-data-climate-change-now-available"
ESS_TERMS_URL = "https://www.europeansocialsurvey.org/contact/disclaimer"


def node_map() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("w6sgq11", "Climate-change worry", "Climate appraisal"),
            ("w6sgq12", "Personal responsibility to reduce climate change", "Climate appraisal"),
            ("w6seq2", "Worry about local extreme weather", "Climate appraisal"),
            ("w6sgq13", "Trust in government to address climate change", "Institutional capacity"),
            ("w6seq4", "Government preparedness for extreme weather", "Institutional capacity"),
            ("w6sgq14", "Environment versus economic growth priority", "Policy orientation and legitimacy"),
            ("w6sgq15", "Familiarity with national climate policies", "Policy orientation and legitimacy"),
            ("w6sgq16", "Confidence climate policies consider everyone views", "Policy orientation and legitimacy"),
            ("w6sgq17", "Confidence in fair climate-policy outcomes", "Policy orientation and legitimacy"),
            ("w6sgq18", "Expected climate-policy impact on jobs", "Expected transition impacts"),
            ("w6sgq19", "Expected lifestyle changes from climate policies", "Expected transition impacts"),
            ("w6sgq20", "Expected daily-life impact of lifestyle changes", "Expected transition impacts"),
            ("w6sgq21", "Concern about ability to pay energy bills", "Personal-cost concerns"),
            ("w6sgq22", "Concern about increased transport costs", "Personal-cost concerns"),
            ("w6sgq23", "Concern about future job loss", "Personal-cost concerns"),
        ],
        columns=["Official Wave 6 variable", "Approved node label", "CAN domain"],
    )


def readiness_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Component": "Official source acquisition and provenance",
                "Status": "Implemented locally",
                "Boundary": "The workflow verifies the official Wave 6 source file and codebook with the configured SHA-256 fingerprint; neither file is distributed here.",
            },
            {
                "Component": "Focused 15-node climate-attitudes mapping",
                "Status": "Approved specification",
                "Boundary": "The nodes are theory-led and exclude the distinct transport/appliance behavioural subsystem from the initial case.",
            },
            {
                "Component": "Wave 6 baseline MGM",
                "Status": "Results pending publication gate",
                "Boundary": "No network, centrality, community, or intervention claim is displayed until feasibility, stability, and replication checks are complete.",
            },
            {
                "Component": "Country replication and split-sample check",
                "Status": "Configured; results pending",
                "Boundary": "Country and held-out-sample checks must be run and reviewed before any public substantive interpretation.",
            },
            {
                "Component": "Temporal panel extension",
                "Status": "Deferred",
                "Boundary": "It requires documented overlap with later released waves and a pre-specified longitudinal model; Wave 6 alone does not establish temporal direction.",
            },
        ]
    )


def render_ess_cronos3_sogreen_case() -> None:
    st.header("ESS CRONOS-3 / SoGreen: Wave 6 climate-attitudes case")
    st.write(
        "This is a **source-cited, locally reproducible second worked case** using the official ESS CRONOS-3 Wave 6 SoGreen release. "
        "The public application contains the analytical specification and access route, but not ESS respondent-level data."
    )
    st.warning(
        "**Results pending a publication gate.** A compact 15-node specification has been approved, but the app will not display a network, centrality ranking, community structure, or intervention claim until the pre-specified feasibility, robustness, and replication checks are complete."
    )

    metrics = st.columns(4)
    metrics[0].metric("Wave 6 records", "9,585")
    metrics[1].metric("CRONOS-3 countries", "11")
    metrics[2].metric("Approved CAN nodes", "15")
    metrics[3].metric("Public analysis state", "Results pending")

    access_tab, nodes_tab, gate_tab, code_tab = st.tabs(
        ["Official data and design", "Approved node map", "Publication gate", "Code and local reproduction"]
    )

    with access_tab:
        st.subheader("Official access; no external microdata hosting")
        st.write(
            "CRONOS-3 is a cross-national probability-based, mixed-mode panel linked to the main ESS. "
            "Wave 6 includes a green-transition module with climate concern, responsibility, government trust, policy legitimacy, expected costs, and extreme-weather items."
        )
        st.markdown(
            f"Download the official file and documentation from the [ESS CRONOS-3 Data Portal]({ESS_PORTAL_URL}). "
            f"Read the [Wave 6 SoGreen release]({SOGREEN_RELEASE_URL}) and the [ESS conditions of use]({ESS_TERMS_URL}) before reuse."
        )
        st.info(
            "The ESS recommends linking to its Data Portal instead of placing its datasets on external websites. The repository therefore stores neither the Wave 6 CSV nor the codebook."
        )
        st.write(
            "The initial analysis is a **between-person Wave 6 baseline network**. Even though CRONOS-3 is a panel, undirected Wave 6 edges are conditional associations; they do not establish within-person change, temporal direction, or verified causal effects."
        )

    with nodes_tab:
        st.subheader("Approved, theory-led baseline node set")
        st.write(
            "The case is deliberately limited to climate appraisal, institutional capacity, policy orientation/legitimacy, expected transition impacts, and personal-cost concerns. Transport and appliance questions are reserved for a later behavioural subsystem analysis rather than being added mechanically to this baseline network."
        )
        nodes = node_map()
        nodes.index = nodes.index + 1
        nodes.index.name = "Node"
        st.dataframe(nodes, width="stretch", hide_index=False, height=560)

    with gate_tab:
        st.subheader("Evidence ledger and publication safeguards")
        st.write(
            "A public worked case is not treated as a substantive result merely because the data are large and available. The ledger separates an implemented, reproducible workflow from claims that require additional evidence."
        )
        st.dataframe(readiness_ledger(), width="stretch", hide_index=True, height=420)
        st.info(
            "The initial feasibility review will check nonresponse handling, response variation, network sparsity, bootstrap edge accuracy, case-drop centrality stability, and a pre-specified split/country replication sequence. If the network remains saturated or unstable, the app will retain the specification and report a transparent non-publication outcome rather than visualising an uninformative graph."
        )

    with code_tab:
        st.subheader("Local/Docker reproduction")
        st.write(
            "After downloading the official files locally, place them in the protected external-data location described below. The app’s Community Cloud deployment remains read-only for this case; full computation is available only locally or in the supplied Docker environment."
        )
        st.code(
            "Rscript --vanilla scripts/verify_ess_cronos3_source.R\n"
            "Rscript --vanilla scripts/validate_config.R --config config/ess_cronos3_sogreen_w6.yml\n"
            "Rscript --vanilla scripts/run_ess_cronos3_w6.R",
            language="bash",
        )
        st.download_button(
            "Download Wave 6 CAN configuration",
            data=CONFIG_PATH.read_bytes(),
            file_name="ess_cronos3_sogreen_w6.yml",
            mime="application/x-yaml",
        )
        st.caption(
            "The configuration records the expected Wave 6 SHA-256 checksum and recodes the documented 9/99 nonresponse values to missing before analysis."
        )
