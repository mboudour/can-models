#!/usr/bin/env Rscript

source(file.path(getwd(), "R", "00_packages.R"))
source(file.path(getwd(), "R", "01_config.R"))
source(file.path(getwd(), "R", "02_data.R"))

input <- data.frame(
  node_a = c(1, 9, 5, 99),
  node_b = c(2, 3, 99, 9),
  category = c(1, 2, 3, 3)
)
config <- list(
  preprocessing = list(
    missing_values = list(list(variables = c("node_a", "node_b"), values = c(9, 99))),
    collapse_values = list(list(variable = "category", from = list(3), to = 2))
  )
)

output <- apply_can_transformations(input, config)
stopifnot(identical(output$node_a, c(1, NA_real_, 5, NA_real_)))
stopifnot(identical(output$node_b, c(2, 3, NA_real_, NA_real_)))
stopifnot(identical(output$category, c(1, 2, 2, 2)))

audit <- attr(output, "transformation_audit")
stopifnot(sum(audit$transformation == "missing_values_to_na") == 2L)
stopifnot(sum(audit$transformation == "collapse_values") == 1L)

cat("Data transformation test passed.\n")
