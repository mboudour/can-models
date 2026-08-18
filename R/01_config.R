source(file.path(can_project_root(), "R", "00_packages.R"))

read_can_config <- function(config_path) {
  require_can_package("yaml")
  root <- can_project_root()
  config_path <- can_relative_path(config_path, root)
  if (!file.exists(config_path)) stop("Configuration file not found: ", config_path, call. = FALSE)
  config <- yaml::read_yaml(config_path)
  attr(config, "config_path") <- config_path
  attr(config, "root") <- root
  validate_can_config(config, check_input = FALSE)
  config
}

config_node_ids <- function(config) {
  vapply(config$network$nodes, function(node) as.character(node$id), character(1))
}

config_node_labels <- function(config) {
  vapply(config$network$nodes, function(node) as.character(node$label), character(1))
}

config_node_domains <- function(config) {
  vapply(config$network$nodes, function(node) as.character(node$domain), character(1))
}

config_node_types <- function(config) {
  ids <- config_node_ids(config)
  values <- vapply(config$network$nodes, function(node) as.character(node$node_type %||% config$network$node_type %||% "ordinal"), character(1))
  stats::setNames(values, ids)
}

config_node_levels <- function(config) {
  ids <- config_node_ids(config)
  values <- vapply(config$network$nodes, function(node) as.integer(node$levels %||% config$network$node_levels %||% NA_integer_), integer(1))
  stats::setNames(values, ids)
}

config_output_path <- function(config, element) {
  root <- attr(config, "root") %||% can_project_root()
  can_relative_path(config$output[[element]], root)
}

`%||%` <- function(x, y) if (is.null(x) || length(x) == 0L) y else x

validate_can_config <- function(config, check_input = TRUE) {
  required_top <- c("project", "input", "sample", "variables", "network", "bootstrapping", "comparisons", "output")
  missing_top <- setdiff(required_top, names(config))
  if (length(missing_top)) stop("Configuration missing top-level section(s): ", paste(missing_top, collapse = ", "), call. = FALSE)

  node_ids <- config_node_ids(config)
  if (length(node_ids) < 3L) stop("Specify at least three network nodes.", call. = FALSE)
  if (anyDuplicated(node_ids)) stop("Network node identifiers must be unique.", call. = FALSE)

  levels <- config_node_levels(config)
  if (any(is.na(levels) | levels < 2L)) stop("Every network node must declare or inherit at least two response levels.", call. = FALSE)
  node_types <- config_node_types(config)
  if (any(!node_types %in% c("ordinal", "continuous", "categorical"))) stop("Network node types must be ordinal, continuous, or categorical.", call. = FALSE)

  filter <- config$sample$filter
  if (!is.null(filter$operator) && !filter$operator %in% c("equals", "not_equals", "in")) {
    stop("sample.filter.operator must be one of equals, not_equals, or in.", call. = FALSE)
  }

  country <- config$comparisons$country
  if (isTRUE(country$enabled) && (!nzchar(country$variable) || country$minimum_n < 2L)) {
    stop("Enabled country comparisons require a variable and minimum_n >= 2.", call. = FALSE)
  }

  if (isTRUE(check_input)) {
    input_path <- can_relative_path(config$input$path, attr(config, "root") %||% can_project_root())
    if (!file.exists(input_path)) stop("Input data file not found: ", input_path, call. = FALSE)
  }

  invisible(TRUE)
}
