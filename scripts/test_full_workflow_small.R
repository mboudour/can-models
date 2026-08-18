#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))
source(file.path(getwd(), "R", "04_diagnostics.R"))
source(file.path(getwd(), "R", "05_factor.R"))
source(file.path(getwd(), "R", "06_compare.R"))
source(file.path(getwd(), "R", "07_country.R"))
source(file.path(getwd(), "R", "08_cluster.R"))
source(file.path(getwd(), "R", "09_networktree.R"))
source(file.path(getwd(), "R", "10_context.R"))

config <- read_can_config("config/chatgpt_example.yml")
# A compact real-data subset keeps the smoke test tractable while exercising every module.
config$network$nodes <- config$network$nodes[seq_len(12L)]
config$factor_models <- list()
config$bootstrapping$edge_bootstrap_iterations <- 1L
config$bootstrapping$case_drop_bootstrap_iterations <- 1L
config$community_detection$bootstrap_consensus_iterations <- 1L
config$comparisons$country$nct_iterations <- 2L
config$comparisons$country$minimum_n <- 75L
config$audit$mardia_max_n <- 500L
config$output$computations_dir <- "new_computations/full_workflow_small"
config$output$figures_dir <- "figures/full_workflow_small"

prepared <- prepare_can_data(config)
country_variable <- config$comparisons$country$variable
available <- prepared$primary_context |>
  dplyr::filter(!is.na(.data[[country_variable]])) |>
  dplyr::count(.data[[country_variable]], name = "n") |>
  dplyr::arrange(dplyr::desc(.data$n)) |>
  dplyr::slice_head(n = 3) |>
  dplyr::pull(1)
set.seed(config$project$seed)
selected_rows <- unlist(lapply(available, function(country) {
  rows <- which(prepared$primary_context[[country_variable]] == country)
  sample(rows, size = min(100L, length(rows)), replace = FALSE)
}))
prepared$primary_data <- prepared$primary_data[selected_rows, , drop = FALSE]
prepared$primary_context <- prepared$primary_context[selected_rows, , drop = FALSE]
prepared$node_data <- prepared$primary_data

write_data_audit(prepared, config)
factor_results <- run_factor_workflow(prepared, config)
primary <- run_primary_network(prepared, config)
diagnostics <- run_diagnostics_workflow(prepared, primary, config)
split_sample <- run_split_sample_comparison(prepared, config)
if (!is.null(split_sample)) save_comparison(split_sample, "split_sample", config)
use_frequency <- run_use_frequency_comparison(prepared, config)
country_workflow <- run_country_networks(prepared, config)
country_clustering <- cluster_country_networks(country_workflow, prepared, config)
networktree <- run_networktree_workflow(prepared, config)
context <- run_contextual_associations(prepared, config)

result <- list(
  primary = primary,
  diagnostics = diagnostics,
  split_sample = split_sample,
  use_frequency = use_frequency,
  country_workflow = country_workflow,
  country_clustering = country_clustering,
  networktree = networktree,
  contextual_associations = context,
  factor_results = factor_results
)
saveRDS(result, "new_computations/full_workflow_small/full_workflow_small.rds")
cat("Small end-to-end full workflow test completed.\n")
