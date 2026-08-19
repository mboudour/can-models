"""Completed ESS CRONOS-3 Wave 6 Green Transition CAN worked-case renderer.

The public page contains only non-row-level derived assets. Official ESS microdata
remain external to the repository and must be downloaded from the ESS Data Portal.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "ess_cronos3_sogreen_w6.yml"
ASSET_DIR = ROOT / "app" / "assets" / "ess_cronos3_green_transition_w6"
ESS_PORTAL_URL = "https://ess.sikt.no/en/series/a46bcac5-b030-444b-9280-441ec97e1bce"
SOGREEN_RELEASE_URL = "https://www.europeansocialsurvey.org/news/article/new-panel-survey-data-climate-change-now-available"
ESS_TERMS_URL = "https://www.europeansocialsurvey.org/contact/disclaimer"
WAVE6_DOI_URL = "https://doi.org/10.21338/cron3w6e01"


@st.cache_data
def read_asset_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(ASSET_DIR / name)


@st.cache_data
def read_nct_summary() -> dict[str, int]:
    return json.loads((ASSET_DIR / "country_nct_summary.json").read_text(encoding="utf-8"))


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
            ("RQ2: Bridge structure", "Do appraisal or policy-legitimacy elements bridge personal transition-cost concerns and green behaviour/engagement?"),
            ("RQ3: Cross-national heterogeneity", "How do the eleven country networks differ in structure, global strength, and bridge location?"),
            ("RQ4: Network types", "Do countries cluster into green-transition attitude architectures distinguished by the roles of legitimacy and household costs?"),
            ("RQ5: Measurement boundary", "Do the policy-legitimacy and personal-cost item families support scale probes, or should they remain distinct network elements?"),
        ],
        columns=["Research question", "Analysis"],
    )


def render_ess_cronos3_sogreen_case() -> None:
    gate = read_asset_csv("publication_gate_summary.csv").iloc[0]
    top_nodes = read_asset_csv("top_nodes.csv")
    top_edges = read_asset_csv("top_edges.csv")
    country_summaries = read_asset_csv("country_network_summaries.csv")
    clusters = read_asset_csv("country_cluster_assignments.csv")
    nct = read_nct_summary()

    st.header("ESS CRONOS-3 / SoGreen: Green Transition Attitude Network")
    st.write(
        "This is a **completed Abadi-style CAN worked case** using the verified official ESS CRONOS-3 Wave 6 SoGreen release. "
        "It maps a 21-node green-transition attitude system across eleven countries."
    )
    st.success(
        "**Completed results bundle.** The page presents pooled MGM results, factor probes, split-sample diagnostics, community structure, eleven country networks, pairwise network comparisons, and country clustering."
    )
    st.info(
        "**Interpretive boundary:** Wave 6 is analysed cross-sectionally. Edges are conditional associations, not verified directional, temporal, or causal effects."
    )

    metrics = st.columns(4)
    metrics[0].metric("Primary-network cases", f"{int(gate.pooled_n):,}")
    metrics[1].metric("Green-transition nodes", int(gate.pooled_nodes))
    metrics[2].metric("Non-zero pooled edges", int(gate.pooled_nonzero_edges))
    metrics[3].metric("Country networks", int(gate.completed_countries))

    overview_tab, network_tab, diagnostics_tab, country_tab, design_tab, code_tab = st.tabs(
        [
            "Results overview",
            "Pooled MGM",
            "Diagnostics and measurement",
            "Country networks",
            "Design and source",
            "Reproduce locally",
        ]
    )

    with overview_tab:
        st.subheader("What the completed analysis shows")
        st.write(
            "The pooled network connects environmental encounter, climate and extreme-weather worry, institutional legitimacy, household transition-cost concerns, and green engagement. "
            "Climate-change worry is the highest-strength node. The strongest direct connection is between the two policy-legitimacy elements: confidence that climate policies consider everyone’s views and confidence that policy outcomes are fair."
        )
        first, second = st.columns(2)
        first.metric("Pooled MGM density", f"{gate.pooled_density:.3f}")
        first.caption("147 of 210 possible undirected edges are non-zero; interpret smaller pooled edges cautiously.")
        second.metric("Split-sample adjacency correlation", f"{gate.split_adjacency_correlation:.3f}")
        second.caption("The two random halves show closely aligned edge patterns.")
        st.subheader("Top pooled nodes by strength")
        st.dataframe(top_nodes[["node", "Strength", "ExpectedInfluence"]], width="stretch", hide_index=True)
        st.subheader("Strongest pooled conditional associations")
        st.dataframe(top_edges[["from", "to", "weight", "sign"]].head(10), width="stretch", hide_index=True)

    with network_tab:
        st.subheader("Pooled 21-node mixed graphical model")
        st.image(
            ASSET_DIR / "pooled_network.png",
            caption="Node colours denote theory-led CAN components. Edge width reflects absolute estimated MGM weight; the display omits the smallest links for legibility.",
            width="stretch",
        )
        st.caption(
            "The graph is a visualisation of the primary MGM, not a causal path model. The table below gives the complete node-to-component legend."
        )
        st.dataframe(node_map(), width="stretch", hide_index=True, height=620)
        st.image(
            ASSET_DIR / "top_node_strength.png",
            caption="Strength is the sum of the absolute weights incident on each node in the pooled primary MGM.",
            width="stretch",
        )

    with diagnostics_tab:
        st.subheader("Abadi-style robustness and measurement checks")
        checks = pd.DataFrame(
            [
                ("Split-sample structure NCT", f"p = {gate.split_structure_invariance_p:.3f}", "No detected structural difference between random halves."),
                ("Split-sample global-strength NCT", f"p = {gate.split_global_strength_p:.3f}", "No detected overall-connectivity difference between random halves."),
                ("Centrality stability sensitivity", f"CS = {gate.centrality_stability_coefficient:.3f}", "Ordinal-GGM EBICglasso case-drop sensitivity; strong stability evidence."),
                ("Walktrap community structure", f"{int(gate.walktrap_communities)} communities", f"{int(gate.community_pairs_coassigned_80_or_more)} node pairs were coassigned in at least 80% of 50 MGM resamples."),
                ("Policy-legitimacy CFA probe", "Metric invariance retained; scalar not retained", "The 3-item probe is just-identified when pooled; do not compare latent means across countries."),
                ("Personal-cost CFA probe", "Metric invariance retained; scalar not retained", "The 3-item probe is just-identified when pooled; do not compare latent means across countries."),
            ],
            columns=["Check", "Result", "Interpretation"],
        )
        st.dataframe(checks, width="stretch", hide_index=True, height=320)
        st.warning(
            "The pooled primary MGM is relatively dense. Edge-accuracy and case-drop centrality results use a clearly labelled **ordinal-GGM EBICglasso sensitivity** (250 edge and 250 case-drop resamples); they support robustness assessment but do not replace the primary mixed graphical model."
        )

    with country_tab:
        st.subheader("Eleven country-specific MGMs")
        st.image(
            ASSET_DIR / "country_density.png",
            caption="Country-network density ranges from 0.071 to 0.248. The dashed line marks the pooled density.",
            width="stretch",
        )
        st.dataframe(country_summaries[["country", "n", "density", "global_strength", "nonzero_edges"]], width="stretch", hide_index=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Completed pairwise NCTs", nct["completed_pairs"])
        c2.metric("FDR structure differences", nct["fdr_structure_differences"])
        c3.metric("FDR global-strength differences", nct["fdr_global_strength_differences"])
        st.write(
            "Twenty-three of 55 country pairs show an FDR-adjusted structural difference, while none shows an FDR-adjusted global-strength difference. "
            "The cross-national result is therefore about differing configurations of associations rather than a country ranking by overall network connectivity."
        )
        st.subheader("Exploratory country-network clustering")
        st.dataframe(clusters, width="stretch", hide_index=True)
        st.caption(
            "Cluster labels are exploratory summaries of edge-matrix similarity; they are not country-level causal types or validated latent classes."
        )

    with design_tab:
        st.subheader("Research design and official source")
        st.write(
            "The analysis is modelled on Abadi et al.’s strategy of embedding a focal attitude family in a wider system of related appraisals, cognitions, and contextual elements. "
            "Here, the focal object is the green transition rather than a narrow climate-policy evaluation bundle."
        )
        st.dataframe(research_questions(), width="stretch", hide_index=True, height=310)
        st.markdown(
            f"The respondent-level source remains outside this repository. Obtain it from the [ESS CRONOS-3 Data Portal]({ESS_PORTAL_URL}), "
            f"consult the [Wave 6 SoGreen release]({SOGREEN_RELEASE_URL}), the [Wave 6 DOI]({WAVE6_DOI_URL}), and the [ESS conditions of use]({ESS_TERMS_URL})."
        )
        st.caption(
            "The public repository contains configuration, code, provenance metadata, and non-row-level derived outputs only. It does not redistribute ESS microdata or the codebook."
        )

    with code_tab:
        st.subheader("Reproduce the completed workflow locally or with Docker")
        st.code(
            "Rscript --vanilla scripts/verify_ess_cronos3_source.R\n"
            "Rscript --vanilla scripts/run_ess_cronos3_green_transition_results.R\n"
            "Rscript --vanilla scripts/run_ess_cronos3_green_transition_diagnostics.R\n"
            "Rscript --vanilla scripts/run_ess_cronos3_green_transition_country_nct.R\n"
            "Rscript --vanilla scripts/build_ess_streamlit_assets.R",
            language="bash",
        )
        st.write(
            "Put the official CSV and HTML codebook in the protected `data/external/ess_cronos3_sogreen/` folder. The source verifier checks the configured file fingerprint before any analysis."
        )
        st.download_button(
            "Download Green Transition CAN configuration",
            data=CONFIG_PATH.read_bytes(),
            file_name="ess_cronos3_sogreen_w6.yml",
            mime="application/x-yaml",
        )
