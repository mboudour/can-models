#!/usr/bin/env python3
"""Build a case-study ledger for every Abadi et al. analytical element.

The script never infers that an unavailable ChatGPT attribute has been measured.
It creates static app assets after the full configured workflow has run.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "new_computations"
ASSETS = ROOT / "app" / "assets" / "chatgpt_case_study"
ASSETS.mkdir(parents=True, exist_ok=True)


def read_csv(relative: str) -> pd.DataFrame | None:
    path = OUT / relative
    try:
        return pd.read_csv(path) if path.exists() and path.stat().st_size else None
    except Exception:
        return None


def exists(relative: str) -> bool:
    return (OUT / relative).exists()


def status_from_file(relative: str) -> str:
    path = OUT / relative
    if not path.exists():
        return "No output artifact produced"
    text = path.read_text(encoding="utf-8", errors="replace").strip().replace("\n", " ")
    return text[:500] if text else "Status file is empty"


def evidence(relative: str) -> str:
    return relative if exists(relative) else "No artifact produced"


sample = read_csv("data_audit/sample_flow.csv")
summary_table = read_csv("networks/primary_mgm/network_summary.csv")
summary = summary_table.iloc[0] if summary_table is not None and len(summary_table) else None
centrality = read_csv("networks/primary_mgm/centrality.csv")
edges = read_csv("networks/primary_mgm/edge_table.csv")
cfa = read_csv("factor_models/satisfaction_q24_cfa_pooled.csv")
country_cfa = read_csv("factor_models/satisfaction_q24_cfa_country.csv")
invariance = read_csv("factor_models/satisfaction_q24_invariance.csv")
efa = read_csv("factor_models/satisfaction_q24_efa_country.csv")
country = read_csv("country_networks/eligible_countries.csv")
pairwise_nct = read_csv("country_networks/pairwise_nct_summary.csv")
adjacency = read_csv("country_networks/adjacency_matrix_correlations.csv")
clusters = read_csv("country_clustering/cluster_assignments.csv")
context = read_csv("contextual_associations/chi_square_cramers_v.csv")
runtime_deferred = exists("full_chatgpt_replication/status.md")
runtime_label = "Runtime deferred after >3-hour full configured run" if runtime_deferred else "Placeholder / diagnostic unavailable"

completed_country_n = int((country["status"] == "completed").sum()) if country is not None and "status" in country else 0
country_reason = (
    f"{completed_country_n} country networks completed."
    if completed_country_n else (runtime_label if runtime_deferred else status_from_file("country_networks/status.md"))
)
pairwise_state = "Completed" if pairwise_nct is not None and len(pairwise_nct) else (runtime_label if runtime_deferred else "Placeholder / no completed pairwise NCT output")
cluster_state = "Completed" if clusters is not None and len(clusters) else (runtime_label if runtime_deferred else "Placeholder / no completed clustering output")
context_state = "Completed" if context is not None and len(context) else (runtime_label if runtime_deferred else "Placeholder / no qualifying categorical-association output")

rows = [
    ("A01", "Design", "Two independent cross-sectional studies", "Not applicable", "One ChatGPT survey only", "No comparable second study or wave", "Not applicable", "No Study 1–Study 2 conclusion or NCT can be made."),
    ("A02", "Sample preparation", "Recoding, filters, exclusions, missing-data check", "Adapted and completed", "Prior-user filter Q13=1; ordinal audit; complete cases", "Completed", evidence("data_audit/sample_flow.csv"), "This is a dataset-specific preprocessing analogue, not Abadi’s participant selection."),
    ("A03", "Distribution", "Mardia multivariate normality", "Completed", "30 ChatGPT CAN nodes", "Completed", evidence("data_audit/mardia_multivariate_normality.csv"), "The diagnostic does not establish suitability for causal inference."),
    ("A04", "RQ1 joint network", "Joint MGM with LASSO and EBIC", "Adapted and completed", "30-node ChatGPT perception CAN", "Completed" if summary is not None else "Missing output", evidence("networks/primary_mgm/network_summary.csv"), "No populism/nativism/threat/conspiracy construct is present."),
    ("A05", "RQ1 network display", "Weighted undirected qgraph network", "Adapted and completed", "Primary ChatGPT MGM network", "Completed" if exists("networks/primary_mgm/edge_table.csv") else "Missing output", evidence("networks/primary_mgm/edge_table.csv"), "Edges are conditional associations, not directions or effects."),
    ("A06", "RQ1 centrality", "Strength centrality", "Adapted and completed", "Strength and expected influence for ChatGPT nodes", "Completed" if centrality is not None else "Missing output", evidence("networks/primary_mgm/centrality.csv"), "Centrality is not evidence that intervening on a node changes the network."),
    ("A07", "RQ1 predictability", "Node predictability", "Adapted and completed", "MGM node predictability", "Completed" if exists("networks/primary_mgm/predictability.csv") else "Missing output", evidence("networks/primary_mgm/predictability.csv"), "Predictability is descriptive in the cross-sectional graph."),
    ("A08", "RQ1 communities", "Walktrap and robust community analysis", "Adapted", "Walktrap/consensus workflow", "Completed" if exists("diagnostics/walktrap_communities.csv") else runtime_label, evidence("diagnostics/walktrap_communities.csv"), "Community labels are exploratory summaries, not confirmed latent factors."),
    ("A09", "RQ1 accuracy/stability", "Bootstrap edge accuracy and case-drop centrality stability", "Adapted", "Configured bootstrap diagnostic", "Completed" if exists("diagnostics/bootnet_diagnostics.rds") else runtime_label, evidence("diagnostics/bootnet_diagnostics.rds"), "If unavailable, no accuracy or stability conclusion is made."),
    ("A10", "RQ1 categorical audit", "Chi-square and Cramér’s V checks", "Adapted", "Configured contextual variables", context_state, evidence("contextual_associations/chi_square_cramers_v.csv"), "These checks audit categorical associations; they do not validate all network edges."),
    ("A11", "Across-study comparison", "NCT, global strength, edge invariance, adjacency correlation", "Not applicable", "No second comparable ChatGPT study", "Not applicable", "No second study", "A random split is only a diagnostic analogue and is not reported as an Abadi Study 1–Study 2 result."),
    ("A12", "RQ2 scale validation", "CFA of the PA scale", "Adapted", "CFA of Q24 ChatGPT satisfaction candidate scale", "Completed" if cfa is not None else "Missing output", evidence("factor_models/satisfaction_q24_cfa_pooled.csv"), "This is not a PA scale; a poor fit blocks factor-score subgroup claims."),
    ("A13", "RQ2 cross-country scale validation", "Country CFA and measurement invariance", "Adapted", "Q24 satisfaction candidate scale", "Completed" if country_cfa is not None else "Missing output", evidence("factor_models/satisfaction_q24_cfa_country.csv"), "This cannot establish cross-country equivalence for political attitudes."),
    ("A14", "RQ2 exploratory factor analysis", "Country-wise EFA after poor CFA fit", "Adapted", "Q24 satisfaction candidate scale", "Completed" if efa is not None else "Missing output", evidence("factor_models/satisfaction_q24_efa_country.csv"), "EFA is descriptive and does not rescue an unsupported substantive scale."),
    ("A15", "RQ2 high/low PA", "High-versus-low PA network comparison", "Not applicable", "No populist-attitude scale", "Not applicable", "No PA item set", "No high/low PA computation is performed or implied."),
    ("A16", "RQ2 country networks", "Country GGM, communities, and centrality", "Adapted", "Country-specific ChatGPT perception networks", "Completed" if completed_country_n >= 2 else runtime_label, evidence("country_networks/eligible_countries.csv"), "Country groups are global student samples, not Abadi’s matched representative European country samples."),
    ("A17", "RQ2 pairwise comparison", "Country adjacency-matrix correlations", "Adapted", "ChatGPT country network correlations", "Completed" if adjacency is not None and len(adjacency) else runtime_label, evidence("country_networks/adjacency_matrix_correlations.csv"), "Comparisons are descriptive and conditional on completed country networks."),
    ("A18", "RQ2 pairwise comparison", "All country-pair NCTs with multiplicity adjustment", "Adapted", "ChatGPT country network NCTs", pairwise_state, evidence("country_networks/pairwise_nct_summary.csv"), "Permutation count and sample adequacy must be inspected before any inferential use."),
    ("A19", "RQ2 country clustering", "k-means, hierarchical, PAM, CLARA; gap/WSS", "Adapted", "Clustering of completed ChatGPT country networks", cluster_state, evidence("country_clustering/cluster_assignments.csv"), "Any clusters summarize this dataset only and do not reproduce Abadi’s political-country clusters."),
    ("A20", "RQ2 pooled cluster networks", "Pooled networks by country cluster", "Adapted", "Pooled ChatGPT country-cluster networks", "Completed" if exists("country_clustering/cluster_assignments.csv") and exists("country_clustering/country_edge_matrix.csv") else runtime_label, evidence("country_clustering/country_edge_matrix.csv"), "Sparse categories or few groups can prevent estimation; status must be inspected."),
    ("A21", "RQ2 NetworkTree", "Country partition consistency check", "Conditional", "NetworkTree with configured moderators", "Completed" if exists("networktree/networktree_result.rds") else (runtime_label if runtime_deferred else status_from_file("networktree/status.txt")), evidence("networktree/status.txt"), "No result is fabricated if the optional package or data requirements are unavailable."),
    ("A22", "RQ3 nativism proxy", "Nativism scale CFA/invariance and high/low networks", "Not applicable", "No nativism construct measured", "Not applicable", "No nativism item set", "No ideological-proxy conclusion is possible."),
    ("A23", "RQ3 political orientation", "Left/centre/right coding and NetworkTree", "Not applicable", "No left-right political-spectrum variable", "Not applicable", "No political-orientation variable", "No left-versus-right conclusion is possible."),
    ("A24", "Separate analogue", "High/low group network comparison", "Adapted but not an Abadi RQ3 replication", "Median split of Q15 ChatGPT use frequency", "Completed" if exists("comparisons/use_frequency_median_split/group_definition.csv") else runtime_label, evidence("comparisons/use_frequency_median_split/group_definition.csv"), "Use-frequency results are kept separate from ideology or attitude-strength claims."),
    ("A25", "RQ4 country differences", "Separate country networks; communities and centrality", "Adapted", "Eligible ChatGPT-user country samples", country_reason, evidence("country_networks/eligible_countries.csv"), "No claim about Abadi’s countries, translations, or national politics is made."),
    ("A26", "RQ4 country similarity", "Country clustering and partition interpretation", "Adapted", "ChatGPT country-network similarity", cluster_state, evidence("country_clustering/cluster_assignments.csv"), "Conclusions are limited to observed sample-network similarity."),
    ("A27", "Paper conclusion", "Populism, nativism, threat, conspiracy, and political-country interpretations", "Not applicable", "Not measured in ChatGPT survey", "Not applicable", "No corresponding attributes", "The case study does not reproduce Abadi’s substantive political conclusions."),
    ("A28", "Case-study conclusion", "Interpret results within CAN theory", "Completed with bounded interpretation", "ChatGPT perceptions conditional-association network", "Completed" if summary is not None else "Missing output", evidence("case_study_conclusions.md"), "No directed causal, intervention, temporal, or policy-effect conclusion is made from this cross-sectional study."),
]
ledger = pd.DataFrame(rows, columns=["id", "paper_element", "Abadi_et_al_computation_or_claim", "literal_replication_status", "ChatGPT_treatment", "execution_status", "evidence", "required_disclaimer"])
ledger.to_csv(ASSETS / "abadi_full_replication_ledger.csv", index=False)

lines = [
    "# Bounded conclusions for the ChatGPT CAN case study",
    "",
    "## What was actually estimated",
]
if sample is not None and summary is not None:
    values = dict(zip(sample["statistic"], sample["value"]))
    lines += [
        f"The configured case study filtered the public survey to **{int(values.get('filtered_rows', 0)):,}** prior ChatGPT users and estimated the primary network on **{int(values.get('primary_network_rows', 0)):,}** complete cases across **{int(summary['p'])}** item-level nodes. The regularized mixed graphical model retained **{int(summary['nonzero_edges'])}** non-zero conditional associations.",
        "",
    ]
if centrality is not None and len(centrality):
    top = centrality.sort_values("Strength", ascending=False).head(5)
    lines += ["The five highest-strength nodes in this fitted graph were: " + "; ".join(f"{row.node} ({row.Strength:.2f})" for row in top.itertuples()) + ".", ""]
if edges is not None and len(edges):
    top_edges = edges.sort_values("abs_weight", ascending=False).head(5)
    lines += ["The five largest estimated conditional associations were: " + "; ".join(f"{row.from_}—{row.to} ({row.weight:.2f})" for row in top_edges.rename(columns={"from": "from_"}).itertuples()) + ".", ""]
if cfa is not None and len(cfa):
    row = cfa.iloc[0]
    lines += [
        "## Scale-validation implication",
        "",
        f"The configured one-factor Q24 satisfaction candidate scale converged but did **not** meet its pre-specified practical fit thresholds (CFI = {row['cfi']:.3f}; RMSEA = {row['rmsea']:.3f}; SRMR = {row['srmr']:.3f}). It is therefore not used as a validated latent attitude-strength scale for high-versus-low network claims.",
        "",
    ]
lines += [
    "## What cannot be concluded",
    "",
    "This case study cannot reproduce or test Abadi et al.’s conclusions about populist attitudes, nativism, symbolic or realistic threat, conspiracy mentality, political orientation, European political context, translations, or differences between two independent studies. Those attributes and that design are absent from the ChatGPT survey.",
    "",
    "The primary network is cross-sectional and undirected. Its edges are conditional associations, not verified directional causal effects. Centrality does not identify an intervention target, and country-pattern results—if completed—describe these observed student samples only.",
]
(ASSETS / "case_study_conclusions.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# Copy output tables that support the ledger whenever they exist.
for relative in [
    "data_audit/node_missingness.csv",
    "data_audit/node_level_diagnostics.csv",
    "diagnostics/walktrap_communities.csv",
    "diagnostics/bootstrap_community_coassignment.csv",
    "factor_models/satisfaction_q24_cfa_pooled.csv",
    "factor_models/satisfaction_q24_cfa_country.csv",
    "factor_models/satisfaction_q24_invariance.csv",
    "factor_models/satisfaction_q24_efa_pooled.csv",
    "factor_models/satisfaction_q24_efa_country.csv",
    "country_networks/eligible_countries.csv",
    "country_networks/adjacency_matrix_correlations.csv",
    "country_networks/pairwise_nct_summary.csv",
    "country_networks/pairwise_nct_edge_invariance.csv",
    "country_clustering/cluster_assignments.csv",
    "country_clustering/gap_statistic.csv",
    "country_clustering/within_sum_of_squares.csv",
    "contextual_associations/chi_square_cramers_v.csv",
]:
    source = OUT / relative
    if source.exists():
        shutil.copy2(source, ASSETS / source.name)

print(f"Wrote full replication ledger to {ASSETS}")
