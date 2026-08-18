source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "02_data.R"))
source(file.path(can_project_root(), "R", "03_network.R"))

walktrap_communities <- function(adjacency) {
  require_can_package("igraph")
  weighted <- abs(adjacency)
  diag(weighted) <- 0
  graph <- igraph::graph_from_adjacency_matrix(weighted, mode = "undirected", weighted = TRUE, diag = FALSE)
  communities <- igraph::cluster_walktrap(graph, weights = igraph::E(graph)$weight)
  membership <- igraph::membership(communities)
  tibble::tibble(node = names(membership), community = as.integer(membership)) |>
    dplyr::arrange(.data$community, .data$node)
}

community_agreement <- function(primary_membership, bootstrap_memberships) {
  if (!length(bootstrap_memberships)) return(tibble::tibble(node_1 = character(), node_2 = character(), coassignment = numeric()))
  nodes <- names(primary_membership)
  coassignment <- matrix(0, nrow = length(nodes), ncol = length(nodes), dimnames = list(nodes, nodes))
  successful <- 0L
  for (membership in bootstrap_memberships) {
    if (!identical(sort(names(membership)), sort(nodes))) next
    ordered <- membership[nodes]
    coassignment <- coassignment + outer(ordered, ordered, FUN = "==")
    successful <- successful + 1L
  }
  if (successful == 0L) return(tibble::tibble(node_1 = character(), node_2 = character(), coassignment = numeric()))
  coassignment <- coassignment / successful
  index <- which(upper.tri(coassignment), arr.ind = TRUE)
  tibble::tibble(node_1 = rownames(coassignment)[index[, 1]], node_2 = colnames(coassignment)[index[, 2]], coassignment = coassignment[index])
}

bootstrap_community_consensus <- function(data, config) {
  iterations <- config$community_detection$bootstrap_consensus_iterations
  nodes <- colnames(data)
  memberships <- vector("list", iterations)
  for (i in seq_len(iterations)) {
    indices <- sample.int(nrow(data), size = nrow(data), replace = TRUE)
    fit <- tryCatch(estimate_mgm_network(data[indices, , drop = FALSE], config), error = function(e) NULL)
    if (!is.null(fit)) {
      membership <- walktrap_communities(fit$adjacency)$community
      names(membership) <- walktrap_communities(fit$adjacency)$node
      memberships[[i]] <- membership[nodes]
    }
  }
  Filter(Negate(is.null), memberships)
}

run_bootnet_diagnostics <- function(data, config) {
  require_can_package("bootnet")
  set.seed(config$project$seed)
  estimated <- tryCatch(
    bootnet::estimateNetwork(
      data,
      default = "mgm",
      type = rep("c", ncol(data)),
      level = rep(config$network$node_levels, ncol(data)),
      verbose = FALSE
    ),
    error = function(e) e
  )
  if (inherits(estimated, "error")) return(list(error = conditionMessage(estimated)))

  edge_boot <- tryCatch(
    bootnet::bootnet(estimated, nBoots = config$bootstrapping$edge_bootstrap_iterations, type = "nonparametric", statistics = c("edge", "strength"), nCores = 1),
    error = function(e) e
  )
  case_boot <- tryCatch(
    bootnet::bootnet(estimated, nBoots = config$bootstrapping$case_drop_bootstrap_iterations, type = "case", statistics = c("strength"), nCores = 1),
    error = function(e) e
  )
  list(estimated = estimated, edge_boot = edge_boot, case_boot = case_boot)
}

save_bootnet_diagnostics <- function(diagnostics, config) {
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "diagnostics"))
  figure_dir <- can_dir_create(file.path(config_output_path(config, "figures_dir"), "diagnostics"))
  if (!is.null(diagnostics$error)) {
    writeLines(c("# Bootstrap diagnostic status", "", diagnostics$error), file.path(output_dir, "bootnet_status.md"))
    return(invisible(NULL))
  }
  saveRDS(diagnostics, file.path(output_dir, "bootnet_diagnostics.rds"))
  for (diagnostic_name in c("edge_boot", "case_boot")) {
    diagnostic <- diagnostics[[diagnostic_name]]
    if (inherits(diagnostic, "error")) {
      writeLines(conditionMessage(diagnostic), file.path(output_dir, paste0(diagnostic_name, "_error.txt")))
      next
    }
    if (inherits(diagnostic, "bootnet")) {
      figure_path <- file.path(figure_dir, paste0(diagnostic_name, "_plot.png"))
      grDevices::png(figure_path, width = 2200, height = 1600, res = 180)
      try(plot(diagnostic, statistics = if (diagnostic_name == "edge_boot") "edge" else "strength", order = "sample"), silent = TRUE)
      grDevices::dev.off()
    }
  }
  invisible(diagnostics)
}

run_diagnostics_workflow <- function(prepared, primary, config) {
  primary_membership <- walktrap_communities(primary$result$adjacency)
  primary_vector <- primary_membership$community
  names(primary_vector) <- primary_membership$node
  consensus_memberships <- bootstrap_community_consensus(prepared$primary_data, config)
  consensus <- community_agreement(primary_vector, consensus_memberships)
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "diagnostics"))
  readr::write_csv(primary_membership, file.path(output_dir, "walktrap_communities.csv"))
  readr::write_csv(consensus, file.path(output_dir, "bootstrap_community_coassignment.csv"))
  bootnet_result <- run_bootnet_diagnostics(prepared$primary_data, config)
  save_bootnet_diagnostics(bootnet_result, config)
  list(walktrap = primary_membership, community_consensus = consensus, bootnet = bootnet_result)
}
