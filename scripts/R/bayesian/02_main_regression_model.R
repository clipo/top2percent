#!/usr/bin/env Rscript
#' Main Bayesian Beta Regression Model
#'
#' Fits the primary Bayesian model for the top 2% scientist rankings analysis.
#' Uses beta regression (appropriate for bounded outcome) with three prior
#' sensitivity variants:
#'   1. Default: Normal(0, 1) on coefficients
#'   2. Skeptical: Normal(0, 0.5) - more conservative
#'   3. Diffuse: Normal(0, 2) - less informative
#'
#' Model:
#'   coverage_beta ~ elsevier_pct_z + books_pct_z + field_type + log_works_z
#'
#' Outputs:
#' - models/main_beta_default.rds
#' - models/main_beta_skeptical.rds
#' - models/main_beta_diffuse.rds
#' - results/model_summaries/main_model_summary.csv
#'
#' Usage:
#'   Rscript bayesian-redo/R/02_main_regression_model.R

# =============================================================================
# SETUP
# =============================================================================

library(brms)
library(tidyverse)
library(bayestestR)
library(posterior)

# Configure Stan for parallel processing
options(mc.cores = parallel::detectCores())
rstan::rstan_options(auto_write = TRUE)

cat("===============================================================================\n")
cat("BAYESIAN BETA REGRESSION MODEL\n")
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
cat(sprintf("Using %d cores for parallel chains\n\n", parallel::detectCores()))

# =============================================================================
# LOAD PREPARED DATA
# =============================================================================

cat("Loading prepared data...\n")
df <- readRDS("bayesian-redo/results/data_prepared.rds")
cat(sprintf("  Loaded %d observations\n\n", nrow(df)))

# =============================================================================
# DEFINE PRIORS
# =============================================================================

cat("===============================================================================\n")
cat("PRIOR SPECIFICATION\n")
cat("===============================================================================\n\n")

# Default priors (weakly informative)
prior_default <- c(
  prior(normal(0, 1), class = "b"),              # Regression coefficients
  prior(normal(0, 2), class = "Intercept"),      # Intercept
  prior(gamma(2, 0.1), class = "phi")            # Beta precision parameter
)

# Skeptical priors (more regularization)
prior_skeptical <- c(
  prior(normal(0, 0.5), class = "b"),
  prior(normal(0, 2), class = "Intercept"),
  prior(gamma(2, 0.1), class = "phi")
)

# Diffuse priors (less informative)
prior_diffuse <- c(
  prior(normal(0, 2), class = "b"),
  prior(normal(0, 3), class = "Intercept"),
  prior(gamma(1, 0.1), class = "phi")
)

cat("Prior sets defined:\n")
cat("  1. DEFAULT:   Normal(0, 1) on coefficients\n")
cat("  2. SKEPTICAL: Normal(0, 0.5) on coefficients (more conservative)\n")
cat("  3. DIFFUSE:   Normal(0, 2) on coefficients (less informative)\n\n")

# =============================================================================
# MODEL FORMULA
# =============================================================================

# Main model formula
# Using standardized predictors for better sampling
model_formula <- bf(
  coverage_beta ~ elsevier_pct_z + books_pct_z + field_type_f + log_works_z
)

cat("Model formula:\n")
cat("  coverage_beta ~ elsevier_pct_z + books_pct_z + field_type_f + log_works_z\n\n")

# =============================================================================
# FIT MODEL WITH DEFAULT PRIORS
# =============================================================================

cat("===============================================================================\n")
cat("FITTING MODEL WITH DEFAULT PRIORS\n")
cat("===============================================================================\n\n")

fit_default <- brm(
  formula = model_formula,
  data = df,
  family = Beta(),
  prior = prior_default,
  chains = 4,
  iter = 4000,
  warmup = 1000,
  seed = 42,
  file = "bayesian-redo/models/main_beta_default",
  file_refit = "on_change"
)

cat("\nModel summary (DEFAULT priors):\n")
print(summary(fit_default))

# Check convergence
cat("\nConvergence diagnostics:\n")
rhat_vals <- rhat(fit_default)
cat(sprintf("  Max Rhat: %.4f (should be < 1.01)\n", max(rhat_vals, na.rm = TRUE)))
ess_bulk <- neff_ratio(fit_default)
cat(sprintf("  Min ESS ratio: %.2f (should be > 0.1)\n", min(ess_bulk, na.rm = TRUE)))

# =============================================================================
# FIT MODEL WITH SKEPTICAL PRIORS
# =============================================================================

cat("\n===============================================================================\n")
cat("FITTING MODEL WITH SKEPTICAL PRIORS\n")
cat("===============================================================================\n\n")

fit_skeptical <- brm(
  formula = model_formula,
  data = df,
  family = Beta(),
  prior = prior_skeptical,
  chains = 4,
  iter = 4000,
  warmup = 1000,
  seed = 42,
  file = "bayesian-redo/models/main_beta_skeptical",
  file_refit = "on_change"
)

cat("\nModel summary (SKEPTICAL priors):\n")
print(summary(fit_skeptical))

# =============================================================================
# FIT MODEL WITH DIFFUSE PRIORS
# =============================================================================

cat("\n===============================================================================\n")
cat("FITTING MODEL WITH DIFFUSE PRIORS\n")
cat("===============================================================================\n\n")

fit_diffuse <- brm(
  formula = model_formula,
  data = df,
  family = Beta(),
  prior = prior_diffuse,
  chains = 4,
  iter = 4000,
  warmup = 1000,
  seed = 42,
  file = "bayesian-redo/models/main_beta_diffuse",
  file_refit = "on_change"
)

cat("\nModel summary (DIFFUSE priors):\n")
print(summary(fit_diffuse))

# =============================================================================
# EXTRACT AND COMPARE POSTERIORS
# =============================================================================

cat("\n===============================================================================\n")
cat("POSTERIOR COMPARISON ACROSS PRIOR SPECIFICATIONS\n")
cat("===============================================================================\n\n")

# Function to extract posterior summary
extract_summary <- function(fit, prior_type) {
  # Get fixed effects
  fe <- fixef(fit)

  # Get posterior draws
  draws <- as_draws_df(fit)

  # Calculate probability of direction and ROPE
  params <- c("b_elsevier_pct_z", "b_books_pct_z",
              "b_field_type_fmixed", "b_field_type_fbook_heavy", "b_log_works_z")

  results <- map_dfr(params, function(p) {
    if (p %in% names(draws)) {
      vals <- draws[[p]]
      tibble(
        prior = prior_type,
        parameter = gsub("b_", "", p),
        median = median(vals),
        ci_lower = quantile(vals, 0.025),
        ci_upper = quantile(vals, 0.975),
        pd = max(mean(vals > 0), mean(vals < 0)),  # Probability of direction
        rope_pct = mean(abs(vals) < 0.1) * 100     # % in ROPE
      )
    }
  })

  return(results)
}

# Extract summaries for all three models
summary_default <- extract_summary(fit_default, "default")
summary_skeptical <- extract_summary(fit_skeptical, "skeptical")
summary_diffuse <- extract_summary(fit_diffuse, "diffuse")

# Combine
all_summaries <- bind_rows(summary_default, summary_skeptical, summary_diffuse)

# Display comparison
cat("Posterior estimates across prior specifications:\n\n")
comparison_wide <- all_summaries %>%
  select(prior, parameter, median, ci_lower, ci_upper, pd) %>%
  pivot_wider(
    names_from = prior,
    values_from = c(median, ci_lower, ci_upper, pd),
    names_glue = "{prior}_{.value}"
  )
print(comparison_wide)

# Save comparison
write_csv(all_summaries, "bayesian-redo/results/model_summaries/prior_sensitivity_comparison.csv")
cat("\nSaved: bayesian-redo/results/model_summaries/prior_sensitivity_comparison.csv\n")

# =============================================================================
# KEY FINDINGS SUMMARY
# =============================================================================

cat("\n===============================================================================\n")
cat("KEY FINDINGS (Default Priors)\n")
cat("===============================================================================\n\n")

# Extract key effects
draws <- as_draws_df(fit_default)

# H1: Elsevier effect
elsevier_effect <- draws$b_elsevier_pct_z
cat("H1 - ELSEVIER EFFECT:\n")
cat(sprintf("  Posterior median: %.4f\n", median(elsevier_effect)))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n",
            quantile(elsevier_effect, 0.025), quantile(elsevier_effect, 0.975)))
cat(sprintf("  Probability of positive effect: %.1f%%\n", mean(elsevier_effect > 0) * 100))
cat(sprintf("  ROPE (|effect| < 0.1): %.1f%%\n\n", mean(abs(elsevier_effect) < 0.1) * 100))

# H2: Book effect
book_effect <- draws$b_books_pct_z
cat("H2 - BOOK EFFECT:\n")
cat(sprintf("  Posterior median: %.4f\n", median(book_effect)))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n",
            quantile(book_effect, 0.025), quantile(book_effect, 0.975)))
cat(sprintf("  Probability of negative effect: %.1f%%\n", mean(book_effect < 0) * 100))
cat(sprintf("  ROPE (|effect| < 0.1): %.1f%%\n\n", mean(abs(book_effect) < 0.1) * 100))

# H4: Field effects
if ("b_field_type_fbook_heavy" %in% names(draws)) {
  field_effect <- draws$b_field_type_fbook_heavy
  cat("H4 - FIELD EFFECT (book_heavy vs journal_heavy):\n")
  cat(sprintf("  Posterior median: %.4f\n", median(field_effect)))
  cat(sprintf("  95%% CI: [%.4f, %.4f]\n",
              quantile(field_effect, 0.025), quantile(field_effect, 0.975)))
  cat(sprintf("  Probability of negative effect: %.1f%%\n", mean(field_effect < 0) * 100))
}

# =============================================================================
# INTERPRETATION NOTE
# =============================================================================

cat("\n===============================================================================\n")
cat("INTERPRETATION NOTE\n")
cat("===============================================================================\n\n")

cat("These coefficients are on the logit scale (beta regression uses logit link).\n")
cat("For interpretation on the probability scale:\n")
cat("  - A coefficient of 0.5 on logit scale = odds ratio of exp(0.5) = 1.65\n")
cat("  - This means ~65% higher odds of coverage per SD increase in predictor\n\n")

cat("To convert to probability scale for a specific predictor value:\n")
cat("  prob = plogis(intercept + coef * predictor_z)\n\n")

# =============================================================================
# SAVE FINAL SUMMARY
# =============================================================================

# Create comprehensive summary table
main_summary <- tibble(
  parameter = c("Intercept", "elsevier_pct_z", "books_pct_z",
                "field_type_mixed", "field_type_book_heavy", "log_works_z"),
  estimate = fixef(fit_default)[, "Estimate"],
  error = fixef(fit_default)[, "Est.Error"],
  ci_lower = fixef(fit_default)[, "Q2.5"],
  ci_upper = fixef(fit_default)[, "Q97.5"]
)

write_csv(main_summary, "bayesian-redo/results/model_summaries/main_model_summary.csv")
cat("Saved: bayesian-redo/results/model_summaries/main_model_summary.csv\n")

# =============================================================================
# DONE
# =============================================================================

cat("\n===============================================================================\n")
cat("MAIN MODEL FITTING COMPLETE\n")
cat("===============================================================================\n\n")

cat("Models saved:\n")
cat("  - bayesian-redo/models/main_beta_default.rds\n")
cat("  - bayesian-redo/models/main_beta_skeptical.rds\n")
cat("  - bayesian-redo/models/main_beta_diffuse.rds\n\n")

cat("Next steps:\n")
cat("  1. Run 03_hierarchical_field_model.R to add random effects\n")
cat("  2. Run 04_hypothesis_tests.R for formal Bayesian hypothesis tests\n")
cat("\n")
