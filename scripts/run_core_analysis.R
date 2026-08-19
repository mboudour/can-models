#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
if (is.na(config_index) || config_index == length(args)) {
  stop("Usage: Rscript scripts/run_core_analysis.R --config config/abadi_study2_public.yml", call. = FALSE)
}
config_path <- args[[config_index + 1L]]

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

saveRDS(list(config = config, prepared = prepared, primary = primary), file.path(config_output_path(config, "computations_dir"), "core_analysis.rds"))
cat("Core CAN analysis completed.\n")
cat("Primary-network sample size: ", primary$result$n, "\n", sep = "")
cat("Non-zero edges: ", nrow(primary$result$edge_table), "\n", sep = "")
