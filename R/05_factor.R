source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "02_data.R"))

factor_model_syntax <- function(items, factor_name = "latent") {
  paste0(factor_name, " =~ ", paste(items, collapse = " + "))
}

factor_safe_names <- function(items) {
  stats::setNames(make.names(items, unique = TRUE), items)
}

factor_lavaan_data <- function(data, items) {
  subset <- data[, items, drop = FALSE]
  safe_names <- factor_safe_names(items)
  names(subset) <- unname(safe_names[items])
  list(data = subset, safe_names = safe_names)
}

extract_cfa_fit <- function(fit, model_id, group = "pooled") {
  measures <- c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr", "aic", "bic")
  values <- tryCatch(lavaan::fitMeasures(fit, measures), error = function(e) rep(NA_real_, length(measures)))
  tibble::as_tibble_row(c(list(model_id = model_id, group = group, converged = lavaan::inspect(fit, "converged")), as.list(values)))
}

run_cfa <- function(data, model_spec, group = "pooled") {
  require_can_packages(c("lavaan", "tibble", "dplyr"))
  items <- model_spec$items
  complete <- data[stats::complete.cases(data[, items, drop = FALSE]), items, drop = FALSE]
  if (nrow(complete) < max(100L, length(items) * 10L)) {
    return(list(fit = NULL, fit_table = tibble::tibble(model_id = model_spec$id, group = group, converged = FALSE, reason = "insufficient complete cases"), loadings = tibble::tibble()))
  }
  lavaan_input <- factor_lavaan_data(complete, items)
  syntax <- factor_model_syntax(unname(lavaan_input$safe_names[items]), factor_name = model_spec$id)
  fit <- tryCatch(
    lavaan::cfa(syntax, data = lavaan_input$data, estimator = model_spec$estimator %||% "MLR", std.lv = TRUE),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(fit = NULL, fit_table = tibble::tibble(model_id = model_spec$id, group = group, converged = FALSE, reason = conditionMessage(fit)), loadings = tibble::tibble()))
  }
  loadings <- lavaan::parameterEstimates(fit, standardized = TRUE) |>
    dplyr::filter(.data$op == "=~") |>
    dplyr::transmute(model_id = model_spec$id, group = group, factor = .data$lhs, item = names(lavaan_input$safe_names)[match(.data$rhs, lavaan_input$safe_names)], estimate = .data$est, standardized_loading = .data$std.all, p_value = .data$pvalue)
  list(fit = fit, fit_table = extract_cfa_fit(fit, model_spec$id, group), loadings = loadings)
}

run_country_cfa <- function(context_data, config, model_spec) {
  country_variable <- config$comparisons$country$variable
  minimum_n <- config$comparisons$country$minimum_n
  if (!isTRUE(model_spec$country_invariance) || !country_variable %in% names(context_data)) return(list(country_fit = tibble::tibble(), invariance = tibble::tibble()))
  eligible <- context_data |>
    dplyr::filter(!is.na(.data[[country_variable]])) |>
    dplyr::count(.data[[country_variable]], name = "n") |>
    dplyr::filter(.data$n >= minimum_n) |>
    dplyr::pull(1)
  individual <- lapply(eligible, function(group_name) {
    subset <- context_data[context_data[[country_variable]] == group_name, , drop = FALSE]
    run_cfa(subset, model_spec, group = as.character(group_name))$fit_table
  })
  country_fit <- dplyr::bind_rows(individual)

  items <- model_spec$items
  invariance_data <- context_data[context_data[[country_variable]] %in% eligible, c(country_variable, items), drop = FALSE]
  invariance_data <- invariance_data[stats::complete.cases(invariance_data), , drop = FALSE]
  if (length(eligible) < 2L || nrow(invariance_data) < 250L) return(list(country_fit = country_fit, invariance = tibble::tibble()))

  safe_names <- factor_safe_names(items)
  names(invariance_data)[match(items, names(invariance_data))] <- unname(safe_names[items])
  syntax <- factor_model_syntax(unname(safe_names[items]), factor_name = model_spec$id)
  configural <- tryCatch(lavaan::cfa(syntax, data = invariance_data, group = country_variable, estimator = model_spec$estimator %||% "MLR", std.lv = TRUE), error = function(e) e)
  metric <- tryCatch(lavaan::cfa(syntax, data = invariance_data, group = country_variable, group.equal = "loadings", estimator = model_spec$estimator %||% "MLR", std.lv = TRUE), error = function(e) e)
  scalar <- tryCatch(lavaan::cfa(syntax, data = invariance_data, group = country_variable, group.equal = c("loadings", "intercepts"), estimator = model_spec$estimator %||% "MLR", std.lv = TRUE), error = function(e) e)
  collect <- function(model, name) {
    if (inherits(model, "error")) return(tibble::tibble(model_id = model_spec$id, invariance_level = name, converged = FALSE, reason = conditionMessage(model)))
    extract_cfa_fit(model, model_spec$id, group = name) |>
      dplyr::rename(invariance_level = .data$group)
  }
  list(country_fit = country_fit, invariance = dplyr::bind_rows(collect(configural, "configural"), collect(metric, "metric"), collect(scalar, "scalar")))
}

run_efa <- function(data, model_spec, group = "pooled") {
  require_can_packages(c("psych", "tibble", "dplyr"))
  items <- model_spec$items
  complete <- data[stats::complete.cases(data[, items, drop = FALSE]), items, drop = FALSE]
  if (nrow(complete) < max(100L, length(items) * 10L)) return(tibble::tibble(model_id = model_spec$id, group = group, item = NA_character_, factor = NA_character_, loading = NA_real_, reason = "insufficient complete cases"))
  poly <- tryCatch(psych::polychoric(complete)$rho, error = function(e) e)
  if (inherits(poly, "error")) return(tibble::tibble(model_id = model_spec$id, group = group, item = NA_character_, factor = NA_character_, loading = NA_real_, reason = conditionMessage(poly)))
  efa <- tryCatch(psych::fa(poly, nfactors = 1, n.obs = nrow(complete), fm = "minres", rotate = "oblimin"), error = function(e) e)
  if (inherits(efa, "error")) return(tibble::tibble(model_id = model_spec$id, group = group, item = NA_character_, factor = NA_character_, loading = NA_real_, reason = conditionMessage(efa)))
  loadings <- as.data.frame(unclass(efa$loadings))
  loadings$item <- rownames(loadings)
  tidyr::pivot_longer(tibble::as_tibble(loadings), cols = -item, names_to = "factor", values_to = "loading") |>
    dplyr::mutate(model_id = model_spec$id, group = group, .before = 1)
}

run_factor_workflow <- function(prepared, config) {
  models <- config$factor_models %||% list()
  if (!length(models)) return(list())
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "factor_models"))
  result <- lapply(models, function(model_spec) {
    pooled <- run_cfa(prepared$filtered, model_spec)
    country <- run_country_cfa(prepared$filtered, config, model_spec)
    pooled_efa <- run_efa(prepared$filtered, model_spec)
    country_variable <- config$comparisons$country$variable
    minimum_n <- config$comparisons$country$minimum_n
    country_efa <- tibble::tibble()
    if (isTRUE(model_spec$country_invariance) && country_variable %in% names(prepared$filtered)) {
      eligible <- prepared$filtered |>
        dplyr::filter(!is.na(.data[[country_variable]])) |>
        dplyr::count(.data[[country_variable]], name = "n") |>
        dplyr::filter(.data$n >= minimum_n) |>
        dplyr::pull(1)
      country_efa <- dplyr::bind_rows(lapply(eligible, function(group_name) run_efa(prepared$filtered[prepared$filtered[[country_variable]] == group_name, , drop = FALSE], model_spec, as.character(group_name))))
    }
    prefix <- model_spec$id
    readr::write_csv(pooled$fit_table, file.path(output_dir, paste0(prefix, "_cfa_pooled.csv")))
    readr::write_csv(pooled$loadings, file.path(output_dir, paste0(prefix, "_cfa_loadings.csv")))
    readr::write_csv(country$country_fit, file.path(output_dir, paste0(prefix, "_cfa_country.csv")))
    readr::write_csv(country$invariance, file.path(output_dir, paste0(prefix, "_invariance.csv")))
    readr::write_csv(pooled_efa, file.path(output_dir, paste0(prefix, "_efa_pooled.csv")))
    readr::write_csv(country_efa, file.path(output_dir, paste0(prefix, "_efa_country.csv")))
    list(pooled_cfa = pooled, country = country, pooled_efa = pooled_efa, country_efa = country_efa)
  })
  names(result) <- vapply(models, function(model) model$id, character(1))
  if (isTRUE(config$output$save_rds)) saveRDS(result, file.path(output_dir, "factor_workflow.rds"))
  result
}
