#!/usr/bin/env Rscript
#' Data Preparation for Bayesian Analysis
#'
#' Loads and prepares data for Bayesian reanalysis of the top 2% scientist
#' rankings study.
#'
#' Key transformations:
#' - Filter to matched researchers (openalex_found == TRUE)
#' - Cap coverage_ratio at 1.5 (outlier handling)
#' - Rescale coverage_ratio to (0, 1) for beta regression
#' - Handle edge cases (0 and 1 values)
#' - Standardize predictors for interpretability
#'
#' Outputs:
#' - data_prepared.rds: Prepared data for modeling
#' - data_summary.csv: Summary statistics
#'
#' Usage:
#'   Rscript bayesian-redo/R/01_data_preparation.R

library(tidyverse)

cat("===============================================================================\n")
cat("DATA PREPARATION FOR BAYESIAN ANALYSIS\n")
cat("===============================================================================\n\n")

# Get project root - handle both direct run and sourced contexts
# Only change directory if not already in correct location
data_file <- "data/openalex_comprehensive_data.csv"
if (!file.exists(data_file)) {
  # Try to find it relative to script location
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    script_path <- sub("--file=", "", file_arg)
    # Go up from bayesian-redo/R/ or bayesian-redo/
    project_root <- normalizePath(file.path(dirname(script_path), ".."))
    if (basename(dirname(script_path)) == "R") {
      project_root <- normalizePath(file.path(dirname(script_path), "../.."))
    }
    setwd(project_root)
  }
}
cat(sprintf("Working directory: %s\n\n", getwd()))

# =============================================================================
# LOAD DATA
# =============================================================================

cat("Loading data...\n")

# Main dataset
df_raw <- read_csv("data/openalex_comprehensive_data.csv", show_col_types = FALSE)
cat(sprintf("  Raw data: %d rows x %d columns\n", nrow(df_raw), ncol(df_raw)))

# =============================================================================
# FILTER AND CLEAN
# =============================================================================

cat("\nFiltering data...\n")

# Step 1: Keep only matched researchers
df <- df_raw %>%
  filter(openalex_found == TRUE | openalex_found == "True")
cat(sprintf("  After OpenAlex filter: %d rows\n", nrow(df)))

# Step 2: Remove missing values in key variables
df <- df %>%
  filter(
    !is.na(coverage_ratio),
    !is.na(elsevier_pct),
    !is.na(books_pct)
  )
cat(sprintf("  After NA removal: %d rows\n", nrow(df)))

# Step 3: Cap coverage_ratio at 1.5 (values above suggest matching errors)
n_capped <- sum(df$coverage_ratio > 1.5)
df <- df %>%
  filter(coverage_ratio <= 1.5)
cat(sprintf("  After capping at 1.5: %d rows (removed %d outliers)\n", nrow(df), n_capped))

# =============================================================================
# TRANSFORM FOR BETA REGRESSION
# =============================================================================

cat("\nTransforming variables for beta regression...\n")

# Beta regression requires outcome in (0, 1) - not including 0 or 1
# Strategy: rescale to (0, 1) and squeeze away from boundaries

df <- df %>%
  mutate(
    # Rescale coverage_ratio from [0, 1.5] to [0, 1]
    coverage_scaled = coverage_ratio / 1.5,

    # Squeeze away from 0 and 1 (beta distribution undefined at boundaries)
    # Using the transformation: y' = (y * (n-1) + 0.5) / n
    # This shrinks toward 0.5 slightly
    n_obs = n(),
    coverage_beta = (coverage_scaled * (n_obs - 1) + 0.5) / n_obs
  )

# Verify transformation
cat(sprintf("  coverage_scaled range: [%.4f, %.4f]\n",
            min(df$coverage_scaled), max(df$coverage_scaled)))
cat(sprintf("  coverage_beta range: [%.4f, %.4f]\n",
            min(df$coverage_beta), max(df$coverage_beta)))

# =============================================================================
# STANDARDIZE PREDICTORS
# =============================================================================

cat("\nStandardizing predictors...\n")

df <- df %>%
  mutate(
    # Standardize continuous predictors (z-scores)
    elsevier_pct_z = (elsevier_pct - mean(elsevier_pct)) / sd(elsevier_pct),
    books_pct_z = (books_pct - mean(books_pct)) / sd(books_pct),
    log_works = log1p(total_works),
    log_works_z = (log_works - mean(log_works)) / sd(log_works),

    # Keep original scale versions too (for interpretability)
    elsevier_pct_10 = elsevier_pct / 10,  # Per 10pp increase
    books_pct_10 = books_pct / 10,        # Per 10pp increase

    # Factor for field_type with reference level
    field_type_f = factor(field_type,
                          levels = c("journal_heavy", "mixed", "book_heavy")),

    # Ensure field is a factor for random effects
    field_f = as.factor(field),

    # Country as factor (for potential random effects)
    country_f = as.factor(country)
  )

# Report standardization
cat("  Predictor means and SDs:\n")
cat(sprintf("    elsevier_pct: mean=%.2f, sd=%.2f\n",
            mean(df$elsevier_pct), sd(df$elsevier_pct)))
cat(sprintf("    books_pct: mean=%.2f, sd=%.2f\n",
            mean(df$books_pct), sd(df$books_pct)))
cat(sprintf("    log_works: mean=%.2f, sd=%.2f\n",
            mean(df$log_works), sd(df$log_works)))

# =============================================================================
# ADD OA VARIABLES (if available)
# =============================================================================

if ("oa_publisher_pct" %in% names(df)) {
  df <- df %>%
    mutate(
      oa_pct_z = (oa_publisher_pct - mean(oa_publisher_pct, na.rm = TRUE)) /
                  sd(oa_publisher_pct, na.rm = TRUE),
      oa_pct_10 = oa_publisher_pct / 10
    )
  cat("  Added OA publisher variables\n")
}

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

cat("\n===============================================================================\n")
cat("DATA SUMMARY\n")
cat("===============================================================================\n\n")

# Overall summary
cat(sprintf("Final sample size: n = %d\n\n", nrow(df)))

# By field type
cat("Coverage by field type:\n")
field_summary <- df %>%
  group_by(field_type_f) %>%
  summarise(
    n = n(),
    mean_coverage = mean(coverage_ratio),
    median_coverage = median(coverage_ratio),
    sd_coverage = sd(coverage_ratio),
    mean_elsevier = mean(elsevier_pct),
    mean_books = mean(books_pct),
    .groups = "drop"
  )
print(field_summary)

# Field counts
cat("\nNumber of unique fields: ", n_distinct(df$field_f), "\n")
cat("Number of unique countries: ", n_distinct(df$country_f), "\n")

# =============================================================================
# SAVE PREPARED DATA
# =============================================================================

cat("\n===============================================================================\n")
cat("SAVING PREPARED DATA\n")
cat("===============================================================================\n\n")

# Save as RDS for efficient R loading
saveRDS(df, "bayesian-redo/results/data_prepared.rds")
cat("Saved: bayesian-redo/results/data_prepared.rds\n")

# Save summary statistics
write_csv(field_summary, "bayesian-redo/results/model_summaries/data_summary_by_field.csv")
cat("Saved: bayesian-redo/results/model_summaries/data_summary_by_field.csv\n")

# Save variable summary
var_summary <- df %>%
  summarise(
    n = n(),
    coverage_mean = mean(coverage_ratio),
    coverage_median = median(coverage_ratio),
    coverage_sd = sd(coverage_ratio),
    elsevier_mean = mean(elsevier_pct),
    elsevier_sd = sd(elsevier_pct),
    books_mean = mean(books_pct),
    books_sd = sd(books_pct),
    n_fields = n_distinct(field_f),
    n_countries = n_distinct(country_f)
  )
write_csv(var_summary, "bayesian-redo/results/model_summaries/variable_summary.csv")
cat("Saved: bayesian-redo/results/model_summaries/variable_summary.csv\n")

# =============================================================================
# PREPARE DATA FOR EACH REPLICATE (for later use)
# =============================================================================

cat("\n===============================================================================\n")
cat("PREPARING REPLICATE DATA\n")
cat("===============================================================================\n\n")

replicate_files <- list.files("data/robustness_analysis/openalex_matched/",
                               pattern = "replicate_.*_openalex_data.csv",
                               full.names = TRUE)

if (length(replicate_files) > 0) {
  cat(sprintf("Found %d replicate files\n", length(replicate_files)))

  prepare_replicate <- function(file_path) {
    rep_df <- read_csv(file_path, show_col_types = FALSE)

    # Apply same transformations
    rep_df <- rep_df %>%
      filter(openalex_found == TRUE | openalex_found == "True") %>%
      filter(!is.na(coverage_ratio), !is.na(elsevier_pct), !is.na(books_pct)) %>%
      filter(coverage_ratio <= 1.5) %>%
      mutate(
        coverage_scaled = coverage_ratio / 1.5,
        n_obs = n(),
        coverage_beta = (coverage_scaled * (n_obs - 1) + 0.5) / n_obs,
        elsevier_pct_z = (elsevier_pct - mean(elsevier_pct)) / sd(elsevier_pct),
        books_pct_z = (books_pct - mean(books_pct)) / sd(books_pct),
        log_works = log1p(total_works),
        log_works_z = (log_works - mean(log_works)) / sd(log_works),
        field_type_f = factor(field_type,
                              levels = c("journal_heavy", "mixed", "book_heavy"))
      )

    return(rep_df)
  }

  # Process each replicate
  replicates <- list()
  for (i in seq_along(replicate_files)) {
    rep_name <- sprintf("replicate_%d", i)
    replicates[[rep_name]] <- prepare_replicate(replicate_files[i])
    cat(sprintf("  %s: n = %d\n", rep_name, nrow(replicates[[rep_name]])))
  }

  # Save all replicates
  saveRDS(replicates, "bayesian-redo/results/replicates_prepared.rds")
  cat("\nSaved: bayesian-redo/results/replicates_prepared.rds\n")

} else {
  cat("No replicate files found (this is OK for initial analysis)\n")
}

# =============================================================================
# DONE
# =============================================================================

cat("\n===============================================================================\n")
cat("DATA PREPARATION COMPLETE\n")
cat("===============================================================================\n\n")

cat("Next steps:\n")
cat("  1. Run 02_main_regression_model.R to fit beta regression\n")
cat("  2. Run 03_hierarchical_field_model.R to add random effects\n")
cat("\n")
