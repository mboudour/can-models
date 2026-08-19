#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))
source(file.path(getwd(), "R", "04_diagnostics.R"))

config <- read_can_config("config/ess_cronos3_sogreen_w6.yml")
config$bootstrapping$edge_bootstrap_iterations <- 2L
config$bootstrapping$case_drop_bootstrap_iterations <- 2L
config$bootstrapping$n_cores <- 2L
config$community_detection$bootstrap_consensus_iterations <- 2L
config$output$computations_dir <- tempfile("ess_mixed_diagnostics_")
config$output$figures_dir <- tempfile("ess_mixed_diagnostics_figures_")
config$output$report_dir <- tempfile("ess_mixed_diagnostics_reports_")

prepared <- prepare_can_data(config)
primary <- run_primary_network(prepared, config)
diagnostics <- run_diagnostics_workflow(prepared, primary, config)
if (!is.null(diagnostics$bootnet$error)) stop(diagnostics$bootnet$error, call. = FALSE)
stopifnot(!inherits(diagnostics$bootnet$edge_boot, "error"))
stopifnot(!inherits(diagnostics$bootnet$case_boot, "error"))

cat("ESS mixed-level diagnostics test passed.\n")
