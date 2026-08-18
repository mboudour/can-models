# Abadi et al. computation coverage and placeholder rules

This repository implements the full **computational repertoire** described in Abadi et al. while separating it from the original paper’s substantive content. The ChatGPT example and any participant dataset will not necessarily meet every design requirement. In those cases, `can-models` writes an explicit status or placeholder file rather than silently omitting a computation or treating a weak substitute as a replication.

| Abadi et al. computation | Repository implementation | Minimum conditions | Placeholder or adaptation policy |
|---|---|---|---|
| Data recoding, complete-case preparation, and multivariate normality diagnostic | `R/02_data.R` | Numeric mapped nodes and a defined analytic sample | Mardia is calculated on a deterministic, configurable subsample when full-sample cost is unsafe; the full dataset remains used for network estimation. |
| Joint mixed graphical network with LASSO/EBIC | `R/03_network.R` | At least three complete numeric nodes; at least two observations per response category | Returns an explicit sparse-category error for an infeasible node set. The app displays this as not eligible. |
| Strength centrality and edge/predictability exports | `R/03_network.R` | Successfully estimated core network | Not run until the core network exists. |
| Non-parametric edge accuracy and case-drop stability bootstrap | `R/04_diagnostics.R` | Eligible core network and sufficient computing time | Quick mode lowers iterations only for feasibility. Full mode is required for final inference. |
| Walktrap communities and robustness check | `R/04_diagnostics.R` | Eligible core network | Bootstrap consensus outputs a co-assignment matrix. |
| Robust CFA, country-wise CFA, EFA, and invariance | `R/05_factor.R` | A user-selected theoretical scale with at least three complete numeric items | The module reports non-convergence or insufficient data in its tables instead of making a scale claim. |
| Network Comparison Test (NCT) | `R/06_compare.R` | Two independent, comparable data partitions | The original two-study design is a placeholder for a one-study upload. A random split-sample check is explicitly labelled as a methodological analogue, not a second study. |
| High/low group networks and NCT | `R/07_country.R` | Numeric grouping variable that is excluded from the compared network | Uses a documented median split. Sparse categories or too-small groups create a `status.md` placeholder. |
| Country GGM networks, adjacency correlations, and all pairwise NCTs | `R/07_country.R` | At least two groups that meet the configured minimum group size | `eligible_countries.csv` records each group’s completed or placeholder status. |
| Country-network k-means, hierarchical, PAM, and CLARA clustering | `R/08_cluster.R` | At least two completed country networks | Gap statistic, WSS, and all clustering assignments are exported; unsupported gap output becomes `NA` rather than stopping the workflow. |
| Pooled country-cluster networks | `R/08_cluster.R` | A selected cluster with sufficient observations and estimable node categories | Per-cluster placeholder status is stored where sparse categories prevent estimation. |
| NetworkTree partitioning | `R/09_networktree.R` | Appropriate moderator variables and the optional R package | `networktree/status.txt` explicitly records package absence or unsupported moderators. |
| Chi-square and Cramér’s V contextual checks | `R/10_context.R` | At least two selected categorical variables | An empty output indicates that no qualifying variable pair was supplied. |

## General rules

The implementation distinguishes three states.

| State | Meaning |
|---|---|
| **Completed** | The computation ran and saved its data, figures, and/or R object. |
| **Not eligible** | The data structure, response coding, sample size, or design does not meet a prerequisite. The interface explains the missing condition before execution. |
| **Placeholder** | The computation is non-applicable or infeasible for the current data. A status file records the reason and no result is fabricated. |

> **Inference rule.** The CAN framework provides the substantive rationale for modelling connected attitude elements. The data in the example and the participant interface are cross-sectional. Consequently, undirected edges are conditional associations, not confirmed causal directions or effect sizes. [1] [2]

## References

[1] Dalege, J., Borsboom, D., van Harreveld, F., van den Berg, H., Conner, M., & van der Maas, H. L. J. (2016). *Toward a formalized account of attitudes: The Causal Attitude Network (CAN) model*. *Psychological Review, 123*(1), 2–22. [https://doi.org/10.1037/a0039802](https://doi.org/10.1037/a0039802)

[2] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the dots with Causal Attitude Network (CAN): A psychological network approach to populist attitudes, nativism, conspiracy mentality and threat appraisals*. *Measurement: Interdisciplinary Research and Perspectives, 23*(4), 393–417. [https://doi.org/10.1080/15366367.2024.2363718](https://doi.org/10.1080/15366367.2024.2363718)
