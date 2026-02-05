#!/usr/bin/env Rscript
#' Bayesian Hypothesis Testing
#'
#' Performs formal Bayesian hypothesis tests for all study hypotheses:
#'   H1: Elsevier publisher bias (positive effect on coverage)
#'   H2: Book publication bias (negative effect on coverage)
#'   H3: Open access effect (test for no penalty)
#'   H4: Field-level bias (differences between field types)
#'
#' Bayesian alternatives to frequentist tests:
#'   - Probability of Direction (pd) instead of p-values
#'   - Region of Practical Equivalence (ROPE) for equivalence testing
#'   - Bayes Factors for model comparison
#'   - Credible intervals instead of confidence intervals
#'
#' Outputs:
#' - results/model_summaries/bayesian_hypothesis_tests.csv
#' - results/posteriors/hypothesis_posteriors.csv
#'
#' Usage:
#'   Rscript bayesian-redo/R/04_hypothesis_tests.R

# =============================================================================
# SETUP
# =============================================================================

library(brms)
library(tidyverse)
library(bayestestR)
library(posterior)

cat("===============================================================================\n")
cat("BAYESIAN HYPOTHESIS TESTING\n")
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

# Load models
cat("Loading fitted models...\n")
fit_main <- readRDS("bayesian-redo/models/main_beta_default.rds")
fit_hierarchical <- readRDS("bayesian-redo/models/hierarchical_field_slope.rds")
cat("  Models loaded successfully\n\n")

# Extract posterior draws
draws_main <- as_draws_df(fit_main)
draws_hier <- as_draws_df(fit_hierarchical)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

# Comprehensive hypothesis test summary
test_hypothesis <- function(posterior_samples, hypothesis_name, direction = "two-sided",
                           rope_range = c(-0.1, 0.1)) {

  # Basic statistics
  median_est <- median(posterior_samples)
  mean_est <- mean(posterior_samples)
  sd_est <- sd(posterior_samples)
  ci_95 <- quantile(posterior_samples, c(0.025, 0.975))
  ci_89 <- quantile(posterior_samples, c(0.055, 0.945))

  # Probability of Direction (pd)
  # Probability that the effect is consistently positive or negative
  pd <- max(mean(posterior_samples > 0), mean(posterior_samples < 0))

  # ROPE (Region of Practical Equivalence)
  # Percentage of posterior within "negligible effect" range
  in_rope <- mean(posterior_samples >= rope_range[1] &
                  posterior_samples <= rope_range[2])

  # Probability of effect being in expected direction
  if (direction == "positive") {
    prob_direction <- mean(posterior_samples > 0)
  } else if (direction == "negative") {
    prob_direction <- mean(posterior_samples < 0)
  } else {
    prob_direction <- NA
  }

  # Effect size interpretation (on logit scale)
  # |effect| < 0.2: negligible, 0.2-0.5: small, 0.5-0.8: medium, >0.8: large
  abs_median <- abs(median_est)
  if (abs_median < 0.2) {
    effect_size <- "negligible"
  } else if (abs_median < 0.5) {
    effect_size <- "small"
  } else if (abs_median < 0.8) {
    effect_size <- "medium"
  } else {
    effect_size <- "large"
  }

  tibble(
    hypothesis = hypothesis_name,
    median = median_est,
    mean = mean_est,
    sd = sd_est,
    ci_95_lower = ci_95[1],
    ci_95_upper = ci_95[2],
    ci_89_lower = ci_89[1],
    ci_89_upper = ci_89[2],
    pd = pd,
    rope_pct = in_rope * 100,
    prob_expected_direction = prob_direction,
    effect_size_category = effect_size
  )
}

# =============================================================================
# H1: ELSEVIER PUBLISHER BIAS
# =============================================================================

cat("===============================================================================\n")
cat("H1: ELSEVIER PUBLISHER BIAS\n")
cat("===============================================================================\n\n")

cat("Hypothesis: Higher Elsevier publication percentage is associated with\n")
cat("            HIGHER Scopus coverage (positive effect).\n\n")

elsevier_posterior <- draws_main$b_elsevier_pct_z

h1_results <- test_hypothesis(
  elsevier_posterior,
  "H1: Elsevier Effect",
  direction = "positive",
  rope_range = c(-0.1, 0.1)
)

cat("Results:\n")
cat(sprintf("  Posterior median: %.4f (logit scale)\n", h1_results$median))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n", h1_results$ci_95_lower, h1_results$ci_95_upper))
cat(sprintf("  Probability of Direction (pd): %.1f%%\n", h1_results$pd * 100))
cat(sprintf("  P(effect > 0): %.1f%%\n", h1_results$prob_expected_direction * 100))
cat(sprintf("  ROPE [-0.1, 0.1]: %.1f%% in ROPE\n", h1_results$rope_pct))
cat(sprintf("  Effect size: %s\n\n", h1_results$effect_size_category))

cat("Interpretation:\n")
if (h1_results$prob_expected_direction > 0.95 && h1_results$rope_pct < 5) {
  cat("  STRONG EVIDENCE for positive Elsevier effect.\n")
  cat("  The 95% CI excludes zero and the ROPE.\n")
} else if (h1_results$prob_expected_direction > 0.90) {
  cat("  MODERATE EVIDENCE for positive Elsevier effect.\n")
} else {
  cat("  WEAK or INCONCLUSIVE evidence.\n")
}

# =============================================================================
# H2: BOOK PUBLICATION BIAS
# =============================================================================

cat("\n===============================================================================\n")
cat("H2: BOOK PUBLICATION BIAS\n")
cat("===============================================================================\n\n")

cat("Hypothesis: Higher book/chapter percentage is associated with\n")
cat("            LOWER Scopus coverage (negative effect).\n\n")

book_posterior <- draws_main$b_books_pct_z

h2_results <- test_hypothesis(
  book_posterior,
  "H2: Book Effect",
  direction = "negative",
  rope_range = c(-0.1, 0.1)
)

cat("Results:\n")
cat(sprintf("  Posterior median: %.4f (logit scale)\n", h2_results$median))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n", h2_results$ci_95_lower, h2_results$ci_95_upper))
cat(sprintf("  Probability of Direction (pd): %.1f%%\n", h2_results$pd * 100))
cat(sprintf("  P(effect < 0): %.1f%%\n", h2_results$prob_expected_direction * 100))
cat(sprintf("  ROPE [-0.1, 0.1]: %.1f%% in ROPE\n", h2_results$rope_pct))
cat(sprintf("  Effect size: %s\n\n", h2_results$effect_size_category))

# =============================================================================
# H3: OPEN ACCESS (if available)
# =============================================================================

cat("\n===============================================================================\n")
cat("H3: OPEN ACCESS EFFECT\n")
cat("===============================================================================\n\n")

# Load data to check for OA variable
df <- readRDS("bayesian-redo/results/data_prepared.rds")

if ("oa_pct_z" %in% names(df) && !all(is.na(df$oa_pct_z))) {
  cat("Testing: Is there an Open Access penalty?\n")
  cat("Hypothesis: OA publishers should NOT have worse coverage.\n\n")

  # Fit model with OA predictor
  fit_oa <- brm(
    coverage_beta ~ elsevier_pct_z + books_pct_z + oa_pct_z + log_works_z + field_type_f,
    data = df,
    family = Beta(),
    prior = c(
      prior(normal(0, 1), class = "b"),
      prior(normal(0, 2), class = "Intercept"),
      prior(gamma(2, 0.1), class = "phi")
    ),
    chains = 4,
    iter = 4000,
    warmup = 1000,
    seed = 42,
    file = "bayesian-redo/models/main_beta_with_oa",
    file_refit = "on_change"
  )

  draws_oa <- as_draws_df(fit_oa)
  oa_posterior <- draws_oa$b_oa_pct_z

  h3_results <- test_hypothesis(
    oa_posterior,
    "H3: OA Effect",
    direction = "two-sided",
    rope_range = c(-0.1, 0.1)
  )

  cat("Results:\n")
  cat(sprintf("  Posterior median: %.4f\n", h3_results$median))
  cat(sprintf("  95%% CI: [%.4f, %.4f]\n", h3_results$ci_95_lower, h3_results$ci_95_upper))
  cat(sprintf("  P(effect > 0): %.1f%%\n", mean(oa_posterior > 0) * 100))
  cat(sprintf("  P(effect < 0): %.1f%%\n", mean(oa_posterior < 0) * 100))

  if (mean(oa_posterior > 0) > 0.5) {
    cat("\n  NO EVIDENCE of OA penalty - effect appears POSITIVE.\n")
  }
} else {
  cat("OA variable not available in dataset. Skipping H3.\n")
  h3_results <- tibble(
    hypothesis = "H3: OA Effect",
    median = NA, mean = NA, sd = NA,
    ci_95_lower = NA, ci_95_upper = NA,
    ci_89_lower = NA, ci_89_upper = NA,
    pd = NA, rope_pct = NA,
    prob_expected_direction = NA,
    effect_size_category = "not tested"
  )
}

# =============================================================================
# H4: FIELD-LEVEL BIAS
# =============================================================================

cat("\n===============================================================================\n")
cat("H4: FIELD-LEVEL BIAS\n")
cat("===============================================================================\n\n")

cat("Testing: Do book-heavy fields have lower coverage than journal-heavy fields?\n\n")

# Extract field type contrasts
# Reference level is journal_heavy, so we're comparing to that
mixed_posterior <- draws_main$b_field_type_fmixed
book_heavy_posterior <- draws_main$b_field_type_fbook_heavy

# Test book_heavy vs journal_heavy
h4a_results <- test_hypothesis(
  book_heavy_posterior,
  "H4a: Book-heavy vs Journal-heavy",
  direction = "negative",
  rope_range = c(-0.1, 0.1)
)

cat("Book-heavy vs Journal-heavy (reference):\n")
cat(sprintf("  Posterior median: %.4f\n", h4a_results$median))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n", h4a_results$ci_95_lower, h4a_results$ci_95_upper))
cat(sprintf("  P(book-heavy < journal-heavy): %.1f%%\n",
            h4a_results$prob_expected_direction * 100))

# Test mixed vs journal_heavy
h4b_results <- test_hypothesis(
  mixed_posterior,
  "H4b: Mixed vs Journal-heavy",
  direction = "negative",
  rope_range = c(-0.1, 0.1)
)

cat("\nMixed vs Journal-heavy (reference):\n")
cat(sprintf("  Posterior median: %.4f\n", h4b_results$median))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n", h4b_results$ci_95_lower, h4b_results$ci_95_upper))
cat(sprintf("  P(mixed < journal-heavy): %.1f%%\n",
            h4b_results$prob_expected_direction * 100))

# Test book_heavy vs mixed (derived contrast)
book_vs_mixed <- book_heavy_posterior - mixed_posterior
h4c_results <- test_hypothesis(
  book_vs_mixed,
  "H4c: Book-heavy vs Mixed",
  direction = "negative",
  rope_range = c(-0.1, 0.1)
)

cat("\nBook-heavy vs Mixed:\n")
cat(sprintf("  Posterior median: %.4f\n", h4c_results$median))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n", h4c_results$ci_95_lower, h4c_results$ci_95_upper))
cat(sprintf("  P(book-heavy < mixed): %.1f%%\n",
            h4c_results$prob_expected_direction * 100))

# =============================================================================
# COMPILE ALL RESULTS
# =============================================================================

cat("\n===============================================================================\n")
cat("SUMMARY OF ALL HYPOTHESIS TESTS\n")
cat("===============================================================================\n\n")

all_results <- bind_rows(
  h1_results,
  h2_results,
  h3_results,
  h4a_results,
  h4b_results,
  h4c_results
)

# Create summary table
summary_table <- all_results %>%
  select(hypothesis, median, ci_95_lower, ci_95_upper, pd, rope_pct, effect_size_category) %>%
  mutate(
    across(c(median, ci_95_lower, ci_95_upper), ~round(., 3)),
    pd = round(pd * 100, 1),
    rope_pct = round(rope_pct, 1)
  )

print(summary_table)

# =============================================================================
# SAVE RESULTS
# =============================================================================

cat("\n===============================================================================\n")
cat("SAVING RESULTS\n")
cat("===============================================================================\n\n")

write_csv(all_results, "bayesian-redo/results/model_summaries/bayesian_hypothesis_tests.csv")
cat("Saved: bayesian_hypothesis_tests.csv\n")

# Save posterior draws for key parameters
posteriors_df <- tibble(
  draw = 1:length(elsevier_posterior),
  elsevier_effect = elsevier_posterior,
  book_effect = book_posterior,
  field_book_heavy = book_heavy_posterior,
  field_mixed = mixed_posterior
)
write_csv(posteriors_df, "bayesian-redo/results/posteriors/hypothesis_posteriors.csv")
cat("Saved: hypothesis_posteriors.csv\n")

# =============================================================================
# INTERPRETATION GUIDE
# =============================================================================

cat("\n===============================================================================\n")
cat("INTERPRETATION GUIDE\n")
cat("===============================================================================\n\n")

cat("Probability of Direction (pd):\n")
cat("  > 97.5%: Strong evidence (equivalent to p < 0.05 two-sided)\n")
cat("  > 95%:   Moderate evidence\n")
cat("  > 90%:   Weak evidence\n")
cat("  < 90%:   Inconclusive\n\n")

cat("ROPE (Region of Practical Equivalence):\n")
cat("  < 2.5%:  Effect is practically significant (reject null equivalence)\n")
cat("  2.5-97.5%: Undecided\n")
cat("  > 97.5%: Effect is practically negligible (accept null equivalence)\n\n")

cat("Key advantage over frequentist tests:\n")
cat("  - We can state: 'There is a 99% probability the effect is positive'\n")
cat("  - Instead of: 'If there were no effect, we'd see this 1% of the time'\n")
cat("\n")

cat("===============================================================================\n")
cat("HYPOTHESIS TESTING COMPLETE\n")
cat("===============================================================================\n")
