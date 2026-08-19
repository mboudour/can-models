#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "06_compare.R"))

config <- read_can_config("config/ess_cronos3_sogreen_w6.yml")
results_path <- file.path(config_output_path(config, "computations_dir"), "results_stage.rds")
if (!file.exists(results_path)) stop("Run scripts/run_ess_cronos3_green_transition_results.R first.", call. = FALSE)
results <- readRDS(results_path)
networks <- results$country_workflow$networks
if (length(networks) < 2L) stop("Fewer than two completed country networks are available for NCT.", call. = FALSE)

output_dir <- can_dir_create(file.path(config_output_path(config, "computations_dir"), "country_networks", "nct_pairs"))
pairs <- utils::combn(names(networks), 2L, simplify = FALSE)

for (pair in pairs) {
  pair_id <- paste(pair, collapse = "__vs__")
  output_file <- file.path(output_dir, paste0(pair_id, ".rds"))
  if (file.exists(output_file)) {
    cat("Skipping completed pair: ", pair_id, "\n", sep = "")
    next
  }
  cat("Running NCT: ", pair_id, "\n", sep = "")
  nct <- run_nct(networks[[pair[[1]]]]$data, networks[[pair[[2]]]]$data, config, pair[[1]], pair[[2]])
  saveRDS(nct, output_file)
}

pair_results <- lapply(sort(list.files(output_dir, pattern = "\\.rds$", full.names = TRUE)), readRDS)
summary <- dplyr::bind_rows(lapply(pair_results, function(result) result$summary))
edges <- dplyr::bind_rows(lapply(pair_results, function(result) result$edge_invariance))
if (nrow(summary)) {
  summary$structure_p_bonferroni <- stats::p.adjust(summary$structure_invariance_p, method = "bonferroni")
  summary$structure_p_fdr <- stats::p.adjust(summary$structure_invariance_p, method = "fdr")
  summary$global_strength_p_bonferroni <- stats::p.adjust(summary$global_strength_p, method = "bonferroni")
  summary$global_strength_p_fdr <- stats::p.adjust(summary$global_strength_p, method = "fdr")
}
readr::write_csv(summary, file.path(config_output_path(config, "computations_dir"), "country_networks", "pairwise_nct_summary.csv"))
readr::write_csv(edges, file.path(config_output_path(config, "computations_dir"), "country_networks", "pairwise_nct_edge_invariance.csv"))
cat("ESS country-pair NCT stage completed.\n")
