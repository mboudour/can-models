#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L || args[[1]] != "--config") {
  stop("Usage: Rscript scripts/test_dynamic_levels.R --config <config.yml>", call. = FALSE)
}
config_path <- args[[2]]
source("R/00_packages.R")
source("R/01_config.R")
source("R/02_data.R")
source("R/03_network.R")

config <- read_can_config(config_path)
prepared <- prepare_can_data(config)
levels <- attr(prepared$primary_data, "mgm_levels")
stopifnot(length(levels) == ncol(prepared$primary_data))
stopifnot(all(levels >= 2L))

set.seed(config$project$seed)
index <- sample.int(nrow(prepared$primary_data), min(1000L, nrow(prepared$primary_data)))
test_data <- prepared$primary_data[index, , drop = FALSE]
attr(test_data, "mgm_levels") <- levels
attr(test_data, "mgm_types") <- attr(prepared$primary_data, "mgm_types")
result <- estimate_mgm_network(test_data, config)

cat("Dynamic-level MGM test passed.\n")
cat("Nodes:", ncol(test_data), "\n")
cat("Observed effective levels:", paste(levels, collapse = ","), "\n")
cat("Nonzero edges:", nrow(result$edge_table), "\n")
