#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
require_can_package("qgraph")
require_can_package("readr")
require_can_package("dplyr")
require_can_package("jsonlite")

base <- "new_computations/ess_cronos3_green_transition_w6"
asset_dir <- "app/assets/ess_cronos3_green_transition_w6"
dir.create(asset_dir, recursive = TRUE, showWarnings = FALSE)

adjacency_table <- readr::read_csv(file.path(base, "networks", "primary_mgm", "adjacency_matrix.csv"), show_col_types = FALSE)
adjacency <- as.matrix(adjacency_table[, -1])
rownames(adjacency) <- adjacency_table[[1]]
colnames(adjacency) <- names(adjacency_table)[-1]
node_key <- readr::read_csv(file.path(base, "networks", "primary_mgm", "network_node_key.csv"), show_col_types = FALSE)
centrality <- readr::read_csv(file.path(base, "top_nodes_by_strength.csv"), show_col_types = FALSE)
top_edges <- readr::read_csv(file.path(base, "top_edges_by_absolute_weight.csv"), show_col_types = FALSE)
gate <- readr::read_csv(file.path(base, "publication_gate_summary.csv"), show_col_types = FALSE)
clusters <- readr::read_csv(file.path(base, "country_clustering", "cluster_assignments.csv"), show_col_types = FALSE)
nct <- readr::read_csv(file.path(base, "country_networks", "pairwise_nct_summary.csv"), show_col_types = FALSE)

rownames(adjacency) <- node_key$label
colnames(adjacency) <- node_key$label
palettes <- c(
  "Environmental encounter" = "#2A9D8F",
  "Affective appraisal and responsibility" = "#E76F51",
  "Institutional capacity and policy legitimacy" = "#457B9D",
  "Personal transition-cost concerns" = "#9C6644",
  "Green behaviour and engagement" = "#6A994E"
)
colors <- unname(palettes[node_key$domain])
colors[is.na(colors)] <- "#6C757D"

png(file.path(asset_dir, "pooled_network.png"), width = 2400, height = 1800, res = 180)
qgraph::qgraph(
  adjacency,
  layout = "spring",
  labels = node_key$label,
  color = colors,
  vsize = 7,
  label.cex = 0.68,
  cut = 0.12,
  minimum = 0.06,
  edge.color = "#6C757D",
  legend = FALSE,
  title = "ESS CRONOS-3 Wave 6: Pooled 21-node Green Transition MGM"
)
dev.off()

top_nodes <- head(centrality, 10L)
png(file.path(asset_dir, "top_node_strength.png"), width = 1800, height = 1200, res = 180)
par(mar = c(5, 15, 4, 2))
barplot(rev(top_nodes$Strength), names.arg = rev(top_nodes$node), horiz = TRUE, las = 1, col = "#457B9D", border = NA, main = "Top pooled nodes by strength", xlab = "Strength")
dev.off()

country_dirs <- list.dirs(file.path(base, "networks"), recursive = FALSE, full.names = TRUE)
country_dirs <- country_dirs[grepl("country_", basename(country_dirs)) & !grepl("country_cluster", basename(country_dirs))]
country_summaries <- dplyr::bind_rows(lapply(country_dirs, function(directory) {
  data <- readr::read_csv(file.path(directory, "network_summary.csv"), show_col_types = FALSE)
  data$country <- sub("^country_", "", basename(directory))
  data
})) |>
  dplyr::arrange(.data$density)

png(file.path(asset_dir, "country_density.png"), width = 1800, height = 1100, res = 180)
par(mar = c(5, 5, 4, 2))
barplot(country_summaries$density, names.arg = country_summaries$country, col = "#2A9D8F", border = NA, ylim = c(0, max(country_summaries$density) * 1.15), main = "Country MGM density", ylab = "Non-zero edge proportion")
abline(h = gate$pooled_density[[1]], lty = 2, col = "#B23A48", lwd = 2)
legend("topleft", legend = "Pooled density", lty = 2, col = "#B23A48", bty = "n")
dev.off()

nct_summary <- list(
  completed_pairs = nrow(nct),
  fdr_structure_differences = sum(nct$structure_p_fdr < 0.05, na.rm = TRUE),
  fdr_global_strength_differences = sum(nct$global_strength_p_fdr < 0.05, na.rm = TRUE)
)
readr::write_csv(top_nodes, file.path(asset_dir, "top_nodes.csv"))
readr::write_csv(top_edges, file.path(asset_dir, "top_edges.csv"))
readr::write_csv(country_summaries, file.path(asset_dir, "country_network_summaries.csv"))
readr::write_csv(clusters, file.path(asset_dir, "country_cluster_assignments.csv"))
readr::write_csv(gate, file.path(asset_dir, "publication_gate_summary.csv"))
jsonlite::write_json(nct_summary, file.path(asset_dir, "country_nct_summary.json"), auto_unbox = TRUE, pretty = TRUE)
cat("ESS Streamlit assets created in ", asset_dir, "\n", sep = "")
