source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "02_data.R"))

network_edge_table <- function(adjacency, node_map = NULL) {
  index <- which(upper.tri(adjacency) & adjacency != 0, arr.ind = TRUE)
  if (!nrow(index)) {
    return(tibble::tibble(from = character(), to = character(), weight = numeric(), abs_weight = numeric(), sign = character()))
  }
  tibble::tibble(
    from = rownames(adjacency)[index[, 1]],
    to = colnames(adjacency)[index[, 2]],
    weight = adjacency[index],
    abs_weight = abs(adjacency[index]),
    sign = ifelse(adjacency[index] > 0, "positive", "negative")
  ) |>
    dplyr::arrange(dplyr::desc(abs_weight))
}

network_density <- function(adjacency) {
  p <- ncol(adjacency)
  if (p < 2L) return(NA_real_)
  sum(adjacency[upper.tri(adjacency)] != 0) / choose(p, 2)
}

network_global_strength <- function(adjacency) sum(abs(adjacency[upper.tri(adjacency)]))

network_centrality <- function(adjacency) {
  centrality <- qgraph::centrality_auto(adjacency)
  node_centrality <- as.data.frame(centrality$node.centrality)
  node_centrality$node <- rownames(node_centrality)
  tibble::as_tibble(node_centrality) |>
    dplyr::relocate(node)
}

network_predictability <- function(mgm_fit, node_names) {
  predicted <- mgm_fit$predictability %||% list()
  errors <- predicted$errors %||% NULL
  if (is.null(errors)) {
    return(tibble::tibble(node = node_names, predictability = NA_real_, measure = NA_character_))
  }
  errors <- unlist(errors)
  values <- rep(NA_real_, length(node_names))
  values[seq_len(min(length(values), length(errors)))] <- 1 - errors[seq_len(min(length(values), length(errors)))]
  tibble::tibble(node = node_names, predictability = values, measure = "1 - mgm predictability error")
}

mgm_category_preflight <- function(data, minimum_events = 2L) {
  sparse <- lapply(names(data), function(node) {
    counts <- table(data[[node]])
    low_levels <- names(counts)[counts < minimum_events]
    if (!length(low_levels)) return(NULL)
    paste0(node, " [", paste(paste0(low_levels, "=", counts[low_levels]), collapse = ", "), "]")
  })
  sparse <- unlist(Filter(Negate(is.null), sparse), use.names = FALSE)
  if (length(sparse)) {
    stop(
      "MGM eligibility failed because at least one response category has fewer than ", minimum_events,
      " observations: ", paste(sparse, collapse = "; "),
      ". Combine theoretically defensible sparse categories, increase the group sample, or mark this subgroup computation as unavailable.",
      call. = FALSE
    )
  }
  invisible(TRUE)
}

estimate_mgm_network <- function(data, config) {
  require_can_packages(c("mgm", "qgraph", "tibble", "dplyr"))
  if (!is.data.frame(data)) data <- as.data.frame(data)
  if (anyNA(data)) stop("MGM estimation requires a complete node dataset. Use complete-case preparation or imputation first.", call. = FALSE)
  mgm_category_preflight(data, minimum_events = config$network$minimum_category_events %||% 2L)
  declared_types <- attr(data, "mgm_types") %||% config_node_types(config)
  declared_levels <- attr(data, "mgm_levels") %||% config_node_levels(config)
  declared_types <- unname(declared_types)
  declared_levels <- unname(declared_levels)
  # mgm represents ordinal responses through its categorical family. Ordinal
  # variables have already been recoded to contiguous observed categories and
  # therefore carry their actual post-filtering response-level count.
  mgm_types <- vapply(declared_types, function(node_type) switch(node_type, ordinal = "c", continuous = "g", categorical = "c", stop("Unsupported network node type: ", node_type, call. = FALSE)), character(1))
  p <- ncol(data)
  if (length(mgm_types) != p || length(declared_levels) != p) stop("Network configuration metadata does not match the number of prepared nodes.", call. = FALSE)
  fit <- mgm::mgm(
    data = as.matrix(data),
    type = mgm_types,
    level = declared_levels,
    k = 2,
    lambdaSel = "EBIC",
    lambdaGam = config$network$ebic_gamma,
    lambdaMin = config$network$lambda_min_ratio %||% 0.05,
    pbar = FALSE
  )
  adjacency <- fit$pairwise$wadj
  rownames(adjacency) <- colnames(data)
  colnames(adjacency) <- colnames(data)
  list(
    estimator = "mgm_lasso_ebic",
    fit = fit,
    adjacency = adjacency,
    edge_table = network_edge_table(adjacency),
    centrality = network_centrality(adjacency),
    predictability = network_predictability(fit, colnames(data)),
    density = network_density(adjacency),
    global_strength = network_global_strength(adjacency),
    n = nrow(data),
    p = ncol(data)
  )
}

estimate_ggm_spearman_network <- function(data, config) {
  require_can_packages(c("qgraph", "tibble", "dplyr"))
  if (!is.data.frame(data)) data <- as.data.frame(data)
  if (anyNA(data)) stop("GGM estimation requires a complete node dataset. Use complete-case preparation or imputation first.", call. = FALSE)
  correlation <- stats::cor(data, method = "spearman")
  adjacency <- qgraph::EBICglasso(correlation, n = nrow(data), gamma = config$network$ebic_gamma)
  rownames(adjacency) <- colnames(data)
  colnames(adjacency) <- colnames(data)
  list(
    estimator = "ggm_spearman_ebicglasso",
    fit = list(correlation = correlation),
    adjacency = adjacency,
    edge_table = network_edge_table(adjacency),
    centrality = network_centrality(adjacency),
    predictability = tibble::tibble(node = colnames(data), predictability = NA_real_, measure = NA_character_),
    density = network_density(adjacency),
    global_strength = network_global_strength(adjacency),
    n = nrow(data),
    p = ncol(data)
  )
}

plot_can_network <- function(network_result, node_map, output_file, config, title = NULL) {
  require_can_package("qgraph")
  domains <- node_map$domain[match(rownames(network_result$adjacency), node_map$label)]
  domain_levels <- unique(node_map$domain)
  palette <- grDevices::hcl.colors(length(domain_levels), palette = "Dynamic")
  colors <- palette[match(domains, domain_levels)]
  names(colors) <- rownames(network_result$adjacency)
  can_dir_create(dirname(output_file))
  grDevices::png(
    filename = output_file,
    width = config$output$figure_width * config$output$figure_dpi,
    height = config$output$figure_height * config$output$figure_dpi,
    res = config$output$figure_dpi
  )
  on.exit(grDevices::dev.off(), add = TRUE)
  node_ids <- seq_len(nrow(network_result$adjacency))
  qgraph::qgraph(
    network_result$adjacency,
    layout = "spring",
    labels = node_ids,
    color = colors,
    posCol = "#2166AC",
    negCol = "#B2182B",
    vsize = 8,
    label.cex = 0.85,
    esize = 11,
    legend = FALSE,
    title = title
  )
  graphics::legend(
    "bottomleft",
    legend = domain_levels,
    col = palette,
    pch = 19,
    pt.cex = 1.2,
    cex = 0.8,
    title = "CAN node domain",
    bty = "n"
  )
  invisible(output_file)
}

save_network_result <- function(network_result, prefix, config, node_map) {
  computations_dir <- config_output_path(config, "computations_dir")
  figures_dir <- config_output_path(config, "figures_dir")
  output_dir <- can_dir_create(file.path(computations_dir, "networks", prefix))
  figure_dir <- can_dir_create(file.path(figures_dir, "networks"))

  utils::write.csv(network_result$adjacency, file.path(output_dir, "adjacency_matrix.csv"), row.names = TRUE)
  readr::write_csv(network_result$edge_table, file.path(output_dir, "edge_table.csv"))
  readr::write_csv(network_result$centrality, file.path(output_dir, "centrality.csv"))
  readr::write_csv(network_result$predictability, file.path(output_dir, "predictability.csv"))
  node_key <- node_map |>
    dplyr::mutate(node_number = match(.data$label, rownames(network_result$adjacency))) |>
    dplyr::select(.data$node_number, .data$source_variable, .data$label, .data$domain, .data$node_type, .data$levels) |>
    dplyr::arrange(.data$node_number)
  readr::write_csv(node_key, file.path(output_dir, "network_node_key.csv"))
  summary <- tibble::tibble(
    estimator = network_result$estimator,
    n = network_result$n,
    p = network_result$p,
    density = network_result$density,
    global_strength = network_result$global_strength,
    nonzero_edges = nrow(network_result$edge_table)
  )
  readr::write_csv(summary, file.path(output_dir, "network_summary.csv"))
  if (isTRUE(config$output$save_rds)) saveRDS(network_result, file.path(output_dir, "network_result.rds"))
  plot_path <- file.path(figure_dir, paste0(prefix, "_network.png"))
  plot_can_network(network_result, node_map, plot_path, config, title = paste0(config$project$title, " — ", prefix))
  list(output_dir = output_dir, figure_path = plot_path, summary = summary)
}

run_primary_network <- function(prepared, config) {
  set.seed(config$project$seed)
  result <- estimate_mgm_network(prepared$primary_data, config)
  saved <- save_network_result(result, "primary_mgm", config, prepared$node_map)
  list(result = result, saved = saved)
}
