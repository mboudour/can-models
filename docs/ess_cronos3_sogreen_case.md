# ESS CRONOS-3 / SoGreen Wave 6 climate-attitudes worked case

## Scope

This is the project’s **second worked case**, separate from the genuine Abadi et al. Study 2 replication. It uses the ESS CRONOS-3 Wave 6 SoGreen climate-attitudes module, which was fielded in October–November 2025 in eleven countries and is available through the ESS Data Portal.[1][2]

The case is a **locally reproducible baseline specification**, not a public microdata mirror. ESS recommends linking to its Data Portal rather than making ESS datasets available on external websites; ESS data are CC BY-NC-SA 4.0.[3] Accordingly, the repository and Streamlit Community Cloud deployment contain no respondent-level ESS data or codebook copy.

## Official source and local acquisition

| Item | Requirement |
|---|---|
| Official release | CRONOS-3 Wave 6, DOI [10.21338/cron3w6e01](https://doi.org/10.21338/cron3w6e01) |
| Portal | [ESS CRONOS-3 Data Portal](https://ess.sikt.no/en/series/a46bcac5-b030-444b-9280-441ec97e1bce) |
| Required local data file | `data/external/ess_cronos3_sogreen/CRON3w6e01.csv` |
| Required local codebook | `data/external/ess_cronos3_sogreen/CRON3w6e01 codebook.html` |
| Expected source SHA-256 | `0a3a647e1b530e33a0e542ce573e53aa4449fba49856af097bb1cdac15b3fe59` |
| Source verification | `Rscript --vanilla scripts/verify_ess_cronos3_source.R` |

All content inside `data/external/` is ignored by Git, except the acquisition instructions in `data/external/README.md`.

## Approved 15-node baseline

The Wave 6 baseline deliberately represents a focused climate-policy attitude system. It excludes the separate transport and appliance behavioural questions, which should be investigated in a future dedicated behavioural-subsystem analysis rather than mixed mechanically into the first network.

| Domain | Variables |
|---|---|
| Climate appraisal | `w6sgq11` climate-change worry; `w6sgq12` personal responsibility to reduce climate change; `w6seq2` worry about local extreme weather |
| Institutional capacity | `w6sgq13` trust in government to address climate change; `w6seq4` government preparedness for extreme weather |
| Policy orientation and legitimacy | `w6sgq14` environment versus economic growth; `w6sgq15` policy familiarity; `w6sgq16` confidence that policies consider everyone’s views; `w6sgq17` confidence in fair policy outcomes |
| Expected transition impacts | `w6sgq18` job-market impact; `w6sgq19` required lifestyle changes; `w6sgq20` daily-life impact |
| Personal-cost concerns | `w6sgq21` energy-bill concern; `w6sgq22` transport-cost concern; `w6sgq23` future job-loss concern |

The configuration converts the documented `9` and `99` nonresponse values to missing before complete-case network preparation. It retains `0` as a valid response where the Wave 6 item uses an 0–10 scale.

## Analytical boundaries

Wave 6 is collected within a panel, but the initial configuration estimates a **between-person, undirected MGM at one wave**. Its edges are conditional associations. They do not demonstrate temporal order, within-person effects, or verified causal relations. A temporal extension must first document identical items in later released waves and specify a design-appropriate longitudinal model.

The configuration declares a split-sample methodological check and country-replication workflow. These are not substitutes for a longitudinal model, and country comparisons remain conditional on the documented minimum sample size, the completed diagnostics, and appropriate multiplicity control.

## Publication gate

The public application intentionally displays no substantive network output until all of the following are reviewed:

1. The official source file and codebook match the recorded edition and checksum.
2. The 15 approved items have adequate response variation after documented missing-value recoding.
3. The regularised primary network is non-trivial and not saturated or dominated by artefacts.
4. Bootstrap edge-accuracy and case-drop centrality-stability diagnostics are complete and acceptable.
5. The split-sample and/or pre-specified country replication evidence is reviewed.
6. The final interpretation preserves the conditional-association and panel-design boundaries.

If this gate is not passed, the repository will retain the data-access instructions and transparent specification but will not present a graph or centrality ranking as a substantive CAN finding.

## Commands

Run these commands from the repository root after the official files have been placed locally:

```bash
Rscript --vanilla scripts/verify_ess_cronos3_source.R
Rscript --vanilla scripts/validate_config.R --config config/ess_cronos3_sogreen_w6.yml
Rscript --vanilla scripts/run_ess_cronos3_w6.R
```

## References

[1] European Social Survey. *New panel survey data on climate change now available* (9 April 2026). https://www.europeansocialsurvey.org/news/article/new-panel-survey-data-climate-change-now-available

[2] European Social Survey European Research Infrastructure (ESS ERIC). (2026). *CRONOS-3 Wave 6*. Sikt — Norwegian Agency for Shared Services in Education and Research. https://doi.org/10.21338/cron3w6e01

[3] European Social Survey. *Disclaimer and conditions of use*. https://www.europeansocialsurvey.org/contact/disclaimer
