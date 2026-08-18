#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))
source(file.path(getwd(), "R", "03_network.R"))

config <- read_can_config("config/chatgpt_example.yml")
result <- readRDS(file.path(config_output_path(config, "computations_dir"), "core_analysis.rds"))
plot_path <- file.path(config_output_path(config, "figures_dir"), "networks", "primary_mgm_network.png")
plot_can_network(result$primary$result, result$prepared$node_map, plot_path, config, title = paste0(config$project$title, " — primary_mgm"))
cat("Regenerated ", plot_path, "\n", sep = "")
