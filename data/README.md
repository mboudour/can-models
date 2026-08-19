# Data provenance and replacement contract

## Bundled original Study 2 data

The repository bundles the authors’ public original Study 2 source files under `data/raw/abadi_study2_2020/`.

| File | Purpose | Original source and terms |
|---|---|---|
| `abadi_2023_four_country_study2.csv` | Individual-level April 2020 four-country survey data | Abadi (2023), UvA Figshare, DOI [10.21942/uva.17085719.v1](https://doi.org/10.21942/uva.17085719.v1) |
| `abadi_2023_qualtrics_codebook.pdf` | Original Qualtrics item wording, value labels, country coding, and reverse-code notation | Same public data record and companion data paper, DOI [10.5334/jopd.86](https://doi.org/10.5334/jopd.86) |

The public record describes 2,031 April 2020 respondents from Germany, Spain, the Netherlands, and the United Kingdom. The replication configuration applies the article’s reported `gender = other` exclusion, yielding a Study 2 analytical sample of 2,030 respondents. It logs all reverse coding and the sparse-age-category handling in the output provenance.

The Figshare metadata declares **CC BY 4.0**, while the record description says **CC BY-SA**. The code is MIT-licensed, but the source data are not covered by the repository code licence. Retain the dataset citation and check the current source record before redistribution or derivative publication.

## Bundled Ravšelj et al. ChatGPT survey example

The repository also bundles the public Version 2 global ChatGPT-perceptions survey under `data/raw/chatgpt_ravselj_2025/`. It is a **non-replication worked example** for the reusable workflow, not part of the original Abadi et al. study design.

| File | Purpose | Citation |
|---|---|---|
| `final_dataset.xlsx` | Public respondent-level survey workbook | Ravšelj et al. (2025), Mendeley Data, Version 2: [10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2) |
| `questionnaire.pdf` | Original survey instrument and item wording | Same public data record |
| `config/chatgpt_ravselj_focus.yml` | Labelled 16-node cross-sectional CAN configuration | See [ChatGPT worked-example documentation](../docs/chatgpt_ravselj_worked_example.md) |

The companion publication is Ravšelj et al., *Higher education students’ perceptions of ChatGPT: A global study of early reactions*, PLOS ONE (2025): [10.1371/journal.pone.0315011](https://doi.org/10.1371/journal.pone.0315011). The completed initial 31-node run is retained as a dense-network diagnostic, not as a substantive centrality or causal finding. Consult the current data-deposit terms before reuse or redistribution.

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
