# Full Abadi et al. replication map for the ChatGPT CAN case study

This document converts **every reported analytical element** of Abadi et al. (2025) into an explicit status for the Ravšelj et al. ChatGPT survey. It distinguishes a literal substantive replication from an implemented computational analogue. The ChatGPT survey is a single, cross-sectional study of higher-education students’ early perceptions of ChatGPT; it is not a dataset on populism, nativism, threat, conspiracy mentality, or political orientation.

| Paper section or result | Abadi et al. computation or claim | ChatGPT data availability | Case-study treatment |
|---|---|---|---|
| Design and participants | Two independently collected representative European studies, including 15-country and 4-country samples | **Absent.** One cross-sectional convenience-oriented global student survey; no second wave/study | Explicit **not available** disclaimer; no Study 1–Study 2 substantive comparison is attempted |
| Data preparation | Recoding demographics, removing observations under stated study rules, missing-data check | **Available, adapted.** Prior-use filter `Q13 = 1`, ordinal coding audit, complete-case flow | Execute and display sample flow, missingness, coding, and data provenance |
| Distributional diagnostic | Mardia multivariate normality test | **Available** | Execute on deterministic 2,000-case diagnostic subsample and display result |
| RQ1: joint network | Joint mixed graphical model containing all relevant attitudes and demographics | **Available, adapted.** 30 ChatGPT item-level nodes spanning behaviour, capability beliefs, governance, risk, satisfaction, attitudes, outcomes, labour expectations, and affect | Execute MGM with LASSO/EBIC; display network, edge list, predictability, centrality, communities |
| RQ1: construct content | PA, nativism, realistic/symbolic threat, conspiracy mentality, demographics | **Absent substantively.** No corresponding political-attitude scales | Explicit **no corresponding attitude attribute** disclaimer; no populism conclusion |
| RQ1: centrality | Strength centrality and identification of central nodes | **Available** | Execute and display strength / expected influence for ChatGPT nodes |
| RQ1: community analysis | Walktrap communities plus robustness check | **Available** | Execute Walktrap and bootstrap co-assignment when supported; display membership and status |
| RQ1: categorical artifact checks | Chi-square tests and Cramér’s V after potentially strong categorical edges | **Partly available.** Country, study field, gender, and other context fields can be audited | Execute qualifying contextual association checks; state that these do not validate substantive CAN edges |
| Replication across studies | NCT, edge invariance, global strength, and adjacency correlation between Study 1 and Study 2 | **Absent.** No independent second study/wave with comparable nodes | Explicit **design unavailable** placeholder. A random split-sample check may be shown only as a diagnostic analogue |
| RQ2 scale validation | CFA of the PA scale, country-wise CFA, EFA after poor fit | **Available only for a different candidate scale.** `Q24a–Q24g` is configured as ChatGPT satisfaction | Execute robust CFA/EFA/invariance for Q24; label as satisfaction-scale validation, never as PA validation |
| RQ2 high versus low PA | Divide participants high/low on a validated PA scale and compare networks | **Absent.** No PA measure | Explicit **no PA scale** placeholder; do not substitute use frequency as an answer to RQ2 |
| RQ2 country networks | PA+nativism GGM, community/centrality plots, country edge correlations, all-pair NCTs | **Available, adapted.** Eight user-country groups meet the configured `n ≥ 500` threshold | Execute country-specific ChatGPT GGM workflow; label as country heterogeneity in LLM perceptions, not PA/nativism |
| RQ2 country clustering | k-means, hierarchical, PAM, CLARA, gap statistic, WSS, pooled cluster networks | **Conditionally available.** Depends on estimable country networks and at least two valid groups | Execute or record explicit sparse-category / convergence placeholder for each unavailable sub-step |
| RQ2 NetworkTree country partition | Test country partitions against clusters | **Conditional.** Requires package availability and supported moderator distribution | Execute if supported; otherwise show package/data status, not a silent omission |
| RQ3 left-right interpretation | Nativism as political-orientation proxy; country-wise CFA/invariance; high/low nativism networks and NCT | **Absent.** No nativism measure | Explicit **no nativism attribute** placeholder |
| RQ3 political spectrum | Political-left/centre/right coding and NetworkTree test | **Absent.** No left-right political orientation variable | Explicit **no political-orientation attribute** placeholder |
| RQ3 methodological analogue | High/low comparison | **Available only as a separate analogue.** `Q15` general ChatGPT-use frequency | Optional median-split use-frequency comparison, clearly separated from RQ3 and never presented as ideological comparison |
| RQ4 country networks | Separate full country networks, communities, centrality, adjacency correlations, NCT | **Available, adapted** for eligible ChatGPT-user country groups | Execute / display exact number of completed groups and ineligible-group reasons |
| RQ4 cluster conclusions | Identify country clusters, inspect differentiating edges, validate by NetworkTree | **Conditional and descriptive.** Country groups are global student samples, not matched European national samples | Execute where supported; conclusions limited to observed ChatGPT-sample network similarity |
| Discussion and conclusion | Explain substantive political-attitude mechanisms, country politics, translations, and intervention targets | **Absent substantively.** These mechanisms were not measured | Explicit prohibition on exporting Abadi’s political conclusions to ChatGPT perceptions |
| ChatGPT conclusions | State what the actual case-study outputs show | **Available within cross-sectional limits** | Report only executed ChatGPT results; interpret edges as conditional associations; no causal direction, intervention priority, or temporal process claim |

## Required interpretation rule

> The CAN model supplies a theory of interacting attitude elements. For this **cross-sectional** ChatGPT survey, all estimated network edges are undirected conditional associations. They are not demonstrated directional causal effects, nor do they establish that changing a central node will change the rest of the system.

## Sources

Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the dots with Causal Attitude Network (CAN): A psychological network approach to populist attitudes, nativism, conspiracy mentality and threat appraisals*. *Measurement: Interdisciplinary Research and Perspectives, 23*(4), 393–417. https://doi.org/10.1080/15366367.2024.2363718

Ravšelj, D., et al. (2025). *Higher education students’ perceptions of ChatGPT: Global survey data*, Version 2. Mendeley Data. https://doi.org/10.17632/ymg9nsn6kn.2
