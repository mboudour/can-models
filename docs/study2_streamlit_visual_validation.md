# Study 2 Streamlit visual validation

**Validated locally:** 2026-08-18

The locally served Streamlit application was inspected in a browser after the ChatGPT workspace was removed. The default workspace displayed:

- the heading **“Abadi et al.: public Study 2 replication”**;
- source metrics of 2,031 public CSV records, 2,030 analysed Study 2 cases, 29 original network nodes, and four original countries;
- source-level logged transformations and the 29-node original-variable table;
- no ChatGPT case-study label, metric, or content; and
- a visible **Complete Abadi et al. replication ledger** with separate Executed, Pending, and Access-gated statuses.

The ledger visibly identifies the executed Study 2 sample preparation and joint network, pending Study 2 diagnostic/group/country outputs, restricted Study 1, and access-gated cross-study comparison. This confirms that the interface no longer presents the unrelated ChatGPT survey as an Abadi et al. replication.

The RQ1 joint-network tab was also inspected. It rendered the 29-node original Study 2 MGM figure, the joint-network summary (*N* = 2,030; 29 nodes; 378 non-zero edges), centrality table, edge table, and Mardia output without a broken image or missing-table error. The figure uses numbered nodes that map to the original-variable node key in the Study 2 scope tab.

## BYOD refinement validation

The revised BYOD landing view was inspected in a browser. The left sidebar contains a visible **“← Return to Study 2 replication”** control above the upload section and an optional **Study design** selector defaulting to **“Not specified.”** The main BYOD landing content shows only the upload prompt; it no longer displays a blanket cross-sectional guardrail before any data are uploaded or a design is selected.

## Ravšelj et al. ChatGPT worked-example validation

**Validated locally:** 2026-08-19

The new **Ravšelj et al. ChatGPT example** workspace rendered from the top-level application selector. It visibly separates itself from the Abadi replication, presents the source-cited PLOS ONE article and Mendeley Data Version 2 links, and reports 23,218 public records, 16,010 prior ChatGPT users, 12,175 focused complete cases, and 16 focused nodes. The opening warning explicitly labels the historical 31-node network as a fully connected diagnostic and prohibits centrality, bridge, causal, or intervention claims. The data/design tab displayed the labels and six CAN domains from the focused configuration without empty labels or default-only colouring.

Visual validation also confirmed that the source citation links, workspace tabs, metrics, explanatory warning, and node table render without overflow or missing assets.
