#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
if (is.na(config_index) || config_index == length(args)) {
  stop("Usage: Rscript scripts/run_example.R --config config/abadi_study2_public.yml", call. = FALSE)
}
config_path <- args[[config_index + 1L]]

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

config <- read_can_config(config_path)
set.seed(config$project$seed)
prepared <- prepare_can_data(config)
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
  configuration = config,
  prepared = prepared,
  factor_results = factor_results,
  primary = primary,
  diagnostics = diagnostics,
  split_sample = split_sample,
  use_frequency = use_frequency,
  country_workflow = country_workflow,
  country_clustering = country_clustering,
  networktree = networktree,
  contextual_associations = context
)
output_path <- file.path(config_output_path(config, "computations_dir"), "full_analysis.rds")
saveRDS(result, output_path)
cat("Full configured CAN workflow completed.\n")
cat("Result object: ", output_path, "\n", sep = "")
