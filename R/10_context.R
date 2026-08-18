source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "02_data.R"))

cramers_v <- function(table) {
  chi <- suppressWarnings(stats::chisq.test(table, correct = FALSE))
  n <- sum(table)
  denominator <- n * min(nrow(table) - 1L, ncol(table) - 1L)
  if (denominator <= 0) return(NA_real_)
  sqrt(unname(chi$statistic) / denominator)
}

run_contextual_associations <- function(prepared, config) {
  variables <- config$contextual_associations$categorical_variables
  variables <- variables[variables %in% names(prepared$filtered)]
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "contextual_associations"))
  if (length(variables) < 2L) {
    readr::write_csv(tibble::tibble(), file.path(output_dir, "chi_square_cramers_v.csv"))
    return(tibble::tibble())
  }
  pairs <- utils::combn(variables, 2L, simplify = FALSE)
  results <- lapply(pairs, function(pair) {
    data <- prepared$filtered[, pair, drop = FALSE]
    data <- data[stats::complete.cases(data), , drop = FALSE]
    table <- table(data[[pair[[1]]]], data[[pair[[2]]]])
    if (nrow(table) < 2L || ncol(table) < 2L) return(tibble::tibble(variable_a = pair[[1]], variable_b = pair[[2]], n = nrow(data), chi_square = NA_real_, df = NA_real_, p_value = NA_real_, cramers_v = NA_real_))
    chi <- suppressWarnings(stats::chisq.test(table, correct = FALSE))
    tibble::tibble(
      variable_a = pair[[1]],
      variable_b = pair[[2]],
      n = nrow(data),
      chi_square = unname(chi$statistic),
      df = unname(chi$parameter),
      p_value = chi$p.value,
      cramers_v = cramers_v(table)
    )
  })
  results <- dplyr::bind_rows(results) |>
    dplyr::mutate(p_adjust_fdr = stats::p.adjust(.data$p_value, method = "fdr"))
  readr::write_csv(results, file.path(output_dir, "chi_square_cramers_v.csv"))
  results
}
