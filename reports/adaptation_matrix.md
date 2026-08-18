# Abadi et al. computational replication: adaptation matrix

This project reproduces the **computations** of Abadi et al. as a reusable workflow. It does not claim to replicate their substantive findings, because the ChatGPT study has a different attitude object, instruments, sampling frame, and data structure.

| Original Abadi et al. element | ChatGPT example implementation | Interpretation |
|---|---|---|
| Two cross-sectional survey studies, analysed jointly and compared using NCT | One cross-sectional global survey; a random split-sample comparison is run as a methodological verification of the two-network comparison code | The split comparison is not a substitute for a second survey wave or independent study. |
| Populist-attitude, nativism, threat, conspiracy, and demographic nodes | Thirty ChatGPT perception nodes covering behaviour, capability, regulation, risk, satisfaction, educational outcomes, labour-market beliefs, and affect | The network is an attitude system towards ChatGPT in higher education. |
| Mixed graphical model with LASSO/EBIC | Same estimator family for the pooled item-level ordinal network | Edges are conditional associations. |
| Strength centrality, bootstrapping, Walktrap communities | Same statistics and diagnostics | Centrality is a structural description, not an intervention effect. |
| CFA/EFA of political scales and country measurement comparisons | Robust CFA/EFA and invariance checks of a configured ChatGPT satisfaction/attitude candidate scale | The factor analysis decides whether any scale-based group procedure is defensible. |
| High/low populist-attitude networks | Conditional factor-score group module plus a clearly labelled median-split use-frequency example | No factor-score group is claimed if CFA does not support the scale. |
| Left/right populist-attitude analysis | Generic NetworkTree moderation procedure using country, field, and usage variables if the optional package is available | There is no direct left/right political analogue in the example data. |
| Country networks and all pairwise NCT comparisons | Country-specific Spearman GGM networks for eligible ChatGPT-user samples, all-pair matrix correlations, and all-pair NCTs | Country comparisons are descriptive and require measurement caution. |
| Clustering country edge matrices | k-means, hierarchical, PAM, and CLARA clustering, with gap statistic and WSS diagnostics | Country clusters describe network similarity, not substantive cultural types. |
| NetworkTree confirmation of country partitions | Optional package-backed module with a transparent status file | The module is not silently omitted when the package is unavailable. |

## Cross-sectional limitation

The CAN model is a substantive theory in which evaluative reactions may be causally linked. The available ChatGPT data are cross-sectional and the estimated networks are undirected. Accordingly, all project outputs use the terms **conditional association**, **network structure**, and **comparison**; they do not claim verified directionality or causal effects. A future multi-wave panel or experiment is required to test temporal or causal hypotheses.

## References

[1] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the dots with Causal Attitude Network (CAN): A psychological network approach to populist attitudes, nativism, conspiracy mentality and threat appraisals*. *Measurement: Interdisciplinary Research and Perspectives, 23*(4), 393–417. [https://doi.org/10.1080/15366367.2024.2363718](https://doi.org/10.1080/15366367.2024.2363718)

[2] Dalege, J., Borsboom, D., van Harreveld, F., van den Berg, H., Conner, M., & van der Maas, H. L. J. (2016). *Toward a formalized account of attitudes: The Causal Attitude Network (CAN) model*. *Psychological Review, 123*(1), 2–22. [https://doi.org/10.1037/a0039802](https://doi.org/10.1037/a0039802)

[3] Ravšelj, D., Aristovnik, A., Keržič, D., Tomaževič, N., Umek, L., Brezovar, N., et al. (2025). *Higher Education Students’ Early Perceptions of ChatGPT: Global Survey Data* (Version 2). Mendeley Data. [https://doi.org/10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2)
