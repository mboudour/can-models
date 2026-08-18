# can-models

`can-models` is a **configuration-driven R project for Causal Attitude Network (CAN) analyses**. It implements the computational workflow used by Abadi et al. for psychological networks—mixed graphical models, LASSO/EBIC estimation, centrality, bootstrap diagnostics, Walktrap communities, factor analysis, Network Comparison Tests, country-network clustering, and NetworkTree partitioning—while keeping the data-specific decisions in YAML configuration files.

The repository includes the public **Higher Education Students’ Early Perceptions of ChatGPT: Global Survey Data** as a complete working example. You can replace the example workbook and edit one configuration file to analyse another compatible cross-sectional survey.

> **Interpretive guardrail.** CAN is a substantive theory in which beliefs, feelings, and behavioural tendencies may influence one another. With cross-sectional survey data, the undirected network edges estimated here are **conditional associations**, not verified directional causal effects. Do not interpret an edge or centrality ranking as proof of a causal intervention target.

## What the project reproduces

| Computational family in Abadi et al. | `can-models` module | ChatGPT example status |
|---|---|---|
| Data recoding, missingness, normality checks | `scripts/run_example.R` / `R/02_data.R` | Implemented |
| LASSO/EBIC mixed graphical model | `R/03_network.R` | Implemented |
| Centrality, bootstrap accuracy, and stability | `R/04_diagnostics.R` | Implemented |
| Walktrap and robust community summaries | `R/04_diagnostics.R` | Implemented |
| CFA, EFA, and invariance checks | `R/05_factor.R` | Implemented |
| Network Comparison Test (NCT) | `R/06_compare.R` | Implemented |
| Country network estimation and matrix correlations | `R/07_country.R` | Implemented |
| Country-network clustering | `R/08_cluster.R` | Implemented |
| NetworkTree partitioning | `R/09_networktree.R` | Implemented when `NetworkTree` is available |
| Categorical association checks | `R/10_context.R` | Implemented |

The ChatGPT data do not contain two independent studies, a populism/nativism scale, or a left–right political-orientation measure. The example therefore uses a **split-sample methodological analogue** for the two-study comparison and clearly labels scale/group analyses that are conditional on model fit. See [reports/adaptation_matrix.md](reports/adaptation_matrix.md).

## Quick start

The analysis requires **R 4.3+**. Start from a shell in the repository root.

```bash
Rscript scripts/setup_environment.R
Rscript scripts/validate_config.R --config config/chatgpt_example.yml
Rscript scripts/run_example.R --config config/chatgpt_example.yml
Rscript scripts/render_report.R --config config/chatgpt_example.yml
```

The first command installs project-local packages and creates `renv.lock`. The run writes generated tables, matrices, logs, and provenance files to `new_computations/`, and figures to `figures/`. Generated files are intentionally ignored by Git so that each analyst can reproduce them locally.

## Streamlit case study and participant workspace

The repository includes a **Streamlit application** at `app/app.py` with two explicit workspaces. **ChatGPT case study** is the default view: it presents the completed 30-node primary CAN, full-sample flow, centrality and strongest-edge tables, node dictionary, methods, and downloads for the public Ravšelj et al. data. **Bring your own data** is a separate workflow in which participants upload a CSV or Excel dataset, map arbitrary raw variable names to CAN nodes and contextual roles, inspect response coding, and generate a standalone YAML configuration without touching the case-study files.

```bash
sudo pip3 install -r requirements-streamlit.txt
streamlit run app/app.py
```

Before any participant-data computation is launched, the BYOD workspace displays an **eligibility table**. It distinguishes modules that are ready from data-supported placeholders: for example, a two-study NCT remains unavailable with a single cross-sectional upload, while country networks require at least two groups that pass the configured minimum sample size. This prevents the app from silently treating non-applicable Abadi et al.–style calculations as completed analyses. See [docs/streamlit_app.md](docs/streamlit_app.md).

For deployment, use [docs/deployment.md](docs/deployment.md). It distinguishes a Streamlit Community Cloud **mapping-only** publication from a Docker-based **full R analysis** deployment.

## Example dataset

The bundled workbook and questionnaire are distributed under the original **CC BY 4.0** terms. They are not covered by the repository’s MIT code licence. Cite both the dataset and companion paper when using the example data.

| Item | Source |
|---|---|
| Dataset | Ravšelj et al. (2025), *Higher Education Students’ Early Perceptions of ChatGPT: Global Survey Data*, Version 2. [https://doi.org/10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2) |
| Companion article | Ravšelj et al. (2025), *Higher education students’ perceptions of ChatGPT: A global study of early reactions*. *PLOS ONE*, 20(2), e0315011. [https://doi.org/10.1371/journal.pone.0315011](https://doi.org/10.1371/journal.pone.0315011) |
| Questionnaire | `data/raw/chatgpt_global_survey/questionnaire.pdf` |
| Example mapping | `config/chatgpt_example.yml` and `docs/data_dictionary_chatgpt.md` |

The full ChatGPT perception instrument was administered only to respondents who had used ChatGPT before. The example filter therefore restricts the core CAN to `Q13 = 1` and treats the resulting graph as a network of **ChatGPT-experienced higher-education students**.

## Reuse with another dataset

1. Copy `config/dataset_template.yml` to a new name.
2. Place the raw data under `data/raw/<your_dataset>/`; do not overwrite the example source files.
3. Define the input file, row filter, ordinal/continuous node types, node labels, scales, country or group variable, and all comparisons in your YAML file.
4. Run `scripts/validate_config.R` to detect missing variables, invalid response levels, and prohibited overlap between group variables and network nodes.
5. Run the example pipeline with your configuration.

The detailed replacement contract is in [docs/reuse_with_your_data.md](docs/reuse_with_your_data.md).

## Project structure

```text
config/              Dataset-specific variables, node sets, and analytic options
R/                   Reusable analysis functions
scripts/             Environment setup, validation, run, and report entry points
data/raw/            Licensed source data, including the complete ChatGPT example
new_computations/    Generated tables, matrices, diagnostics, and provenance logs
figures/             Generated network and diagnostic figures
reports/             Rendered analysis template and adaptation matrix
docs/                Methodological documentation and output catalogue
```

## Core references

[1] Dalege, J., Borsboom, D., van Harreveld, F., van den Berg, H., Conner, M., & van der Maas, H. L. J. (2016). *Toward a formalized account of attitudes: The Causal Attitude Network (CAN) model*. *Psychological Review, 123*(1), 2–22. [https://doi.org/10.1037/a0039802](https://doi.org/10.1037/a0039802)

[2] Abadi, D., Bertlich, T., Dalege, J., & Fischer, A. (2025). *Connecting the dots with Causal Attitude Network (CAN): A psychological network approach to populist attitudes, nativism, conspiracy mentality and threat appraisals*. *Measurement: Interdisciplinary Research and Perspectives, 23*(4), 393–417. [https://doi.org/10.1080/15366367.2024.2363718](https://doi.org/10.1080/15366367.2024.2363718)

[3] Epskamp, S., Borsboom, D., & Fried, E. I. (2018). *Estimating psychological networks and their accuracy: A tutorial paper*. *Behavior Research Methods, 50*, 195–212. [https://doi.org/10.3758/s13428-017-0862-1](https://doi.org/10.3758/s13428-017-0862-1)

[4] Haslbeck, J. M. B., & Waldorp, L. J. (2020). *mgm: Estimating time-varying mixed graphical models in high-dimensional data*. *Journal of Statistical Software, 93*(8), 1–46. [https://doi.org/10.18637/jss.v093.i08](https://doi.org/10.18637/jss.v093.i08)
