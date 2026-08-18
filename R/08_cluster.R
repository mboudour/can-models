source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "03_network.R"))
source(file.path(can_project_root(), "R", "07_country.R"))

country_edge_matrix <- function(country_networks) {
  if (length(country_networks) < 2L) stop("At least two country networks are required for clustering.", call. = FALSE)
  vectors <- lapply(country_networks, function(entry) upper_edge_vector(entry$result$adjacency))
  matrix <- do.call(rbind, vectors)
  rownames(matrix) <- names(country_networks)
  matrix
}

cluster_country_networks <- function(country_workflow, prepared, config) {
  country_networks <- country_workflow$networks
  if (length(country_networks) < 2L) return(NULL)
  edge_matrix <- country_edge_matrix(country_networks)
  max_k <- min(6L, nrow(edge_matrix) - 1L)
  if (max_k < 2L) return(NULL)
  set.seed(config$project$seed)

  gap_result <- tryCatch(
    cluster::clusGap(edge_matrix, FUNcluster = function(x, k) list(cluster = stats::kmeans(x, centers = k, nstart = 100)$cluster), K.max = max_k, B = 100),
    error = function(error) error
  )
  if (is.list(gap_result) && !is.null(gap_result$Tab)) {
    gap_table <- tibble::tibble(k = seq_len(max_k), gap = gap_result$Tab[, "gap"], se_sim = gap_result$Tab[, "SE.sim"], log_wss = gap_result$Tab[, "logW"])
    gap_k <- which.max(gap_result$Tab[, "gap"])
  } else {
    gap_table <- tibble::tibble(k = seq_len(max_k), gap = NA_real_, se_sim = NA_real_, log_wss = NA_real_)
    gap_k <- 1L
  }

  wss <- vapply(seq_len(max_k), function(k) stats::kmeans(edge_matrix, centers = k, nstart = 100)$tot.withinss, numeric(1))
  wss_table <- tibble::tibble(k = seq_len(max_k), total_within_ss = wss)
  selected_k <- if (gap_k == 1L && nrow(edge_matrix) >= 4L) 2L else gap_k
  selected_k <- max(1L, min(selected_k, max_k))

  kmeans_clusters <- stats::kmeans(edge_matrix, centers = selected_k, nstart = 100)$cluster
  hierarchical_clusters <- stats::cutree(stats::hclust(stats::dist(edge_matrix)), k = selected_k)
  pam_clusters <- cluster::pam(edge_matrix, k = selected_k)$clustering
  clara_clusters <- cluster::clara(edge_matrix, k = selected_k, samples = min(50L, nrow(edge_matrix)))$clustering
  assignments <- tibble::tibble(
    country = rownames(edge_matrix),
    kmeans = as.integer(kmeans_clusters),
    hierarchical = as.integer(hierarchical_clusters),
    pam = as.integer(pam_clusters),
    clara = as.integer(clara_clusters)
  )

  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "country_clustering"))
  figure_dir <- can_dir_create(file.path(config_output_path(config, "figures_dir"), "country_clustering"))
  utils::write.csv(edge_matrix, file.path(output_dir, "country_edge_matrix.csv"), row.names = TRUE)
  readr::write_csv(gap_table, file.path(output_dir, "gap_statistic.csv"))
  readr::write_csv(wss_table, file.path(output_dir, "within_sum_of_squares.csv"))
  readr::write_csv(assignments, file.path(output_dir, "cluster_assignments.csv"))
  grDevices::png(file.path(figure_dir, "country_network_dendrogram.png"), width = 1800, height = 1200, res = 160)
  plot(stats::hclust(stats::dist(edge_matrix)), main = "Hierarchical clustering of country CAN edge matrices", xlab = "Country", sub = "")
  grDevices::dev.off()

  pooled_networks <- list()
  for (cluster_id in sort(unique(kmeans_clusters))) {
    countries <- names(kmeans_clusters)[kmeans_clusters == cluster_id]
    row_index <- prepared$primary_context[[config$comparisons$country$variable]] %in% countries
    data_cluster <- prepared$primary_data[row_index, , drop = FALSE]
    if (nrow(data_cluster) < 50L) next
    result <- tryCatch(estimate_mgm_network(data_cluster, config), error = function(error) error)
    if (inherits(result, "error")) {
      pooled_networks[[paste0("cluster_", cluster_id)]] <- list(countries = countries, data = data_cluster, result = NULL, status = "placeholder", reason = conditionMessage(result))
      next
    }
    saved <- save_network_result(result, paste0("country_cluster_", cluster_id), config, prepared$node_map)
    pooled_networks[[paste0("cluster_", cluster_id)]] <- list(countries = countries, data = data_cluster, result = result, saved = saved, status = "completed")
  }
  result <- list(edge_matrix = edge_matrix, gap = gap_table, wss = wss_table, selected_k = selected_k, assignments = assignments, pooled_networks = pooled_networks)
  if (isTRUE(config$output$save_rds)) saveRDS(result, file.path(output_dir, "country_clustering_workflow.rds"))
  result
}
