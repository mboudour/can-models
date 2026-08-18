#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
if (is.na(config_index) || config_index == length(args)) {
  stop("Usage: Rscript scripts/validate_config.R --config config/chatgpt_example.yml", call. = FALSE)
}
config_path <- args[[config_index + 1L]]

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))

config <- read_can_config(config_path)
raw_data <- read_can_data(config)
validate_analysis_variables(raw_data, config)
prepared <- prepare_can_data(config)
write_data_audit(prepared, config)

cat("Configuration valid.\n")
cat("Project: ", config$project$id, "\n", sep = "")
cat("Raw rows: ", nrow(prepared$raw), "\n", sep = "")
cat("Filtered rows: ", nrow(prepared$filtered), "\n", sep = "")
cat("Primary-network complete cases: ", nrow(prepared$primary_data), "\n", sep = "")
cat("Nodes: ", ncol(prepared$primary_data), "\n", sep = "")
