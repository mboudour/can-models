args <- commandArgs(trailingOnly = TRUE)
project_root <- normalizePath(if (length(args)) args[[1]] else getwd(), mustWork = TRUE)
source(file.path(project_root, 'R', '00_packages.R'))
source(file.path(project_root, 'R', '01_config.R'))

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

config <- read_can_config('config/ccam_dec2024_climate_engagement.yml')
run_dir <- file.path(project_root, config$output$computations_dir)
figure_dir <- file.path(project_root, config$output$figures_dir)
asset_dir <- file.path(project_root, 'app', 'assets', 'ccam_dec2024_climate_engagement')
dir.create(asset_dir, recursive = TRUE, showWarnings = FALSE)

copy_public <- function(source, destination) {
  if (!file.exists(source)) stop('Required derived CCAM output not found: ', source, call. = FALSE)
  file.copy(source, destination, overwrite = TRUE)
}

copy_public(file.path(figure_dir, 'networks', 'primary_mgm_network.png'), file.path(asset_dir, 'pooled_network.png'))
edge <- read_csv(file.path(run_dir, 'networks', 'primary_mgm', 'edge_table.csv'), show_col_types = FALSE)
centrality <- read_csv(file.path(run_dir, 'networks', 'primary_mgm', 'centrality.csv'), show_col_types = FALSE)
predictability <- read_csv(file.path(run_dir, 'networks', 'primary_mgm', 'predictability.csv'), show_col_types = FALSE)
node_map <- read_csv(file.path(run_dir, 'data_audit', 'node_map.csv'), show_col_types = FALSE)
sample_flow <- read_csv(file.path(run_dir, 'data_audit', 'sample_flow.csv'), show_col_types = FALSE)

centrality_column <- intersect(c('Strength', 'strength'), names(centrality))[[1]]
top_nodes <- centrality |>
  arrange(desc(.data[[centrality_column]])) |>
  transmute(node, strength = .data[[centrality_column]]) |>
  left_join(node_map |> select(label, domain), by = c('node' = 'label'))

summary <- tibble(
  metric = c('Primary-network sample size', 'Nodes', 'Non-zero edges', 'Possible edges', 'Network density', 'Gate decision'),
  value = c(sample_flow$value[sample_flow$statistic == 'primary_network_rows'][[1]], nrow(node_map), nrow(edge), choose(nrow(node_map), 2), round(nrow(edge) / choose(nrow(node_map), 2), 3), 'Not publication-ready: saturated network')
)

sensitivity_path <- '/home/ubuntu/ccam_feasibility_summary.csv'
if (!file.exists(sensitivity_path)) stop('Private CCAM feasibility summary is unavailable.', call. = FALSE)
sensitivity <- read_csv(sensitivity_path, show_col_types = FALSE)

write_csv(summary, file.path(asset_dir, 'network_summary.csv'))
write_csv(top_nodes, file.path(asset_dir, 'top_nodes.csv'))
write_csv(edge, file.path(asset_dir, 'edge_table.csv'))
write_csv(predictability, file.path(asset_dir, 'predictability.csv'))
write_csv(node_map, file.path(asset_dir, 'node_map.csv'))
write_csv(sensitivity, file.path(asset_dir, 'sensitivity_summary.csv'))
write_csv(sample_flow, file.path(asset_dir, 'sample_flow.csv'))

copy_public(file.path(run_dir, 'factor_models', 'anticipated_harm_cfa_pooled.csv'), file.path(asset_dir, 'anticipated_harm_cfa.csv'))
copy_public(file.path(run_dir, 'factor_models', 'transition_policy_support_cfa_pooled.csv'), file.path(asset_dir, 'policy_support_cfa.csv'))

writeLines(c(
  'CCAM December 2024 public feasibility assets',
  'Derived non-row-level assets only; no respondent-level records or source data are included.',
  'Primary ordinal MGM: 102 of 105 possible edges (density 0.971).',
  'The page must state that this saturated network is not a substantive or publication-ready CAN result.'
), file.path(asset_dir, 'README.txt'))

cat('CCAM feasibility assets written to ', asset_dir, '\n', sep = '')
