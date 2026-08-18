source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "03_network.R"))

upper_edge_vector <- function(adjacency) adjacency[upper.tri(adjacency)]

compare_adjacency_matrices <- function(adjacency_a, adjacency_b, label_a = "network_a", label_b = "network_b") {
  if (!identical(rownames(adjacency_a), rownames(adjacency_b))) stop("Adjacency matrices must have identical ordered node labels.", call. = FALSE)
  x <- upper_edge_vector(adjacency_a)
  y <- upper_edge_vector(adjacency_b)
  correlation <- suppressWarnings(stats::cor.test(x, y, method = "pearson"))
  tibble::tibble(
    network_a = label_a,
    network_b = label_b,
    adjacency_correlation = unname(correlation$estimate),
    p_value = correlation$p.value,
    n_edges = length(x),
    global_strength_a = network_global_strength(adjacency_a),
    global_strength_b = network_global_strength(adjacency_b),
    density_a = network_density(adjacency_a),
    density_b = network_density(adjacency_b)
  )
}

run_nct <- function(data_a, data_b, config, label_a = "network_a", label_b = "network_b") {
  require_can_package("NetworkComparisonTest")
  if (!identical(colnames(data_a), colnames(data_b))) stop("NCT inputs must have identical ordered node columns.", call. = FALSE)
  nct <- tryCatch(
    NetworkComparisonTest::NCT(
      data1 = as.matrix(data_a),
      data2 = as.matrix(data_b),
      it = config$comparisons$country$nct_iterations,
      binary.data = FALSE,
      paired = FALSE,
      weighted = TRUE,
      test.edges = TRUE,
      gamma = config$network$ebic_gamma,
      progressbar = FALSE
    ),
    error = function(e) e
  )
  if (inherits(nct, "error")) {
    return(list(result = NULL, summary = tibble::tibble(network_a = label_a, network_b = label_b, completed = FALSE, error = conditionMessage(nct)), edge_invariance = tibble::tibble()))
  }
  scalar_value <- function(value) {
    if (is.null(value) || !length(value)) return(NA_real_)
    numeric_value <- suppressWarnings(as.numeric(unlist(value, use.names = FALSE)))
    if (!length(numeric_value)) NA_real_ else numeric_value[[1]]
  }
  summary <- tibble::tibble(
    network_a = label_a,
    network_b = label_b,
    completed = TRUE,
    structure_invariance_statistic = scalar_value(nct$nwinv.real),
    structure_invariance_p = scalar_value(nct$nwinv.pval),
    global_strength_difference = scalar_value(nct$glstrinv.real),
    global_strength_p = scalar_value(nct$glstrinv.pval),
    edge_invariance_p = scalar_value(nct$einv.pval)
  )
  edge_table <- tibble::tibble()
  edge_pvalues <- nct$einv.pvals %||% NULL
  if (!is.null(edge_pvalues)) {
    if (is.matrix(edge_pvalues) || is.array(edge_pvalues)) {
      index <- which(upper.tri(edge_pvalues), arr.ind = TRUE)
      edge_table <- tibble::tibble(
        network_a = label_a,
        network_b = label_b,
        node_a = rownames(edge_pvalues)[index[, 1]],
        node_b = colnames(edge_pvalues)[index[, 2]],
        p_value = as.numeric(edge_pvalues[index])
      )
    } else {
      values <- as.numeric(unlist(edge_pvalues, use.names = FALSE))
      edge_table <- tibble::tibble(
        network_a = label_a,
        network_b = label_b,
        edge_index = seq_along(values),
        p_value = values
      )
    }
  }
  list(result = nct, summary = summary, edge_invariance = edge_table)
}

run_split_sample_comparison <- function(prepared, config) {
  if (!isTRUE(config$comparisons$split_sample$enabled)) return(NULL)
  set.seed(config$project$seed)
  n <- nrow(prepared$primary_data)
  indices <- sample.int(n, size = floor(n * config$comparisons$split_sample$proportion_first_sample), replace = FALSE)
  data_a <- prepared$primary_data[indices, , drop = FALSE]
  data_b <- prepared$primary_data[-indices, , drop = FALSE]
  result_a <- tryCatch(estimate_mgm_network(data_a, config), error = function(error) error)
  result_b <- tryCatch(estimate_mgm_network(data_b, config), error = function(error) error)
  if (inherits(result_a, "error") || inherits(result_b, "error")) {
    reason <- paste(c(if (inherits(result_a, "error")) paste0("split_a: ", conditionMessage(result_a)), if (inherits(result_b, "error")) paste0("split_b: ", conditionMessage(result_b))), collapse = "\n\n")
    return(list(status = "placeholder", reason = reason, data_a = data_a, data_b = data_b))
  }
  correlation <- compare_adjacency_matrices(result_a$adjacency, result_b$adjacency, "split_a", "split_b")
  nct <- run_nct(data_a, data_b, config, "split_a", "split_b")
  list(status = "completed", data_a = data_a, data_b = data_b, result_a = result_a, result_b = result_b, matrix_correlation = correlation, nct = nct)
}

save_comparison <- function(comparison, prefix, config) {
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "comparisons", prefix))
  if (identical(comparison$status, "placeholder")) {
    writeLines(c("# Computation placeholder", "", comparison$reason), file.path(output_dir, "status.md"))
    return(invisible(output_dir))
  }
  readr::write_csv(comparison$matrix_correlation, file.path(output_dir, "adjacency_correlation.csv"))
  readr::write_csv(comparison$nct$summary, file.path(output_dir, "nct_summary.csv"))
  readr::write_csv(comparison$nct$edge_invariance, file.path(output_dir, "nct_edge_invariance.csv"))
  if (!is.null(comparison$nct$result) && isTRUE(config$output$save_rds)) saveRDS(comparison$nct$result, file.path(output_dir, "nct_result.rds"))
  invisible(output_dir)
}
