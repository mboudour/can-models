# Output catalogue

Every run writes an auditable record below `new_computations/` and figures below `figures/`. The files are generated rather than committed so that results can be regenerated after a change of data, configuration, or package version.

| Directory or file | Computational purpose | Corresponding Abadi et al. procedure |
|---|---|---|
| `run_metadata/provenance.json` | Source file checksum, time, sample sizes, seed | Reproducibility record |
| `run_metadata/configuration_snapshot.yml` | Exact node map and analytical options used in the run | Reproducible configuration |
| `data_audit/sample_flow.csv` | Raw, filtered, and complete-case sample size | Data preparation |
| `data_audit/node_missingness.csv` | Item-level missingness and number of observed response levels | Data-quality assessment |
| `data_audit/node_map.csv` | Source variables, labels, domains, and node type | Network operationalisation |
| `networks/primary_mgm/` | Adjacency matrix, edges, centrality, predictability, summary | Joint MGM, LASSO/EBIC, centrality |
| `figures/networks/primary_mgm_network.png` | Signed, weighted spring-layout network | qgraph visualisation |
| `factor_models/*_cfa_pooled.csv` | Robust-CFA fit statistics | CFA |
| `factor_models/*_cfa_country.csv` | Country-specific CFA fit statistics | Country-wise CFA |
| `factor_models/*_invariance.csv` | Configural, metric, and scalar multi-group fit statistics | Measurement-invariance assessment |
| `factor_models/*_efa_*.csv` | Polychoric EFA loadings | EFA after scale-fit assessment |
| `diagnostics/bootnet_diagnostics.rds` | Bootstrapped edge and case-drop results | Accuracy and stability bootstrap |
| `diagnostics/walktrap_communities.csv` | Primary Walktrap membership | Community detection |
| `diagnostics/bootstrap_community_coassignment.csv` | Bootstrap co-assignment proportions | Robustness check for communities |
| `comparisons/split_sample/` | Split-sample adjacency correlation and NCT | Two-network comparison analogue |
| `comparisons/use_frequency_median_split/` | High/low use grouping, matrix correlation, NCT | High/low attitude-group workflow analogue |
| `country_networks/eligible_countries.csv` | Groups passing configured sample-size threshold | Country-analysis eligibility |
| `country_networks/adjacency_matrix_correlations.csv` | All country-pair edge-matrix correlations | Country-network similarity |
| `country_networks/pairwise_nct_summary.csv` | NCT structure/global-strength/edge results with adjusted p-values | All pairwise country NCTs |
| `country_clustering/gap_statistic.csv` | k-means gap-statistic diagnostic | Country-network clustering |
| `country_clustering/within_sum_of_squares.csv` | Alternative WSS cluster-count diagnostic | Cluster robustness check |
| `country_clustering/cluster_assignments.csv` | k-means, hierarchical, PAM, and CLARA assignments | Multiple clustering algorithms |
| `country_clustering/country_clustering_workflow.rds` | Pooled cluster-network objects | Joint cluster-network estimation |
| `networktree/status.txt` | Completion status or reproducible package-availability note | NetworkTree partitioning |
| `contextual_associations/chi_square_cramers_v.csv` | Chi-square and Cramér’s V associations | Categorical-variable artifact checks |
| `full_analysis.rds` | All computational objects from one full run | Complete reproducibility object |

> **Interpretation rule.** The files describe conditional associations in cross-sectional data. They do not establish directionality or causal effects between attitude nodes.
