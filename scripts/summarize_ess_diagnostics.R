#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
input_path <- if (length(args)) args[[1]] else "new_computations/ess_cronos3_green_transition_w6/diagnostics/diagnostics_stage.rds"
output_path <- "new_computations/ess_cronos3_green_transition_w6/diagnostics/publication_gate_diagnostic_summary.csv"

source(file.path(getwd(), "R", "00_packages.R"))
require_can_package("bootnet")
requireNamespace("readr", quietly = TRUE)
requireNamespace("tibble", quietly = TRUE)

diagnostics <- readRDS(input_path)
edge_boot <- diagnostics$bootnet$edge_boot
case_boot <- diagnostics$bootnet$case_boot

edge_rows <- if (is.null(edge_boot$bootTable)) 0L else nrow(edge_boot$bootTable)
case_rows <- if (is.null(case_boot$bootTable)) 0L else nrow(case_boot$bootTable)
cor_stability <- tryCatch(bootnet::corStability(case_boot), error = function(error) NA_real_)

estimator_label <- diagnostics$bootnet$estimator_label
if (is.null(estimator_label)) estimator_label <- "not_recorded"
summary <- tibble::tibble(
  stability_estimator = estimator_label,
  edge_bootstrap_rows = edge_rows,
  case_bootstrap_rows = case_rows,
  centrality_stability_coefficient = cor_stability,
  walktrap_communities = length(unique(diagnostics$walktrap$community)),
  community_coassignment_pairs = nrow(diagnostics$community_consensus)
)
readr::write_csv(summary, output_path)
print(summary)
