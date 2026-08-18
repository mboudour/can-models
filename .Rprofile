source("renv/activate.R")

# Keep the project-local package library first while allowing the reproducible
# example to reuse compatible system libraries when available.
project_library <- normalizePath(".Rlib", mustWork = FALSE)
.libPaths(unique(c(project_library, .libPaths(), .Library.site, .Library)))
