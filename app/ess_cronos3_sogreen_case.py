"""ESS CRONOS-3 Wave 6 Green Transition CAN worked-case renderer.

This presentation intentionally follows the visible analysis sequence used in the
Abadi Study 2 replication workspace. Only non-row-level derived outputs are
bundled; official ESS respondent-level files remain external to the repository.
"""

from __future__ import annotations

from pathlib import Path

import json
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "ess_cronos3_sogreen_w6.yml"
ASSET_DIR = ROOT / "app" / "assets" / "ess_cronos3_green_transition_w6"
ESS_PORTAL_URL = "https://ess.sikt.no/en/series/a46bcac5-b030-444b-9280-441ec97e1bce"
SOGREEN_RELEASE_URL = "https://www.europeansocialsurvey.org/news/article/new-panel-survey-data-climate-change-now-available"
ESS_TERMS_URL = "https://www.europeansocialsurvey.org/contact/disclaimer"
WAVE6_DOI_URL = "https://doi.org/10.21338/cron3w6e01"


@st.cache_data(show_spinner=False)
def ess_table(filename: str) -> pd.DataFrame:
    return pd.read_csv(ASSET_DIR / filename)


@st.cache_data(show_spinner=False)
def ess_nct_summary() -> dict[str, int]:
    return json.loads((ASSET_DIR / "country_nct_summary.json").read_text(encoding="utf-8"))


def download_file(label: str, filename: str, mime: str, key: str) -> None:
    path = ASSET_DIR / filename
    st.download_button(label, data=path.read_bytes(), file_name=filename, mime=mime, key=key)


def analysis_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Analysis component": "ESS source preparation and provenance",
                "Abadi-style counterpart": "Study 2 sample preparation and original-variable mapping",
                "Status": "Executed",
                "Evidence / boundary": "The official Wave 6 CSV and codebook were verified locally against the configured SHA-256 fingerprint; the app bundles no respondent-level ESS data.",
            },
            {
                "Analysis component": "RQ1: 21-node pooled Green Transition MGM",
                "Abadi-style counterpart": "RQ1: joint Study 2 MGM",
                "Status": "Executed",
                "Evidence / boundary": "7,841 complete cases; 21 theory-led nodes; 147 non-zero conditional associations. The pooled network is dense (0.700), so smaller edges require caution.",
            },
            {
                "Analysis component": "RQ1: Mardia, centrality, edge accuracy/stability, and Walktrap communities",
                "Abadi-style counterpart": "RQ1: network characterisation and robustness",
                "Status": "Executed with labelled sensitivity",
                "Evidence / boundary": "Mardia, Walktrap, and community resampling are bundled. Edge accuracy and case-drop stability use an explicitly labelled ordinal-GGM EBICglasso sensitivity, not a replacement for the primary MGM.",
            },
            {
                "Analysis component": "Policy-legitimacy and personal-cost CFA/EFA probes",
                "Abadi-style counterpart": "PA and nativism scale checks",
                "Status": "Executed",
                "Evidence / boundary": "Both are three-item, just-identified pooled CFA probes. Metric invariance is retained; scalar invariance is not retained, so latent means are not compared across countries.",
            },
            {
                "Analysis component": "RQ2: bridge and centrality structure",
                "Abadi-style counterpart": "RQ2: subgroup network interpretation",
                "Status": "Executed",
                "Evidence / boundary": "The page displays node strength, strongest associations, and four Walktrap communities. These are conditional-association descriptors, not intervention targets.",
            },
            {
                "Analysis component": "RQ3: random split-sample reproducibility",
                "Abadi-style counterpart": "Methodological comparison check",
                "Status": "Executed",
                "Evidence / boundary": "Split-sample edge-matrix correlation is 0.883; NCT structure p = .175 and global-strength p = .506. This is not a second study or a temporal test.",
            },
            {
                "Analysis component": "RQ4: eleven country MGM networks",
                "Abadi-style counterpart": "RQ4: country networks",
                "Status": "Executed",
                "Evidence / boundary": "All eleven eligible country networks were estimated with the same node map and documented category treatment.",
            },
            {
                "Analysis component": "RQ4: pairwise country NCTs",
                "Abadi-style counterpart": "RQ4: country network-comparison tests",
                "Status": "Executed",
                "Evidence / boundary": "All 55 country-pair NCTs completed. Twenty-three show FDR-adjusted structural differences; none shows an FDR-adjusted global-strength difference.",
            },
            {
                "Analysis component": "RQ4: country edge-matrix clustering",
                "Abadi-style counterpart": "RQ4: country-network clustering",
                "Status": "Executed; exploratory",
                "Evidence / boundary": "Country edge matrices were clustered as exploratory summaries, not validated latent country types.",
            },
            {
                "Analysis component": "Temporal panel extension",
                "Abadi-style counterpart": "New extension beyond the single-wave analysis",
                "Status": "Not executed",
                "Evidence / boundary": "Wave 6 is analysed as a cross-sectional between-person network. A temporal or within-person model requires verified item overlap in later waves and a separate pre-specified design.",
            },
        ]
    )


def render_ess_cronos3_sogreen_case() -> None:
    flow = ess_table("sample_flow.csv").set_index("statistic")["value"]
    summary = ess_table("network_summary.csv").iloc[0]
    diagnostics = ess_table("publication_gate_diagnostic_summary.csv").iloc[0]
    nct = ess_nct_summary()

    st.header("ESS CRONOS-3 / SoGreen: Green Transition Attitude Network")
    st.write(
        "This workspace is the **completed ESS counterpart** to the Abadi Study 2 replication. "
        "It applies the same CAN workflow sequence—scope and sample preparation, RQ1 joint network, scale checks, reproducibility diagnostics, country networks, NCTs, clustering, and a complete ledger—to a 21-node green-transition attitude system."
    )
    st.warning(
        "Interpretive boundary: although CRONOS-3 is a panel, the displayed Wave 6 network is cross-sectional. Its undirected edges are conditional associations, not verified directional, temporal, or causal effects."
    )

    metrics = st.columns(4)
    metrics[0].metric("Official Wave 6 records", f"{int(flow['raw_rows']):,}")
    metrics[1].metric("Analysed ESS cases", f"{int(flow['primary_network_rows']):,}")
    metrics[2].metric("Green Transition nodes", int(summary["p"]))
    metrics[3].metric("Original countries", "11")

    scope_tab, network_tab, scale_tab, ledger_tab, country_tab, data_tab = st.tabs(
        [
            "ESS scope",
            "RQ1 joint network",
            "Scale checks and RQ2–RQ4",
            "Complete analysis ledger",
            "Country networks, NCTs, and clustering",
            "Data and code",
        ]
    )

    with scope_tab:
        st.subheader("Why this is a genuine ESS CAN worked case")
        st.write(
            "The official Wave 6 SoGreen release contains a coherent green-transition attitude system: environmental encounter, climate and extreme-weather appraisal, institutional capacity and policy legitimacy, perceived household costs, and green behaviour/engagement. "
            "The redesigned system intentionally replaces the initial narrow policy-evaluation bundle, which was close to saturated in private feasibility work."
        )
        st.markdown("**Sample preparation and logged transformations**")
        st.dataframe(ess_table("sample_flow.csv"), width="stretch", hide_index=True)
        st.dataframe(
            ess_table("transformation_audit.csv").rename(
                columns={"variable": "Original Wave 6 variable", "transformation": "Logged transformation", "affected_n": "Affected cases"}
            ),
            width="stretch",
            hide_index=True,
        )
        st.caption(
            "Documented 9/99 nonresponse values are converted to missing. A uniform adjacent-category collapse is applied to the rare top category of the two policy-legitimacy items in every country, so country MGM coding is not adapted post hoc."
        )
        st.markdown("**Approved 21-node mapping**")
        nodes = ess_table("node_map.csv").rename(
            columns={"source_variable": "Original Wave 6 variable", "label": "Node label", "domain": "CAN domain", "node_type": "Response type", "levels": "Response levels"}
        )
        nodes.index = nodes.index + 1
        nodes.index.name = "Node"
        st.dataframe(nodes, width="stretch", height=620)

    with network_tab:
        st.subheader("RQ1: pooled 21-node Green Transition MGM")
        st.image(
            ASSET_DIR / "pooled_network.png",
            caption="21-node Wave 6 MGM with LASSO/EBIC selection. Node colours correspond to the ESS scope table; edge thickness reflects estimated conditional-association magnitude. The smallest edges are hidden only for display legibility.",
            width="stretch",
        )
        columns = st.columns(2)
        with columns[0]:
            st.markdown("**Joint-network summary**")
            st.dataframe(
                pd.DataFrame([summary]).rename(
                    columns={"estimator": "Estimator", "n": "Complete cases", "p": "Nodes", "density": "Density", "global_strength": "Global strength", "nonzero_edges": "Non-zero edges"}
                ),
                width="stretch",
                hide_index=True,
            )
            st.markdown("**Highest-strength nodes**")
            st.dataframe(ess_table("centrality.csv").sort_values("Strength", ascending=False).head(12), width="stretch", hide_index=True)
        with columns[1]:
            st.markdown("**Strongest estimated conditional associations**")
            edges = ess_table("edge_table.csv").sort_values("abs_weight", ascending=False).head(15)
            st.dataframe(edges[["from", "to", "weight", "sign"]], width="stretch", hide_index=True)
            st.markdown("**Predictability export**")
            st.dataframe(ess_table("predictability.csv").sort_values("predictability", ascending=False).head(12), width="stretch", hide_index=True)
        st.markdown("**Mardia multivariate-normality diagnostic**")
        st.dataframe(ess_table("mardia_multivariate_normality.csv"), width="stretch", hide_index=True)

    with scale_tab:
        st.subheader("Scale checks, RQ2 bridge structure, and RQ3 reproducibility")
        st.write(
            "As in the Study 2 workspace, factor checks are shown before any scale-level interpretation. The two ESS scale families are retained as item-level network elements; their three-item pooled CFAs are just-identified and therefore do not supply a meaningful global fit test."
        )
        columns = st.columns(2)
        with columns[0]:
            st.markdown("**Policy-legitimacy CFA probe**")
            st.dataframe(ess_table("policy_legitimacy_cfa_pooled.csv"), width="stretch", hide_index=True)
            st.markdown("**Country invariance sequence**")
            st.dataframe(ess_table("policy_legitimacy_invariance.csv"), width="stretch", hide_index=True)
            st.markdown("**Pooled EFA loadings**")
            st.dataframe(ess_table("policy_legitimacy_efa_pooled.csv"), width="stretch", hide_index=True)
        with columns[1]:
            st.markdown("**Personal-transition-cost CFA probe**")
            st.dataframe(ess_table("personal_transition_cost_cfa_pooled.csv"), width="stretch", hide_index=True)
            st.markdown("**Country invariance sequence**")
            st.dataframe(ess_table("personal_transition_cost_invariance.csv"), width="stretch", hide_index=True)
            st.markdown("**Pooled EFA loadings**")
            st.dataframe(ess_table("personal_transition_cost_efa_pooled.csv"), width="stretch", hide_index=True)
        st.markdown("**RQ2: community and centrality-stability evidence**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Walktrap communities", int(diagnostics["walktrap_communities"]))
        c2.metric("Centrality stability (CS)", f"{diagnostics['centrality_stability_coefficient']:.3f}")
        c3.metric("Community pairs ≥ 80%", int(diagnostics["community_coassignment_pairs"]))
        st.caption("The CS coefficient comes from an explicitly labelled ordinal-GGM EBICglasso case-drop sensitivity; it assesses robustness without replacing the primary MGM.")
        st.markdown("**RQ3: split-sample methodological check**")
        st.dataframe(ess_table("adjacency_correlation.csv"), width="stretch", hide_index=True)
        st.dataframe(ess_table("nct_summary.csv"), width="stretch", hide_index=True)
        st.info(
            "The split is a methodological reproducibility check, not a second study, longitudinal comparison, or causal test. The split-sample edge-matrix correlation is 0.883."
        )

    with ledger_tab:
        st.subheader("Complete ESS Abadi-style analysis ledger")
        st.write(
            "Every completed and non-completed branch of this adapted CAN study is logged below. The completed country workflow is an ESS-specific analogue to the paper’s country-comparison branch; it is not claimed to be a direct replication of Study 1 or Study 2 substantive results."
        )
        ledger = analysis_ledger()
        st.dataframe(ledger, width="stretch", height=650, hide_index=True)
        st.download_button(
            "Download ESS analysis ledger",
            data=ledger.to_csv(index=False).encode("utf-8"),
            file_name="ess_cronos3_green_transition_analysis_ledger.csv",
            mime="text/csv",
            key="download_ess_ledger",
        )
        st.download_button(
            "Download ESS results and interpretation note",
            data=(ROOT / "docs" / "ess_cronos3_green_transition_results.md").read_bytes(),
            file_name="ess_cronos3_green_transition_results.md",
            mime="text/markdown",
            key="download_ess_results_note",
        )

    with country_tab:
        st.subheader("RQ4: eleven country networks, pairwise NCTs, and clustering")
        st.image(
            ASSET_DIR / "country_density.png",
            caption="Country MGM density ranges from 0.071 to 0.248. The dashed line marks the pooled-network density; it is not a country-level benchmark or a causal quantity.",
            width="stretch",
        )
        st.markdown("**Completed country MGM networks**")
        st.dataframe(ess_table("country_network_summaries.csv"), width="stretch", hide_index=True)
        nct = ess_nct_summary()
        c1, c2, c3 = st.columns(3)
        c1.metric("Completed pairwise NCTs", nct["completed_pairs"])
        c2.metric("FDR structure differences", nct["fdr_structure_differences"])
        c3.metric("FDR global-strength differences", nct["fdr_global_strength_differences"])
        st.write(
            "The completed 55-pair NCT schedule finds FDR-adjusted differences in network structure for 23 country pairs and none in global strength. This supports a configuration-based, rather than country-ranking, interpretation."
        )
        st.dataframe(ess_table("pairwise_nct_summary.csv"), width="stretch", hide_index=True, height=360)
        st.markdown("**Exploratory country edge-matrix clustering**")
        st.dataframe(ess_table("country_cluster_assignments.csv"), width="stretch", hide_index=True)
        st.caption("Country clusters are exploratory edge-matrix summaries. They are not validated latent country types and do not establish causal explanations for cross-country differences.")

    with data_tab:
        st.subheader("Official ESS data, non-row-level results, and reproduction files")
        st.write(
            "The official respondent-level CSV and HTML codebook are not downloadable here. The ESS conditions recommend portal linking rather than redistribution. The public workspace instead offers the configuration and non-row-level derived tables needed to audit the displayed results."
        )
        st.markdown(
            f"**Sources:** [ESS CRONOS-3 Data Portal]({ESS_PORTAL_URL}); [Wave 6 SoGreen release]({SOGREEN_RELEASE_URL}); [Wave 6 DOI]({WAVE6_DOI_URL}); and [ESS conditions of use]({ESS_TERMS_URL})."
        )
        downloads = [
            ("Download Green Transition configuration", CONFIG_PATH, "ess_cronos3_sogreen_w6.yml", "application/x-yaml"),
            ("Download primary MGM edge table", ASSET_DIR / "edge_table.csv", "ess_cronos3_green_transition_edges.csv", "text/csv"),
            ("Download primary MGM centrality", ASSET_DIR / "centrality.csv", "ess_cronos3_green_transition_centrality.csv", "text/csv"),
            ("Download primary MGM predictability", ASSET_DIR / "predictability.csv", "ess_cronos3_green_transition_predictability.csv", "text/csv"),
            ("Download country NCT summary", ASSET_DIR / "pairwise_nct_summary.csv", "ess_cronos3_country_nct_summary.csv", "text/csv"),
            ("Download pooled network image", ASSET_DIR / "pooled_network.png", "ess_cronos3_green_transition_mgm.png", "image/png"),
        ]
        columns = st.columns(2)
        for index, (label, path, filename, mime) in enumerate(downloads):
            with columns[index % 2]:
                st.download_button(label, data=path.read_bytes(), file_name=filename, mime=mime, key=f"ess_download_{index}")
        st.markdown("**Local staged reproduction**")
        st.code(
            "Rscript --vanilla scripts/verify_ess_cronos3_source.R\n"
            "Rscript --vanilla scripts/run_ess_cronos3_green_transition_results.R\n"
            "Rscript --vanilla scripts/run_ess_cronos3_green_transition_diagnostics.R\n"
            "Rscript --vanilla scripts/run_ess_cronos3_green_transition_country_nct.R\n"
            "Rscript --vanilla scripts/build_ess_streamlit_assets.R",
            language="bash",
        )
