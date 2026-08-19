#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L || args[[1]] != "--config") {
  stop("Usage: Rscript scripts/run_chatgpt_focus_spearman.R --config <config.yml>", call. = FALSE)
}
source("R/00_packages.R")
source("R/01_config.R")
source("R/02_data.R")
source("R/03_network.R")

config <- read_can_config(args[[2]])
prepared <- prepare_can_data(config)
write_data_audit(prepared, config)
result <- estimate_ggm_spearman_network(prepared$primary_data, config)
saved <- save_network_result(result, "focused_ggm_spearman", config, prepared$node_map)
print(saved$summary)
