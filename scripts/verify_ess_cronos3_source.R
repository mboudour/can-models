#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
config_index <- match("--config", args)
config_path <- if (is.na(config_index)) {
  "config/ess_cronos3_sogreen_w6.yml"
} else {
  if (config_index == length(args)) stop("Usage: Rscript scripts/verify_ess_cronos3_source.R [--config path/to/config.yml]", call. = FALSE)
  args[[config_index + 1L]]
}

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
require_can_package("digest")

config <- read_can_config(config_path)
source_path <- can_relative_path(config$input$path, attr(config, "root") %||% can_project_root())
codebook_path <- can_relative_path(config$input$questionnaire, attr(config, "root") %||% can_project_root())
expected_checksum <- as.character(config$input$expected_checksum_sha256 %||% "")

if (!file.exists(source_path)) stop("Official Wave 6 data file not found: ", source_path, call. = FALSE)
if (!file.exists(codebook_path)) stop("Official Wave 6 codebook not found: ", codebook_path, call. = FALSE)
if (!nzchar(expected_checksum)) stop("Configuration does not declare input.expected_checksum_sha256.", call. = FALSE)

actual_checksum <- digest::digest(file = source_path, algo = "sha256")
if (!identical(tolower(actual_checksum), tolower(expected_checksum))) {
  stop(
    "Official Wave 6 file checksum does not match the configured source edition.\n",
    "Expected: ", expected_checksum, "\n",
    "Actual:   ", actual_checksum,
    call. = FALSE
  )
}

cat("Official ESS CRONOS-3 Wave 6 source verified.\n")
cat("Data: ", source_path, "\n", sep = "")
cat("Codebook: ", codebook_path, "\n", sep = "")
cat("SHA-256: ", actual_checksum, "\n", sep = "")
cat("DOI: ", config$input$source_doi, "\n", sep = "")
