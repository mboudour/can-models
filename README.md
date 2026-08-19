# can-models

`can-models` is a **configuration-driven R project for Causal Attitude Network (CAN) analyses**. It implements the computational workflow reported by Abadi et al.—mixed graphical models, LASSO/EBIC estimation, centrality, bootstrap diagnostics, Walktrap communities, CFA/EFA, Network Comparison Tests, country-network clustering, and NetworkTree partitioning—while retaining dataset-specific decisions in YAML files.

The repository centres on a genuine **public Study 2 replication workspace** based on the Abadi et al. authors’ original April 2020 four-country dataset. Study 1 remains explicitly access-gated because the original 15-country 2019 data are restricted under the article’s H2020/GDPR data-availability statement.

> **Interpretive guardrail.** CAN is a substantive theory in which beliefs, feelings, and behavioural tendencies may influence one another. With cross-sectional survey data, the undirected network edges estimated here are **conditional associations**, not verified directional causal effects. Do not interpret an edge or centrality ranking as proof of a causal intervention target.

## Genuine replication scope

| Paper component | Public Study 2 status | Boundary |
|---|---|---|
| Study 2 sample preparation and original variables | Executed | The public file contains 2,031 records. The documented gender=other exclusion gives *N* = 2,030; all records pass the retained attention check. |
| RQ1 joint 29-node MGM, LASSO/EBIC, centrality, predictability, and Mardia check | Executed | Uses the original country, demographic, threat, populist-attitude, nativism, and conspiracy-mentality variables. |
| PA and nativism CFA, country CFA/invariance, and EFA | Executed | The seven-item one-factor PA CFA fits poorly; the project does not silently convert it into an unqualified PA score. |
| Bootstrap accuracy/stability, robust communities, categorical artefact checks | Implemented; intensive run pending | Not displayed as completed until its offline computation finishes. |
| RQ2 high/low PA networks; RQ3 political-orientation networks; RQ4 country networks, NCTs, clustering, and NetworkTree | Public data available; computations pending | The required Study 2 variables exist, but exact appendix decision rules and intensive output remain to be verified before claims are made. |
| Study 1 analysis, Study 1–Study 2 NCT, and two-study conclusions | Access-gated | Enabled only after the authors authorize the restricted 15-country data and documentation. |

The full methodological boundary and item-level correspondence are documented in [docs/abadi_genuine_replication_scope.md](docs/abadi_genuine_replication_scope.md).

## Quick start

The analysis requires **R 4.3+**. Start from a shell in the repository root.

```bash
Rscript scripts/setup_environment.R
Rscript scripts/validate_config.R --config config/abadi_study2_public.yml
Rscript scripts/run_core_analysis.R --config config/abadi_study2_public.yml
Rscript scripts/run_example.R --config config/abadi_study2_public.yml
```

The core command performs the data audit, factor-model workflow, and primary original-variable CAN. The complete configured workflow adds diagnostics and intensive subgroup/country modules. Generated tables, matrices, logs, and provenance are written to `new_computations/`; figures are written to `figures/`.

## Streamlit public workspace and BYOD workflow

The repository includes a **Streamlit application** at `app/app.py` with two explicit workspaces.

| Workspace | Purpose |
|---|---|
| **Abadi et al. Study 2 replication** | The default public workspace. It displays the original-data sample flow, logged transformations, 29-node joint network, factor-model results, a paper-wide replication ledger, and the precise Study 1 access gate. |
| **Bring your own data** | A separate participant workflow. Users upload a CSV/XLSX file, map arbitrary raw variable names to CAN nodes and domains, inspect eligibility, and download a reproducible YAML configuration. |

```bash
sudo pip3 install -r requirements-streamlit.txt
streamlit run app/app.py
```

Before any participant-data computation is launched, the BYOD workspace displays an **eligibility table**. It identifies ready analyses, required data/design conditions, and transparent placeholders. A single uploaded cross-sectional dataset, for example, cannot be misrepresented as a two-study NCT.

For deployment, see [docs/deployment.md](docs/deployment.md). It distinguishes Streamlit Community Cloud **mapping-only** publication from Docker-based **full R analysis** hosting.

## Public original Study 2 data

The worked replication uses the public four-country April 2020 data deposit and Qualtrics codebook. Preserve the source citation when reusing the data. Figshare metadata names **CC BY 4.0**, whereas the record description refers to **CC BY-SA**; consult the current record before reuse or redistribution.

| Item | Source |
|---|---|
| Study 2 respondent data | `data/raw/abadi_study2_2020/abadi_2023_four_country_study2.csv` |
| Original Qualtrics codebook | `data/raw/abadi_study2_2020/abadi_2023_qualtrics_codebook.pdf` |
| Study 2 CAN mapping | `config/abadi_study2_public.yml` |
| Public data record | Abadi (2023), UvA Figshare: [https://doi.org/10.21942/uva.17085719.v1](https://doi.org/10.21942/uva.17085719.v1) |
| Data paper | Abadi, Arnaldo, & Fischer (2023): [https://doi.org/10.5334/jopd.86](https://doi.org/10.5334/jopd.86) |

## Study 1 access gate

The 2019 15-country Study 1 data are not bundled. The paper says that they are restricted by H2020 GDPR agreements and directs access requests to the corresponding author. The Streamlit application includes an email-free required-materials checklist. Until access is granted, the repository does not simulate Study 1 results, a cross-study NCT, or the paper’s two-study conclusions.

## Reuse with another dataset

1. Copy `config/dataset_template.yml` to a new name.
2. Place the raw data under `data/raw/<your_dataset>/`; do not overwrite the original Study 2 source files.
3. Define the input file, sample filter, item response types and levels, node labels, scales, country/group variables, transformations, and comparisons in YAML.
4. Run `scripts/validate_config.R` to identify missing variables, unsuitable response coding, and prohibited overlap between group variables and network nodes.
5. Run the core and, where eligible, full workflows with the new configuration.

The detailed replacement contract is in [docs/reuse_with_your_data.md](docs/reuse_with_your_data.md).

## Project structure

```text
config/              Dataset-specific variables, node sets, transformations, and analytic options
R/                   Reusable analysis functions
scripts/             Environment setup, validation, run, and report entry points
data/raw/            Licensed source data, including public original Study 2 data
new_computations/    Generated tables, matrices, diagnostics, and provenance logs
figures/             Generated network and diagnostic figures
reports/             Rendered analysis templates and methodological matrices
docs/                Methodological, reuse, deployment, and access-gate documentation
```

## Core references

[1] Dalege, J., Borsboom, D., van Harreveld, F., van den Berg, H., Conner, M., & van der Maas, H. L. J. (2016). *Toward a formalized account of attitudes: The Causal Attitude Network (CAN) model*. *Psychological Review, 123*(1), 2–22. [https://doi.org/10.1037/a0039802](https://doi.org/10.1037/a0039802)

[2] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the dots with Causal Attitude Network (CAN): A psychological network approach to populist attitudes, nativism, conspiracy mentality and threat appraisals*. *Measurement: Interdisciplinary Research and Perspectives, 23*(4), 393–417. [https://doi.org/10.1080/15366367.2024.2363718](https://doi.org/10.1080/15366367.2024.2363718)

[3] Abadi, D. (2023). *A Dataset of Social-Psychological and Emotional Reactions during the COVID-19 Pandemic across Four European Countries*. UvA Figshare. [https://doi.org/10.21942/uva.17085719.v1](https://doi.org/10.21942/uva.17085719.v1)

[4] Abadi, D., Arnaldo, I., & Fischer, A. (2023). *A Dataset of Social Psychological and Emotional Reactions During the COVID-19 Pandemic Across Four European Countries*. *Journal of Open Psychology Data*. [https://doi.org/10.5334/jopd.86](https://doi.org/10.5334/jopd.86)

[5] Epskamp, S., Borsboom, D., & Fried, E. I. (2018). *Estimating psychological networks and their accuracy: A tutorial paper*. *Behavior Research Methods, 50*, 195–212. [https://doi.org/10.3758/s13428-017-0862-1](https://doi.org/10.3758/s13428-017-0862-1)

[6] Haslbeck, J. M. B., & Waldorp, L. J. (2020). *mgm: Estimating time-varying mixed graphical models in high-dimensional data*. *Journal of Statistical Software, 93*(8), 1–46. [https://doi.org/10.18637/jss.v093.i08](https://doi.org/10.18637/jss.v093.i08)
