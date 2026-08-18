# Data provenance and replacement contract

## Bundled example data

The repository bundles two unmodified public source files under `data/raw/chatgpt_global_survey/`:

| File | Purpose | Original source and terms |
|---|---|---|
| `finaldataset.xlsx` | Individual-level global higher-education student survey responses | Ravšelj et al. (2025), Mendeley Data, Version 2, DOI [10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2), **CC BY 4.0** |
| `questionnaire.pdf` | Instrument wording and response options | Same public dataset record, **CC BY 4.0** |

The files are an illustrative working dataset, not part of the MIT licence that covers the repository code. Any reuse must retain the source attribution and comply with the original CC BY 4.0 licence.

## Replacing the example data

A replacement dataset must satisfy the following conditions.

| Requirement | Reason |
|---|---|
| One row per participant | The CAN analyses estimate relations among individual response variables. |
| At least three item-level attitude variables | A network cannot be estimated meaningfully with fewer than three nodes. |
| Explicit numeric coding for ordinal items | The example uses integers 1–5. Recode non-numeric categories before estimation or add a data-preparation transformation. |
| A complete and documented node map | Every node must have a source variable, a human-readable label, and a theoretical CAN domain. |
| A known sample filter | The analytic sample must be reproducible—for example, prior users of an LLM. |
| Optional country/group variable | Needed only for country or subgroup network comparisons. |
| Appropriate permissions | Do not add confidential or non-redistributable data to a public repository. |

The configuration validator checks source-file existence, all referenced variables, node uniqueness, filter validity, level variation, and the prohibited overlap between a subgrouping variable and the network that it is used to compare.

> **Data and theory warning.** Replacing the data does not make cross-sectional estimates directional or causal. The CAN framework motivates the node structure and hypotheses; the resulting undirected network edges remain conditional associations unless a temporal or experimental design supports stronger inference.
