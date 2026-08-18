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
config$bootstrapping$edge_bootstrap_iterations <- 5L
config$bootstrapping$case_drop_bootstrap_iterations <- 5L
config$community_detection$bootstrap_consensus_iterations <- 2L
config$comparisons$country$nct_iterations <- 5L
config$comparisons$country$minimum_n <- 1000L
config$output$computations_dir <- "new_computations/smoke_test"
config$output$figures_dir <- "figures/smoke_test"

prepared <- prepare_can_data(config)
primary <- run_primary_network(prepared, config)
diagnostics <- run_diagnostics_workflow(prepared, primary, config)
split <- run_split_sample_comparison(prepared, config)
if (!is.null(split)) save_comparison(split, "split_sample", config)
use_frequency <- run_use_frequency_comparison(prepared, config)
countries <- run_country_networks(prepared, config)
clustering <- cluster_country_networks(countries, prepared, config)
networktree <- run_networktree_workflow(prepared, config)
context <- run_contextual_associations(prepared, config)

saveRDS(list(primary = primary, diagnostics = diagnostics, split = split, use_frequency = use_frequency, countries = countries, clustering = clustering, networktree = networktree, context = context), "new_computations/smoke_test/smoke_test.rds")
cat("Smoke test completed.\n")
