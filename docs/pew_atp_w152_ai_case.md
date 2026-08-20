# Pew American Trends Panel Wave 152 AI Attitude Network pathway

## Status

This is a **public-source, pre-analysis CAN pathway**, not a completed result case. It is intentionally separate from the original-data Abadi Study 2 replication and from the completed ESS CRONOS-3 / SoGreen case. The aim is to make a rigorous, reproducible U.S. AI-attitude study possible without distributing Pew Research Center respondent-level data or treating public toplines as microdata.

> **Interpretive boundary.** Wave 152 is a single cross-sectional survey wave. If a network is later estimated, its undirected edges will be conditional associations among between-person responses. The word *causal* in CAN refers to the substantive attitude-system theory; the analysis will not establish directional, temporal, or intervention effects.

## Why Wave 152 was selected

Wave 152 was fielded from **12 to 18 August 2024** and covers artificial intelligence and human enhancement.[1] Its final questionnaire contains a broad but coherent all-respondent AI-attitude system: awareness and perceived exposure, excitement/concern, personal control, personal and societal expectations, future AI capability and harms, employment expectations, regulation, and confidence in government and companies.[2]

| Candidate wave | Field dates | Primary AI focus | Decision |
|---|---:|---|---|
| ATP Wave 99 | 1–7 Nov. 2021 | AI/human-enhancement technologies and technology-specific concerns | Not selected: less cohesive for contemporary generative-AI and governance attitudes. |
| ATP Wave 119 | 12–18 Dec. 2022 | Workplace AI, health-care AI, and awareness of everyday AI | Strong alternative, but narrower and pre-dates Wave 152's broader current AI framework. |
| **ATP Wave 152** | **12–18 Aug. 2024** | AI orientation, anticipated impacts, capability/risk, control, regulation, and chatbots | **Selected**: strongest all-respondent attitude-system coverage for the initial worked case. |

## Official data-access boundary

Pew's official Wave 152 dataset page states that dataset downloads require a Pew Research Center account.[1] The public page provides the official survey context and links to the final questionnaire and topline, but the browser-visible download flow requires an email address, email verification, and acceptance of current Pew account terms. The project therefore does not obtain, host, commit, upload, or redistribute the respondent-level data outside that authorised route.

The public materials collected for documentation are the official Wave 152 landing page, report, methodology page, final questionnaire, and topline. They support theory and mapping audit but cannot substitute for individual-level data in a network model.

## Pre-specified 15-node candidate network

The mapping below is deliberately restricted to questions asked of **all respondents**. It excludes conditional chatbot-use/helpfulness items and form-specific impact/job batteries in the first analysis, because adding those items could silently reduce the analytic population or mix different random-form samples.

| Domain | Questionnaire IDs | Candidate nodes |
|---|---|---|
| AI exposure and personal orientation | `AI_HEARD`, `USEAI`, `CNCEXC`, `AICONTROL1` | AI awareness; perceived frequency of AI interaction; excitement versus concern; perceived personal control over AI use |
| Societal consequences and personal benefit | `AICHANGE`, `PERSBENHRM`, `AIJOBS` | Expected national impact; expected personal benefit versus harm; expected jobs impact |
| AI capability and future risk | `TRSTAIPRS`, `FUTRAI_a`, `FUTRAI_b`, `FUTRAI_c`, `FUTRAI_d` | Trust AI for diagnosis; AI autonomy; major harm; productivity; happiness |
| Governance and institutional confidence | `AIREG`, `REGCONFG`, `REGCONFI` | Concern about insufficient regulation; confidence in government regulation; confidence in companies' responsible AI use |

The exact column spellings, response directions, randomisation fields, and available categories must be verified against the official downloaded microdata. Documented `98` and `99` codes are candidates for nonresponse recoding, subject to exact file-level verification.[2]

## Required feasibility and publication gate

The public worked case must not display substantive network results until all checks below are passed.

| Gate | Required evidence |
|---|---|
| Source provenance | Official Wave 152 file acquired through a verified Pew account; filename and SHA-256 recorded locally. |
| Variable audit | All 15 all-respondent items present with codebook-consistent values and adequate response variation. |
| Analytic sample | At least 3,000 complete cases after documented nonresponse handling; complete-case loss reported. |
| Design integrity | No estimand change caused by conditional routing, random form, or unrecorded response-category collapse. |
| Network interpretability | Regularised primary network is not saturated and shows interpretable cross-domain structure. |
| Robustness | Split-sample, EBIC, weighting, and item-set sensitivities are pre-specified and saved. |
| Public claim | No directional, causal, or temporal language based only on the Wave 152 cross-section. |

If the network is saturated, unstable, or otherwise fails this gate, the public pathway will retain the transparent source/mapping record without presenting a misleading substantive result.

## Local handoff once official data are available

The authorised user should place the downloaded file in `data/external/pew_atp_w152/`, which is ignored by Git and excluded from Docker build contexts. The `config/pew_atp_w152_ai_attitudes_manifest.yml` file provides the source manifest and node map. A file-specific execution configuration will be created only after exact column names and coding have been verified.

## Sources

[1] [Pew Research Center, *American Trends Panel Wave 152*](https://www.pewresearch.org/dataset/american-trends-panel-wave-152/).

[2] [Pew Research Center, *2024 American Trends Panel Wave 152 final questionnaire*](https://www.pewresearch.org/wp-content/uploads/sites/20/2025/03/pi_2025.04.03_us-public-and-ai-experts_questionnaire.pdf).

[3] [Pew Research Center, *How the U.S. Public and AI Experts View Artificial Intelligence*](https://www.pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts-view-artificial-intelligence/).

[4] [Pew Research Center, *U.S. public and AI experts methodology*](https://www.pewresearch.org/internet/2025/04/03/us-public-and-ai-experts-methodology/).
