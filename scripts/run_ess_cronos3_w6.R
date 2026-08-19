#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
config_path <- if (is.na(config_index)) {
  "config/ess_cronos3_sogreen_w6.yml"
} else {
  if (config_index == length(args)) stop("Usage: Rscript scripts/run_ess_cronos3_w6.R [--config path/to/config.yml]", call. = FALSE)
  args[[config_index + 1L]]
}

verification <- system2(
  "Rscript",
  c("--vanilla", "scripts/verify_ess_cronos3_source.R", "--config", config_path),
  stdout = TRUE,
  stderr = TRUE
)
verification_status <- attr(verification, "status")
if (is.null(verification_status)) verification_status <- 0L
cat(paste(verification, collapse = "\n"), "\n", sep = "")
if (verification_status != 0L) stop("Source verification failed; analysis was not started.", call. = FALSE)

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))
source(file.path(getwd(), "R", "05_factor.R"))

config <- read_can_config(config_path)
prepared <- prepare_can_data(config)
write_data_audit(prepared, config)
run_factor_workflow(prepared, config)
primary <- run_primary_network(prepared, config)

saveRDS(
  list(config = config, prepared = prepared, primary = primary),
  file.path(config_output_path(config, "computations_dir"), "core_analysis.rds")
)
cat("ESS CRONOS-3 Wave 6 core CAN analysis completed.\n")
cat("Primary-network sample size: ", primary$result$n, "\n", sep = "")
cat("Non-zero edges: ", nrow(primary$result$edge_table), "\n", sep = "")
