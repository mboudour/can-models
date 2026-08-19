# ESS CRONOS-3 / SoGreen Wave 6 Green Transition Attitude Network

## Scope

This is the project’s **second worked case**, separate from the genuine Abadi et al. Study 2 replication. It adapts the *logic* of Abadi et al.’s CAN workflow to the ESS CRONOS-3 Wave 6 SoGreen module: a focal attitude system is analysed together with its appraisals, contextual encounter, behavioural elements, and cross-national heterogeneity.[1]

The attitude object is the **green transition**. The project does not treat the initial narrow bundle of climate-policy evaluation items as the entire attitude system. That bundle produced a near-saturated private feasibility network and is not shown as a substantive result. The approved protocol instead represents environmental encounter, climate and extreme-weather appraisal, institutional legitimacy, perceived transition costs, and green behaviour/engagement.

## Official access and protected data

ESS recommends linking to its Data Portal rather than hosting ESS datasets externally, and its data are CC BY-NC-SA 4.0.[2] The repository and public Streamlit deployment therefore contain no respondent-level Wave 6 data or codebook copy.

| Item | Requirement |
|---|---|
| Official release | CRONOS-3 Wave 6, DOI [10.21338/cron3w6e01](https://doi.org/10.21338/cron3w6e01) |
| Portal | [ESS CRONOS-3 Data Portal](https://ess.sikt.no/en/series/a46bcac5-b030-444b-9280-441ec97e1bce) |
| Required local data file | `data/external/ess_cronos3_sogreen/CRON3w6e01.csv` |
| Required local codebook | `data/external/ess_cronos3_sogreen/CRON3w6e01 codebook.html` |
| Expected source SHA-256 | `0a3a647e1b530e33a0e542ce573e53aa4449fba49856af097bb1cdac15b3fe59` |
| Source verification | `Rscript --vanilla scripts/verify_ess_cronos3_source.R` |

All content in `data/external/` is ignored by Git, except the acquisition instructions in `data/external/README.md`. The folder is also excluded from Docker build contexts.

## Approved 21-node model

> **Green Transition Attitude Network:** the interconnected environmental encounters, appraisals, legitimacy evaluations, cost concerns, and behavioural/engagement elements through which citizens encounter and judge climate-oriented societal transition.

| CAN component | Wave 6 variables |
|---|---|
| Environmental encounter | `w6sgq2` local air-pollution concern; `w6seq1_1` flooding; `w6seq1_2` drought; `w6seq1_3` wildfire; `w6seq1_4` heavy storm; `w6seq1_5` extended extreme heat |
| Affective appraisal and responsibility | `w6sgq11` climate-change worry; `w6seq2` local extreme-weather worry; `w6sgq12` personal responsibility |
| Institutional capacity and policy legitimacy | `w6sgq13` government climate trust; `w6seq4` government preparedness; `w6sgq14` environment-versus-growth priority; `w6sgq15` policy familiarity; `w6sgq16` inclusive policy process; `w6sgq17` fair policy outcomes |
| Personal transition-cost concerns | `w6sgq21` energy-bill concern; `w6sgq22` transport-cost concern; `w6sgq23` job-loss concern |
| Green behaviour and engagement | `w6sgq6` public-transport use; `w6sgq9` energy-efficient appliance choice; `w6vq5_2` participation in an environmental-protection organisation |

The protocol converts documented `9` and `99` nonresponse values to missing. To make every country MGM estimable with the same coding, it applies the same adjacent-category collapse of the rare top category for `w6sgq16` and `w6sgq17` in every country. This is logged in the transformation audit and must be retained in sensitivity reporting.

## Abadi-style research questions

| Research question | Purpose |
|---|---|
| RQ1: Joint system | Estimate conditional associations connecting encounter, appraisal, legitimacy, personal cost, and behaviour in the pooled network. |
| RQ2: Bridge structure | Test whether appraisal or legitimacy items bridge cost concerns with green behaviour and civic engagement. |
| RQ3: Cross-national heterogeneity | Compare the same MGM specification in all eleven countries. |
| RQ4: Network types | Cluster country edge matrices and identify configurations distinguished by legitimacy versus cost connections. |
| RQ5: Measurement boundary | Use CFA/EFA to assess the policy-legitimacy and personal-cost item families without replacing network items with scores unless justified. |

## Analysis protocol

1. Verify the official data file and codebook against the recorded SHA-256 fingerprint.
2. Estimate the 21-node mixed graphical model (MGM) with LASSO/EBIC and report sample flow, category diagnostics, density, edge distribution, predictability, and ordinal-data caveats.[3]
3. Run CFA/EFA and, where eligible, country invariance diagnostics for the three-item policy-legitimacy and personal-cost families.
4. Run nonparametric edge bootstraps, case-drop centrality stability, and Walktrap/community-consensus diagnostics. No bridge or centrality result is substantively interpreted unless its stability is adequate.[4]
5. Conduct the pre-specified split-sample replication check.
6. Estimate the identically coded MGM in all eleven countries. The configuration sets `minimum_n: 400`, uses `network_estimator: mgm`, provides pairwise Network Comparison Tests with multiplicity adjustment, and exports country edge-matrix correlations.
7. Cluster country network edge matrices using the project’s multiple clustering procedures.
8. Treat any temporal panel extension as a separate future protocol. Wave 6 alone provides no temporal or within-person effects.

## Publication boundary

The public application displays **no substantive network output** until the following gate is met:

1. Source provenance and item coding have been verified.
2. The pooled network is non-trivial and not saturated or dominated by artefacts.
3. CFA/EFA, bootstrap edge accuracy, and case-drop centrality stability have been reviewed.
4. The split-sample and cross-country results are complete and interpretation is stable across the specified checks.
5. All claims preserve the conditional-association, cross-sectional-within-wave, and non-causal boundaries.

A failed gate is a reportable methodological result, not a reason to display an uninformative graph.

## Commands

Run from the repository root after the official data files are placed locally:

```bash
Rscript --vanilla scripts/verify_ess_cronos3_source.R
Rscript --vanilla scripts/validate_config.R --config config/ess_cronos3_sogreen_w6.yml
Rscript --vanilla scripts/run_ess_cronos3_w6.R
Rscript --vanilla scripts/run_ess_cronos3_green_transition_full.R
```

The final command is computationally intensive because it includes bootstraps, the country workflow, pairwise NCTs, and clustering.

## References

[1] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the dots with Causal Attitude Network (CAN): A psychological network approach to populist attitudes, nativism, conspiracy mentality and threat appraisals*. *Measurement: Interdisciplinary Research and Perspectives, 23*(4), 393–417. [https://doi.org/10.1080/15366367.2024.2363718](https://doi.org/10.1080/15366367.2024.2363718)

[2] European Social Survey. *Disclaimer and conditions of use*. https://www.europeansocialsurvey.org/contact/disclaimer

[3] Haslbeck, J. M. B., & Waldorp, L. J. (2020). *mgm: Estimating time-varying mixed graphical models in high-dimensional data*. *Journal of Statistical Software, 93*(8), 1–46. [https://doi.org/10.18637/jss.v093.i08](https://doi.org/10.18637/jss.v093.i08)

[4] Epskamp, S., Borsboom, D., & Fried, E. I. (2018). *Estimating psychological networks and their accuracy: A tutorial paper*. *Behavior Research Methods, 50*, 195–212. [https://doi.org/10.3758/s13428-017-0862-1](https://doi.org/10.3758/s13428-017-0862-1)
