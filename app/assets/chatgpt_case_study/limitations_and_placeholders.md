# Why some Abadi et al. elements are not reported as ChatGPT results

The ChatGPT case study is a **computational CAN workflow demonstration**, not a substantive reproduction of Abadi et al.’s findings on populism and nativism. The following distinctions are displayed alongside the full replication ledger.

| Status | Meaning in this case study | Paper elements affected |
|---|---|---|
| **Completed** | A computation was executed with the specified ChatGPT configuration and its result is available for inspection. | Data audit, Mardia diagnostic, 30-node joint MGM, edge table, centrality, predictability, Q24 candidate-scale CFA/EFA/invariance, and bounded case-study conclusions. |
| **Not applicable: missing construct or design** | The ChatGPT dataset does not contain a required variable or design component. No substitute is presented as a literal replication. | Two-study NCT; populist-attitude scale; nativism scale; symbolic/realistic threat; conspiracy mentality; left–right political orientation; Abadi’s political-country and translation conclusions. |
| **Runtime deferred** | The computation is implemented and configured, but the fully configured static run did not complete after more than three hours on a single CPU core. This is a computational-resource limitation, not evidence of no effect or no data. | 100 community bootstrap refits; 250 edge and 250 case-drop bootstrap refits; use-frequency MGM comparison; country MGMs; all pairwise country NCTs; country clustering; NetworkTree; contextual categorical checks. |
| **Cross-sectional inference limit** | The available data cannot identify temporal ordering or directed causal effects. | Every network edge, centrality statement, and any potential country comparison. |

## Variables and attributes that are absent

The Ravšelj et al. survey does **not** provide item-level measures of populist attitudes, nativism, realistic threat, symbolic threat, conspiracy mentality, political-left/centre/right placement, or the two independent studies that underpin Abadi et al.’s RQ1–RQ4 conclusions. It also does not reproduce the paper’s matched European-country sampling frame, translation procedures, or political context. Consequently, no result in this app is interpreted as evidence about those substantive topics.

## What the executed ChatGPT case study can support

The executed 30-node network describes conditional associations among selected ChatGPT perceptions, evaluations, affect, use, and expected educational/labour outcomes in the configured complete-case sample. It does not identify directional effects, intervention targets, or population-level country differences. The full offline workflow command is retained in the repository for execution in a Docker/R environment with sufficient compute capacity.
