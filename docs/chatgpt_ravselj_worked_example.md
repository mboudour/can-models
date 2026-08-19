# Ravšelj et al. ChatGPT Perceptions Worked Example

## Purpose

This is the second worked example in `can-models`. It is **not** a replication of Abadi et al. (2025). Instead, it demonstrates the reusable CAN workflow on the public global survey of higher-education students’ early perceptions of ChatGPT reported by Ravšelj et al. (2025).[1] The corresponding public Version 2 data deposit provides the respondent-level workbook and questionnaire used here.[2]

> The design is a single cross-sectional survey. Accordingly, all undirected network edges are interpreted as **conditional associations**, not verified directional causal effects, temporal processes, or intervention effects.[3]

## Source and analytical population

The public workbook contains **23,218** records. The worked example filters to respondents reporting prior ChatGPT use (`Q13 = 1`), giving **16,010** respondents before complete-case handling. The pre-specified focused configuration contains 16 five-category ordinal nodes from use, capability beliefs, governance, risk appraisal, evaluations, expected educational outcomes, and feelings. It retains **12,175** complete cases.

| Source | Citation and access |
|---|---|
| Companion publication | Ravšelj et al., *Higher education students’ perceptions of ChatGPT: A global study of early reactions*, PLOS ONE (2025). [1] |
| Public data and questionnaire | Ravšelj et al., *Higher Education Students’ Early Perceptions of ChatGPT: Global Survey Data*, Version 2. [2] |
| CAN framework | Dalege et al., *Toward a formalized account of attitudes: The Causal Attitude Network (CAN) model*. [3] |
| Workflow comparator | Abadi et al., *Connecting the Dots with CAN*. [4] |

## Why the original 31-node run is retained only as a diagnostic

The user-generated 31-node first run completed technically on **12,009** complete cases but retained all **465 of 465 possible edges**. The network density is therefore 1.00. This output is retained in the application to demonstrate a critical workflow rule: a network that is fully connected and visually overplotted should not be promoted to a substantive centrality, bridge, or intervention finding.

The diagnostic figure also used generic numeric labels and one default domain colour because the initial BYOD YAML contained blank labels and did not preserve the intended domain mapping. The reusable workflow now replaces blank or duplicated labels with source variable names; the historical diagnostic is displayed unchanged for auditability.

## Focused-model sensitivity

The bundled `chatgpt_ravselj_focus.yml` specifies 16 labelled nodes before estimation, raises the EBIC gamma to .50, and constrains the regularization path. The ordinal MGM remains fully connected (120 of 120 possible edges). A Spearman EBICglasso sensitivity network remains dense (109 of 120 edges). These results show that merely reducing the node count or changing estimator family does not create a defensible sparse attitude network for this item set.

The worked example therefore does not report centrality rankings as findings. It makes explicit that a publishable application would require a stronger theory-led measurement plan, sensitivity/robustness work, and a revised primary network specification rather than a post-hoc graphical threshold.

## Publication-readiness conclusion

The existing run is **not publishable as a stand-alone substantive CAN result**. It is, however, an informative teaching and reproducibility case because it makes technical failures, complete-case loss, dense-network selection, and the boundary between CAN theory and cross-sectional evidence visible. A future manuscript based on these data would need a smaller theory-led node set, a preregistered penalty/sensitivity plan, bootstrap accuracy and centrality-stability diagnostics, an explicit missing-data sensitivity analysis, carefully justified country comparisons, and either split-sample/holdout or independent replication.

## References

[1] Ravšelj, D., Keržič, D., Tomaževič, N., Umek, L., Brezovar, N., et al. (2025). *Higher education students’ perceptions of ChatGPT: A global study of early reactions*. PLOS ONE. [https://doi.org/10.1371/journal.pone.0315011](https://doi.org/10.1371/journal.pone.0315011)

[2] Ravšelj, D., et al. (2025). *Higher Education Students’ Early Perceptions of ChatGPT: Global Survey Data*, Version 2. Mendeley Data. [https://doi.org/10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2)

[3] Dalege, J., Borsboom, D., van Harreveld, F., van den Berg, H., Conner, M., & van der Maas, H. L. J. (2016). *Toward a formalized account of attitudes: The Causal Attitude Network (CAN) model*. Psychological Review. [https://doi.org/10.1037/a0039802](https://doi.org/10.1037/a0039802)

[4] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the Dots with Causal Attitude Network (CAN): A Psychological Network Approach to Populist Attitudes, Nativism, Conspiracy Mentality and Threat Appraisals*. [https://doi.org/10.1080/15366367.2024.2363718](https://doi.org/10.1080/15366367.2024.2363718)
