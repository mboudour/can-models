#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
require_can_package("readr")
require_can_package("dplyr")
require_can_package("tibble")

base <- "new_computations/ess_cronos3_green_transition_w6"
primary <- readr::read_csv(file.path(base, "networks", "primary_mgm", "network_summary.csv"), show_col_types = FALSE)
centrality <- readr::read_csv(file.path(base, "networks", "primary_mgm", "centrality.csv"), show_col_types = FALSE)
edges <- readr::read_csv(file.path(base, "networks", "primary_mgm", "edge_table.csv"), show_col_types = FALSE)
split <- readr::read_csv(file.path(base, "comparisons", "split_sample", "adjacency_correlation.csv"), show_col_types = FALSE)
split_nct <- readr::read_csv(file.path(base, "comparisons", "split_sample", "nct_summary.csv"), show_col_types = FALSE)
country <- readr::read_csv(file.path(base, "country_networks", "eligible_countries.csv"), show_col_types = FALSE)
nct <- readr::read_csv(file.path(base, "country_networks", "pairwise_nct_summary.csv"), show_col_types = FALSE)
diagnostic <- readr::read_csv(file.path(base, "diagnostics", "publication_gate_diagnostic_summary.csv"), show_col_types = FALSE)
communities <- readr::read_csv(file.path(base, "diagnostics", "walktrap_communities.csv"), show_col_types = FALSE)
coassignment <- readr::read_csv(file.path(base, "diagnostics", "bootstrap_community_coassignment.csv"), show_col_types = FALSE)

country_network_dirs <- list.dirs(file.path(base, "networks"), recursive = FALSE, full.names = TRUE)
country_network_dirs <- country_network_dirs[grepl("country_", basename(country_network_dirs)) & !grepl("country_cluster", basename(country_network_dirs))]
country_summaries <- dplyr::bind_rows(lapply(country_network_dirs, function(directory) {
  data <- readr::read_csv(file.path(directory, "network_summary.csv"), show_col_types = FALSE)
  data$country <- sub("^country_", "", basename(directory))
  data
}))

summary <- tibble::tibble(
  pooled_n = primary$n[[1]],
  pooled_nodes = primary$p[[1]],
  pooled_density = primary$density[[1]],
  pooled_nonzero_edges = primary$nonzero_edges[[1]],
  split_adjacency_correlation = split$adjacency_correlation[[1]],
  split_structure_invariance_p = split_nct$structure_invariance_p[[1]],
  split_global_strength_p = split_nct$global_strength_p[[1]],
  completed_countries = sum(country$status == "completed"),
  country_density_min = min(country_summaries$density),
  country_density_max = max(country_summaries$density),
  country_nct_pairs = nrow(nct),
  country_nct_structure_fdr_lt_05 = sum(nct$structure_p_fdr < 0.05, na.rm = TRUE),
  country_nct_global_strength_fdr_lt_05 = sum(nct$global_strength_p_fdr < 0.05, na.rm = TRUE),
  centrality_stability_coefficient = diagnostic$centrality_stability_coefficient[[1]],
  walktrap_communities = diagnostic$walktrap_communities[[1]],
  community_pairs_coassigned_80_or_more = sum(coassignment$coassignment >= 0.80, na.rm = TRUE)
)
readr::write_csv(summary, file.path(base, "publication_gate_summary.csv"))
readr::write_csv(dplyr::arrange(centrality, dplyr::desc(.data$Strength)), file.path(base, "top_nodes_by_strength.csv"))
readr::write_csv(dplyr::arrange(edges, dplyr::desc(abs(.data$weight))), file.path(base, "top_edges_by_absolute_weight.csv"))
print(summary)
