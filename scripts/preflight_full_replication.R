#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
if (is.na(config_index) || config_index == length(args)) {
  stop("Usage: Rscript scripts/preflight_full_replication.R --config <path>", call. = FALSE)
}

config_path <- args[[config_index + 1L]]
source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))

config <- read_can_config(config_path)
prepared <- prepare_can_data(config)
country_var <- config$variables$country
use_var <- config$variables$use_frequency
out_dir <- file.path(config$output$computations_dir, "preflight")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

summary <- data.frame(
  measure = c("raw_rows", "filtered_rows", "primary_complete_cases", "mapped_nodes", "country_minimum_n", "country_variable", "use_frequency_variable"),
  value = c(
    nrow(prepared$raw),
    nrow(prepared$filtered),
    nrow(prepared$primary_data),
    ncol(prepared$primary_data),
    config$comparisons$country$minimum_n,
    country_var,
    use_var
  )
)
write.csv(summary, file.path(out_dir, "preflight_summary.csv"), row.names = FALSE)

if (!is.null(country_var) && nzchar(country_var) && country_var %in% names(prepared$filtered)) {
  counts <- sort(table(prepared$filtered[[country_var]]), decreasing = TRUE)
  country_counts <- data.frame(country = names(counts), n = as.integer(counts), row.names = NULL)
  country_counts$eligible_at_configured_minimum <- country_counts$n >= config$comparisons$country$minimum_n
  write.csv(country_counts, file.path(out_dir, "country_counts.csv"), row.names = FALSE)
}

if (!is.null(use_var) && nzchar(use_var) && use_var %in% names(prepared$filtered)) {
  use_values <- table(prepared$filtered[[use_var]], useNA = "ifany")
  use_distribution <- data.frame(value = names(use_values), n = as.integer(use_values), row.names = NULL)
  write.csv(use_distribution, file.path(out_dir, "use_frequency_distribution.csv"), row.names = FALSE)
}

cat("Preflight completed: ", out_dir, "\n", sep = "")
