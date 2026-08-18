#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))
source(file.path(getwd(), "R", "04_diagnostics.R"))
source(file.path(getwd(), "R", "06_compare.R"))

config <- read_can_config("config/chatgpt_example.yml")
config$bootstrapping$edge_bootstrap_iterations <- 2L
config$bootstrapping$case_drop_bootstrap_iterations <- 2L
config$comparisons$country$nct_iterations <- 2L
config$output$computations_dir <- "new_computations/component_test"
config$output$figures_dir <- "figures/component_test"
prepared <- prepare_can_data(config)
set.seed(config$project$seed)
subset_index <- sample.int(nrow(prepared$primary_data), 750L)
data <- prepared$primary_data[subset_index, , drop = FALSE]
first <- data[seq_len(375L), , drop = FALSE]
second <- data[376:750, , drop = FALSE]

bootstrap <- run_bootnet_diagnostics(data, config)
save_bootnet_diagnostics(bootstrap, config)
nct <- run_nct(first, second, config, "component_a", "component_b")
comparison <- list(matrix_correlation = tibble::tibble(network_a = "component_a", network_b = "component_b", adjacency_correlation = NA_real_, p_value = NA_real_, n_edges = NA_integer_, global_strength_a = NA_real_, global_strength_b = NA_real_, density_a = NA_real_, density_b = NA_real_), nct = nct)
save_comparison(comparison, "component_nct", config)
cat("Component test completed.\n")
