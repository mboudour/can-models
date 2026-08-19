# Streamlit application: original Study 2 replication, ChatGPT example, and participant workflow

The Streamlit application has three distinct workspaces. **Abadi et al. Study 2 replication** is the default public view. It uses the authors’ original public April 2020 four-country data and Qualtrics codebook, rather than a topic-adjacent example. It displays the Study 2 sample flow, logged transformations, original 29-node mixed graphical model, centrality and edge exports, scale diagnostics, and a transparent paper-wide ledger. **Ravšelj et al. ChatGPT example** is a separately labelled, source-cited application of the reusable workflow to the public global survey of higher-education students’ ChatGPT perceptions. It does not claim to replicate Abadi et al.; it exposes the dense-network diagnostic, focused-model sensitivity, and publication-readiness boundary. **Bring your own data** is a separate configuration generator and local analysis launcher; it never assumes a participant’s raw variables follow any predefined naming convention.

Run the application from the repository root after installing the Python requirements.

```bash
sudo pip3 install -r requirements-streamlit.txt
streamlit run app/app.py
```

## Original Study 2 replication ledger

The public source is the UvA Figshare dataset collected in April 2020 in Germany, Spain, the Netherlands, and the United Kingdom. It includes the original country, demographics, realistic/symbolic threat, populist-attitude, nativism, and conspiracy-mentality items used for the 29-node Study 2 network. The codebook identifies reverse-coded items with an asterisk, and the application exposes each applied transformation rather than applying it silently.

The application classifies every paper component as one of three states:

| State | Meaning |
|---|---|
| **Executed** | The public Study 2 data and documented procedure have been run; the result is displayed or downloadable. |
| **Pending** | The public Study 2 data support the computation, but an intensive run or an exact appendix decision rule is still required. No substantive result is implied. |
| **Access-gated** | The computation needs the restricted 2019 Study 1 data, which are not bundled or reconstructed. |

The public Study 2 joint MGM, sample preparation, Mardia diagnostic, centrality/predictability exports, and PA/nativism CFA/EFA workflow are executed. The seven-item one-factor PA model fits poorly, and the interface therefore does not silently treat it as a validated score for high/low PA networks. The original Study 2 data support RQ2–RQ4, including political-orientation and country comparisons, but the app labels those modules as pending until the published grouping rules are verified and their intensive computations complete.

The 2019 15-country Study 1 data are restricted by the article’s H2020/GDPR data-availability statement. The application presents an email-free required-materials checklist for enabling the access-gated module. It does not present a fabricated Study 1 network, a cross-study NCT, or two-study substantive conclusions. The detailed boundary is in [abadi_genuine_replication_scope.md](abadi_genuine_replication_scope.md).

## Ravšelj et al. ChatGPT worked example

The ChatGPT workspace cites both the companion paper—Ravšelj et al., *Higher education students’ perceptions of ChatGPT: A global study of early reactions*, PLOS ONE (2025), [10.1371/journal.pone.0315011](https://doi.org/10.1371/journal.pone.0315011)—and the public Version 2 data record, [10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2). It filters to prior users (`Q13 = 1`) and retains 16,010 users before complete-case handling.

The completed 31-node BYOD run is deliberately shown as a diagnostic: it retained every possible edge and is therefore not a sparse, interpretable CAN result. The workspace does not report its centrality ranking as a substantive result. A smaller labelled sensitivity model is included to show that simply reducing the node count or switching estimator does not automatically resolve dense-network selection. The complete assessment is available in [chatgpt_ravselj_worked_example.md](chatgpt_ravselj_worked_example.md).

## How participant variable names and study design are handled

After a participant uploads a CSV or Excel file, the app profiles every column: data type, non-missing count, missingness, unique values, and—where meaningful—numeric range. The participant then selects their own source columns as CAN nodes and assigns each a readable label and an attitude-system domain. The saved YAML configuration stores this mapping explicitly.

The BYOD landing page does not assume that every uploaded dataset is cross-sectional. Users may optionally record whether their study is cross-sectional, longitudinal/panel, or experimental/quasi-experimental. Interpretation guidance is shown only after data upload and reflects that selection. The current core workflow estimates network structure; it does not automatically estimate temporal, within-person, or intervention effects merely because a longitudinal or experimental dataset is uploaded.

| User action | What the app saves | Why it matters |
|---|---|---|
| Select a raw column as a network node | `network.nodes[].id` | Tells the R analysis which original column to estimate as a network node. |
| Supply a readable node label | `network.nodes[].label` | Makes figures and tables understandable without changing the original data. |
| Select a CAN domain | `network.nodes[].domain` | Controls the conceptual colour grouping in network output. |
| Set an optional sample filter | `sample.filter` | Makes the analytic population reproducible. |
| Select a country/group variable | `comparisons.country.variable` | Enables country-network eligibility checks and, where possible, country analyses. |
| Select a candidate factor scale | `factor_models` | Activates CFA, EFA, and eligible country invariance checks. |

The core estimator expects numeric item codes. If a participant has responses such as `Strongly disagree` / `Strongly agree`, the interface identifies them as non-numeric and does not mark the joint MGM as ready until the data have been recoded. It therefore separates **variable naming**, which the interface solves through mapping, from **response coding**, which must be statistically valid.

## Analysis eligibility and placeholders

The app presents an eligibility table before a computation is run. A row is marked **Ready** only when the uploaded data satisfy the relevant structural requirements. A **Placeholder** is a documented non-execution state: it names the missing requirement and prevents a calculation from being mistaken for a valid result.

| Computational family | Minimum requirement | Placeholder behaviour when not supported |
|---|---|---|
| Joint MGM / LASSO / EBIC network | At least three mapped numeric nodes and adequate complete cases | Reports missing node, numeric-coding, or sample-size requirement. |
| Centrality, bootstrap accuracy/stability, Walktrap communities | Eligible joint network | Marks diagnostic block unavailable until a core network exists. |
| CFA, country CFA, EFA, invariance | At least three coherent selected scale items; country analysis also needs adequate country groups | Explains that no latent scale or adequate group structure was supplied. |
| Original two-study NCT | Two independent comparable studies or waves | Always remains a placeholder for a single cross-sectional upload; a random split is not treated as a substitute. |
| High/low subgroup networks | Numeric grouping variable not retained as a network node | Explains the overlap or absence of a grouping variable. |
| Country networks, all pairwise NCTs, and matrix correlations | Two or more eligible country/group samples | Reports number of eligible groups at the selected minimum sample size. |
| Country clustering and pooled cluster networks | Two or more country networks; three or more are preferable | Keeps the clustering module as a placeholder when network groups cannot be formed. |
| NetworkTree | Suitable moderators plus optional `NetworkTree` R package | Writes a status file if the package is not installed rather than silently omitting the procedure. |
| Chi-square and Cramér’s V checks | Two selected categorical variables | Reports that categorical variables must be selected. |

## Reproducible run bundle

Selecting **Create configuration and run bundle** writes a separate directory under `user_runs/`. It contains the original upload, generated `config.yml`, a variable profile, a SHA-256 checksum manifest, console logs, and generated R outputs. The app does not overwrite the original Study 2 source data or its configuration.

The participant can download the YAML configuration and rerun it outside the interface:

```bash
Rscript scripts/validate_config.R --config user_runs/<run-id>/config.yml
Rscript scripts/run_core_analysis.R --config user_runs/<run-id>/config.yml
Rscript scripts/run_example.R --config user_runs/<run-id>/config.yml
```

The interface labels **Quick mode** as a feasibility check. Full bootstrap, exhaustive country NCT, and clustering workflows can be substantially slower and should be selected only after the mapping and core network have been validated.

> **Interpretive limit.** The interface implements a CAN-informed workflow, not an automatic causal-inference engine. The interpretation shown in a run follows the user-selected study design. Cross-sectional network edges are conditional associations; longitudinal and experimental causal claims require a design-appropriate model and estimand.
