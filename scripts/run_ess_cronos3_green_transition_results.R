#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))
source(file.path(getwd(), "R", "05_factor.R"))
source(file.path(getwd(), "R", "06_compare.R"))
source(file.path(getwd(), "R", "07_country.R"))
source(file.path(getwd(), "R", "08_cluster.R"))
source(file.path(getwd(), "R", "10_context.R"))

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
config_path <- if (is.na(config_index)) "config/ess_cronos3_sogreen_w6.yml" else args[[config_index + 1L]]

config <- read_can_config(config_path)
verification <- system2(
  "Rscript",
  c("--vanilla", "scripts/verify_ess_cronos3_source.R", "--config", config_path),
  stdout = TRUE,
  stderr = TRUE
)
if (!is.null(attr(verification, "status")) && attr(verification, "status") != 0L) stop("Official ESS source verification failed.", call. = FALSE)
cat(paste(verification, collapse = "\n"), "\n", sep = "")

set.seed(config$project$seed)
prepared <- prepare_can_data(config)
write_data_audit(prepared, config)
factor_results <- run_factor_workflow(prepared, config)
primary <- run_primary_network(prepared, config)
split_sample <- run_split_sample_comparison(prepared, config)
if (!is.null(split_sample)) save_comparison(split_sample, "split_sample", config)

# Country MGMs and clustering are saved independently of the expensive NCT matrix.
# The pairwise NCT stage is intentionally run by its own resumable script.
country_config <- config
country_config$comparisons$country$all_pairwise_nct <- FALSE
country_workflow <- run_country_networks(prepared, country_config)
country_clustering <- cluster_country_networks(country_workflow, prepared, country_config)
context <- run_contextual_associations(prepared, config)

result <- list(
  configuration = config,
  prepared = prepared,
  factor_results = factor_results,
  primary = primary,
  split_sample = split_sample,
  country_workflow = country_workflow,
  country_clustering = country_clustering,
  contextual_associations = context
)
output_path <- file.path(config_output_path(config, "computations_dir"), "results_stage.rds")
saveRDS(result, output_path)
cat("ESS Green Transition results stage completed.\n")
cat("Result object: ", output_path, "\n", sep = "")
