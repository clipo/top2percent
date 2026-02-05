#!/usr/bin/env Rscript
#' Master Script: Run All Bayesian Analyses
#'
#' This script runs the complete Bayesian analysis pipeline:
#'   1. Install dependencies (if needed)
#'   2. Prepare data
#'   3. Fit main beta regression (3 prior variants)
#'   4. Fit hierarchical models
#'   5. Bayesian hypothesis tests
#'   6. Model comparison
#'   7. Visualizations
#'   8. Frequentist comparison
#'   9. Replicate analysis (optional, time-intensive)
#'
#' Usage:
#'   Rscript bayesian-redo/run_all.R           # Full analysis (excl. replicates)
#'   Rscript bayesian-redo/run_all.R --full    # Full analysis incl. replicates
#'   Rscript bayesian-redo/run_all.R --quick   # Just main model
#'
#' Estimated times:
#'   --quick: ~15-30 minutes
#'   default: ~1-2 hours
#'   --full:  ~3-5 hours

# =============================================================================
# SETUP
# =============================================================================

args <- commandArgs(trailingOnly = TRUE)
run_mode <- if ("--full" %in% args) "full" else if ("--quick" %in% args) "quick" else "default"

cat("===============================================================================\n")
cat("BAYESIAN REANALYSIS: MASTER SCRIPT\n")
cat("===============================================================================\n\n")

start_time <- Sys.time()

# Get script directory (works with Rscript)
get_script_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    return(dirname(normalizePath(sub("^--file=", "", file_arg))))
  }
  return("bayesian-redo")
}

script_dir <- get_script_dir()

# Set working directory to project root
if (basename(script_dir) == "bayesian-redo") {
  project_root <- dirname(script_dir)
} else {
  project_root <- file.path(script_dir, "..")
}
setwd(project_root)
project_root <- getwd()

cat(sprintf("Project root: %s\n", project_root))
cat(sprintf("Run mode: %s\n", run_mode))
cat(sprintf("Start time: %s\n\n", start_time))

# Helper function to run scripts
run_script <- function(script_path, description) {
  cat(sprintf("\n>>> %s <<<\n", description))
  cat(sprintf("Running: %s\n", script_path))
  cat(paste(rep("-", 70), collapse = ""), "\n")

  result <- tryCatch({
    source(script_path, local = new.env())
    TRUE
  }, error = function(e) {
    cat(sprintf("ERROR: %s\n", conditionMessage(e)))
    FALSE
  })

  if (result) {
    cat(sprintf("Completed: %s\n", description))
  } else {
    cat(sprintf("FAILED: %s\n", description))
  }

  return(result)
}

# =============================================================================
# STEP 1: INSTALL DEPENDENCIES
# =============================================================================

cat("===============================================================================\n")
cat("STEP 1: CHECKING DEPENDENCIES\n")
cat("===============================================================================\n")

# Check if brms is installed
if (!requireNamespace("brms", quietly = TRUE)) {
  cat("Installing dependencies...\n")
  run_script("bayesian-redo/R/00_install_deps.R", "Install Dependencies")
} else {
  cat("Dependencies already installed.\n")
  cat(sprintf("  brms version: %s\n", as.character(packageVersion("brms"))))
}

# =============================================================================
# STEP 2: DATA PREPARATION
# =============================================================================

cat("\n===============================================================================\n")
cat("STEP 2: DATA PREPARATION\n")
cat("===============================================================================\n")

if (!file.exists("bayesian-redo/results/data_prepared.rds")) {
  run_script("bayesian-redo/R/01_data_preparation.R", "Data Preparation")
} else {
  cat("Data already prepared. Loading...\n")
  df <- readRDS("bayesian-redo/results/data_prepared.rds")
  cat(sprintf("  Loaded %d observations\n", nrow(df)))
}

# =============================================================================
# STEP 3: MAIN REGRESSION MODEL
# =============================================================================

cat("\n===============================================================================\n")
cat("STEP 3: MAIN BETA REGRESSION MODEL\n")
cat("===============================================================================\n")

run_script("bayesian-redo/R/02_main_regression_model.R", "Main Beta Regression (3 prior variants)")

if (run_mode == "quick") {
  cat("\n>>> Quick mode: Stopping after main model <<<\n")
  end_time <- Sys.time()
  cat(sprintf("\nTotal time: %.1f minutes\n", difftime(end_time, start_time, units = "mins")))
  quit(save = "no")
}

# =============================================================================
# STEP 4: HIERARCHICAL MODELS
# =============================================================================

cat("\n===============================================================================\n")
cat("STEP 4: HIERARCHICAL MODELS\n")
cat("===============================================================================\n")

run_script("bayesian-redo/R/03_hierarchical_field_model.R", "Hierarchical Field Models")

# =============================================================================
# STEP 5: BAYESIAN HYPOTHESIS TESTS
# =============================================================================

cat("\n===============================================================================\n")
cat("STEP 5: BAYESIAN HYPOTHESIS TESTS\n")
cat("===============================================================================\n")

run_script("bayesian-redo/R/04_hypothesis_tests.R", "Bayesian Hypothesis Tests")

# =============================================================================
# STEP 6: MODEL COMPARISON
# =============================================================================

cat("\n===============================================================================\n")
cat("STEP 6: MODEL COMPARISON (LOO-CV)\n")
cat("===============================================================================\n")

run_script("bayesian-redo/R/05_model_comparison.R", "Model Comparison")

# =============================================================================
# STEP 7: VISUALIZATIONS
# =============================================================================

cat("\n===============================================================================\n")
cat("STEP 7: POSTERIOR VISUALIZATIONS\n")
cat("===============================================================================\n")

run_script("bayesian-redo/R/06_posterior_visualization.R", "Posterior Visualizations")

# =============================================================================
# STEP 8: FREQUENTIST COMPARISON
# =============================================================================

cat("\n===============================================================================\n")
cat("STEP 8: FREQUENTIST COMPARISON\n")
cat("===============================================================================\n")

run_script("bayesian-redo/R/07_frequentist_comparison.R", "Frequentist Comparison")

# =============================================================================
# STEP 9: REPLICATE ANALYSIS (OPTIONAL)
# =============================================================================

if (run_mode == "full") {
  cat("\n===============================================================================\n")
  cat("STEP 9: REPLICATE ANALYSIS\n")
  cat("===============================================================================\n")
  cat("WARNING: This step takes 2-4 hours!\n\n")

  run_script("bayesian-redo/R/08_run_all_replicates.R", "Replicate Analysis")
} else {
  cat("\n===============================================================================\n")
  cat("STEP 9: REPLICATE ANALYSIS (SKIPPED)\n")
  cat("===============================================================================\n")
  cat("Run with --full flag to include replicate analysis.\n")
}

# =============================================================================
# SUMMARY
# =============================================================================

end_time <- Sys.time()
duration <- difftime(end_time, start_time, units = "mins")

cat("\n")
cat("===============================================================================\n")
cat("BAYESIAN ANALYSIS COMPLETE\n")
cat("===============================================================================\n\n")

cat(sprintf("Start time: %s\n", start_time))
cat(sprintf("End time: %s\n", end_time))
cat(sprintf("Total duration: %.1f minutes\n\n", duration))

cat("Generated outputs:\n")
cat("\nModels (bayesian-redo/models/):\n")
model_files <- list.files("bayesian-redo/models", pattern = "\\.rds$")
for (f in model_files) cat(sprintf("  - %s\n", f))

cat("\nResults (bayesian-redo/results/):\n")
result_files <- list.files("bayesian-redo/results", pattern = "\\.csv$", recursive = TRUE)
for (f in result_files) cat(sprintf("  - %s\n", f))

cat("\nFigures (bayesian-redo/figures/):\n")
fig_files <- list.files("bayesian-redo/figures", pattern = "\\.(pdf|png)$")
for (f in fig_files) cat(sprintf("  - %s\n", f))

cat("\n===============================================================================\n")
cat("See bayesian-redo/METHODS.md for detailed methods documentation.\n")
cat("See bayesian-redo/README.md for reproduction instructions.\n")
cat("===============================================================================\n")
