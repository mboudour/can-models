"""Static public workspace for the genuine Abadi et al. Study 2 replication."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "app" / "assets" / "abadi_study2_public"
STUDY2_DATA_DIR = ROOT / "data" / "raw" / "abadi_study2_2020"


@st.cache_data(show_spinner=False)
def study2_table(filename: str) -> pd.DataFrame:
    return pd.read_csv(ASSET_DIR / filename)


def download_file(label: str, path: Path, filename: str, mime: str, key: str) -> None:
    st.download_button(label, data=path.read_bytes(), file_name=filename, mime=mime, key=key)


def replication_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Paper component": "Study 2 sample preparation",
                "Original-paper requirement": "Four-country April 2020 sample; exclude non-passing attention checks and gender=other respondents.",
                "Public-data status": "Executed",
                "Evidence / boundary": "The public CSV has 2,031 rows, all pass the recorded attention check, and one gender=other record is removed: analysed N = 2,030.",
            },
            {
                "Paper component": "RQ1: 29-node joint MGM",
                "Original-paper requirement": "MGM with LASSO and EBIC over demographics, threats, PA, nativism, and conspiracy mentality.",
                "Public-data status": "Executed",
                "Evidence / boundary": "The authors’ original 29 variables are mapped from the public Study 2 CSV and the 2,030-case joint MGM is bundled below.",
            },
            {
                "Paper component": "RQ1: Mardia diagnostic and categorical checks",
                "Original-paper requirement": "Assess multivariate normality and investigate categorical-variable artefacts.",
                "Public-data status": "Mardia executed; categorical artefact checks pending full workflow",
                "Evidence / boundary": "Mardia output is bundled. The categorical-association module remains an explicit pending Study 2 computation, not a null result.",
            },
            {
                "Paper component": "RQ1: centrality, predictability, bootstrap accuracy/stability, Walktrap communities",
                "Original-paper requirement": "Characterise the inferred joint network and assess robustness.",
                "Public-data status": "Centrality/predictability executed; bootstrap and consensus-community runs pending",
                "Evidence / boundary": "The full bootstrap/community sequence is implemented in the repository but is intentionally not claimed as completed until the high-cost offline run finishes.",
            },
            {
                "Paper component": "PA scale CFA, country CFA/invariance, and EFA",
                "Original-paper requirement": "Evaluate the seven-item populist-attitudes scale and use EFA when necessary.",
                "Public-data status": "Executed",
                "Evidence / boundary": "The pooled seven-item one-factor CFA fits poorly (CFI 0.595; RMSEA 0.186), so a unitary PA-score interpretation is not assumed. The EFA outputs are available for review.",
            },
            {
                "Paper component": "RQ2: high- versus low-PA networks",
                "Original-paper requirement": "Compare nativism, threat, and conspiracy networks among high- and low-PA respondents.",
                "Public-data status": "Data available; grouping rule requires appendix verification",
                "Evidence / boundary": "The public items are present, but the exact score/grouping procedure must be verified from the paper’s supplement before this is presented as a faithful replication.",
            },
            {
                "Paper component": "RQ3: left- versus right-wing PA networks",
                "Original-paper requirement": "Compare PA networks by political orientation.",
                "Public-data status": "Data available; Study 2 group-network/NCT run pending",
                "Evidence / boundary": "Original political orientation `A3.9` and all PA items are present. No result is displayed until the configured group-network and NCT computation has been run.",
            },
            {
                "Paper component": "RQ4: country networks, similarity, NCTs, clustering, NetworkTree",
                "Original-paper requirement": "Compare country-specific PA networks and identify cross-country structure.",
                "Public-data status": "Data available; four-country intensive workflow pending",
                "Evidence / boundary": "All four original country samples meet the configured minimum size. Country networks and pairwise comparisons remain pending computational output, not absent data.",
            },
            {
                "Paper component": "Study 1: August 2019 15-country analyses",
                "Original-paper requirement": "Reproduce the 15-country Study 1 network, country comparisons, and clustering.",
                "Public-data status": "Access-gated",
                "Evidence / boundary": "The paper’s data-availability statement restricts the Study 1 data under H2020 GDPR agreements. The access gate lists the material required for an authorized replication; it does not manufacture outputs.",
            },
            {
                "Paper component": "Cross-study NCT and two-study conclusions",
                "Original-paper requirement": "Compare Study 1 and Study 2 networks and draw two-study conclusions.",
                "Public-data status": "Access-gated",
                "Evidence / boundary": "A genuine two-study comparison is impossible until authorized Study 1 data and documentation are received and verified.",
            },
        ]
    )


def render_abadi_study2_replication() -> None:
    st.header("Abadi et al.: public Study 2 replication")
    st.write(
        "This workspace uses the authors’ **original public April 2020 four-country dataset**, not an unrelated application dataset. "
        "It is a transparent independent reimplementation of the published Study 2 workflow, while Study 1 and the cross-study analyses remain access-gated until the restricted 15-country data are authorized."
    )
    st.warning(
        "Interpretive boundary: the CAN model supplies a substantive theory of interacting attitude elements. These Study 2 data are cross-sectional; the empirical undirected edges are conditional associations, not verified directional causal effects."
    )

    flow = study2_table("sample_flow.csv").set_index("statistic")["value"]
    summary = study2_table("network_summary.csv").iloc[0]
    metrics = st.columns(4)
    metrics[0].metric("Public CSV records", f"{int(flow['raw_rows']):,}")
    metrics[1].metric("Analysed Study 2 cases", f"{int(flow['primary_network_rows']):,}")
    metrics[2].metric("Original network nodes", f"{int(summary['p'])}")
    metrics[3].metric("Original countries", "4")

    overview_tab, network_tab, scale_tab, ledger_tab, study1_tab, data_tab = st.tabs(
        [
            "Study 2 scope",
            "RQ1 joint network",
            "Scale checks and RQ2–RQ4",
            "Complete replication ledger",
            "Study 1 access gate",
            "Data and code",
        ]
    )

    with overview_tab:
        st.subheader("Why this is a genuine Study 2 replication")
        st.write(
            "The public source contains the original Qualtrics variables for country, gender, age, subjective social status, religion, education, realistic and symbolic threat, seven populist-attitude items, three nativism items, and five conspiracy-mentality items. The source codebook identifies reverse-coded items with an asterisk; those transformations and the reported exclusion are logged below."
        )
        st.dataframe(
            study2_table("transformation_audit.csv").rename(
                columns={
                    "variable": "Original variable",
                    "transformation": "Logged transformation",
                    "affected_n": "Affected cases",
                }
            ),
            width="stretch",
            hide_index=True,
        )
        st.caption(
            "The age category with one observation was merged with the adjacent oldest category for MGM eligibility. This explicit recode is not silently presented as a result from the publisher supplement, which remains blocked by the publisher CAPTCHA and should be checked when available."
        )
        node_map = study2_table("node_map.csv")
        node_map.index = node_map.index + 1
        node_map.index.name = "Node"
        st.dataframe(
            node_map.rename(
                columns={
                    "source_variable": "Original Study 2 variable",
                    "label": "Node label",
                    "domain": "CAN domain",
                    "node_type": "Response type",
                    "levels": "Response levels",
                }
            ),
            width="stretch",
            height=560,
        )

    with network_tab:
        st.subheader("RQ1: public Study 2 joint network")
        st.image(
            str(ASSET_DIR / "primary_mgm_network.png"),
            caption="29-node Study 2 MGM with LASSO/EBIC selection. Node numbers correspond to the Study 2 scope table; edge thickness reflects estimated conditional-association magnitude.",
            width="stretch",
        )
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Joint-network summary**")
            st.dataframe(
                pd.DataFrame([summary]).rename(
                    columns={
                        "estimator": "Estimator",
                        "n": "Complete cases",
                        "p": "Nodes",
                        "density": "Density",
                        "global_strength": "Global strength",
                        "nonzero_edges": "Non-zero edges",
                    }
                ),
                width="stretch",
                hide_index=True,
            )
            st.markdown("**Highest-strength nodes**")
            centrality = study2_table("centrality.csv").sort_values("Strength", ascending=False).head(12)
            st.dataframe(centrality, width="stretch", hide_index=True)
        with cols[1]:
            st.markdown("**Strongest estimated conditional associations**")
            edges = study2_table("edge_table.csv").sort_values("abs_weight", ascending=False).head(15)
            st.dataframe(edges[["from", "to", "weight", "sign"]], width="stretch", hide_index=True)
            st.markdown("**Predictability export**")
            predictability = study2_table("predictability.csv").sort_values("predictability", ascending=False).head(12)
            st.dataframe(predictability, width="stretch", hide_index=True)
        st.markdown("**Mardia multivariate-normality diagnostic**")
        st.dataframe(study2_table("mardia_multivariate_normality.csv"), width="stretch", hide_index=True)

    with scale_tab:
        st.subheader("Scale checks and the conditional RQ2–RQ4 branches")
        st.write(
            "The paper uses CFA/EFA before interpreting some subgroup branches. The public Study 2 implementation therefore displays those diagnostics before any high/low PA claim. A poor one-factor PA fit is evidence against silently turning seven items into an unqualified single score."
        )
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Seven-item populist-attitudes CFA**")
            st.dataframe(study2_table("populist_attitudes_study2_cfa_pooled.csv"), width="stretch", hide_index=True)
            st.markdown("**Country invariance sequence**")
            st.dataframe(study2_table("populist_attitudes_study2_invariance.csv"), width="stretch", hide_index=True)
        with cols[1]:
            st.markdown("**Three-item nativism CFA**")
            st.dataframe(study2_table("nativism_study2_cfa_pooled.csv"), width="stretch", hide_index=True)
            st.markdown("**Nativism country invariance sequence**")
            st.dataframe(study2_table("nativism_study2_invariance.csv"), width="stretch", hide_index=True)
        st.info(
            "The public data support RQ2–RQ4, but the high/low-PA grouping, political-orientation NCTs, country network/NCT runs, clustering, NetworkTree, and bootstrap sequence are deliberately shown as pending until their exact published decision rules are verified and their intensive computations finish. They are not omitted or interpreted as negative findings."
        )

    with ledger_tab:
        st.subheader("Complete Abadi et al. replication ledger")
        st.write(
            "Every major paper component is accounted for below. ‘Access-gated’ means the original Study 1 data are restricted; ‘pending’ means the original public Study 2 data exist but the result is not yet claimed as executed."
        )
        ledger = replication_ledger()
        st.dataframe(ledger, width="stretch", height=650, hide_index=True)
        st.download_button(
            "Download replication ledger",
            data=ledger.to_csv(index=False).encode("utf-8"),
            file_name="abadi_study2_replication_ledger.csv",
            mime="text/csv",
            key="download_study2_ledger",
        )
        download_file(
            "Download genuine-replication scope",
            ROOT / "docs" / "abadi_genuine_replication_scope.md",
            "abadi_genuine_replication_scope.md",
            "text/markdown",
            "download_study2_scope",
        )

    with study1_tab:
        st.subheader("Study 1: 15-country access gate")
        st.warning(
            "Study 1 is not bundled, inferred, or reconstructed from secondary sources. The authors’ data-availability statement places the 2019 15-country data under H2020 GDPR access restrictions."
        )
        st.write(
            "The genuine two-study ledger will be enabled only after an authorized de-identified Study 1 file, codebook, response coding, exclusions, questionnaire translations, and variable map have been received and verified against the article. A secure analysis environment or author-run checksum-verifiable script would also be acceptable if data transfer is not permitted."
        )
        st.markdown("**Materials required before the Study 1 module can be enabled**")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Required material": "De-identified analytic file", "Purpose": "Reconstruct the 15-country Study 1 network and comparison samples."},
                    {"Required material": "Codebook and response-value coding", "Purpose": "Map the original variables and preserve ordinal/categorical treatment."},
                    {"Required material": "Reverse coding, exclusions, and country identifiers", "Purpose": "Reproduce preprocessing and country-specific analysis branches."},
                    {"Required material": "Questionnaire translations and original variable map", "Purpose": "Audit cross-country measurement and published node selection."},
                    {"Required material": "Authorized execution arrangement, if applicable", "Purpose": "Support secure remote analysis or author-run reproducibility checks without public data transfer."},
                ]
            ),
            width="stretch",
            hide_index=True,
        )
        st.caption("No contact template or personal contact details are displayed in this application.")

    with data_tab:
        st.subheader("Original public Study 2 data and reproducibility files")
        st.write(
            "The data and Qualtrics codebook below are the authors’ public four-country Study 2 deposit. Cite the dataset record and companion data paper when reusing them. The Figshare API metadata names CC BY 4.0, while the repository description refers to CC BY-SA; check the current repository record before reuse or redistribution."
        )
        downloads = [
            ("Download original Study 2 CSV", STUDY2_DATA_DIR / "abadi_2023_four_country_study2.csv", "abadi_2023_four_country_study2.csv", "text/csv"),
            ("Download original Qualtrics codebook", STUDY2_DATA_DIR / "abadi_2023_qualtrics_codebook.pdf", "abadi_2023_qualtrics_codebook.pdf", "application/pdf"),
            ("Download Study 2 replication configuration", ROOT / "config" / "abadi_study2_public.yml", "abadi_study2_public.yml", "application/x-yaml"),
            ("Download joint-network edge table", ASSET_DIR / "edge_table.csv", "abadi_study2_primary_mgm_edges.csv", "text/csv"),
            ("Download joint-network centrality", ASSET_DIR / "centrality.csv", "abadi_study2_primary_mgm_centrality.csv", "text/csv"),
            ("Download Study 2 network image", ASSET_DIR / "primary_mgm_network.png", "abadi_study2_primary_mgm_network.png", "image/png"),
        ]
        columns = st.columns(2)
        for index, (label, path, filename, mime) in enumerate(downloads):
            with columns[index % 2]:
                download_file(label, path, filename, mime, f"study2_download_{index}")
        st.markdown(
            "**Sources:** [public Study 2 dataset](https://doi.org/10.21942/uva.17085719.v1); [Study 2 data paper](https://doi.org/10.5334/jopd.86); [Abadi et al. CAN paper](https://doi.org/10.1080/15366367.2024.2363718); and [Dalege et al. CAN model](https://doi.org/10.1037/a0039802)."
        )
