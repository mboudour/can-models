# Data provenance and replacement contract

## Bundled original Study 2 data

The repository bundles the authors’ public original Study 2 source files under `data/raw/abadi_study2_2020/`.

| File | Purpose | Original source and terms |
|---|---|---|
| `abadi_2023_four_country_study2.csv` | Individual-level April 2020 four-country survey data | Abadi (2023), UvA Figshare, DOI [10.21942/uva.17085719.v1](https://doi.org/10.21942/uva.17085719.v1) |
| `abadi_2023_qualtrics_codebook.pdf` | Original Qualtrics item wording, value labels, country coding, and reverse-code notation | Same public data record and companion data paper, DOI [10.5334/jopd.86](https://doi.org/10.5334/jopd.86) |

The public record describes 2,031 April 2020 respondents from Germany, Spain, the Netherlands, and the United Kingdom. The replication configuration applies the article’s reported `gender = other` exclusion, yielding a Study 2 analytical sample of 2,030 respondents. It logs all reverse coding and the sparse-age-category handling in the output provenance.

The Figshare metadata declares **CC BY 4.0**, while the record description says **CC BY-SA**. The code is MIT-licensed, but the source data are not covered by the repository code licence. Retain the dataset citation and check the current source record before redistribution or derivative publication.

## ESS CRONOS-3 / SoGreen Wave 6 is official-access only

The second worked case does **not** bundle the ESS CRONOS-3 Wave 6 data or codebook. ESS recommends linking to the ESS Data Portal instead of hosting its datasets externally, and its data are licensed CC BY-NC-SA 4.0. Download the official `CRON3w6e01.csv` and codebook from the [CRONOS-3 Data Portal](https://ess.sikt.no/en/series/a46bcac5-b030-444b-9280-441ec97e1bce), then keep them in the Git-ignored location described in [`data/external/README.md`](external/README.md).

The case configuration records the official Wave 6 DOI ([10.21338/cron3w6e01](https://doi.org/10.21338/cron3w6e01)) and expected SHA-256 file fingerprint. Use `scripts/verify_ess_cronos3_source.R` before analysis; never commit, redistribute, or expose the ESS respondent-level files in the public Streamlit app.

## Study 1 is not bundled

The August 2019 15-country Study 1 data are restricted by the article’s H2020/GDPR data-availability statement. This repository does not reconstruct or simulate Study 1. The full two-study ledger remains disabled until the authors authorize a de-identified Study 1 analytic file and documentation.

## Replacing the example data

A replacement dataset must satisfy the following conditions.

| Requirement | Reason |
|---|---|
| One row per participant | The CAN analyses estimate relations among individual response variables. |
| At least three item-level attitude variables | A network cannot be estimated meaningfully with fewer than three nodes. |
| Explicit numeric coding for ordinal items | Recode non-numeric categories before estimation or add a logged data-preparation transformation. |
| A complete and documented node map | Every node needs a source variable, a human-readable label, a theoretical CAN domain, response type, and response levels. |
| A known sample filter | The analytic sample must be reproducible. |
| Logged reverse coding and category transformations | Item direction and any sparse-category handling must be auditable. |
| Optional country/group variable | Needed only for country or subgroup network comparisons. |
| Appropriate permissions | Do not add confidential or non-redistributable data to a public repository. |

The configuration validator checks source-file existence, all referenced variables, node uniqueness, filter validity, response-level variation, and prohibited overlap between a subgrouping variable and the network it is used to compare.

> **Data and theory warning.** Replacing the data does not make cross-sectional estimates directional or causal. The CAN framework motivates the node structure and hypotheses; resulting undirected network edges remain conditional associations unless a temporal or experimental design supports stronger inference.
