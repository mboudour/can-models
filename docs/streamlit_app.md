# Streamlit interface: participant workflow

The Streamlit interface is a **configuration generator and local analysis launcher** for `can-models`. It is designed for datasets whose variable names do not resemble the ChatGPT example and therefore never assumes that a variable is called `Q15`, `country`, or anything else.

Run it from the repository root after installing the Python requirements.

```bash
sudo pip3 install -r requirements-streamlit.txt
streamlit run app/app.py
```

## How variable names are handled

After a participant uploads a CSV or Excel file, the app profiles every column: data type, non-missing count, missingness, number of unique values, and—where meaningful—numeric range. The participant then selects their own source columns as CAN nodes and assigns each a readable label and an attitude-system domain. The saved YAML configuration stores this mapping explicitly.

| User action | What the app saves | Why it matters |
|---|---|---|
| Select a raw column as a network node | `network.nodes[].id` | Tells the R analysis which original column to estimate as a network node. |
| Supply a readable node label | `network.nodes[].label` | Makes figures and tables understandable without changing the original data. |
| Select a CAN domain | `network.nodes[].domain` | Controls the conceptual colour grouping in network output. |
| Set an optional sample filter | `sample.filter` | Makes the analytic population reproducible. |
| Select a country/group variable | `comparisons.country.variable` | Enables country-network eligibility checks and, where possible, country analyses. |
| Select a candidate factor scale | `factor_models` | Activates CFA, EFA, and eligible country invariance checks. |

The current core estimator expects numeric item codes. If a participant has responses such as `Strongly disagree` / `Strongly agree`, the interface identifies them as non-numeric and does not mark the joint MGM as ready until the data have been recoded. It therefore separates **variable naming**, which the interface solves through mapping, from **response coding**, which must be statistically valid.

## Analysis eligibility and placeholders

The app presents an eligibility table before a computation is run. A row is marked **Ready** only when the uploaded data satisfy the relevant structural requirements. A **Placeholder** is a documented non-execution state: it names the missing requirement and prevents a calculation from being mistaken for a valid result.

| Computational family | Minimum requirement | Placeholder behaviour when not supported |
|---|---|---|
| Joint MGM / LASSO / EBIC network | At least three mapped numeric nodes and adequate complete cases | Reports missing node, numeric-coding, or sample-size requirement. |
| Centrality, bootstrap accuracy/stability, Walktrap communities | Eligible joint network | Marks diagnostic block unavailable until a core network exists. |
| CFA, country CFA, EFA, invariance | At least three coherent selected scale items; country analysis also needs adequate country groups | Explains that no latent scale or adequate group structure was supplied. |
| Original two-study NCT | Two independent comparable studies or waves | Always remains a placeholder for a single cross-sectional upload; the optional random split is labelled a methodological check only. |
| High/low subgroup networks | Numeric grouping variable not retained as a network node | Explains the overlap or absence of a grouping variable. |
| Country networks, all pairwise NCTs, and matrix correlations | Two or more eligible country/group samples | Reports number of eligible groups at the selected minimum sample size. |
| Country clustering and pooled cluster networks | Two or more country networks; three or more are preferable | Keeps the clustering module as a placeholder when network groups cannot be formed. |
| NetworkTree | Suitable moderators plus optional `NetworkTree` R package | Writes a status file if the package is not installed rather than silently omitting the procedure. |
| Chi-square and Cramér’s V checks | Two selected categorical variables | Reports that categorical variables must be selected. |

## Reproducible run bundle

Selecting **Create configuration and run bundle** writes a separate directory under `user_runs/`. It contains the original upload, generated `config.yml`, a variable profile, a SHA-256 checksum manifest, console logs, and generated R outputs. The app does not overwrite the bundled ChatGPT example data or its configuration.

The participant can download the YAML configuration and rerun it outside the interface:

```bash
Rscript scripts/validate_config.R --config user_runs/<run-id>/config.yml
Rscript scripts/run_core_analysis.R --config user_runs/<run-id>/config.yml
Rscript scripts/run_example.R --config user_runs/<run-id>/config.yml
```

The interface labels **Quick mode** as a feasibility check. Full bootstrap, exhaustive country NCT, and clustering workflows can be substantially slower and should be chosen only after the mapping and core network have been validated.

> **Interpretive limit.** The interface implements a CAN-informed workflow, not an automatic causal-inference engine. Cross-sectional network edges are conditional associations. Directional causal claims require an appropriate longitudinal or experimental design.
