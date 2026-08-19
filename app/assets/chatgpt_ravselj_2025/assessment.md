# Assessment of the Initial ChatGPT CAN Run

## Scope of the completed run

The run analysed respondents who reported having used ChatGPT (`Q13 = 1`). It retained **16,010** users from **23,218** submitted records and estimated the 31-node model on **12,009 complete cases**, excluding **4,001 users (25.0%)** through complete-case analysis. The nodes covered use, capability/reliability beliefs, governance and risk appraisal, personal/evaluative appraisal, expected educational outcomes, and affect.

The model was estimated as an ordinal mixed graphical model (MGM) with LASSO/EBIC selection. In a cross-sectional CAN-informed analysis, the resulting undirected edges are conditional associations, not verified directional causal effects.[1][2]

## What the output shows

The run completed technically after the response-level and node-label repair. Its strongest positive conditional associations are concentrated in closely related item pairs: information satisfaction–accuracy (`Q24f`–`Q24g`), information efficiency–reliability (`Q19d`–`Q19e`), satisfaction with assistance–information quality (`Q24e`–`Q24f`), expected study efficiency–motivation (`Q26e`–`Q26f`), and perceived cheating–inaccurate-information risks (`Q22b`–`Q22e`). The factor subset `Q24e`, `Q24f`, and `Q24g` has high standardized loadings (.716, .950, and .792), but its one-factor CFA has zero degrees of freedom and therefore provides no test of model fit.

## Critical diagnostic finding

The reported primary network is **fully connected**: all **465 of 465 possible edges** are non-zero (density = 1.00). Its smallest absolute edge is .0348 and its median is .1316. This is not a sparse, visually or substantively interpretable network. It also invalidates a simple “most central node” story: in a fully connected graph, strength and expected-influence rankings are dominated by the general density and by near-redundant item blocks.

The saved figure confirms the problem. It uses generic numeric node labels and one domain colour because the original BYOD configuration contained blank labels and did not retain the intended domain settings. The source code now normalizes empty labels, but that does not turn this particular dense output into a publication-ready substantive result.

## What cannot be claimed from this run

The present output does not support a claim that a particular belief, emotion, or use behaviour **causes** another. It does not establish within-person processes, temporal ordering, intervention targets, or a replication of Abadi et al.’s political-attitude findings. It also does not include edge-accuracy bootstraps, case-drop centrality stability, a preregistered sensitivity analysis, country network comparisons, or an independent replication. The remaining 25.0% complete-case exclusion needs a missing-data sensitivity analysis.

## Publication-readiness judgment

> **No: the current 31-node output is not publishable as a stand-alone substantive CAN result.**

The underlying data and research question may support a publishable paper, but only after a redesigned and transparent analysis plan. The most promising contribution is a **cross-sectional network study of higher-education students’ ChatGPT perceptions**, not a direct Abadi et al. replication. The paper should present the current fully dense network as a diagnostic/sensitivity result, not as the primary finding.

A defensible manuscript would need: (1) a theory-led, smaller primary node set that avoids redundant near-parallel items; (2) clear descriptive labels and attitude domains; (3) an a priori EBIC-penalty/sensitivity plan rather than a post-hoc edge threshold; (4) bootstrap accuracy and centrality-stability diagnostics; (5) a stated missing-data strategy and complete-case sensitivity; (6) a country-comparison plan limited to sufficiently sized, conceptually comparable groups; and (7) either a holdout/independent replication or an explicit exploratory designation. Any CAN language should remain theory-led and should not be turned into directional causal claims from this single cross-sectional survey.[1][3][4]

## Recommended role in `can-models`

The ChatGPT survey should become the project’s **second worked example**, clearly marked as a non-Abadi application. It should include a source-cited, labelled configuration; the completed 31-node run as a technical diagnostic; a revised, pre-specified focused-network workflow; and a methods page that contrasts what is reusable from Abadi et al. with what is not supported by the Ravšelj et al. design.

## References

[1] Dalege, J., Borsboom, D., van Harreveld, F., van den Berg, H., Conner, M., & van der Maas, H. L. J. (2016). *Toward a formalized account of attitudes: The Causal Attitude Network (CAN) model*. Psychological Review. https://doi.org/10.1037/a0039802

[2] Ravšelj, D., et al. (2025). *Higher education students’ perceptions of ChatGPT: A global study of early reactions*. PLOS ONE. https://doi.org/10.1371/journal.pone.0315011

[3] Epskamp, S., Borsboom, D., & Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. *Behavior Research Methods, 50*, 195–212. https://doi.org/10.3758/s13428-017-0862-1

[4] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the Dots with Causal Attitude Network (CAN): A Psychological Network Approach to Populist Attitudes, Nativism, Conspiracy Mentality and Threat Appraisals*. https://doi.org/10.1080/15366367.2024.2363718
