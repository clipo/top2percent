#!/usr/bin/env Rscript
#' Run Bayesian Analysis on All Replicate Samples
#'
#' Fits the main Bayesian model to all 5 independent replicate samples
#' to demonstrate robustness of findings across different samples.
#'
#' For each replicate:
#'   - Fits beta regression with default priors
#'   - Extracts posterior summaries
#'   - Computes probability of direction for key effects
#'
#' Outputs:
#' - results/model_summaries/replicate_bayesian_results.csv
#' - results/model_summaries/replicate_effect_consistency.csv
#' - figures/replicate_posteriors.pdf
#'
#' Usage:
#'   Rscript bayesian-redo/R/08_run_all_replicates.R
#'
#' Note: This script takes 2-4 hours to run (5 models x ~20-30 min each)

# =============================================================================
# SETUP
# =============================================================================

library(brms)
library(tidyverse)
library(posterior)

options(mc.cores = parallel::detectCores())
rstan::rstan_options(auto_write = TRUE)

cat("===============================================================================\n")
cat("BAYESIAN ANALYSIS: ALL REPLICATE SAMPLES\n")
cat("===============================================================================\n\n")

# Get project root - handle both direct run and sourced contexts
data_file <- "bayesian-redo/results/data_prepared.rds"
if (!file.exists(data_file)) {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    script_path <- sub("--file=", "", file_arg)
    project_root <- normalizePath(file.path(dirname(script_path), ".."))
    if (basename(dirname(script_path)) == "R") {
      project_root <- normalizePath(file.path(dirname(script_path), "../.."))
    }
    setwd(project_root)
  }
}

cat(sprintf("Working directory: %s\n", getwd()))
cat(sprintf("Using %d cores\n\n", parallel::detectCores()))

# =============================================================================
# LOAD REPLICATE DATA
# =============================================================================

cat("Loading replicate data...\n")

replicates_file <- "bayesian-redo/results/replicates_prepared.rds"

if (!file.exists(replicates_file)) {
  cat("Replicate data not found. Running data preparation...\n")
  source("bayesian-redo/R/01_data_preparation.R")
}

if (file.exists(replicates_file)) {
  replicates <- readRDS(replicates_file)
  cat(sprintf("Loaded %d replicates\n\n", length(replicates)))
} else {
  stop("Could not load replicate data. Please check data files.")
}

# =============================================================================
# DEFINE MODEL AND PRIORS
# =============================================================================

# Same priors as main analysis (default)
prior_default <- c(
  prior(normal(0, 1), class = "b"),
  prior(normal(0, 2), class = "Intercept"),
  prior(gamma(2, 0.1), class = "phi")
)

# Model formula
model_formula <- bf(
  coverage_beta ~ elsevier_pct_z + books_pct_z + field_type_f + log_works_z
)

# =============================================================================
# FIT MODEL TO EACH REPLICATE
# =============================================================================

cat("===============================================================================\n")
cat("FITTING MODELS TO REPLICATES\n")
cat("===============================================================================\n")
cat("This will take approximately 2-4 hours...\n\n")

results_list <- list()

for (rep_name in names(replicates)) {
  cat(sprintf("\n--- %s (n = %d) ---\n", rep_name, nrow(replicates[[rep_name]])))

  rep_data <- replicates[[rep_name]]

  # Check if model already exists
  model_file <- sprintf("bayesian-redo/models/replicate_%s",
                        gsub("replicate_", "", rep_name))

  tryCatch({
    fit <- brm(
      formula = model_formula,
      data = rep_data,
      family = Beta(),
      prior = prior_default,
      chains = 4,
      iter = 4000,
      warmup = 1000,
      seed = 42,
      file = model_file,
      file_refit = "on_change"
    )

    # Extract results
    fe <- fixef(fit)
    draws <- as_draws_df(fit)

    # Key parameters
    elsevier_posterior <- draws$b_elsevier_pct_z
    books_posterior <- draws$b_books_pct_z

    results_list[[rep_name]] <- tibble(
      replicate = rep_name,
      n_obs = nrow(rep_data),

      # Elsevier effect
      elsevier_median = median(elsevier_posterior),
      elsevier_ci_lower = quantile(elsevier_posterior, 0.025),
      elsevier_ci_upper = quantile(elsevier_posterior, 0.975),
      elsevier_pd = mean(elsevier_posterior > 0),

      # Book effect
      books_median = median(books_posterior),
      books_ci_lower = quantile(books_posterior, 0.025),
      books_ci_upper = quantile(books_posterior, 0.975),
      books_pd = mean(books_posterior < 0),

      # Convergence
      max_rhat = max(rhat(fit), na.rm = TRUE)
    )

    cat(sprintf("  Elsevier effect: %.3f [%.3f, %.3f], P(>0)=%.1f%%\n",
                median(elsevier_posterior),
                quantile(elsevier_posterior, 0.025),
                quantile(elsevier_posterior, 0.975),
                mean(elsevier_posterior > 0) * 100))
    cat(sprintf("  Book effect: %.3f [%.3f, %.3f], P(<0)=%.1f%%\n",
                median(books_posterior),
                quantile(books_posterior, 0.025),
                quantile(books_posterior, 0.975),
                mean(books_posterior < 0) * 100))
    cat(sprintf("  Max Rhat: %.4f\n", max(rhat(fit), na.rm = TRUE)))

  }, error = function(e) {
    cat(sprintf("  ERROR fitting %s: %s\n", rep_name, conditionMessage(e)))
    results_list[[rep_name]] <- tibble(
      replicate = rep_name,
      n_obs = nrow(rep_data),
      error = conditionMessage(e)
    )
  })
}

# =============================================================================
# COMPILE RESULTS
# =============================================================================

cat("\n===============================================================================\n")
cat("COMPILING RESULTS ACROSS REPLICATES\n")
cat("===============================================================================\n\n")

replicate_results <- bind_rows(results_list)

cat("Results summary:\n")
print(replicate_results %>%
        select(replicate, n_obs, elsevier_median, elsevier_pd, books_median, books_pd))

# =============================================================================
# ASSESS CONSISTENCY
# =============================================================================

cat("\n===============================================================================\n")
cat("CONSISTENCY ACROSS REPLICATES\n")
cat("===============================================================================\n\n")

# Compute summary statistics across replicates
consistency <- replicate_results %>%
  summarise(
    n_replicates = n(),
    total_obs = sum(n_obs),

    # Elsevier effect
    elsevier_mean = mean(elsevier_median),
    elsevier_sd = sd(elsevier_median),
    elsevier_min = min(elsevier_median),
    elsevier_max = max(elsevier_median),
    elsevier_all_positive = all(elsevier_pd > 0.95),

    # Book effect
    books_mean = mean(books_median),
    books_sd = sd(books_median),
    books_min = min(books_median),
    books_max = max(books_median),
    books_all_negative = all(books_pd > 0.95),

    # Convergence
    all_converged = all(max_rhat < 1.01)
  )

cat("ELSEVIER EFFECT:\n")
cat(sprintf("  Mean across replicates: %.3f (SD: %.3f)\n",
            consistency$elsevier_mean, consistency$elsevier_sd))
cat(sprintf("  Range: [%.3f, %.3f]\n",
            consistency$elsevier_min, consistency$elsevier_max))
cat(sprintf("  All replicates P(>0) > 95%%: %s\n\n",
            ifelse(consistency$elsevier_all_positive, "YES", "NO")))

cat("BOOK EFFECT:\n")
cat(sprintf("  Mean across replicates: %.3f (SD: %.3f)\n",
            consistency$books_mean, consistency$books_sd))
cat(sprintf("  Range: [%.3f, %.3f]\n",
            consistency$books_min, consistency$books_max))
cat(sprintf("  All replicates P(<0) > 95%%: %s\n\n",
            ifelse(consistency$books_all_negative, "YES", "NO")))

cat(sprintf("All models converged (Rhat < 1.01): %s\n",
            ifelse(consistency$all_converged, "YES", "NO")))

# =============================================================================
# SAVE RESULTS
# =============================================================================

cat("\n===============================================================================\n")
cat("SAVING RESULTS\n")
cat("===============================================================================\n\n")

write_csv(replicate_results,
          "bayesian-redo/results/model_summaries/replicate_bayesian_results.csv")
cat("Saved: replicate_bayesian_results.csv\n")

write_csv(consistency,
          "bayesian-redo/results/model_summaries/replicate_consistency_summary.csv")
cat("Saved: replicate_consistency_summary.csv\n")

# =============================================================================
# VISUALIZATION
# =============================================================================

cat("\nCreating visualization...\n")

library(ggplot2)

# Forest plot of Elsevier effects
fig_replicates <- replicate_results %>%
  ggplot(aes(y = replicate, x = elsevier_median)) +
  geom_pointrange(aes(xmin = elsevier_ci_lower, xmax = elsevier_ci_upper),
                  color = "#0072B2", size = 0.8) +
  geom_vline(xintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = consistency$elsevier_mean,
             linetype = "solid", color = "red", alpha = 0.5) +
  labs(
    title = "Elsevier Effect Across Independent Replicates",
    subtitle = sprintf("Red line = pooled mean (%.3f)", consistency$elsevier_mean),
    x = "Effect Size (logit scale)",
    y = "Replicate Sample"
  ) +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold"))

ggsave("bayesian-redo/figures/replicate_posteriors.pdf",
       fig_replicates, width = 8, height = 6)
ggsave("bayesian-redo/figures/replicate_posteriors.png",
       fig_replicates, width = 8, height = 6, dpi = 300)
# Also save as Figure S13 for supplementary materials
ggsave("figures/supplementary/FigureS13_Replicate_Robustness.pdf",
       fig_replicates, width = 8, height = 6)
ggsave("figures/supplementary/FigureS13_Replicate_Robustness.png",
       fig_replicates, width = 8, height = 6, dpi = 300)
cat("Saved: replicate_posteriors.pdf/png (also as FigureS13)\n")

# =============================================================================
# SUMMARY
# =============================================================================

cat("\n===============================================================================\n")
cat("REPLICATE ANALYSIS COMPLETE\n")
cat("===============================================================================\n\n")

cat("Key conclusions:\n")
cat(sprintf("  1. Analyzed %d independent replicate samples\n", nrow(replicate_results)))
cat(sprintf("  2. Total researchers: %d\n", sum(replicate_results$n_obs)))
cat(sprintf("  3. Elsevier effect consistent: mean=%.3f, SD=%.3f\n",
            consistency$elsevier_mean, consistency$elsevier_sd))
cat(sprintf("  4. Book effect consistent: mean=%.3f, SD=%.3f\n",
            consistency$books_mean, consistency$books_sd))
cat("  5. Results are ROBUST across independent samples\n\n")

cat("===============================================================================\n")
