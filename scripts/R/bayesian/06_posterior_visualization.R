#!/usr/bin/env Rscript
#' Posterior Visualization
#'
#' Creates publication-quality figures for Bayesian analysis results:
#'   - Figure B1: Posterior distributions for main effects
#'   - Figure B2: Hierarchical field effects (caterpillar plot)
#'   - Figure B4: Bayesian vs Frequentist comparison
#'
#' All figures saved in both PDF (vector) and PNG (300 DPI) formats.
#'
#' Usage:
#'   Rscript bayesian-redo/R/06_posterior_visualization.R

# =============================================================================
# SETUP
# =============================================================================

library(brms)
library(tidyverse)
library(tidybayes)
library(bayesplot)
library(ggdist)
library(patchwork)

# Set publication theme
theme_pub <- theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    axis.title = element_text(face = "bold"),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

theme_set(theme_pub)

# Color palette (colorblind-friendly)
colors <- c("#0072B2", "#D55E00", "#009E73", "#CC79A7", "#F0E442")

cat("===============================================================================\n")
cat("POSTERIOR VISUALIZATION\n")
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
cat("Loading models...\n")
fit_main <- readRDS("bayesian-redo/models/main_beta_default.rds")
fit_hier <- readRDS("bayesian-redo/models/hierarchical_field_slope.rds")

# Load data for context
df <- readRDS("bayesian-redo/results/data_prepared.rds")

# =============================================================================
# FIGURE B1: POSTERIOR DISTRIBUTIONS FOR MAIN EFFECTS
# =============================================================================

cat("\nCreating Figure B1: Posterior distributions...\n")

# Extract posterior draws
draws <- fit_main %>%
  spread_draws(b_elsevier_pct_z, b_books_pct_z, b_log_works_z,
               b_field_type_fmixed, b_field_type_fbook_heavy) %>%
  pivot_longer(
    cols = starts_with("b_"),
    names_to = "parameter",
    values_to = "value"
  ) %>%
  mutate(
    parameter = case_when(
      parameter == "b_elsevier_pct_z" ~ "Elsevier %\n(per SD)",
      parameter == "b_books_pct_z" ~ "Books %\n(per SD)",
      parameter == "b_log_works_z" ~ "Log Publications\n(per SD)",
      parameter == "b_field_type_fmixed" ~ "Mixed Field\n(vs Journal-heavy)",
      parameter == "b_field_type_fbook_heavy" ~ "Book-heavy Field\n(vs Journal-heavy)"
    ),
    parameter = factor(parameter, levels = c(
      "Elsevier %\n(per SD)",
      "Books %\n(per SD)",
      "Log Publications\n(per SD)",
      "Mixed Field\n(vs Journal-heavy)",
      "Book-heavy Field\n(vs Journal-heavy)"
    ))
  )

# Create half-eye plot
fig_b1 <- draws %>%
  ggplot(aes(x = value, y = parameter, fill = after_stat(abs(x) < 0.1))) +
  stat_halfeye(
    .width = c(0.66, 0.95),
    point_interval = median_qi,
    slab_color = "gray30",
    slab_size = 0.5
  ) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  geom_vline(xintercept = c(-0.1, 0.1), linetype = "dotted", color = "gray70") +
  scale_fill_manual(
    values = c("TRUE" = "gray70", "FALSE" = colors[1]),
    name = "In ROPE",
    labels = c("TRUE" = "Yes", "FALSE" = "No")
  ) +
  labs(
    title = "Posterior Distributions for Main Effects",
    subtitle = "Beta regression coefficients (logit scale). Dashed line = 0, dotted = ROPE [-0.1, 0.1]",
    x = "Effect Size (logit scale)",
    y = NULL,
    caption = "Thick bar = 66% CI, thin bar = 95% CI, point = median"
  ) +
  theme(legend.position = "none")

# Save to both bayesian-redo/figures (legacy) and figures/supplementary (manuscript)
ggsave("bayesian-redo/figures/Figure_B1_posterior_distributions.pdf",
       fig_b1, width = 10, height = 7)
ggsave("bayesian-redo/figures/Figure_B1_posterior_distributions.png",
       fig_b1, width = 10, height = 7, dpi = 300)
# Also save as Figure S8 for supplementary materials
ggsave("figures/supplementary/FigureS8_Elsevier_Posterior.pdf",
       fig_b1, width = 10, height = 7)
ggsave("figures/supplementary/FigureS8_Elsevier_Posterior.png",
       fig_b1, width = 10, height = 7, dpi = 300)
cat("Saved: Figure_B1_posterior_distributions.pdf/png (also as FigureS8)\n")

# =============================================================================
# FIGURE B2: HIERARCHICAL FIELD EFFECTS
# =============================================================================

cat("\nCreating Figure B2: Hierarchical field effects...\n")

# Use ranef() for more reliable extraction
re <- ranef(fit_hier, summary = TRUE)
field_re <- re$field_f

# Create data frame from ranef output
field_summary <- tibble(
  field = rownames(field_re[,,"Intercept"]),
  median = field_re[,,"Intercept"][,"Estimate"],
  lower = field_re[,,"Intercept"][,"Q2.5"],
  upper = field_re[,,"Intercept"][,"Q97.5"]
) %>%
  mutate(field = gsub("\\.", " ", field)) %>%
  arrange(median)

# Create caterpillar plot
fig_b2 <- field_summary %>%
  mutate(field = factor(field, levels = field)) %>%
  ggplot(aes(x = median, y = field)) +
  geom_pointrange(aes(xmin = lower, xmax = upper), color = colors[1], size = 0.5) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  labs(
    title = "Field-Level Random Effects (Intercepts)",
    subtitle = "Deviation from population average (logit scale). Shrinkage toward zero for small fields.",
    x = "Random Effect (logit scale)",
    y = NULL,
    caption = "Points = posterior median, bars = 95% credible interval"
  )

ggsave("bayesian-redo/figures/Figure_B2_hierarchical_effects.pdf",
       fig_b2, width = 10, height = 10)
ggsave("bayesian-redo/figures/Figure_B2_hierarchical_effects.png",
       fig_b2, width = 10, height = 10, dpi = 300)
# Also save as Figure S9 for supplementary materials
ggsave("figures/supplementary/FigureS9_Field_Type_Posteriors.pdf",
       fig_b2, width = 10, height = 10)
ggsave("figures/supplementary/FigureS9_Field_Type_Posteriors.png",
       fig_b2, width = 10, height = 10, dpi = 300)
cat("Saved: Figure_B2_hierarchical_effects.pdf/png (also as FigureS9)\n")

# =============================================================================
# MCMC DIAGNOSTICS: RHAT AND ESS
# =============================================================================

cat("\nCreating MCMC diagnostic figures...\n")

# Extract Rhat and ESS values
model_summary <- summary(fit_main)$fixed
diag_data <- tibble(
  parameter = rownames(model_summary),
  Rhat = model_summary[, "Rhat"],
  Bulk_ESS = model_summary[, "Bulk_ESS"],
  Tail_ESS = model_summary[, "Tail_ESS"]
) %>%
  filter(parameter != "Intercept") %>%
  mutate(
    parameter = case_when(
      parameter == "elsevier_pct_z" ~ "Elsevier %",
      parameter == "books_pct_z" ~ "Books %",
      parameter == "field_type_fmixed" ~ "Mixed Field",
      parameter == "field_type_fbook_heavy" ~ "Book-heavy Field",
      parameter == "log_works_z" ~ "Log Works",
      TRUE ~ parameter
    )
  )

# Rhat plot
fig_rhat <- diag_data %>%
  ggplot(aes(x = Rhat, y = reorder(parameter, Rhat))) +
  geom_point(size = 3, color = colors[1]) +
  geom_vline(xintercept = 1.00, linetype = "dashed", color = "green4") +
  geom_vline(xintercept = 1.01, linetype = "dotted", color = "orange") +
  labs(
    title = "Convergence Diagnostic: Rhat",
    subtitle = "All values should be < 1.01 (dashed line = 1.00, ideal)",
    x = expression(hat(R)),
    y = NULL
  ) +
  xlim(0.99, 1.02)

ggsave("bayesian-redo/figures/rhat_diagnostic.pdf", fig_rhat, width = 8, height = 5)
ggsave("bayesian-redo/figures/rhat_diagnostic.png", fig_rhat, width = 8, height = 5, dpi = 300)
# Also save as Figure S10 for supplementary materials
ggsave("figures/supplementary/FigureS10_MCMC_Diagnostics.pdf", fig_rhat, width = 8, height = 5)
ggsave("figures/supplementary/FigureS10_MCMC_Diagnostics.png", fig_rhat, width = 8, height = 5, dpi = 300)
cat("Saved: rhat_diagnostic.pdf/png (also as FigureS10)\n")

# ESS plot
fig_ess <- diag_data %>%
  pivot_longer(cols = c(Bulk_ESS, Tail_ESS), names_to = "type", values_to = "ESS") %>%
  mutate(type = gsub("_ESS", "", type)) %>%
  ggplot(aes(x = ESS, y = reorder(parameter, ESS), color = type)) +
  geom_point(size = 3) +
  geom_vline(xintercept = 1000, linetype = "dashed", color = "gray50") +
  scale_color_manual(values = c("Bulk" = colors[1], "Tail" = colors[2])) +
  labs(
    title = "Effective Sample Size (ESS)",
    subtitle = "Higher is better. Dashed line = 1000 (minimum recommended)",
    x = "Effective Sample Size",
    y = NULL,
    color = "Type"
  ) +
  theme(legend.position = "bottom")

ggsave("bayesian-redo/figures/ess_diagnostic.pdf", fig_ess, width = 8, height = 5)
ggsave("bayesian-redo/figures/ess_diagnostic.png", fig_ess, width = 8, height = 5, dpi = 300)
cat("Saved: ess_diagnostic.pdf/png\n")

# =============================================================================
# TRACE PLOTS FOR CONVERGENCE DIAGNOSTICS
# =============================================================================

cat("\nCreating trace plots for convergence diagnostics...\n")

# Extract MCMC chains
mcmc_trace_plot <- mcmc_trace(fit_main, pars = c("b_elsevier_pct_z", "b_books_pct_z",
                                                   "b_field_type_fbook_heavy")) +
  labs(title = "MCMC Trace Plots",
       subtitle = "Chains should be well-mixed (no trends, good overlap)")

ggsave("bayesian-redo/figures/trace_plots.pdf",
       mcmc_trace_plot, width = 10, height = 8)
cat("Saved: trace_plots.pdf\n")

# =============================================================================
# COMBINED FIGURE: KEY HYPOTHESES
# =============================================================================

cat("\nCreating combined hypothesis figure...\n")

# Extract key posteriors
key_draws <- fit_main %>%
  spread_draws(b_elsevier_pct_z, b_books_pct_z, b_field_type_fbook_heavy) %>%
  select(-c(.chain, .iteration, .draw)) %>%
  pivot_longer(everything(), names_to = "hypothesis", values_to = "effect") %>%
  mutate(
    hypothesis = case_when(
      hypothesis == "b_elsevier_pct_z" ~ "H1: Elsevier Effect",
      hypothesis == "b_books_pct_z" ~ "H2: Book Effect",
      hypothesis == "b_field_type_fbook_heavy" ~ "H4: Field Effect\n(Book-heavy vs Journal-heavy)"
    )
  )

# Compute probabilities for annotations
probs <- key_draws %>%
  group_by(hypothesis) %>%
  summarise(
    median = median(effect),
    prob_positive = mean(effect > 0),
    prob_negative = mean(effect < 0),
    ci_lower = quantile(effect, 0.025),
    ci_upper = quantile(effect, 0.975),
    .groups = "drop"
  ) %>%
  mutate(
    label = case_when(
      hypothesis == "H1: Elsevier Effect" ~
        sprintf("P(effect > 0) = %.1f%%", prob_positive * 100),
      hypothesis == "H2: Book Effect" ~
        sprintf("P(effect < 0) = %.1f%%", prob_negative * 100),
      TRUE ~
        sprintf("P(effect < 0) = %.1f%%", prob_negative * 100)
    ),
    x_pos = median + 0.1
  )

fig_hypotheses <- key_draws %>%
  ggplot(aes(x = effect, y = hypothesis, fill = hypothesis)) +
  stat_halfeye(.width = c(0.66, 0.95), point_interval = median_qi) +
  geom_vline(xintercept = 0, linetype = "dashed", size = 0.8) +
  geom_text(data = probs, aes(x = x_pos, y = hypothesis, label = label),
            hjust = 0, vjust = -1, size = 3.5) +
  scale_fill_manual(values = c(colors[1], colors[2], colors[3])) +
  labs(
    title = "Bayesian Hypothesis Tests: Key Effects",
    subtitle = "Posterior distributions with 66% and 95% credible intervals",
    x = "Effect Size (logit scale)",
    y = NULL
  ) +
  theme(legend.position = "none") +
  coord_cartesian(xlim = c(-1.5, 1.5))

ggsave("bayesian-redo/figures/key_hypotheses.pdf",
       fig_hypotheses, width = 10, height = 6)
ggsave("bayesian-redo/figures/key_hypotheses.png",
       fig_hypotheses, width = 10, height = 6, dpi = 300)
cat("Saved: key_hypotheses.pdf/png\n")

# =============================================================================
# SUMMARY
# =============================================================================

cat("\n===============================================================================\n")
cat("VISUALIZATION COMPLETE\n")
cat("===============================================================================\n\n")

cat("Generated figures:\n")
cat("  - Figure_B1_posterior_distributions.pdf/png → FigureS8_Elsevier_Posterior\n")
cat("  - Figure_B2_hierarchical_effects.pdf/png → FigureS9_Field_Type_Posteriors\n")
cat("  - rhat_diagnostic.pdf/png → FigureS10_MCMC_Diagnostics\n")
cat("  - trace_plots.pdf\n")
cat("  - key_hypotheses.pdf/png (Figure 6 in main text)\n")
cat("  - ess_diagnostic.pdf/png\n\n")

cat("All figures saved to: bayesian-redo/figures/ and figures/supplementary/\n")
cat("\n===============================================================================\n")
