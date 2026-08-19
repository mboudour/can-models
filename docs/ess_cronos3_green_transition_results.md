# ESS CRONOS-3 Wave 6 Green Transition CAN Results

## Eligibility decision

The completed 21-node **Green Transition Attitude Network** is eligible for presentation as a full worked case in this repository and Streamlit application. It is no longer a results-pending protocol. The analysis uses the official ESS CRONOS-3 Wave 6 file verified against the recorded SHA-256 fingerprint and DOI.[1]

This decision means that the network has sufficient structural variation, reproducibility evidence, and cross-country differentiation to support an instructive Abadi-style CAN workflow. It does **not** guarantee acceptance by a journal. The evidence remains observational and Wave 6 is analysed as a cross-sectional attitude network: its edges are conditional associations, not verified directional or temporal causal effects.

| Publication-gate criterion | Completed result | Decision |
|---|---:|---|
| Pooled primary network | 7,841 complete cases; 21 nodes; 147 non-zero edges | Completed |
| Pooled network density | 0.700 | Retain with dense-network caution; not saturated |
| Split-sample edge-matrix correlation | 0.883 | Stable |
| Split-sample structure-invariance test | *p* = .175 | No detectable split-sample structural difference |
| Split-sample global-strength test | *p* = .506 | No detectable split-sample global-strength difference |
| Country networks | 11 of 11 eligible countries completed | Completed |
| Country-network density range | 0.071–0.248 | Meaningful country-level variation |
| Pairwise country NCTs | 55 of 55 completed | Completed |
| FDR-significant country structure differences | 23 of 55 | Cross-country structural heterogeneity retained |
| FDR-significant country global-strength differences | 0 of 55 | Overall connectivity is comparatively similar |
| Community structure | Four Walktrap communities; 97 node pairs coassigned in at least 80% of 50 resamples | Retained |
| Centrality stability | CS coefficient = 0.750 in an ordinal-GGM EBICglasso sensitivity | Strong sensitivity evidence |

## Principal pooled results

The strongest pooled nodes by strength are **climate-change worry**, **worry about local extreme weather**, the two policy-legitimacy nodes, household energy-bill concern, and trust in government to address climate change. The strongest edge is between the two policy-legitimacy nodes: confidence that policies consider everyone’s views and confidence that climate-policy outcomes are fair. The next strongest links connect household-cost concerns, climate worry with local air-pollution concern, climate worry with personal responsibility, and climate worry with local extreme-weather worry.

The system is substantively interpretable because it is not merely a redundant policy-evaluation bundle. It connects environmental encounter/appraisal, institutional legitimacy, personal transition costs, and behavioural engagement. The Walktrap result supplies four empirical communities; it should not be treated as a confirmed factor structure.

## Factor and country checks

The two three-item CFA probes are just-identified at the pooled level and therefore do not provide a meaningful global fit test. They are included as descriptive construct checks, not as proof that the full network is a latent-factor model. Across countries, metric invariance is acceptable for both the policy-legitimacy and personal-transition-cost probes, whereas scalar invariance is not supported. The application therefore does not compare latent means across countries.

All eleven country MGM networks were estimated successfully. Pairwise NCT results identify structural differences after FDR adjustment in 23 of 55 country pairs, but no FDR-adjusted difference in global strength. The scientific interpretation is therefore about **differences in the configuration of conditional associations**, not about a simple ranking of countries as more or less connected.

## Diagnostic interpretation

The primary MGM remains relatively dense (0.700), so small pooled edges must not be over-interpreted. The primary network is the estimand. The 250-resample edge-accuracy and case-drop centrality outputs use an **ordinal-GGM EBICglasso sensitivity**, explicitly labelled as such, because directly bootstrapping the 21-node MGM is computationally infeasible within the public reproducibility environment. This sensitivity does not replace the primary MGM; it assesses whether the principal adjacency and centrality conclusions are robust to an ordinal-GGM representation.

## Reproducible workflow

The public repository contains the configuration, checksum verifier, staged results runner, diagnostics runner, pairwise NCT runner, and non-row-level derived assets. The official respondent-level data remain outside version control and must be downloaded from the ESS source by each analyst.[1]

[1]: https://doi.org/10.21338/cron3w6e01 "ESS CRONOS-3 Wave 6 data"
