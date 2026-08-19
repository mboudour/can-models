#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))
source(file.path(getwd(), "R", "04_diagnostics.R"))

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

prepared <- prepare_can_data(config)
primary <- run_primary_network(prepared, config)
diagnostics <- run_diagnostics_workflow(prepared, primary, config)
output_path <- file.path(config_output_path(config, "computations_dir"), "diagnostics", "diagnostics_stage.rds")
saveRDS(diagnostics, output_path)
cat("ESS Green Transition diagnostics stage completed.\n")
cat("Diagnostic object: ", output_path, "\n", sep = "")
