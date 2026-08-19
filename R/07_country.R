source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "02_data.R"))
source(file.path(can_project_root(), "R", "03_network.R"))
source(file.path(can_project_root(), "R", "06_compare.R"))

eligible_country_groups <- function(context_data, config) {
  country_config <- config$comparisons$country
  if (!isTRUE(country_config$enabled)) return(character())
  country_variable <- country_config$variable
  context_data |>
    dplyr::filter(!is.na(.data[[country_variable]])) |>
    dplyr::count(.data[[country_variable]], name = "n") |>
    dplyr::filter(.data$n >= country_config$minimum_n) |>
    dplyr::arrange(dplyr::desc(.data$n)) |>
    dplyr::pull(1) |>
    as.character()
}

run_country_networks <- function(prepared, config) {
  groups <- eligible_country_groups(prepared$primary_context, config)
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "country_networks"))
  if (!length(groups)) {
    writeLines("No country/group samples met the configured minimum sample size.", file.path(output_dir, "status.md"))
    return(list(networks = list(), eligible_groups = tibble::tibble(), matrix_correlations = tibble::tibble(), nct_summary = tibble::tibble(), nct_edges = tibble::tibble(), pairwise = list()))
  }

  country_variable <- config$comparisons$country$variable
  country_estimator <- config$comparisons$country$network_estimator %||% "ggm_spearman"
  estimate_country_network <- switch(
    country_estimator,
    mgm = estimate_mgm_network,
    ggm_spearman = estimate_ggm_spearman_network,
    stop("Unsupported comparisons.country.network_estimator: ", country_estimator, call. = FALSE)
  )
  attempts <- lapply(groups, function(group_name) {
    index <- prepared$primary_context[[country_variable]] == group_name
    network_data <- prepared$primary_data[index, , drop = FALSE]
    result <- tryCatch(estimate_country_network(network_data, config), error = function(error) error)
    if (inherits(result, "error")) {
      return(list(name = group_name, data = network_data, result = NULL, error = conditionMessage(result)))
    }
    saved <- save_network_result(result, paste0("country_", gsub("[^A-Za-z0-9]+", "_", group_name)), config, prepared$node_map)
    list(name = group_name, data = network_data, result = result, saved = saved, error = NA_character_)
  })
  names(attempts) <- groups
  eligible <- tibble::tibble(
    country = groups,
    n = vapply(attempts, function(entry) nrow(entry$data), numeric(1)),
    status = ifelse(vapply(attempts, function(entry) !is.null(entry$result), logical(1)), "completed", "placeholder"),
    reason = vapply(attempts, function(entry) entry$error %||% NA_character_, character(1))
  )
  networks <- attempts[vapply(attempts, function(entry) !is.null(entry$result), logical(1))]
  readr::write_csv(eligible, file.path(output_dir, "eligible_countries.csv"))

  if (length(networks) < 2L) {
    writeLines("Fewer than two eligible country networks were estimated. Pairwise correlations, NCT, and country clustering remain placeholders; see eligible_countries.csv.", file.path(output_dir, "status.md"))
    readr::write_csv(tibble::tibble(), file.path(output_dir, "adjacency_matrix_correlations.csv"))
    readr::write_csv(tibble::tibble(), file.path(output_dir, "pairwise_nct_summary.csv"))
    readr::write_csv(tibble::tibble(), file.path(output_dir, "pairwise_nct_edge_invariance.csv"))
    return(list(networks = networks, eligible_groups = eligible, matrix_correlations = tibble::tibble(), nct_summary = tibble::tibble(), nct_edges = tibble::tibble(), pairwise = list()))
  }

  valid_groups <- names(networks)
  pairs <- utils::combn(valid_groups, 2L, simplify = FALSE)
  correlations <- lapply(pairs, function(pair) {
    compare_adjacency_matrices(networks[[pair[[1]]]]$result$adjacency, networks[[pair[[2]]]]$result$adjacency, pair[[1]], pair[[2]])
  })
  matrix_correlations <- dplyr::bind_rows(correlations)
  if (nrow(matrix_correlations)) matrix_correlations$p_adjust_bonferroni <- stats::p.adjust(matrix_correlations$p_value, method = "bonferroni")
  if (nrow(matrix_correlations)) matrix_correlations$p_adjust_fdr <- stats::p.adjust(matrix_correlations$p_value, method = "fdr")

  nct_results <- list()
  if (isTRUE(config$comparisons$country$all_pairwise_nct)) {
    nct_results <- lapply(pairs, function(pair) {
      nct <- run_nct(networks[[pair[[1]]]]$data, networks[[pair[[2]]]]$data, config, pair[[1]], pair[[2]])
      list(pair = pair, nct = nct)
    })
    names(nct_results) <- vapply(pairs, paste, collapse = "__vs__", character(1))
  }
  nct_summary <- dplyr::bind_rows(lapply(nct_results, function(entry) entry$nct$summary))
  nct_edges <- dplyr::bind_rows(lapply(nct_results, function(entry) entry$nct$edge_invariance))
  if (nrow(nct_summary)) {
    nct_summary$structure_p_bonferroni <- stats::p.adjust(nct_summary$structure_invariance_p, method = "bonferroni")
    nct_summary$structure_p_fdr <- stats::p.adjust(nct_summary$structure_invariance_p, method = "fdr")
    nct_summary$global_strength_p_bonferroni <- stats::p.adjust(nct_summary$global_strength_p, method = "bonferroni")
    nct_summary$global_strength_p_fdr <- stats::p.adjust(nct_summary$global_strength_p, method = "fdr")
  }

  readr::write_csv(matrix_correlations, file.path(output_dir, "adjacency_matrix_correlations.csv"))
  readr::write_csv(nct_summary, file.path(output_dir, "pairwise_nct_summary.csv"))
  readr::write_csv(nct_edges, file.path(output_dir, "pairwise_nct_edge_invariance.csv"))
  if (isTRUE(config$output$save_rds)) saveRDS(list(networks = networks, attempts = attempts, nct_results = nct_results), file.path(output_dir, "country_network_workflow.rds"))
  list(networks = networks, eligible_groups = eligible, matrix_correlations = matrix_correlations, nct_summary = nct_summary, nct_edges = nct_edges, pairwise = nct_results)
}

run_use_frequency_comparison <- function(prepared, config) {
  setting <- config$comparisons$use_frequency_median_split
  if (!isTRUE(setting$enabled)) return(NULL)
  variable <- setting$variable
  if (!variable %in% names(prepared$primary_context)) stop("Use-frequency group variable missing from primary context: ", variable, call. = FALSE)
  use_label <- prepared$node_map$label[match(variable, prepared$node_map$source_variable)]
  if (is.na(use_label)) stop("Use-frequency group variable must be included in the configured node map before it can be excluded.", call. = FALSE)
  group_values <- prepared$primary_context[[variable]]
  median_value <- stats::median(group_values, na.rm = TRUE)
  group <- ifelse(group_values <= median_value, "lower_or_equal_use", "higher_use")
  node_data <- prepared$primary_data[, setdiff(colnames(prepared$primary_data), use_label), drop = FALSE]
  node_map <- prepared$node_map[prepared$node_map$label != use_label, , drop = FALSE]
  data_a <- node_data[group == "lower_or_equal_use", , drop = FALSE]
  data_b <- node_data[group == "higher_use", , drop = FALSE]
  result_a <- tryCatch(estimate_mgm_network(data_a, config), error = function(error) error)
  result_b <- tryCatch(estimate_mgm_network(data_b, config), error = function(error) error)
  if (inherits(result_a, "error") || inherits(result_b, "error")) {
    reason <- paste(c(if (inherits(result_a, "error")) paste0("lower_or_equal_use: ", conditionMessage(result_a)), if (inherits(result_b, "error")) paste0("higher_use: ", conditionMessage(result_b))), collapse = "\n\n")
    comparison <- list(status = "placeholder", reason = reason, median_value = median_value, n_lower_or_equal = nrow(data_a), n_higher = nrow(data_b))
    save_comparison(comparison, "use_frequency_median_split", config)
    output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "comparisons", "use_frequency_median_split"))
    readr::write_csv(tibble::tibble(median_value = median_value, n_lower_or_equal = nrow(data_a), n_higher = nrow(data_b)), file.path(output_dir, "group_definition.csv"))
    return(comparison)
  }
  saved_a <- save_network_result(result_a, "use_frequency_lower_or_equal", config, node_map)
  saved_b <- save_network_result(result_b, "use_frequency_higher", config, node_map)
  comparison <- list(
    status = "completed",
    data_a = data_a,
    data_b = data_b,
    result_a = result_a,
    result_b = result_b,
    matrix_correlation = compare_adjacency_matrices(result_a$adjacency, result_b$adjacency, "lower_or_equal_use", "higher_use"),
    nct = run_nct(data_a, data_b, config, "lower_or_equal_use", "higher_use"),
    median_value = median_value,
    n_lower_or_equal = nrow(data_a),
    n_higher = nrow(data_b),
    saved = list(lower_or_equal = saved_a, higher = saved_b)
  )
  save_comparison(comparison, "use_frequency_median_split", config)
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "comparisons", "use_frequency_median_split"))
  readr::write_csv(tibble::tibble(median_value = median_value, n_lower_or_equal = nrow(data_a), n_higher = nrow(data_b)), file.path(output_dir, "group_definition.csv"))
  comparison
}
