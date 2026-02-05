#!/usr/bin/env Rscript
#' Install Bayesian Analysis Dependencies
#'
#' This script installs all R packages required for the Bayesian reanalysis
#' of the top 2% scientist rankings study.
#'
#' Required packages:
#' - brms: Bayesian regression models using Stan
#' - rstan: R interface to Stan
#' - bayesplot: Plotting for Bayesian models
#' - loo: Leave-one-out cross-validation
#' - tidybayes: Tidy data extraction from Bayesian models
#' - posterior: Posterior distribution manipulation
#' - bayestestR: Bayesian hypothesis testing utilities
#'
#' Usage:
#'   Rscript bayesian-redo/R/00_install_deps.R
#'
#' Note: Stan requires a C++ toolchain. On Linux, install build-essential.
#'       On Mac, install Xcode command line tools.
#'       On Windows, install Rtools.

cat("===============================================================================\n")
cat("BAYESIAN ANALYSIS DEPENDENCY INSTALLATION\n")
cat("===============================================================================\n\n")

# Set CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Define required packages with minimum versions
required_packages <- list(
  brms = "2.20.0",
  rstan = "2.26.0",
  bayesplot = "1.10.0",
  loo = "2.6.0",
  tidybayes = "3.0.0",
  posterior = "1.4.0",
  bayestestR = "0.13.0",
  # Additional utilities
  tidyverse = "2.0.0",
  ggdist = "3.3.0"
)

# Function to check and install packages
install_if_needed <- function(pkg, min_version) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("Installing %s...\n", pkg))
    install.packages(pkg, dependencies = TRUE)
    installed <- TRUE
  } else {
    current_version <- as.character(packageVersion(pkg))
    if (compareVersion(current_version, min_version) < 0) {
      cat(sprintf("Updating %s from %s to >= %s...\n", pkg, current_version, min_version))
      install.packages(pkg, dependencies = TRUE)
      installed <- TRUE
    } else {
      cat(sprintf("OK: %s %s (>= %s required)\n", pkg, current_version, min_version))
      installed <- FALSE
    }
  }
  return(installed)
}

# Install packages
cat("Checking and installing packages...\n\n")
any_installed <- FALSE

for (pkg in names(required_packages)) {
  result <- install_if_needed(pkg, required_packages[[pkg]])
  any_installed <- any_installed || result
}

cat("\n")

# Verify Stan toolchain
cat("===============================================================================\n")
cat("VERIFYING STAN TOOLCHAIN\n")
cat("===============================================================================\n\n")

# Check if Stan can compile
cat("Testing Stan compilation (this may take a moment)...\n")
tryCatch({
  library(rstan)

  # Simple test model
  test_code <- "
  parameters {
    real y;
  }
  model {
    y ~ normal(0, 1);
  }
  "

  # Try to compile (not run)
  test_model <- stan_model(model_code = test_code, verbose = FALSE)
  cat("OK: Stan toolchain is working!\n\n")

}, error = function(e) {
  cat("\nWARNING: Stan compilation failed!\n")
  cat("Error message:", conditionMessage(e), "\n\n")
  cat("Please ensure you have a C++ toolchain installed:\n")
  cat("  - Linux: sudo apt-get install build-essential\n")
  cat("  - Mac: xcode-select --install\n")
  cat("  - Windows: Install Rtools from https://cran.r-project.org/bin/windows/Rtools/\n\n")
})

# Configure Stan options for parallel processing
cat("===============================================================================\n")
cat("CONFIGURING STAN OPTIONS\n")
cat("===============================================================================\n\n")

# Detect number of cores
n_cores <- parallel::detectCores()
cat(sprintf("Detected %d CPU cores\n", n_cores))

# Set recommended options
cat("Setting recommended Stan options:\n")
cat("  - mc.cores: Using all available cores for parallel chains\n")
cat("  - auto_write: Caching compiled models\n\n")

# These will be set in the analysis scripts
cat("Add the following to your .Rprofile or at the start of analysis scripts:\n")
cat(sprintf("  options(mc.cores = %d)\n", n_cores))
cat("  rstan_options(auto_write = TRUE)\n\n")

# Final summary
cat("===============================================================================\n")
cat("INSTALLATION SUMMARY\n")
cat("===============================================================================\n\n")

cat("Installed packages:\n")
for (pkg in names(required_packages)) {
  if (requireNamespace(pkg, quietly = TRUE)) {
    ver <- as.character(packageVersion(pkg))
    cat(sprintf("  [OK] %s %s\n", pkg, ver))
  } else {
    cat(sprintf("  [MISSING] %s\n", pkg))
  }
}

cat("\n")
cat("Next steps:\n")
cat("  1. Run 01_data_preparation.R to load and prepare data\n")
cat("  2. Run 02_main_regression_model.R to fit the main Bayesian model\n")
cat("\n")
cat("===============================================================================\n")
