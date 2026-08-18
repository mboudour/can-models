#!/usr/bin/env Rscript

options(repos = c(CRAN = "https://cloud.r-project.org"))
file_argument <- commandArgs(trailingOnly = FALSE)
file_argument <- sub("^--file=", "", file_argument[grepl("^--file=", file_argument)])
script_path <- if (length(file_argument)) normalizePath(file_argument[[1]]) else normalizePath("scripts/setup_environment.R")
project_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
local_library <- file.path(project_root, ".Rlib")
dir.create(local_library, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(local_library, .libPaths()))

core_packages <- c(
  "renv", "readxl", "yaml", "digest", "jsonlite", "dplyr", "tidyr", "purrr",
  "tibble", "stringr", "readr", "ggplot2", "qgraph", "bootnet", "mgm",
  "networktools", "NetworkComparisonTest", "lavaan", "psych", "semTools",
  "GPArotation", "igraph", "factoextra", "cluster", "rmarkdown", "knitr",
  "testthat", "MASS", "withr", "scales"
)
optional_packages <- c("NetworkTree")

install_missing <- function(packages, required = TRUE) {
  missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
  if (!length(missing)) return(invisible(character()))
  message("Installing: ", paste(missing, collapse = ", "))
  tryCatch(
    install.packages(missing, lib = local_library, dependencies = c("Depends", "Imports", "LinkingTo"), Ncpus = 1L),
    error = function(e) {
      if (required) stop("Unable to install required package(s): ", paste(missing, collapse = ", "), "\n", conditionMessage(e))
      warning("Optional package install failed: ", conditionMessage(e))
    }
  )
  still_missing <- missing[!vapply(missing, requireNamespace, logical(1), quietly = TRUE)]
  if (length(still_missing) && required) stop("Required package(s) remain unavailable: ", paste(still_missing, collapse = ", "))
  still_missing
}

install_missing("renv", required = TRUE)
# Do not activate an isolated renv library during bootstrap: compatible binary
# packages installed by the operating system remain available through .libPaths().
# The lockfile is still written after installation for reproducibility.
install_missing(core_packages, required = TRUE)
missing_optional <- install_missing(optional_packages, required = FALSE)

status_path <- file.path(project_root, "docs", "environment_status.md")
status_lines <- c(
  "# Analysis environment status",
  "",
  paste0("Generated: ", format(Sys.time(), tz = "UTC", usetz = TRUE)),
  "",
  "## Required packages",
  "",
  paste0("- `", core_packages, "`: ", ifelse(vapply(core_packages, requireNamespace, logical(1), quietly = TRUE), "available", "missing")),
  "",
  "## Optional packages",
  "",
  paste0("- `", optional_packages, "`: ", ifelse(vapply(optional_packages, requireNamespace, logical(1), quietly = TRUE), "available", "missing")),
  ""
)
writeLines(status_lines, status_path)
renv::snapshot(project = project_root, type = "explicit", prompt = FALSE)
message("Environment ready. Optional packages unavailable: ", if (length(missing_optional)) paste(missing_optional, collapse = ", ") else "none")
