#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
config_path <- if (is.na(config_index)) {
  "config/ess_cronos3_sogreen_w6.yml"
} else {
  if (config_index == length(args)) stop("Usage: Rscript scripts/run_ess_cronos3_green_transition_full.R [--config path/to/config.yml]", call. = FALSE)
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

result <- system2(
  "Rscript",
  c("--vanilla", "scripts/run_example.R", "--config", config_path),
  stdout = TRUE,
  stderr = TRUE
)
result_status <- attr(result, "status")
if (is.null(result_status)) result_status <- 0L
cat(paste(result, collapse = "\n"), "\n", sep = "")
if (result_status != 0L) stop("The complete Green Transition CAN workflow did not complete.", call. = FALSE)
