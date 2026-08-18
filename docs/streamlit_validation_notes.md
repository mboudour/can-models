# Streamlit validation notes

## Initial launch check

The application was launched locally with Streamlit on port 8501 and exposed for inspection. The landing page rendered the expected title, scope statement, cross-sectional causal-inference guardrail, and prompt to upload a CSV or Excel dataset. The browser inspection session then returned to a blank page before upload controls could be exercised, so upload/mapping behaviour is additionally tested through the repository’s local smoke-test scripts and static configuration checks.

## Primary network figure check

The completed ChatGPT example primary MGM was regenerated from its saved analysis object after a visual review. The original automatically generated legend repeated every full node label and obscured the right half of the graph. The revised figure uses numbered nodes, a concise domain legend, and a `network_node_key.csv` output that maps each number to the source variable, human-readable label, and CAN domain. The revised 30-node network is readable at full resolution and preserves the complete node mapping in a machine-readable companion table.
