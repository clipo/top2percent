#!/usr/bin/env Rscript
#' Model Comparison using LOO-CV
#'
#' Compares all fitted models using Leave-One-Out Cross-Validation (LOO-CV)
#' to determine the best-fitting model for the data.
#'
#' LOO-CV provides:
#'   - ELPD (Expected Log Predictive Density): Higher is better
#'   - Pareto k diagnostics: Identifies influential observations
#'   - Model weights: Relative evidence for each model
#'
#' Also performs posterior predictive checks to verify model assumptions.
#'
#' Outputs:
#' - results/diagnostics/loo_comparison.csv
#' - results/diagnostics/pareto_k_diagnostics.csv
#' - figures/Figure_B3_pp_checks.pdf
#'
#' Usage:
#'   Rscript bayesian-redo/R/05_model_comparison.R

# =============================================================================
# SETUP
# =============================================================================

library(brms)
library(loo)
library(tidyverse)
library(bayesplot)

cat("===============================================================================\n")
cat("MODEL COMPARISON (LOO-CV)\n")
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

# Load all models
cat("Loading models...\n")
model_files <- list(
  "Main (default)" = "bayesian-redo/models/main_beta_default.rds",
  "Main (skeptical)" = "bayesian-redo/models/main_beta_skeptical.rds",
  "Main (diffuse)" = "bayesian-redo/models/main_beta_diffuse.rds",
  "Hierarchical (field)" = "bayesian-redo/models/hierarchical_field_intercept.rds",
  "Hierarchical (field+slope)" = "bayesian-redo/models/hierarchical_field_slope.rds"
)

models <- list()
for (name in names(model_files)) {
  if (file.exists(model_files[[name]])) {
    models[[name]] <- readRDS(model_files[[name]])
    cat(sprintf("  Loaded: %s\n", name))
  } else {
    cat(sprintf("  Missing: %s\n", name))
  }
}

cat(sprintf("\nLoaded %d models\n\n", length(models)))

# =============================================================================
# COMPUTE LOO-CV FOR EACH MODEL
# =============================================================================

cat("===============================================================================\n")
cat("COMPUTING LOO-CV\n")
cat("===============================================================================\n\n")

cat("This may take a few minutes...\n\n")

loo_results <- list()
for (name in names(models)) {
  cat(sprintf("Computing LOO for: %s\n", name))
  loo_results[[name]] <- loo(models[[name]], cores = parallel::detectCores())
}

# =============================================================================
# COMPARE MODELS
# =============================================================================

cat("\n===============================================================================\n")
cat("MODEL COMPARISON RESULTS\n")
cat("===============================================================================\n\n")

# Create comparison table
comparison <- loo_compare(loo_results)
print(comparison)

# Extract key statistics
comparison_df <- as_tibble(comparison, rownames = "model") %>%
  mutate(
    rank = row_number(),
    elpd_diff = elpd_diff,
    se_diff = se_diff,
    significant = abs(elpd_diff) > 2 * se_diff  # Rough significance criterion
  )

cat("\n\nInterpretation:\n")
cat("  - elpd_diff: Difference in expected log predictive density (higher = better)\n")
cat("  - SE: Standard error of the difference\n")
cat("  - Models are ranked from best (top) to worst (bottom)\n")
cat("  - Difference > 2*SE suggests meaningful improvement\n\n")

# Best model
best_model <- comparison_df$model[1]
cat(sprintf("Best model: %s\n", best_model))

# =============================================================================
# PARETO K DIAGNOSTICS
# =============================================================================

cat("\n===============================================================================\n")
cat("PARETO K DIAGNOSTICS\n")
cat("===============================================================================\n\n")

cat("Pareto k values indicate reliability of LOO estimates:\n")
cat("  k < 0.5: Good (reliable)\n")
cat("  0.5 < k < 0.7: OK (some uncertainty)\n")
cat("  k > 0.7: Bad (influential observation, results unreliable)\n\n")

# Check best model's Pareto k values
best_loo <- loo_results[[best_model]]
k_values <- best_loo$diagnostics$pareto_k

k_summary <- tibble(
  category = c("Good (k < 0.5)", "OK (0.5 < k < 0.7)", "Bad (k > 0.7)"),
  count = c(
    sum(k_values < 0.5),
    sum(k_values >= 0.5 & k_values < 0.7),
    sum(k_values >= 0.7)
  ),
  percentage = count / length(k_values) * 100
)

print(k_summary)

if (sum(k_values >= 0.7) > 0) {
  cat(sprintf("\nWARNING: %d observations have k > 0.7\n", sum(k_values >= 0.7)))
  cat("These are influential observations that may affect results.\n")
  cat("Consider robust alternatives or investigate these cases.\n")
} else {
  cat("\nAll Pareto k values are acceptable. LOO estimates are reliable.\n")
}

# =============================================================================
# POSTERIOR PREDICTIVE CHECKS
# =============================================================================

cat("\n===============================================================================\n")
cat("POSTERIOR PREDICTIVE CHECKS\n")
cat("===============================================================================\n\n")

cat("Generating posterior predictive check plots...\n")

# Load data for grouping
df <- readRDS("bayesian-redo/results/data_prepared.rds")

# Set up PDF output
pdf("bayesian-redo/figures/Figure_B3_pp_checks.pdf", width = 12, height = 10)

# Plot 1: Density overlay
p1 <- pp_check(models[[best_model]], type = "dens_overlay", ndraws = 100) +
  labs(title = "A. Posterior Predictive: Density Overlay",
       subtitle = "Dark line = observed, light lines = predicted from posterior") +
  theme_minimal(base_size = 12)
print(p1)

# Plot 2: Distribution of statistics
p2 <- pp_check(models[[best_model]], type = "stat", stat = "mean") +
  labs(title = "B. Posterior Predictive: Mean",
       subtitle = "Vertical line = observed mean, histogram = predicted means") +
  theme_minimal(base_size = 12)
print(p2)

# Plot 3: Grouped by field type
if ("field_type_f" %in% names(df)) {
  p3 <- pp_check(models[[best_model]], type = "intervals_grouped",
                 group = "field_type_f", prob = 0.5, prob_outer = 0.95) +
    labs(title = "C. Posterior Predictive: By Field Type",
         subtitle = "Points = observed, intervals = predicted 50% and 95% CI") +
    theme_minimal(base_size = 12)
  print(p3)
}

# Plot 4: Residuals vs fitted
p4 <- pp_check(models[[best_model]], type = "error_scatter_avg") +
  labs(title = "D. Residuals vs Fitted",
       subtitle = "Should show no systematic pattern") +
  theme_minimal(base_size = 12)
print(p4)

dev.off()

cat("Saved: bayesian-redo/figures/Figure_B3_pp_checks.pdf\n")

# =============================================================================
# MODEL WEIGHTS
# =============================================================================

cat("\n===============================================================================\n")
cat("MODEL WEIGHTS (STACKING)\n")
cat("===============================================================================\n\n")

# Compute stacking weights
stacking_weights <- loo_model_weights(loo_results, method = "stacking")
cat("Stacking weights (optimal combination of models):\n")
for (i in seq_along(stacking_weights)) {
  cat(sprintf("  %s: %.3f\n", names(stacking_weights)[i], stacking_weights[i]))
}

# Pseudo-BMA weights
pbma_weights <- loo_model_weights(loo_results, method = "pseudobma")
cat("\nPseudo-BMA weights (Bayesian model averaging):\n")
for (i in seq_along(pbma_weights)) {
  cat(sprintf("  %s: %.3f\n", names(pbma_weights)[i], pbma_weights[i]))
}

# =============================================================================
# SAVE RESULTS
# =============================================================================

cat("\n===============================================================================\n")
cat("SAVING RESULTS\n")
cat("===============================================================================\n\n")

# Save comparison table
write_csv(comparison_df, "bayesian-redo/results/diagnostics/loo_comparison.csv")
cat("Saved: loo_comparison.csv\n")

# Save Pareto k summary
write_csv(k_summary, "bayesian-redo/results/diagnostics/pareto_k_summary.csv")
cat("Saved: pareto_k_summary.csv\n")

# Save model weights
weights_df <- tibble(
  model = names(stacking_weights),
  stacking_weight = as.numeric(stacking_weights),
  pbma_weight = as.numeric(pbma_weights)
)
write_csv(weights_df, "bayesian-redo/results/diagnostics/model_weights.csv")
cat("Saved: model_weights.csv\n")

# =============================================================================
# SUMMARY
# =============================================================================

cat("\n===============================================================================\n")
cat("MODEL COMPARISON SUMMARY\n")
cat("===============================================================================\n\n")

cat(sprintf("Best model by LOO-CV: %s\n", best_model))
cat(sprintf("Best model by stacking: %s\n",
            names(stacking_weights)[which.max(stacking_weights)]))
cat(sprintf("ELPD of best model: %.1f (SE: %.1f)\n",
            loo_results[[best_model]]$estimates["elpd_loo", "Estimate"],
            loo_results[[best_model]]$estimates["elpd_loo", "SE"]))

cat("\nRecommendation:\n")
if (best_model == names(stacking_weights)[which.max(stacking_weights)]) {
  cat(sprintf("  Use '%s' for inference.\n", best_model))
} else {
  cat("  LOO and stacking disagree. Consider model averaging.\n")
}

cat("\n===============================================================================\n")
cat("MODEL COMPARISON COMPLETE\n")
cat("===============================================================================\n")
