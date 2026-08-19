"""Source-cited ESS CRONOS-3 Wave 6 Green Transition Attitude Network renderer.

This public view contains the approved research protocol and no respondent-level
ESS data or substantive network result until the publication gate is satisfied.
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
            ("w6sgq2", "Local air-pollution concern", "Environmental encounter"),
            ("w6seq1_1", "Experienced severe flooding", "Environmental encounter"),
            ("w6seq1_2", "Experienced drought", "Environmental encounter"),
            ("w6seq1_3", "Experienced wildfire", "Environmental encounter"),
            ("w6seq1_4", "Experienced heavy storm", "Environmental encounter"),
            ("w6seq1_5", "Experienced extended extreme heat", "Environmental encounter"),
            ("w6sgq11", "Climate-change worry", "Affective appraisal and responsibility"),
            ("w6seq2", "Worry about local extreme weather", "Affective appraisal and responsibility"),
            ("w6sgq12", "Personal responsibility to reduce climate change", "Affective appraisal and responsibility"),
            ("w6sgq13", "Trust in government to address climate change", "Institutional capacity and policy legitimacy"),
            ("w6seq4", "Government preparedness for extreme weather", "Institutional capacity and policy legitimacy"),
            ("w6sgq14", "Environment versus economic-growth priority", "Institutional capacity and policy legitimacy"),
            ("w6sgq15", "Familiarity with national climate policies", "Institutional capacity and policy legitimacy"),
            ("w6sgq16", "Confidence policies consider everyone views", "Institutional capacity and policy legitimacy"),
            ("w6sgq17", "Confidence in fair climate-policy outcomes", "Institutional capacity and policy legitimacy"),
            ("w6sgq21", "Concern about ability to pay energy bills", "Personal transition-cost concerns"),
            ("w6sgq22", "Concern about increased transport costs", "Personal transition-cost concerns"),
            ("w6sgq23", "Concern about future job loss", "Personal transition-cost concerns"),
            ("w6sgq6", "Public-transport use", "Green behaviour and engagement"),
            ("w6sgq9", "Energy-efficient appliance choice", "Green behaviour and engagement"),
            ("w6vq5_2", "Participated in an environmental-protection organisation", "Green behaviour and engagement"),
        ],
        columns=["Official Wave 6 variable", "Approved node label", "CAN component"],
    )


def research_questions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("RQ1: Joint system", "Which conditional associations connect environmental encounter, affective appraisal, legitimacy, personal costs, and green behaviour?"),
            ("RQ2: Bridge structure", "Do exposure/worry or policy-legitimacy elements bridge personal transition-cost concerns and green behaviour/engagement?"),
            ("RQ3: Cross-national heterogeneity", "How do the eleven country networks differ in structure, global strength, and bridge location?"),
            ("RQ4: Network types", "Do countries cluster into green-transition attitude architectures distinguished by the role of legitimacy versus household costs?"),
            ("RQ5: Measurement boundary", "Do the policy-legitimacy and personal-cost item families support scale models, or should they remain distinct network elements?"),
        ],
        columns=["Research question", "Protocol"],
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
                "Component": "21-node Green Transition Attitude Network",
                "Status": "Approved specification",
                "Boundary": "The design broadens the attitude object beyond a saturated policy-evaluation bundle to environmental encounter, appraisal, legitimacy, costs, and behaviour.",
            },
            {
                "Component": "Pooled Wave 6 MGM and measurement diagnostics",
                "Status": "Configured; results pending publication gate",
                "Boundary": "No graph, centrality, community, bridge, or intervention claim is displayed until robustness and measurement checks are complete.",
            },
            {
                "Component": "Eleven-country MGM, NCT, and clustering workflow",
                "Status": "Configured; results pending",
                "Boundary": "Country models use the same node map and a uniform documented category treatment. Pairwise inference requires multiplicity control and substantive review.",
            },
            {
                "Component": "Split-sample reproducibility check",
                "Status": "Configured; results pending",
                "Boundary": "It is a methodological replication check, not a longitudinal or causal comparison.",
            },
            {
                "Component": "Temporal panel extension",
                "Status": "Deferred",
                "Boundary": "It requires documented item overlap in later released waves and a pre-specified longitudinal model; Wave 6 alone does not establish temporal direction.",
            },
        ]
    )


def render_ess_cronos3_sogreen_case() -> None:
    st.header("ESS CRONOS-3 / SoGreen: Green Transition Attitude Network")
    st.write(
        "This is a **source-cited, locally reproducible second worked case** using the official ESS CRONOS-3 Wave 6 SoGreen release. "
        "It applies the Causal Attitude Network framework to citizens’ green-transition attitude systems across eleven countries."
    )
    st.warning(
        "**Results pending a publication gate.** The approved protocol has 21 theory-led nodes, but the app will not display a network, centrality ranking, country typology, community structure, or intervention claim until the pre-specified robustness, measurement, and cross-country checks are complete."
    )

    metrics = st.columns(4)
    metrics[0].metric("Wave 6 records", "9,585")
    metrics[1].metric("CRONOS-3 countries", "11")
    metrics[2].metric("Approved CAN nodes", "21")
    metrics[3].metric("Public analysis state", "Results pending")

    access_tab, questions_tab, nodes_tab, gate_tab, code_tab = st.tabs(
        ["Official data and design", "Abadi-style research questions", "Approved node map", "Publication gate", "Code and local reproduction"]
    )

    with access_tab:
        st.subheader("Official access; no external microdata hosting")
        st.write(
            "CRONOS-3 is a cross-national probability-based, mixed-mode panel linked to the main ESS. "
            "The Green Transition Attitude Network treats environmental encounter, climate/extreme-weather appraisal, governmental capacity and legitimacy, perceived personal costs, and green behaviour as interacting components of one attitude system."
        )
        st.markdown(
            f"Download the official file and documentation from the [ESS CRONOS-3 Data Portal]({ESS_PORTAL_URL}). "
            f"Read the [Wave 6 SoGreen release]({SOGREEN_RELEASE_URL}) and the [ESS conditions of use]({ESS_TERMS_URL}) before reuse."
        )
        st.info(
            "The ESS recommends linking to its Data Portal instead of placing its datasets on external websites. The repository therefore stores neither the Wave 6 CSV nor the codebook."
        )
        st.write(
            "The initial analysis is a **between-person Wave 6 network**. Although CRONOS-3 is a panel, undirected Wave 6 edges are conditional associations; they do not establish within-person change, temporal direction, or verified causal effects."
        )

    with questions_tab:
        st.subheader("A cross-national CAN study analogous to Abadi et al.")
        st.write(
            "As Abadi et al. situated populist attitudes among threat appraisals, related cognitions, and context, this protocol situates green-transition evaluations among direct environmental encounter, affective appraisal, institutional legitimacy, personal costs, and behaviour."
        )
        st.dataframe(research_questions(), width="stretch", hide_index=True, height=340)

    with nodes_tab:
        st.subheader("Approved 21-node Green Transition Attitude Network")
        st.write(
            "The node set is theory-led. It is not a reduced version of the earlier saturated policy-evaluation bundle: behavioural and experiential components are intentionally included so that the attitude object is the green transition, rather than policy evaluation alone."
        )
        nodes = node_map()
        nodes.index = nodes.index + 1
        nodes.index.name = "Node"
        st.dataframe(nodes, width="stretch", hide_index=False, height=700)
        st.caption(
            "The configuration recodes documented 9/99 nonresponse values to missing. It applies the same adjacent-category collapse to the rare top category of the two policy-legitimacy items in every country, rather than adapting coding country by country."
        )

    with gate_tab:
        st.subheader("Evidence ledger and publication safeguards")
        st.write(
            "The original narrow 15-node policy-evaluation feasibility network was close to saturated and is not displayed. The redesigned system is configured for a fresh, transparent analysis; it is not presented as a finished result."
        )
        st.dataframe(readiness_ledger(), width="stretch", hide_index=True, height=510)
        st.info(
            "Publication requires: item-level response and missing-data checks; a non-trivial, non-saturated pooled MGM; CFA/EFA diagnostics for policy legitimacy and personal cost; bootstrap edge accuracy and case-drop centrality stability; split-sample reproducibility; and country-network/NCT/clustering review. If these checks fail, the app will report the outcome without visualising an uninformative graph."
        )

    with code_tab:
        st.subheader("Local/Docker reproduction")
        st.write(
            "After downloading the official files locally, place them in the protected external-data location described below. The Community Cloud deployment remains read-only for this case; the full R analysis is intentionally available only locally or in the supplied Docker environment."
        )
        st.code(
            "Rscript --vanilla scripts/verify_ess_cronos3_source.R\n"
            "Rscript --vanilla scripts/validate_config.R --config config/ess_cronos3_sogreen_w6.yml\n"
            "Rscript --vanilla scripts/run_ess_cronos3_w6.R\n"
            "Rscript --vanilla scripts/run_ess_cronos3_green_transition_full.R",
            language="bash",
        )
        st.download_button(
            "Download Green Transition CAN configuration",
            data=CONFIG_PATH.read_bytes(),
            file_name="ess_cronos3_sogreen_w6.yml",
            mime="application/x-yaml",
        )
        st.caption(
            "The full workflow includes a source check, 21-node MGM, factor diagnostics, bootstrap/community diagnostics, split-sample comparison, eleven-country MGM workflow, NCT, and country-network clustering."
        )
