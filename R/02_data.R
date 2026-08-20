source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))

read_can_data <- function(config) {
  require_can_packages(c("readxl", "readr", "haven", "digest", "dplyr", "tibble"))
  validate_can_config(config, check_input = TRUE)
  path <- can_relative_path(config$input$path, attr(config, "root") %||% can_project_root())
  extension <- tolower(tools::file_ext(path))
  data <- switch(
    extension,
    xlsx = readxl::read_excel(path, sheet = config$input$sheet, .name_repair = "minimal"),
    xls = readxl::read_excel(path, sheet = config$input$sheet, .name_repair = "minimal"),
    csv = readr::read_csv(path, show_col_types = FALSE, name_repair = "minimal"),
    sav = haven::read_sav(path, user_na = FALSE),
    stop("Unsupported input format: ", extension, ". Supported formats are xlsx, xls, csv, and sav.", call. = FALSE)
  )
  attr(data, "source_path") <- path
  attr(data, "source_checksum") <- digest::digest(file = path, algo = "sha256")
  data
}

apply_can_transformations <- function(data, config) {
  missing_specs <- config$preprocessing$missing_values %||% list()
  missing_audit <- unlist(lapply(missing_specs, function(spec) {
    variables <- as.character(unlist(spec$variables %||% spec$variable, use.names = FALSE))
    missing_values <- as.numeric(unlist(spec$values %||% spec$value, use.names = FALSE))
    if (!length(variables) || any(!nzchar(variables))) stop("Missing-value specification needs one or more variables.", call. = FALSE)
    if (!length(missing_values) || any(is.na(missing_values))) stop("Missing-value specification needs numeric values.", call. = FALSE)
    lapply(variables, function(variable) {
      if (!variable %in% names(data)) stop("Missing-value variable not present: ", variable, call. = FALSE)
      original <- suppressWarnings(as.numeric(data[[variable]]))
      if (any(!is.na(data[[variable]]) & is.na(original))) stop("Missing-value variable is not numeric: ", variable, call. = FALSE)
      affected <- sum(original %in% missing_values, na.rm = TRUE)
      data[[variable]] <<- ifelse(original %in% missing_values, NA_real_, original)
      tibble::tibble(variable = variable, transformation = "missing_values_to_na", missing_values = paste(missing_values, collapse = ","), affected_n = affected, nonmissing_n = sum(!is.na(data[[variable]])))
    })
  }), recursive = FALSE)

  reverse_specs <- config$preprocessing$reverse_code %||% list()
  reverse_audit <- lapply(reverse_specs, function(spec) {
    variable <- as.character(spec$variable)
    minimum <- as.numeric(spec$minimum %||% 1)
    maximum <- as.numeric(spec$maximum)
    if (!nzchar(variable) || !variable %in% names(data)) stop("Reverse-code variable not present: ", variable, call. = FALSE)
    if (is.na(maximum) || maximum <= minimum) stop("Reverse-code specification needs maximum > minimum for `", variable, "`.", call. = FALSE)
    original <- suppressWarnings(as.numeric(data[[variable]]))
    if (any(!is.na(data[[variable]]) & is.na(original))) stop("Reverse-code variable is not numeric: ", variable, call. = FALSE)
    data[[variable]] <<- ifelse(is.na(original), NA_real_, minimum + maximum - original)
    tibble::tibble(variable = variable, transformation = "reverse_code", minimum = minimum, maximum = maximum, nonmissing_n = sum(!is.na(original)))
  })

  collapse_specs <- config$preprocessing$collapse_values %||% list()
  collapse_audit <- lapply(collapse_specs, function(spec) {
    variable <- as.character(spec$variable)
    from_values <- as.numeric(unlist(spec$from, use.names = FALSE))
    to_value <- as.numeric(spec$to)
    if (!nzchar(variable) || !variable %in% names(data)) stop("Category-collapse variable not present: ", variable, call. = FALSE)
    if (!length(from_values) || is.na(to_value)) stop("Category-collapse specification needs from and to values for `", variable, "`.", call. = FALSE)
    original <- suppressWarnings(as.numeric(data[[variable]]))
    if (any(!is.na(data[[variable]]) & is.na(original))) stop("Category-collapse variable is not numeric: ", variable, call. = FALSE)
    affected <- sum(original %in% from_values, na.rm = TRUE)
    data[[variable]] <<- ifelse(original %in% from_values, to_value, original)
    tibble::tibble(variable = variable, transformation = "collapse_values", minimum = NA_real_, maximum = NA_real_, nonmissing_n = sum(!is.na(original)), from_values = paste(from_values, collapse = ","), to_value = to_value, affected_n = affected)
  })

  attr(data, "transformation_audit") <- dplyr::bind_rows(missing_audit, reverse_audit, collapse_audit)
  data
}

apply_can_filter <- function(data, filter) {
  if (is.null(filter$variable) || !nzchar(filter$variable)) return(data)
  variable <- as.character(filter$variable)
  if (!variable %in% names(data)) stop("Filter variable not present: ", variable, call. = FALSE)
  operator <- filter$operator %||% "equals"
  value <- filter$value
  values <- data[[variable]]
  keep <- if (identical(operator, "equals")) {
    values == value
  } else if (identical(operator, "not_equals")) {
    values != value
  } else if (identical(operator, "in")) {
    values %in% unlist(value)
  } else {
    stop("Unsupported filter operator: ", operator, call. = FALSE)
  }
  data[which(!is.na(keep) & keep), , drop = FALSE]
}

validate_analysis_variables <- function(data, config) {
  node_ids <- config_node_ids(config)
  declared <- unique(c(
    node_ids,
    config$sample$filter$variable,
    unlist(config$variables, use.names = FALSE),
    config$comparisons$country$variable,
    config$comparisons$use_frequency_median_split$variable,
    unlist(config$comparisons$networktree$moderators, use.names = FALSE),
    unlist(config$contextual_associations$categorical_variables, use.names = FALSE),
    unlist(lapply(config$factor_models %||% list(), function(model) model$items), use.names = FALSE)
  ))
  declared <- declared[!is.na(declared) & nzchar(declared)]
  missing_variables <- setdiff(declared, names(data))
  if (length(missing_variables)) {
    stop("Configuration refers to missing variable(s): ", paste(missing_variables, collapse = ", "), call. = FALSE)
  }

  if (isTRUE(config$comparisons$use_frequency_median_split$enabled) &&
      !isTRUE(config$comparisons$use_frequency_median_split$exclude_from_network) &&
      config$comparisons$use_frequency_median_split$variable %in% node_ids) {
    stop("A grouping variable cannot also remain in the compared network. Set exclude_from_network: true or disable the comparison.", call. = FALSE)
  }

  invisible(TRUE)
}

normalize_node_labels <- function(labels, node_ids) {
  original <- as.character(labels)
  cleaned <- trimws(original)
  missing_label <- is.na(cleaned) | !nzchar(cleaned)
  cleaned[missing_label] <- node_ids[missing_label]
  normalized <- make.unique(cleaned, sep = "__")
  tibble::tibble(
    source_variable = node_ids,
    requested_label = original,
    label = normalized,
    label_changed = original != normalized
  )
}

coerce_ordinal_nodes <- function(data, node_ids, levels, node_types) {
  converted <- data[, node_ids, drop = FALSE]
  effective_levels <- stats::setNames(rep(NA_integer_, length(node_ids)), node_ids)
  diagnostics <- lapply(node_ids, function(node) {
    values <- converted[[node]]
    if (is.factor(values)) values <- as.character(values)
    numeric_values <- suppressWarnings(as.numeric(values))
    non_missing <- !is.na(values)
    if (any(non_missing & is.na(numeric_values))) {
      stop("Node `", node, "` contains non-numeric values. Add a numeric coding stage before network estimation.", call. = FALSE)
    }
    observed <- sort(unique(numeric_values[!is.na(numeric_values)]))
    if (length(observed) < 2L) stop("Node `", node, "` has fewer than two observed levels.", call. = FALSE)
    declared_levels <- levels[[node]]
    node_type <- node_types[[node]]
    # mgm requires categorical observations to be contiguous 1..K and `level`
    # to equal the actual K. Filtering can remove a response category even when
    # an item was originally a five-point scale, so preserve an explicit audit
    # and recode only the estimator-facing copy.
    if (node_type %in% c("ordinal", "categorical")) {
      converted_values <- match(numeric_values, observed)
      converted_values[is.na(numeric_values)] <- NA_integer_
      converted[[node]] <<- converted_values
      effective_levels[[node]] <<- length(observed)
    } else {
      converted[[node]] <<- numeric_values
      effective_levels[[node]] <<- NA_integer_
    }
    tibble::tibble(
      node = node,
      observed_levels = paste(observed, collapse = ","),
      n_levels = length(observed),
      declared_levels = declared_levels,
      effective_mgm_levels = effective_levels[[node]],
      recoded_for_mgm = node_type %in% c("ordinal", "categorical")
    )
  })
  list(data = converted, level_diagnostics = dplyr::bind_rows(diagnostics), effective_levels = effective_levels)
}

prepare_can_data <- function(config) {
  raw <- apply_can_transformations(read_can_data(config), config)
  validate_analysis_variables(raw, config)
  filtered <- apply_can_filter(raw, config$sample$filter)
  node_ids <- config_node_ids(config)
  requested_labels <- config_node_labels(config)
  label_audit <- normalize_node_labels(requested_labels, node_ids)
  labels <- label_audit$label
  domains <- config_node_domains(config)
  node_types <- config_node_types(config)
  node_levels <- config_node_levels(config)
  ordinal <- coerce_ordinal_nodes(filtered, node_ids, node_levels, node_types)
  node_data <- ordinal$data
  names(node_data) <- labels

  if (isTRUE(config$sample$complete_case_primary_network)) {
    complete_rows <- stats::complete.cases(node_data)
    primary_data <- node_data[complete_rows, , drop = FALSE]
    primary_context <- filtered[complete_rows, , drop = FALSE]
  } else {
    complete_rows <- rep(TRUE, nrow(node_data))
    primary_data <- node_data
    primary_context <- filtered
  }

  node_map <- label_audit |>
    dplyr::mutate(
      domain = domains,
      node_type = unname(node_types[node_ids]),
      levels = unname(ordinal$effective_levels[node_ids])
    )

  # Keep item-specific estimator metadata on the prepared matrices. These
  # attributes survive ordinary data-frame handling and prevent a blanket
  # five-level declaration from failing when observed categories differ.
  attr(node_data, "mgm_levels") <- ordinal$effective_levels
  attr(primary_data, "mgm_levels") <- ordinal$effective_levels
  attr(node_data, "mgm_types") <- node_types
  attr(primary_data, "mgm_types") <- node_types

  list(
    raw = raw,
    filtered = filtered,
    node_data = node_data,
    primary_data = primary_data,
    primary_context = primary_context,
    complete_rows = complete_rows,
    node_map = node_map,
    level_diagnostics = ordinal$level_diagnostics,
    label_audit = label_audit,
    transformation_audit = attr(raw, "transformation_audit"),
    source_path = attr(raw, "source_path"),
    source_checksum = attr(raw, "source_checksum")
  )
}

write_data_audit <- function(prepared, config) {
  output_dir <- config_output_path(config, "computations_dir")
  can_dir_create(output_dir)
  metadata_dir <- can_dir_create(file.path(output_dir, "run_metadata"))
  sample_dir <- can_dir_create(file.path(output_dir, "data_audit"))

  node_missingness <- tibble::tibble(
    source_variable = config_node_ids(config),
    label = config_node_labels(config),
    missing_n = vapply(prepared$node_data, function(x) sum(is.na(x)), numeric(1)),
    missing_percent = round(100 * vapply(prepared$node_data, function(x) mean(is.na(x)), numeric(1)), 3),
    unique_values = vapply(prepared$node_data, function(x) dplyr::n_distinct(x, na.rm = TRUE), numeric(1))
  )
  readr::write_csv(node_missingness, file.path(sample_dir, "node_missingness.csv"))
  readr::write_csv(prepared$level_diagnostics, file.path(sample_dir, "node_level_diagnostics.csv"))
  readr::write_csv(prepared$node_map, file.path(sample_dir, "node_map.csv"))
  readr::write_csv(prepared$label_audit %||% tibble::tibble(), file.path(sample_dir, "node_label_audit.csv"))
  readr::write_csv(prepared$transformation_audit %||% tibble::tibble(), file.path(sample_dir, "transformation_audit.csv"))

  sample_summary <- tibble::tibble(
    statistic = c("raw_rows", "filtered_rows", "primary_network_rows", "excluded_for_complete_case"),
    value = c(nrow(prepared$raw), nrow(prepared$filtered), nrow(prepared$primary_data), nrow(prepared$filtered) - nrow(prepared$primary_data))
  )
  readr::write_csv(sample_summary, file.path(sample_dir, "sample_flow.csv"))

  # psych::mardia has computational cost that grows rapidly with sample size.
  # Use a deterministic cap for a diagnostic check while retaining the full data
  # for all substantive network estimations.
  mardia_max_n <- config$audit$mardia_max_n %||% 2000L
  mardia_data <- prepared$primary_data
  mardia_sampled <- FALSE
  if (nrow(mardia_data) > mardia_max_n) {
    set.seed(config$project$seed)
    mardia_data <- mardia_data[sample.int(nrow(mardia_data), mardia_max_n), , drop = FALSE]
    mardia_sampled <- TRUE
  }
  mardia_result <- tryCatch(
    psych::mardia(as.matrix(mardia_data), plot = FALSE),
    error = function(error) error
  )
  if (inherits(mardia_result, "error")) {
    readr::write_csv(tibble::tibble(status = "not_completed", n_used = nrow(mardia_data), sampled_for_computational_feasibility = mardia_sampled, reason = conditionMessage(mardia_result)), file.path(sample_dir, "mardia_multivariate_normality.csv"))
  } else {
    scalar_names <- c("n.obs", "n.var", "b1p", "b2p", "skew", "small.skew", "p.skew", "p.small", "kurtosis", "p.kurt")
    normality_values <- unlist(mardia_result[intersect(scalar_names, names(mardia_result))], use.names = TRUE)
    normality_table <- tibble::tibble(statistic = names(normality_values), value = as.numeric(normality_values))
    normality_table$n_used <- nrow(mardia_data)
    normality_table$sampled_for_computational_feasibility <- mardia_sampled
    readr::write_csv(normality_table, file.path(sample_dir, "mardia_multivariate_normality.csv"))
  }

  provenance <- list(
    timestamp_utc = can_timestamp(),
    project_id = config$project$id,
    config_path = attr(config, "config_path"),
    source_path = prepared$source_path,
    source_checksum_sha256 = prepared$source_checksum,
    n_raw = nrow(prepared$raw),
    n_filtered = nrow(prepared$filtered),
    n_primary = nrow(prepared$primary_data),
    seed = config$project$seed
  )
  jsonlite::write_json(provenance, file.path(metadata_dir, "provenance.json"), pretty = TRUE, auto_unbox = TRUE)
  yaml::write_yaml(config, file.path(metadata_dir, "configuration_snapshot.yml"))
  saveRDS(prepared, file.path(sample_dir, "prepared_data.rds"))

  invisible(list(sample_summary = sample_summary, node_missingness = node_missingness, provenance = provenance))
}
