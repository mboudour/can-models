source(file.path(can_project_root(), "R", "00_packages.R"))
source(file.path(can_project_root(), "R", "01_config.R"))
source(file.path(can_project_root(), "R", "02_data.R"))

run_networktree_workflow <- function(prepared, config) {
  output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "networktree"))
  setting <- config$comparisons$networktree
  if (!isTRUE(setting$enabled)) {
    writeLines("NetworkTree disabled in configuration.", file.path(output_dir, "status.txt"))
    return(list(status = "disabled"))
  }
  if (!require_can_package("NetworkTree", optional = TRUE)) {
    writeLines("NetworkTree package is unavailable in the active R environment. The workflow is retained as an optional module; install NetworkTree and rerun this analysis.", file.path(output_dir, "status.txt"))
    return(list(status = "package_unavailable"))
  }
  moderators <- setting$moderators
  moderators <- moderators[moderators %in% names(prepared$primary_context)]
  if (!length(moderators)) {
    writeLines("No configured NetworkTree moderators are available in the primary context data.", file.path(output_dir, "status.txt"))
    return(list(status = "no_available_moderators"))
  }

  data <- cbind(prepared$primary_data, prepared$primary_context[, moderators, drop = FALSE])
  result <- tryCatch(
    NetworkTree::networktree(data = data, variables = colnames(prepared$primary_data), moderators = moderators),
    error = function(e) e
  )
  if (inherits(result, "error")) {
    writeLines(conditionMessage(result), file.path(output_dir, "status.txt"))
    return(list(status = "error", error = conditionMessage(result)))
  }
  saveRDS(result, file.path(output_dir, "networktree_result.rds"))
  writeLines("NetworkTree completed. Inspect networktree_result.rds for the package-native tree and subnetworks.", file.path(output_dir, "status.txt"))
  list(status = "completed", result = result)
}
