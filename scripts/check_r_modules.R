#!/usr/bin/env Rscript

modules <- c(
  "00_packages.R", "01_config.R", "02_data.R", "03_network.R", "04_diagnostics.R",
  "05_factor.R", "06_compare.R", "07_country.R", "08_cluster.R", "09_networktree.R", "10_context.R"
)
for (module in modules) {
  source(file.path(getwd(), "R", module))
  cat("Loaded ", module, "\n", sep = "")
}
cat("All R modules parsed and loaded successfully.\n")
