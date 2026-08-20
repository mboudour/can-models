"""Pew American Trends Panel Wave 152 AI attitude-network pathway.

The public app intentionally does not bundle Pew respondent-level microdata. It
presents the official source, questionnaire-derived mapping, and pre-specified
feasibility gate until an authorised user obtains the official file through
Pew's account-based dataset access flow.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "config" / "pew_atp_w152_ai_attitudes_manifest.yml"
PEW_DATASET_URL = "https://www.pewresearch.org/dataset/american-trends-panel-wave-152/"
PEW_REPORT_URL = "https://www.pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts-view-artificial-intelligence/"
PEW_METHODS_URL = "https://www.pewresearch.org/internet/2025/04/03/us-public-and-ai-experts-methodology/"
PEW_QUESTIONNAIRE_URL = "https://www.pewresearch.org/wp-content/uploads/sites/20/2025/03/pi_2025.04.03_us-public-and-ai-experts_questionnaire.pdf"
PEW_TOPLINE_URL = "https://www.pewresearch.org/wp-content/uploads/sites/20/2025/03/pi_2025.04.03_us-public-and-ai-experts_topline.pdf"
PEW_TERMS_URL = "https://www.pewresearch.org/about/terms-and-conditions/"


@st.cache_data(show_spinner=False)
def manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def planned_nodes_table(source: dict) -> pd.DataFrame:
    nodes = pd.DataFrame(source["network"]["planned_nodes"])
    nodes.index = nodes.index + 1
    nodes.index.name = "Node"
    return nodes.rename(
        columns={
            "questionnaire_id": "Questionnaire item",
            "label": "Planned node label",
            "domain": "CAN domain",
            "universe": "Respondent universe",
        }
    )


def analysis_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Analysis component": "Official source, questionnaire, topline, and methodology",
                "Abadi-style counterpart": "Original Study 2 data provenance and variable mapping",
                "Status": "Public documentation collected",
                "Evidence / boundary": "Official Wave 152 landing page, final questionnaire, topline, report, and methodology are identified. The app does not redistribute Pew microdata.",
            },
            {
                "Analysis component": "RQ1: planned pooled AI Attitude MGM",
                "Abadi-style counterpart": "RQ1: joint Study 2 MGM",
                "Status": "Pre-specified; not executed",
                "Evidence / boundary": "A 15-node all-respondent mapping covers exposure, personal orientation, societal consequences, AI capability/future risk, and governance. Exact exported names and response distributions require the official downloaded dataset.",
            },
            {
                "Analysis component": "Data audit, missingness, and response-category checks",
                "Abadi-style counterpart": "Study 2 sample preparation",
                "Status": "Blocked by official microdata access",
                "Evidence / boundary": "The public questionnaire documents 98/99 nonresponse coding, but file-level frequencies and form/routing verification cannot be inferred from the questionnaire alone.",
            },
            {
                "Analysis component": "Centrality, edge accuracy, case-drop stability, and communities",
                "Abadi-style counterpart": "RQ1 network characterisation and robustness",
                "Status": "Not executed",
                "Evidence / boundary": "Enabled only after the primary MGM passes the pre-specified density, distribution, and complete-case gate.",
            },
            {
                "Analysis component": "Factor probes and split-sample reproducibility",
                "Abadi-style counterpart": "Scale checks and methodological comparison",
                "Status": "Not executed",
                "Evidence / boundary": "Candidate latent families must be chosen after inspecting the official item distributions; a split is a reproducibility check, not a second study or causal comparison.",
            },
            {
                "Analysis component": "Temporal or multi-wave AI comparison",
                "Abadi-style counterpart": "Two-study comparison",
                "Status": "Not pre-specified",
                "Evidence / boundary": "Waves 99, 119, and 152 use different AI instruments. A cross-wave analysis requires a separately verified item-overlap map and harmonisation plan.",
            },
        ]
    )


def render_pew_atp_w152_ai_case() -> None:
    source = manifest()
    project = source["project"]
    input_info = source["input"]
    gate = source["feasibility_gate"]

    st.header("Pew American Trends Panel Wave 152: AI Attitude Network")
    st.write(
        "This is a **separate U.S. public-opinion CAN pathway**, not an Abadi replication and not an ESS result. "
        "Wave 152 is selected because its official 2024 questionnaire contains a coherent AI-attitude system spanning AI exposure, orientation, anticipated consequences, capability/risk, and governance."
    )
    st.warning(
        "Results are intentionally not displayed. Official Pew respondent-level microdata require an email-verified Pew Research Center account and acceptance of its Terms of Use. "
        "The dataset has not been downloaded into this repository or Streamlit, and no substantive network will be shown until an authorised local copy passes the documented feasibility gate."
    )

    metrics = st.columns(4)
    metrics[0].metric("Selected source", "ATP Wave 152")
    metrics[1].metric("Field dates", "12–18 Aug. 2024")
    metrics[2].metric("Pre-specified nodes", len(source["network"]["planned_nodes"]))
    metrics[3].metric("Public result status", "Not yet eligible")

    scope_tab, rq1_tab, ledger_tab, data_tab = st.tabs(
        ["Pew scope", "Proposed RQ1 network", "Complete analysis ledger", "Data access and code"]
    )

    with scope_tab:
        st.subheader("Why Wave 152 is the selected Pew AI source")
        st.write(
            "The official Wave 152 questionnaire was fielded on the U.S. American Trends Panel in August 2024. "
            "It asks all respondents about awareness and everyday interaction with AI, excitement versus concern, perceived control, expected personal and national impacts, jobs, trust in AI capability, future risks and benefits, regulation, and confidence in government and companies."
        )
        st.markdown(
            f"**Official sources:** [Wave 152 dataset page]({PEW_DATASET_URL}); [Pew report]({PEW_REPORT_URL}); "
            f"[methodology]({PEW_METHODS_URL}); [final questionnaire]({PEW_QUESTIONNAIRE_URL}); and [topline]({PEW_TOPLINE_URL})."
        )
        st.markdown("**Public-source handling**")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Resource": "Respondent-level microdata", "Status": "Account-gated official download", "Repository/app treatment": "Never bundled or redistributed"},
                    {"Resource": "Questionnaire and topline", "Status": "Public official documents", "Repository/app treatment": "Linked for audit and item verification"},
                    {"Resource": "Configuration manifest", "Status": "Public reproducibility file", "Repository/app treatment": "Downloadable below"},
                ]
            ),
            width="stretch",
            hide_index=True,
        )
        st.caption(
            "The planned analysis is a cross-sectional network of between-person conditional associations. It will not use the word causal to claim verified directional, temporal, or intervention effects."
        )

    with rq1_tab:
        st.subheader("Proposed RQ1: How is the U.S. AI attitude system conditionally organised?")
        st.write(
            "The mapping avoids routed chatbot-use items and form-specific impact batteries in the first network. It therefore begins with 15 questionnaire items asked of all Wave 152 respondents, reducing avoidable complete-case loss and avoiding a hidden estimand change caused by form assignment."
        )
        st.dataframe(planned_nodes_table(source), width="stretch", height=590)
        st.markdown("**Publication and feasibility gate**")
        st.dataframe(
            pd.DataFrame({"Required check": gate["required_checks"]}),
            width="stretch",
            hide_index=True,
        )
        st.info(
            "This is a theory-led candidate map, not a result. Exact file variable names, coding direction, response distributions, and complete-case coverage are verified only after the official file is downloaded through Pew's authorised process."
        )

    with ledger_tab:
        st.subheader("Complete Pew AI analysis ledger")
        ledger = analysis_ledger()
        st.dataframe(ledger, width="stretch", height=520, hide_index=True)
        st.download_button(
            "Download Pew AI analysis ledger",
            data=ledger.to_csv(index=False).encode("utf-8"),
            file_name="pew_atp_w152_ai_analysis_ledger.csv",
            mime="text/csv",
            key="download_pew_ai_ledger",
        )

    with data_tab:
        st.subheader("Official Pew data access and local reproducibility")
        st.write(
            "The official dataset page requires a Pew Research Center account. The correct workflow is to obtain the file through that page, record its filename and SHA-256, and place it only in the protected local folder shown below. The file must not be committed, uploaded to the public app, or shared through this repository."
        )
        st.code(input_info["protected_local_folder"], language="text")
        st.markdown(
            f"Create or log into an account at the [official Wave 152 data page]({PEW_DATASET_URL}) and accept the [Pew Terms of Use]({PEW_TERMS_URL}). "
            "After the official download, use the included manifest as the questionnaire-derived mapping record and verify its exact exported variable names before any R analysis."
        )
        st.download_button(
            "Download Wave 152 AI mapping manifest",
            data=MANIFEST_PATH.read_bytes(),
            file_name="pew_atp_w152_ai_attitudes_manifest.yml",
            mime="application/x-yaml",
            key="download_pew_ai_manifest",
        )
        st.caption(
            "The direct implementation remains deliberately inactive until the official source file is accessible. This avoids fabricating a network, treating public toplines as respondent-level data, or bypassing Pew's account and terms requirements."
        )
