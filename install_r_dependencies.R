#!/usr/bin/env Rscript
# R Package Dependencies for Reproducibility Package
#
# This script installs all required R packages for figure generation.
# Run this once before generating figures.
#
# Usage:
#   Rscript install_r_dependencies.R
#
# Or from R console:
#   source("install_r_dependencies.R")

cat("Installing R dependencies for reproducibility package...\n")
cat(paste(rep("=", 80), collapse=""), "\n")

# Set CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Required packages with minimum versions
required_packages <- list(
  list(name = "ggplot2", version = "3.4.0", description = "Graphics and visualization"),
  list(name = "dplyr", version = "1.1.0", description = "Data manipulation"),
  list(name = "tidyr", version = "1.3.0", description = "Data tidying"),
  list(name = "scales", version = "1.2.0", description = "Scale functions for visualization")
)

# Function to check if package meets version requirement
check_package <- function(pkg_info) {
  pkg_name <- pkg_info$name
  min_version <- pkg_info$version
  
  if (!requireNamespace(pkg_name, quietly = TRUE)) {
    return(list(installed = FALSE, current_version = NULL, needs_update = TRUE))
  }
  
  current_version <- as.character(packageVersion(pkg_name))
  needs_update <- compareVersion(current_version, min_version) < 0
  
  return(list(
    installed = TRUE,
    current_version = current_version,
    needs_update = needs_update
  ))
}

# Check and install packages
for (pkg_info in required_packages) {
  pkg_name <- pkg_info$name
  status <- check_package(pkg_info)
  
  if (!status$installed) {
    cat(sprintf("Installing %s (>= %s)...\n", pkg_name, pkg_info$version))
    install.packages(pkg_name, quiet = TRUE)
    cat(sprintf("  ✓ Installed %s\n", pkg_name))
  } else if (status$needs_update) {
    cat(sprintf("Updating %s: %s -> >= %s...\n", 
                pkg_name, status$current_version, pkg_info$version))
    install.packages(pkg_name, quiet = TRUE)
    new_version <- as.character(packageVersion(pkg_name))
    cat(sprintf("  ✓ Updated to %s\n", new_version))
  } else {
    cat(sprintf("✓ %s %s (>= %s required) - %s\n",
                pkg_name, status$current_version, pkg_info$version, 
                pkg_info$description))
  }
}

cat("\n")
cat(paste(rep("=", 80), collapse=""), "\n")
cat("✓ All R dependencies installed successfully!\n")
cat("\n")
cat("Package summary:\n")
for (pkg_info in required_packages) {
  version <- as.character(packageVersion(pkg_info$name))
  cat(sprintf("  - %s: %s\n", pkg_info$name, version))
}

cat("\n")
cat("Next steps:\n")
cat("  1. Generate all figures: python3 generate_all_figures.py\n")
cat("  2. Or generate Figures 1-3 only: Rscript scripts/R/figures_1_2_3_coverage_analysis.R\n")
cat("  3. See README_REPRODUCIBILITY.md for full instructions\n")
cat("\n")
