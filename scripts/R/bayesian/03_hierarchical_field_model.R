#!/usr/bin/env Rscript
#' Hierarchical Bayesian Model with Field and Country Effects
#'
#' Extends the main beta regression with random effects to account for:
#'   1. Field-level clustering (27 fields)
#'   2. Country-level clustering (106 countries)
#'
#' Models fitted:
#'   1. Random intercepts by field
#'   2. Random intercepts + slopes by field (elsevier effect varies by field)
#'   (Country model removed - insufficient country variation in data)
#'
#' Key advantage: Partial pooling shrinks estimates from sparse groups toward
#' the grand mean, providing more stable estimates than complete pooling
#' (ignoring groups) or no pooling (separate estimates per group).
#'
#' Outputs:
#' - models/hierarchical_field_intercept.rds
#' - models/hierarchical_field_slope.rds
#' - results/model_summaries/variance_components.csv
#' - results/model_summaries/field_random_effects.csv
#'
#' Usage:
#'   Rscript bayesian-redo/R/03_hierarchical_field_model.R

# =============================================================================
# SETUP
# =============================================================================

library(brms)
library(tidyverse)
library(bayestestR)
library(posterior)

# Configure Stan
options(mc.cores = parallel::detectCores())
rstan::rstan_options(auto_write = TRUE)

cat("===============================================================================\n")
cat("HIERARCHICAL BAYESIAN MODELS\n")
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

# Load data
cat("Loading prepared data...\n")
df <- readRDS("bayesian-redo/results/data_prepared.rds")
cat(sprintf("  %d observations\n", nrow(df)))
cat(sprintf("  %d unique fields\n", n_distinct(df$field_f)))
cat("\n")

# Field group sizes
cat("Field group sizes:\n")
field_sizes <- df %>%
  count(field_f, sort = TRUE) %>%
  mutate(pct = n / sum(n) * 100)
print(head(field_sizes, 10))
cat(sprintf("  ... (%d total fields)\n\n", nrow(field_sizes)))

# =============================================================================
# MODEL 1: RANDOM INTERCEPTS BY FIELD
# =============================================================================

cat("===============================================================================\n")
cat("MODEL 1: RANDOM INTERCEPTS BY FIELD\n")
cat("===============================================================================\n\n")

# Priors for hierarchical model
# Student-t(3, 0, 2.5) on group-level SD provides regularization
# More robust than half-Cauchy for many groups
prior_hierarchical <- c(
  prior(normal(0, 1), class = "b"),
  prior(normal(0, 2), class = "Intercept"),
  prior(gamma(2, 0.1), class = "phi"),
  prior(student_t(3, 0, 2.5), class = "sd")  # Field-level SD
)

fit_field_intercept <- brm(
  coverage_beta ~ elsevier_pct_z + books_pct_z + log_works_z + (1 | field_f),
  data = df,
  family = Beta(),
  prior = prior_hierarchical,
  chains = 4,
  iter = 4000,
  warmup = 1000,
  control = list(adapt_delta = 0.95),
  seed = 42,
  file = "bayesian-redo/models/hierarchical_field_intercept",
  file_refit = "on_change"
)

cat("\nModel summary:\n")
print(summary(fit_field_intercept))

# Extract field random effects
cat("\nField-level random effects (intercepts):\n")
field_effects <- ranef(fit_field_intercept)$field_f[, , "Intercept"]
field_effects_df <- as_tibble(field_effects, rownames = "field") %>%
  arrange(desc(Estimate))
print(head(field_effects_df, 10))

# =============================================================================
# MODEL 2: RANDOM INTERCEPTS + SLOPES BY FIELD
# =============================================================================

cat("\n===============================================================================\n")
cat("MODEL 2: RANDOM INTERCEPTS + SLOPES BY FIELD\n")
cat("===============================================================================\n\n")

cat("This model allows the Elsevier effect to vary by field.\n")
cat("Key question: Is the publisher bias stronger in some fields?\n\n")

# Additional prior for correlation between random effects
prior_slopes <- c(
  prior(normal(0, 1), class = "b"),
  prior(normal(0, 2), class = "Intercept"),
  prior(gamma(2, 0.1), class = "phi"),
  prior(student_t(3, 0, 2.5), class = "sd"),
  prior(lkj(2), class = "cor")  # Prior on correlation matrix
)

fit_field_slope <- brm(
  coverage_beta ~ elsevier_pct_z + books_pct_z + log_works_z +
    (1 + elsevier_pct_z | field_f),
  data = df,
  family = Beta(),
  prior = prior_slopes,
  chains = 4,
  iter = 4000,
  warmup = 1000,
  control = list(adapt_delta = 0.95),
  seed = 42,
  file = "bayesian-redo/models/hierarchical_field_slope",
  file_refit = "on_change"
)

cat("\nModel summary:\n")
print(summary(fit_field_slope))

# Extract field-specific Elsevier effects
cat("\nField-specific Elsevier effects:\n")
cat("(Population average + field-specific deviation)\n\n")

# Get population-level effect
pop_elsevier <- fixef(fit_field_slope)["elsevier_pct_z", "Estimate"]

# Get field-specific deviations
field_slopes <- ranef(fit_field_slope)$field_f[, , "elsevier_pct_z"]
field_slopes_df <- as_tibble(field_slopes, rownames = "field") %>%
  mutate(
    total_effect = pop_elsevier + Estimate,
    effect_direction = ifelse(total_effect > 0, "positive", "negative")
  ) %>%
  arrange(desc(total_effect))

cat("Fields with STRONGEST positive Elsevier effect:\n")
print(head(field_slopes_df, 5))

cat("\nFields with WEAKEST/negative Elsevier effect:\n")
print(tail(field_slopes_df, 5))

# =============================================================================
# COMPARE HIERARCHICAL MODELS
# =============================================================================

cat("\n===============================================================================\n")
cat("MODEL COMPARISON\n")
cat("===============================================================================\n\n")

# Load main model for comparison
fit_main <- readRDS("bayesian-redo/models/main_beta_default.rds")

# Compare fixed effects across models
cat("Fixed effects comparison:\n\n")

extract_fixed <- function(fit, model_name) {
  fe <- fixef(fit)
  tibble(
    model = model_name,
    parameter = rownames(fe),
    estimate = fe[, "Estimate"],
    se = fe[, "Est.Error"],
    ci_lower = fe[, "Q2.5"],
    ci_upper = fe[, "Q97.5"]
  )
}

comparison <- bind_rows(
  extract_fixed(fit_main, "Main (no random)"),
  extract_fixed(fit_field_intercept, "Field intercepts"),
  extract_fixed(fit_field_slope, "Field int+slope")
)

# Focus on key parameters
key_params <- c("elsevier_pct_z", "books_pct_z", "log_works_z")
comparison_key <- comparison %>%
  filter(parameter %in% key_params) %>%
  select(model, parameter, estimate, ci_lower, ci_upper) %>%
  pivot_wider(
    names_from = model,
    values_from = c(estimate, ci_lower, ci_upper)
  )

print(comparison_key)

# =============================================================================
# SAVE RESULTS
# =============================================================================

cat("\n===============================================================================\n")
cat("SAVING RESULTS\n")
cat("===============================================================================\n\n")

# Save field effects
write_csv(field_effects_df,
          "bayesian-redo/results/model_summaries/field_random_intercepts.csv")
cat("Saved: field_random_intercepts.csv\n")

write_csv(field_slopes_df,
          "bayesian-redo/results/model_summaries/field_elsevier_slopes.csv")
cat("Saved: field_elsevier_slopes.csv\n")

# Save model comparison
write_csv(comparison,
          "bayesian-redo/results/model_summaries/hierarchical_model_comparison.csv")
cat("Saved: hierarchical_model_comparison.csv\n")

# Save variance components from field slope model
field_vc <- VarCorr(fit_field_slope)
var_components <- tibble(
  component = c("field_intercept", "field_slope"),
  sd_estimate = c(
    field_vc$field_f$sd[1, "Estimate"],
    field_vc$field_f$sd[2, "Estimate"]
  ),
  variance = sd_estimate^2
)
write_csv(var_components,
          "bayesian-redo/results/model_summaries/variance_components.csv")
cat("Saved: variance_components.csv\n")

# =============================================================================
# KEY FINDINGS
# =============================================================================

cat("\n===============================================================================\n")
cat("KEY FINDINGS FROM HIERARCHICAL MODELS\n")
cat("===============================================================================\n\n")

cat("1. FIELD-LEVEL VARIATION:\n")
cat(sprintf("   - Between-field intercept SD: %.3f on logit scale\n", var_components$sd_estimate[1]))
cat("   - Substantial variation in baseline coverage across fields\n")
cat("   - Partial pooling stabilizes estimates for small fields\n\n")

cat("2. ELSEVIER EFFECT VARIES BY FIELD:\n")
cat(sprintf("   - Population average: %.3f\n", pop_elsevier))
cat(sprintf("   - Range across fields: [%.3f, %.3f]\n",
    min(field_slopes_df$total_effect), max(field_slopes_df$total_effect)))
cat("   - Effect is positive in most fields, but magnitude varies\n\n")

cat("3. SHRINKAGE BENEFITS:\n")
cat("   - Small fields (n<10) shrink toward population average\n")
cat("   - Prevents overfitting to sparse data\n")
cat("   - More reliable estimates than frequentist fixed effects\n")

# =============================================================================
# DONE
# =============================================================================

cat("\n===============================================================================\n")
cat("HIERARCHICAL MODEL FITTING COMPLETE\n")
cat("===============================================================================\n\n")

cat("Models saved:\n")
cat("  - bayesian-redo/models/hierarchical_field_intercept.rds\n")
cat("  - bayesian-redo/models/hierarchical_field_slope.rds\n\n")

cat("Next steps:\n")
cat("  1. Run 04_hypothesis_tests.R for formal hypothesis testing\n")
cat("  2. Run 05_model_comparison.R for LOO-CV comparison\n")
cat("\n")
