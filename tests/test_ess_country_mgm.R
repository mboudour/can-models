#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))
source(file.path(getwd(), "R", "06_compare.R"))
source(file.path(getwd(), "R", "07_country.R"))

config <- read_can_config("config/ess_cronos3_sogreen_w6.yml")
config$comparisons$country$minimum_n <- 1100L
config$comparisons$country$all_pairwise_nct <- FALSE
config$output$computations_dir <- tempfile("ess_country_mgm_")
config$output$figures_dir <- tempfile("ess_country_mgm_figures_")
config$output$report_dir <- tempfile("ess_country_mgm_reports_")

prepared <- prepare_can_data(config)
workflow <- run_country_networks(prepared, config)
stopifnot(nrow(workflow$eligible_groups) == 1L)
stopifnot(workflow$eligible_groups$status[[1]] == "completed")
stopifnot(workflow$networks[[1]]$result$estimator == "mgm_lasso_ebic")

fr_index <- prepared$primary_context$cntry == "FR"
fr_data <- refresh_mgm_subset_metadata(prepared$primary_data[fr_index, , drop = FALSE], config)
fr_result <- estimate_mgm_network(fr_data, config)
stopifnot(fr_result$estimator == "mgm_lasso_ebic")

cat("ESS country MGM estimator test passed.\n")
