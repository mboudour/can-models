initial_local_library <- file.path(normalizePath(getwd(), mustWork = FALSE), ".Rlib")
if (dir.exists(initial_local_library)) .libPaths(unique(c(initial_local_library, .libPaths())))

can_required_packages <- c(
  "readxl", "yaml", "digest", "jsonlite", "dplyr", "tidyr", "purrr", "tibble",
  "stringr", "readr", "ggplot2", "qgraph", "bootnet", "mgm", "networktools",
  "NetworkComparisonTest", "lavaan", "psych", "semTools", "GPArotation", "igraph",
  "factoextra", "cluster", "rmarkdown", "knitr", "MASS", "withr", "scales"
)

can_optional_packages <- c("NetworkTree")

require_can_package <- function(package, optional = FALSE) {
  if (!requireNamespace(package, quietly = TRUE)) {
    message_text <- paste0(
      "Package `", package, "` is required for this operation. ",
      "Run `Rscript scripts/setup_environment.R` from the project root."
    )
    if (optional) {
      warning(message_text, call. = FALSE)
      return(FALSE)
    }
    stop(message_text, call. = FALSE)
  }
  TRUE
}

require_can_packages <- function(packages = can_required_packages) {
  invisible(vapply(packages, require_can_package, logical(1)))
}

can_project_root <- function() {
  root <- normalizePath(getwd(), mustWork = FALSE)
  if (file.exists(file.path(root, "config")) && file.exists(file.path(root, "R"))) return(root)

  script_paths <- commandArgs(trailingOnly = FALSE)
  script_paths <- sub("^--file=", "", script_paths[grepl("^--file=", script_paths)])
  if (length(script_paths)) {
    candidate <- normalizePath(file.path(dirname(script_paths[[1]]), ".."), mustWork = FALSE)
    if (file.exists(file.path(candidate, "config")) && file.exists(file.path(candidate, "R"))) return(candidate)
  }

  stop("Run from the can-models project root or pass an explicit project root.", call. = FALSE)
}

can_relative_path <- function(path, root = can_project_root()) {
  if (is.null(path) || !nzchar(path)) return(NA_character_)
  if (grepl("^(/|[A-Za-z]:[/\\\\])", path)) return(normalizePath(path, mustWork = FALSE))
  normalizePath(file.path(root, path), mustWork = FALSE)
}

can_timestamp <- function() format(Sys.time(), tz = "UTC", usetz = TRUE)

can_dir_create <- function(path) {
  dir.create(path, recursive = TRUE, showWarnings = FALSE)
  normalizePath(path, mustWork = TRUE)
}
