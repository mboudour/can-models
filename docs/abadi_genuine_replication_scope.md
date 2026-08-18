# Genuine Abadi et al. replication design

## Principle

The public application will no longer present the Ravšelj et al. ChatGPT data as an Abadi et al. case study. Its replication workspace will be anchored in the authors’ **original April 2020 four-country dataset**, which the authors publicly deposited on UvA Figshare. This supports a genuine **Study 2 data replication and independent computational reimplementation** of the reported methods. It cannot, on its own, be described as a full two-study replication of Abadi et al. (2025).

> **Terminology.** “Study 2 replication” means re-running the paper’s documented computations on the public Study 2 respondent-level data with the original variables, item wording, country sample, and documented exclusions. “Two-study replication” will be used only after authorized Study 1 data are received and verified.

## Data basis

| Paper study | Original design | Available data | Replication status |
|---|---|---|---|
| **Study 1** | August 2019; 15 European countries; reported final *N* = 8,046 | Restricted under the paper’s H2020 GDPR data-availability statement | **Access-gated.** The workspace exposes the exact required data package and a request template, but does not fabricate results. |
| **Study 2** | April 2020; Germany, Spain, Netherlands, United Kingdom; reported final *N* = 2,030 | Public Figshare CSV and Qualtrics codebook; raw file contains 2,031 valid respondents | **Public replication.** The workspace will implement the documented exclusions and reported analyses. |

## Faithful Study 2 replication ledger

| Paper element | Public Study 2 replication action | Status once implemented |
|---|---|---|
| Sample preparation | Use original CSV, retain the four original countries, remove the one `gender = other` respondent documented in the paper, preserve the attention-check record, apply original reverse coding. | Executable |
| Original variable set | Use country; gender; age; subjective social status; religion; political orientation; education; 8 realistic/symbolic-threat items; 7 populist-attitude items; 3 nativism items; and 5 Conspiracy Mentality Questionnaire items. | Executable |
| Distributional check | Reproduce Mardia skewness and kurtosis diagnostic after documented sample preparation. | Executable |
| Joint Study 2 network (RQ1) | Estimate the Study 2 mixed graphical model using the paper’s reported MGM/LASSO/EBIC approach, calculate centrality and predictability, draw a weighted undirected network, test bootstrap accuracy/stability, and evaluate Walktrap/robust communities. | Executable |
| Categorical-artifact check | Produce the chi-square/Cramér’s V checks for categorical variables to flag potentially inflated MGM categorical edges. | Executable |
| PA scale analysis (RQ2) | Reproduce the 7-item Study 2 populist-attitudes CFA, country CFA/invariance assessment, and country-level EFA if the CFA/invariance step fails. High/low PA networks remain conditional on a valid scale score, as in the paper. | Executable with model-dependent outcome |
| Nativism and political orientation (RQ3) | Reproduce the Study 2 nativism-scale checks and the left/right political-orientation network comparison using the original political-orientation variable. | Executable with model-dependent outcome |
| Country networks and similarity (RQ4) | Estimate Germany, Spain, Netherlands, and United Kingdom networks; calculate network summaries, country pair adjacency correlations, pairwise NCTs with correction, and four-country clustering; fit NetworkTree if supported. | Executable but computationally intensive |
| Cross-study comparison | Study 1–Study 2 NCT, cross-study community comparison, and cross-study conclusions. | **Not executable until Study 1 authorization.** |
| Substantive conclusion | Report only results that follow from the executed Study 2 output. Label all cross-study and 15-country claims as access-gated. | Executable with boundary |

## Evidence of item correspondence

The public Qualtrics codebook identifies the exact Study 2 variables needed by the paper. These include `A20.1`–`A20.3`, `A21.1`, `A21.2*`, `A22.1`–`A22.2` for seven populist-attitude items; `A23.1`–`A23.3` for nativism; `A24.1`–`A24.5` for conspiracy mentality; `A9.1`, `A9.2`, `A9.3*`, `A9.4`–`A9.7`, and `A9.8*` for realistic/symbolic threat; and original demographic/political variables such as `Country`, `A3.1`, `A3.2`, `A3.7`, `A3.8`, `A3.9`, and `A3.10`.

The stars are part of the original CSV and codebook notation for reverse-coded items. The replication configuration must rename and reverse these variables in a logged preprocessing step rather than treating the asterisk as an arbitrary column-name variation.

## Study 1 data package required before enabling the remaining ledger

The study-access request will ask for a de-identified data file and codebook that provide, at minimum, the cleaned Study 1 analytic sample, country codes, original item names/labels, response-value coding, reverse-coding rules, exclusion flags, questionnaire translations, and the exact variable set included in the published model. If raw transfer is not permissible, a secure analysis environment or an author-run replication script with checksum-verifiable output would also support the access-gated module.

## Interpretive limit

Both studies are cross-sectional. Even once both datasets are authorized and the published computation is reproduced, empirical undirected network edges are conditional associations and do not establish temporal order or verified directional causal effects.

## References

[1] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the Dots with Causal Attitude Network (CAN): A Psychological Network Approach to Populist Attitudes, Nativism, Conspiracy Mentality and Threat Appraisals*. https://doi.org/10.1080/15366367.2024.2363718

[2] Abadi, D. (2023). *A Dataset of Social-Psychological and Emotional Reactions during the COVID-19 Pandemic across Four European Countries*. UvA Figshare. https://doi.org/10.21942/uva.17085719.v1

[3] Abadi, D., Arnaldo, I., & Fischer, A. (2023). *A Dataset of Social Psychological and Emotional Reactions During the COVID-19 Pandemic Across Four European Countries*. Journal of Open Psychology Data. https://doi.org/10.5334/jopd.86
