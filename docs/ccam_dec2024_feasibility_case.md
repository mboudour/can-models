# CCAM December 2024 Climate-Engagement CAN Feasibility Case

## Status and scope

This is the third public `can-models` case. It is a **transparent feasibility case**, not a completed substantive or publication-ready CAN worked case. It applies the same source-provenance, theory-led item-selection, ordinal MGM, factor-probe, and specification-sensitivity logic as the completed cases and then reports why the result fails the project’s non-saturation gate.

The source is the December 2024 (Wave 31) cross-sectional release from *Climate Change in the American Mind: National Survey Data on Public Opinion (2008–2024)*, curated by the Yale Program on Climate Change Communication and George Mason University Center for Climate Change Communication.[1] The public archive has DOI [`10.17605/OSF.IO/JW79P`](https://doi.org/10.17605/OSF.IO/JW79P).

> **Interpretive boundary.** The displayed network estimates undirected conditional associations in a single cross-sectional survey wave. It does not establish temporal order, directional causal effects, within-person dynamics, or intervention effects. The word *causal* in CAN refers to a theory of attitude-element interaction, not an empirical causal claim from this design.

## Data access and redistribution boundary

The official CCAM archive is publicly downloadable from its [OSF project](https://osf.io/jw79p/), but its Terms of Use prohibit redistribution or transfer of respondent-level data. The repository, Docker image, and Streamlit application therefore contain no respondent-level CCAM records. They contain only a reproducible YAML configuration, non-row-level derived outputs, source checksum, implementation code, and the feasibility assessment.

The verified official SPSS source fingerprint is:

```text
db6c0d5f0f8acea6591ed4a803a85be1491aa4b0a02239b74792a636997477eb
```

To reproduce locally, place the official archive in `data/external/ccam_2008_2024/` and retain its original filename, `CCAM SPSS Data 2008-2024.sav`. That directory is excluded from Git and Docker build context.

| Stage | Result |
|---|---|
| Official archive and codebook audit | Completed; Wave 31 is December 2024. |
| Source verification | Completed; expected SHA-256 matched locally. |
| Sample extraction | 1,013 December 2024 records; 995 primary-network complete cases. |
| Primary network | 15-node ordinal MGM; 102 of 105 possible edges; density 0.971. |
| Measurement probes | Completed for anticipated climate harm and climate transition-policy support. |
| Non-saturation sensitivities | Completed; no tested theory-led specification met the gate. |
| Bootstrap, centrality stability, cross-wave replication, and public substantive interpretation | Deliberately not run after saturated-network gate failure. |

## Pre-specified node system

The primary system combined four conceptually distinct families: climate belief and attribution; affective and anticipated risk; climate policy and transition support; and climate communication/attention. The 15 official variables are fully documented in `config/ccam_dec2024_climate_engagement.yml` and in the app’s scope tab. The documented CCAM code `-1` was recoded as missing before complete-case estimation.

This theory-led breadth was intentional. It tested whether a bridge network could be formed across belief, risk, policy, and communication rather than estimating a narrow redundant scale.

## Feasibility result and gate decision

The primary ordinal MGM was nearly complete: **102 of 105 possible conditional associations** remained non-zero after LASSO/EBIC selection (density **0.971**). Increasing the EBIC gamma to 0.50 reduced the density only to **0.895**. Smaller theory-led bridge systems remained between **0.964 and 1.000** dense.

| Specification | Nodes | Complete cases | EBIC gamma | Edges | Density |
|---|---:|---:|---:|---:|---:|
| Primary climate-engagement system | 15 | 995 | 0.25 | 102 / 105 | 0.971 |
| Primary climate-engagement system | 15 | 995 | 0.50 | 94 / 105 | 0.895 |
| Domain-bridging system | 11 | 997 | 0.25 | 55 / 55 | 1.000 |
| Domain-bridging system | 11 | 997 | 0.50 | 53 / 55 | 0.964 |
| Compact bridge system | 9 | 1,000 | 0.25 / 0.50 | 36 / 36 | 1.000 |
| Compact bridge system | 8 | 1,002 | 0.25 / 0.50 | 28 / 28 | 1.000 |

The result therefore does **not** support an interpretable sparse-network narrative, a centrality-based substantive claim, or a publication-ready CAN analysis. The app displays the graph and derived tables solely so users can audit the gate failure rather than mistake omitted results for untested analyses.

## Public workspace structure

The Streamlit CCAM workspace contains the following tabs.

| Tab | Purpose |
|---|---|
| **CCAM scope** | Source provenance, sample flow, logged missing-value handling, and 15-node map. |
| **RQ1 feasibility network** | The derived graph, network summary, node/edge exports, and an explicit warning against interpretation. |
| **Measurement and sensitivity checks** | CFA probes and the complete non-saturation sensitivity table. |
| **Complete analysis ledger** | Executed, failed, and deliberately withheld branches in an Abadi-style ledger. |
| **Data and code** | Official source links, source checksum, configuration download, and local reproduction instructions. |

## References

[1] Marlon, J. R., Carman, J., Roser-Renouf, C., Wang, X., Nisbet, M. C., Leiserowitz, A., & Maibach, E. W. (2025). *Climate Change in the American Mind: National Survey Data on Public Opinion (2008–2024)*. Yale Program on Climate Change Communication and George Mason University Center for Climate Change Communication. https://doi.org/10.17605/OSF.IO/JW79P

## Visual validation

The public workspace was visually validated locally after restart of the Streamlit application. The selector exposes CCAM as the third case alongside Abadi Study 2, ESS CRONOS-3 / SoGreen, and BYOD. On entry, the page visibly states the 102/105-edge, density-0.971 gate failure in a prominent error panel before the graph or rankings. The scope tab renders the sample-flow table and the complete 15-node official variable map, while the remaining tabs provide the graph, measurement/sensitivity tables, ledger, and official-source/data-protection instructions. No respondent-level CCAM records appear in the interface.
