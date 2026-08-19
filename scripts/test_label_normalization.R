#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L || args[[1]] != "--config") {
  stop("Usage: Rscript scripts/test_label_normalization.R --config <config.yml>", call. = FALSE)
}
source("R/00_packages.R")
source("R/01_config.R")
source("R/02_data.R")
source("R/03_network.R")

config <- read_can_config(args[[2]])
config$network$nodes[[1]]$label <- ""
config$network$nodes[[2]]$label <- ""
config$network$nodes[[3]]$label <- "Duplicated label"
config$network$nodes[[4]]$label <- "Duplicated label"
prepared <- prepare_can_data(config)
labels <- prepared$node_map$label
stopifnot(all(nzchar(labels)), !anyDuplicated(labels))

set.seed(config$project$seed)
index <- sample.int(nrow(prepared$primary_data), min(500L, nrow(prepared$primary_data)))
test_data <- prepared$primary_data[index, , drop = FALSE]
attr(test_data, "mgm_levels") <- attr(prepared$primary_data, "mgm_levels")
attr(test_data, "mgm_types") <- attr(prepared$primary_data, "mgm_types")
result <- estimate_mgm_network(test_data, config)
stopifnot(!is.null(result$adjacency))
cat("Label normalization MGM test passed.\n")
cat("Normalized labels:", paste(head(labels, 4), collapse = " | "), "\n")
