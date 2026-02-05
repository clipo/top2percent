#!/usr/bin/env Rscript
#' Generate Manuscript-Ready Tables
#'
#' Creates publication-ready CSV tables formatted for easy pasting into
#' Word/Google Docs manuscripts.
#'
#' Outputs:
#' - results/manuscript_tables/Table_B1_Main_Results.csv
#' - results/manuscript_tables/Table_B2_Frequentist_Comparison.csv
#' - results/manuscript_tables/Table_B3_Field_Effects.csv
#' - results/manuscript_tables/Table_B4_Prior_Sensitivity.csv
#' - results/manuscript_tables/Table_B5_Replicate_Robustness.csv (if available)
#'
#' Usage:
#'   Rscript bayesian-redo/R/09_manuscript_tables.R

# =============================================================================
# SETUP
# =============================================================================

library(tidyverse)

cat("===============================================================================\n")
cat("GENERATING MANUSCRIPT TABLES\n")
cat("===============================================================================\n\n")

# Get project root
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

results_dir <- "bayesian-redo/results/model_summaries"
output_dir <- "bayesian-redo/results/manuscript_tables"

# =============================================================================
# TABLE B1: MAIN BAYESIAN RESULTS (Hypothesis Tests)
# =============================================================================

cat("Creating Table B1: Main Bayesian Hypothesis Tests...\n")

hyp_tests <- read_csv(file.path(results_dir, "bayesian_hypothesis_tests.csv"),
                      show_col_types = FALSE)

table_b1 <- hyp_tests %>%
  select(hypothesis, median, ci_95_lower, ci_95_upper, pd, rope_pct) %>%
  mutate(
    # Format estimate with CI
    `Estimate [95% CrI]` = sprintf("%.3f [%.3f, %.3f]",
                                   median, ci_95_lower, ci_95_upper),
    # Format pd as percentage
    `P(Direction)` = sprintf("%.1f%%", pd * 100),
    # Format ROPE
    `% in ROPE` = sprintf("%.1f%%", rope_pct),
    # Interpretation
    Evidence = case_when(
      pd > 0.995 & rope_pct < 10 ~ "Strong",
      pd > 0.975 & rope_pct < 25 ~ "Moderate",
      pd > 0.95 ~ "Weak",
      TRUE ~ "Inconclusive"
    )
  ) %>%
  select(
    Hypothesis = hypothesis,
    `Estimate [95% CrI]`,
    `P(Direction)`,
    `% in ROPE`,
    Evidence
  )

write_csv(table_b1, file.path(output_dir, "Table_B1_Main_Results.csv"))
cat("  Saved: Table_B1_Main_Results.csv\n")

# =============================================================================
# TABLE B2: FREQUENTIST VS BAYESIAN COMPARISON
# =============================================================================

cat("Creating Table B2: Frequentist vs Bayesian Comparison...\n")

freq_comp <- read_csv(file.path(results_dir, "frequentist_vs_bayesian.csv"),
                      show_col_types = FALSE)

table_b2 <- freq_comp %>%
  mutate(
    # Format frequentist
    `Frequentist Est. [95% CI]` = sprintf("%.3f [%.3f, %.3f]",
                                          freq_estimate, freq_ci_lower, freq_ci_upper),
    # Format Bayesian
    `Bayesian Est. [95% CrI]` = sprintf("%.3f [%.3f, %.3f]",
                                        bayes_median, bayes_ci_lower, bayes_ci_upper),
    # Format p-value
    `p-value` = case_when(
      as.numeric(freq_p) < 0.001 ~ "<0.001",
      TRUE ~ sprintf("%.3f", as.numeric(freq_p))
    ),
    # Difference
    `% Diff` = sprintf("%.1f%%", abs(diff_pct))
  ) %>%
  select(
    Parameter = param_label,
    `Frequentist Est. [95% CI]`,
    `p-value`,
    `Bayesian Est. [95% CrI]`,
    `% Diff`
  )

write_csv(table_b2, file.path(output_dir, "Table_B2_Frequentist_Comparison.csv"))
cat("  Saved: Table_B2_Frequentist_Comparison.csv\n")

# =============================================================================
# TABLE B3: FIELD RANDOM EFFECTS
# =============================================================================

cat("Creating Table B3: Field-Level Effects...\n")

field_int <- read_csv(file.path(results_dir, "field_random_intercepts.csv"),
                      show_col_types = FALSE)

table_b3 <- field_int %>%
  arrange(desc(abs(Estimate))) %>%
  head(15) %>%
  mutate(
    `Effect [95% CrI]` = sprintf("%.3f [%.3f, %.3f]", Estimate, Q2.5, Q97.5),
    Direction = ifelse(Estimate > 0, "Higher coverage", "Lower coverage")
  ) %>%
  select(
    Field = field,
    `Effect [95% CrI]`,
    Direction
  )

write_csv(table_b3, file.path(output_dir, "Table_B3_Field_Effects.csv"))
cat("  Saved: Table_B3_Field_Effects.csv\n")

# =============================================================================
# TABLE B4: PRIOR SENSITIVITY
# =============================================================================

cat("Creating Table B4: Prior Sensitivity Analysis...\n")

prior_sens <- read_csv(file.path(results_dir, "prior_sensitivity_comparison.csv"),
                       show_col_types = FALSE)

# Reshape to wide format for comparison
table_b4 <- prior_sens %>%
  filter(parameter != "phi") %>%
  select(parameter, prior, median, ci_lower, ci_upper) %>%
  mutate(
    estimate = sprintf("%.3f [%.3f, %.3f]", median, ci_lower, ci_upper)
  ) %>%
  select(parameter, prior, estimate) %>%
  pivot_wider(names_from = prior, values_from = estimate) %>%
  rename(
    Parameter = parameter,
    `Skeptical Prior` = skeptical,
    `Default Prior` = default,
    `Diffuse Prior` = diffuse
  )

write_csv(table_b4, file.path(output_dir, "Table_B4_Prior_Sensitivity.csv"))
cat("  Saved: Table_B4_Prior_Sensitivity.csv\n")

# Generate Figure S12: Prior Sensitivity Visualization
library(ggplot2)

cat("Creating Figure S12: Prior Sensitivity Visualization...\n")

fig_s12_data <- prior_sens %>%
  filter(parameter != "phi", parameter != "Intercept") %>%
  mutate(
    param_label = case_when(
      parameter == "elsevier_pct_z" ~ "Elsevier %",
      parameter == "books_pct_z" ~ "Books %",
      parameter == "field_type_fmixed" ~ "Mixed vs Journal",
      parameter == "field_type_fbook_heavy" ~ "Book-heavy vs Journal",
      parameter == "log_works_z" ~ "Log Works",
      TRUE ~ parameter
    ),
    prior = factor(prior, levels = c("skeptical", "default", "diffuse"))
  )

fig_s12 <- fig_s12_data %>%
  ggplot(aes(y = param_label, x = median, color = prior)) +
  geom_pointrange(
    aes(xmin = ci_lower, xmax = ci_upper),
    position = position_dodge(width = 0.5),
    size = 0.7
  ) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  scale_color_manual(
    values = c("skeptical" = "#E69F00", "default" = "#0072B2", "diffuse" = "#009E73"),
    labels = c("Skeptical\nN(0, 0.5)", "Default\nN(0, 1)", "Diffuse\nN(0, 2.5)")
  ) +
  labs(
    title = "Prior Sensitivity Analysis",
    subtitle = "Effect estimates are robust across prior specifications",
    x = "Effect Size (logit scale)",
    y = NULL,
    color = "Prior"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold"),
    legend.position = "bottom",
    legend.title = element_text(face = "bold")
  )

ggsave("bayesian-redo/figures/Figure_S12_prior_sensitivity.pdf",
       fig_s12, width = 10, height = 6)
ggsave("bayesian-redo/figures/Figure_S12_prior_sensitivity.png",
       fig_s12, width = 10, height = 6, dpi = 300)
# Also save to supplementary figures directory
ggsave("figures/supplementary/FigureS12_Prior_Sensitivity.pdf",
       fig_s12, width = 10, height = 6)
ggsave("figures/supplementary/FigureS12_Prior_Sensitivity.png",
       fig_s12, width = 10, height = 6, dpi = 300)
cat("  Saved: Figure_S12_prior_sensitivity.pdf/png (also as FigureS12)\n")

# =============================================================================
# TABLE B5: REPLICATE ROBUSTNESS (if available)
# =============================================================================

cat("Creating Table B5: Replicate Robustness...\n")

replicate_file <- file.path(results_dir, "replicate_bayesian_results.csv")

if (file.exists(replicate_file)) {
  replicate_results <- read_csv(replicate_file, show_col_types = FALSE)

  table_b5 <- replicate_results %>%
    mutate(
      Sample = gsub("replicate_", "Sample ", replicate),
      `Elsevier Effect [95% CrI]` = sprintf("%.3f [%.3f, %.3f]",
                                            elsevier_median, elsevier_ci_lower, elsevier_ci_upper),
      `P(Elsevier > 0)` = sprintf("%.1f%%", elsevier_pd * 100),
      `Book Effect [95% CrI]` = sprintf("%.3f [%.3f, %.3f]",
                                        books_median, books_ci_lower, books_ci_upper),
      `P(Books < 0)` = sprintf("%.1f%%", books_pd * 100),
      Converged = ifelse(max_rhat < 1.01, "Yes", "No")
    ) %>%
    select(
      Sample,
      n = n_obs,
      `Elsevier Effect [95% CrI]`,
      `P(Elsevier > 0)`,
      `Book Effect [95% CrI]`,
      `P(Books < 0)`,
      Converged
    )

  write_csv(table_b5, file.path(output_dir, "Table_B5_Replicate_Robustness.csv"))
  cat("  Saved: Table_B5_Replicate_Robustness.csv\n")
} else {
  cat("  Replicate results not yet available (run 08_run_all_replicates.R first)\n")
}

# =============================================================================
# SUMMARY
# =============================================================================

cat("\n===============================================================================\n")
cat("MANUSCRIPT TABLES COMPLETE\n")
cat("===============================================================================\n\n")

cat("Generated tables:\n")
cat("  - Table_B1_Main_Results.csv: Bayesian hypothesis tests\n")
cat("  - Table_B2_Frequentist_Comparison.csv: Method comparison\n")
cat("  - Table_B3_Field_Effects.csv: Hierarchical field effects\n")
cat("  - Table_B4_Prior_Sensitivity.csv: Prior robustness\n")
if (file.exists(replicate_file)) {
  cat("  - Table_B5_Replicate_Robustness.csv: Replicate analysis\n")
}

cat("\nGenerated figures:\n")
cat("  - FigureS12_Prior_Sensitivity.png/.pdf: Prior sensitivity visualization\n")

cat("\nAll tables are formatted for direct pasting into Word/Google Docs.\n")
cat("===============================================================================\n")
