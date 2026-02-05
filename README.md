# Complete Reproducibility Package

## Publisher Bias in Widely-Used Scientist Rankings

**Authors**: Carl P. Lipo, Robert J. DiNapoli, Benjamin Andrus
**Affiliation**: Binghamton University
**Contact**: clipo@binghamton.edu

This package contains everything needed to reproduce the analysis documenting systematic publisher, book, and field bias in the "top 2% of scientists" rankings (Ioannidis et al., 2024).

---

## Quick Start

### One-Command Reproduction

```bash
chmod +x REPRODUCE_ALL.sh
./REPRODUCE_ALL.sh
```

This will:
1. Check system requirements (Python 3.12+, R 4.3+)
2. Install all dependencies
3. Run all analyses (frequentist + optionally Bayesian)
4. Generate all figures (6 main + 7 supplementary + Bayesian diagnostics)

**Estimated time**: ~5-10 minutes (without Bayesian); ~1-2 hours (with full Bayesian)

---

## Key Findings

### Bayesian Analysis Results

| Hypothesis | Effect (β) | 95% CrI | P(Direction) | % in ROPE | Evidence |
|------------|-----------|---------|--------------|-----------|----------|
| H1: Elsevier Effect | +0.156 | [0.081, 0.231] | 100.0% | 7.3% | **Strong** |
| H2: Book Effect | -0.081 | [-0.164, -0.000] | 97.5% | 67.5% | Weak |
| H3: OA Effect | +0.011 | [-0.053, 0.074] | 63.6% | 99.7% | Inconclusive |
| H4a: Book-heavy vs Journal-heavy | -0.967 | [-1.173, -0.763] | 100.0% | 0.0% | **Strong** |
| H4b: Mixed vs Journal-heavy | -0.754 | [-0.934, -0.573] | 100.0% | 0.0% | **Strong** |
| H4c: Book-heavy vs Mixed | -0.214 | [-0.370, -0.060] | 99.6% | 7.6% | **Strong** |

### Coverage Statistics

| Field Type | n | Median Coverage | IQR | Missing >50% |
|------------|---|-----------------|-----|--------------|
| Book-heavy | 186 | 32.6% | 22.8%-44.9% | 76% |
| Mixed | 204 | 40.5% | 28.2%-55.6% | 68% |
| Journal-heavy | 174 | 76.2% | 59.4%-90.1% | 14% |
| **Overall** | **564** | **45.3%** | **29.6%-69.0%** | **55%** |

### Ranking Instability

- **Correlation**: Spearman ρ = 0.567 (Scopus vs OpenAlex rankings using same formula)
- **Median shift**: 143,277 positions when using complete data
- **Maximum shift**: 1.2 million positions (Ernst Gombrich, art history)
- **Implication**: Same formula, different data → dramatically different rankings

---

## Directory Structure

```
complete_reproducibility_package/
├── README.md                      # This file
├── REPRODUCE_ALL.sh               # Master reproduction script
├── requirements.txt               # Python dependencies
├── r_requirements.txt             # R dependencies (including Bayesian)
├── install_r_dependencies.R       # R package installer
│
├── manuscript/                    # Manuscript files
│   ├── MANUSCRIPT_NATURE_COMMUNICATIONS.md    # Source (Markdown)
│   └── MANUSCRIPT_NATURE_COMMUNICATIONS.docx  # Output (Word)
│
├── data/                          # All data files
│   ├── comprehensive_sample.csv              # 600 researchers sample
│   ├── openalex_comprehensive_data.csv       # 564 with valid coverage
│   ├── openalex_data_with_orcid.csv          # ORCID-verified subset (362)
│   ├── openalex_rankings_full.csv            # Ranking replication (541)
│   ├── scopus_vs_openalex_rankings.csv       # Ranking comparison
│   ├── award_winners_case_studies.csv        # Nobel/Pulitzer cases
│   ├── citation_quality_*.csv                # Journal impact controls
│   ├── university_adoption/                  # Institutional adoption data
│   └── robustness_analysis/                  # 5-replicate robustness data
│
├── scripts/                       # Analysis scripts
│   ├── python/                    # Python scripts (18 files)
│   │   ├── figure_4_university_adoption.py
│   │   ├── create_manuscript_visualizations.py
│   │   ├── figureS1-S6*.py        # Supplementary figure scripts
│   │   ├── citation_quality_analysis.py
│   │   ├── comprehensive_statistical_analysis.py
│   │   └── ...
│   └── R/                         # R scripts
│       ├── figures_1_2_3_coverage_analysis.R
│       └── bayesian/              # Bayesian analysis (10 scripts)
│           ├── run_all.R          # Master Bayesian script
│           ├── 01_data_preparation.R
│           ├── 02_main_regression_model.R
│           ├── 03_hierarchical_field_model.R
│           ├── 04_hypothesis_tests.R
│           ├── 05_model_comparison.R
│           ├── 06_posterior_visualization.R
│           ├── 07_frequentist_comparison.R
│           ├── 08_run_all_replicates.R
│           └── 09_manuscript_tables.R
│
├── figures/                       # All figures
│   ├── main/                      # Main manuscript figures (1-5)
│   │   ├── Figure1_University_Adoption.png/.pdf
│   │   ├── Figure2_Coverage_by_Field.png/.pdf
│   │   ├── Figure3_Elsevier_vs_Coverage.png/.pdf
│   │   ├── Figure4_Books_vs_Coverage.png/.pdf
│   │   └── Figure5_Scopus_vs_OpenAlex_Rankings.png/.pdf
│   ├── supplementary/             # Supplementary figures (S1-S7)
│   │   ├── FigureS1_Sample_Characteristics.png/.pdf
│   │   ├── FigureS2_Coverage_Distribution.png
│   │   ├── FigureS3_Publisher_Breakdown.png
│   │   ├── FigureS4_OA_Analysis.png
│   │   ├── FigureS5_Regression_Diagnostics.png
│   │   ├── FigureS6_Extreme_Cases.png
│   │   └── FigureS7_Ranking_Changes_Distribution.png/.pdf
│   └── bayesian/                  # Bayesian analysis figures
│       ├── key_hypotheses.png/.pdf           # Figure 6 in manuscript
│       ├── Figure_B1_posterior_distributions.png/.pdf
│       ├── Figure_B2_hierarchical_effects.png/.pdf
│       ├── Figure_B3_pp_checks.pdf
│       ├── Figure_B4_bayesian_vs_frequentist.png/.pdf
│       ├── trace_plots.pdf                   # MCMC diagnostics
│       ├── rhat_diagnostic.png/.pdf          # Convergence
│       ├── ess_diagnostic.png/.pdf           # Effective sample size
│       └── replicate_posteriors.png/.pdf     # Robustness
│
├── results/                       # Analysis results
│   └── bayesian/
│       ├── manuscript_tables/     # Tables B1-B5 (CSV)
│       │   ├── Table_B1_Main_Results.csv
│       │   ├── Table_B2_Frequentist_Comparison.csv
│       │   ├── Table_B3_Field_Effects.csv
│       │   ├── Table_B4_Prior_Sensitivity.csv
│       │   └── Table_B5_Replicate_Robustness.csv
│       └── model_summaries/       # Detailed model output
│
├── tables/                        # Generated tables (CSV)
│   ├── Table1_Summary.csv
│   ├── table_summary_statistics.csv
│   └── extreme_ranking_improvements.csv
│
└── docs/                          # Documentation
    └── SCRIPT_INDEX.md            # Detailed script documentation
```

---

## System Requirements

### Required Software

| Software | Minimum Version | Purpose |
|----------|----------------|---------|
| Python | 3.12+ | Main analysis, figures |
| R | 4.3+ | Statistical analysis, Bayesian models |

### Python Packages

```bash
pip install -r requirements.txt
```

**Contents of requirements.txt**:
```
pandas>=2.0
numpy>=1.24
scipy>=1.11
statsmodels>=0.14
matplotlib>=3.7
seaborn>=0.12
requests>=2.31
```

### R Packages (Base Analysis)

```bash
Rscript install_r_dependencies.R
```

**Key packages**: ggplot2, dplyr, tidyr, readr, scales, ggrepel

### R Packages (Bayesian Analysis)

```R
install.packages(c("brms", "rstan", "loo", "bayestestR",
                   "tidybayes", "posterior", "bayesplot", "ggdist"))
```

**Notes**:
- brms/Stan requires a C++ compiler
- On macOS: Install Xcode Command Line Tools (`xcode-select --install`)
- On Windows: Install Rtools
- Full Bayesian analysis takes ~1-2 hours (MCMC sampling)

---

## Running the Analysis

### Option 1: Full Automated Reproduction

```bash
./REPRODUCE_ALL.sh
```

### Option 2: Step-by-Step

#### Step 1: Verify Setup

```bash
python -c "import pandas; import scipy; import matplotlib; print('Python OK')"
Rscript -e "library(ggplot2); library(dplyr); print('R OK')"
```

#### Step 2: Generate Main Figures (R)

```bash
cd scripts/R
Rscript figures_1_2_3_coverage_analysis.R
```

Generates: Figures 2, 3, 4 (coverage by field, Elsevier effect, book effect)

#### Step 3: Generate Main Figures (Python)

```bash
cd scripts/python
python figure_4_university_adoption.py          # Figure 1
python create_manuscript_visualizations.py      # Figure 5
```

#### Step 4: Generate Supplementary Figures

```bash
cd scripts/python
python figureS1_sample_characteristics.py
python figureS2_coverage_distribution.py
python figureS3_publisher_breakdown.py
python figureS4_regression_diagnostics.py
python figureS5_oa_analysis.py
python figureS6_extreme_cases.py
```

#### Step 5: Bayesian Analysis (Optional, ~1-2 hours)

```bash
cd scripts/R/bayesian
Rscript run_all.R           # Full analysis (recommended)
# OR
Rscript run_all.R --quick   # Quick mode (~20 min, fewer iterations)
```

Generates:
- Figure 6 (key_hypotheses.png) - Bayesian hypothesis tests
- Supplementary Figures S8-S13 (MCMC diagnostics, sensitivity)
- Tables B1-B5 (manuscript_tables/)

---

## Main Figures

| Figure | Description | Script |
|--------|-------------|--------|
| **Figure 1** | University adoption of rankings (2022-2024) | `figure_4_university_adoption.py` |
| **Figure 2** | Scopus coverage by field type (box plots) | `figures_1_2_3_coverage_analysis.R` |
| **Figure 3** | Elsevier % vs coverage (scatterplot) | `figures_1_2_3_coverage_analysis.R` |
| **Figure 4** | Book % vs coverage (scatterplot) | `figures_1_2_3_coverage_analysis.R` |
| **Figure 5** | Scopus vs OpenAlex ranking comparison | `create_manuscript_visualizations.py` |
| **Figure 6** | Bayesian hypothesis tests (posteriors) | `06_posterior_visualization.R` |

---

## Supplementary Figures

| Figure | Description |
|--------|-------------|
| **S1** | Sample characteristics (field distribution, geography) |
| **S2** | Coverage distribution histograms |
| **S3** | Publisher breakdown by field type |
| **S4** | Open access publisher analysis |
| **S5** | Regression diagnostics |
| **S6** | Extreme undercounting cases |
| **S7** | Ranking changes distribution |
| **S8** | Elsevier effect posterior (detailed) |
| **S9** | Field type effect posteriors |
| **S10** | MCMC diagnostics (trace plots, R-hat) |
| **S11** | Bayesian vs frequentist comparison |
| **S12** | Prior sensitivity analysis |
| **S13** | Robustness across 5 independent replicates |

---

## Data Files

### Primary Data

| File | Description | n |
|------|-------------|---|
| `comprehensive_sample.csv` | Stratified random sample from top 2% dataset | 600 |
| `openalex_comprehensive_data.csv` | Matched to OpenAlex with valid coverage ratios | 564 |
| `openalex_data_with_orcid.csv` | ORCID-verified subset for validation | 362 |
| `scopus_vs_openalex_rankings.csv` | Ranking comparison using same formula | 541 |

### Key Variables

| Variable | Description |
|----------|-------------|
| `coverage_ratio` | Scopus publications / OpenAlex publications |
| `elsevier_pct` | Percentage of works in Elsevier journals |
| `books_pct` | Percentage of works that are books/chapters |
| `field_type` | book_heavy / mixed / journal_heavy |
| `rank` | Global rank in original Scopus-based rankings |

---

## Bayesian Methods

### Model Specification

**Primary model**: Beta regression with logit link
```
coverage_ratio ~ elsevier_pct_z + books_pct_z + oa_pct_z + field_type
```

### MCMC Settings

- **Chains**: 4
- **Warmup**: 2,000 iterations
- **Sampling**: 4,000 iterations per chain
- **Total samples**: 16,000 post-warmup
- **Priors**: Weakly informative Normal(0, 2.5)

### Convergence Diagnostics

- **R-hat**: All parameters < 1.01
- **ESS**: All effective sample sizes > 1,000
- **Trace plots**: Well-mixed chains (see Figure S10)

### Evidence Classification

| Criterion | Classification |
|-----------|----------------|
| > 97% P(Direction) AND < 25% ROPE | **Strong** evidence |
| > 90% P(Direction) OR 25-75% ROPE | Moderate evidence |
| 75-90% P(Direction) | Weak evidence |
| < 75% P(Direction) OR > 75% ROPE | Inconclusive |

### ROPE (Region of Practical Equivalence)

- **Range**: [-0.1, 0.1] on logit scale
- **Interpretation**: Effects within ROPE are practically negligible

---

## Validation

### ORCID Verification

- **362 researchers (60.3%)** have unique ORCID identifiers
- **359 with valid coverage data** used for verification
- **Bias persists** in ORCID-verified subset:
  - Elsevier effect: 26.4 pp (vs 30.6 pp full sample)
  - Book bias: r = -0.503 (vs r = -0.534 full sample)
  - Field-type gap: 32.3 pp (vs 43.6 pp full sample)
- **Conclusion**: Findings not artifacts of name-matching errors

### Robustness Analysis

- **5 independent replicate samples** (n=400 each)
- **Total: 2,000 researchers** matched to OpenAlex
- **All replicates significant** (p < 0.001)
- **Effect size stability**: SD < 0.10 across replicates

---

## Troubleshooting

### Python Issues

```bash
# Missing packages
pip install -r requirements.txt

# Wrong Python version
python3 --version  # Should be 3.12+
```

### R Issues

```bash
# Missing packages
Rscript install_r_dependencies.R

# Bayesian packages
Rscript -e "install.packages('brms')"
```

### Bayesian Analysis Fails

1. **C++ compiler missing**: Install Xcode (macOS) or Rtools (Windows)
2. **Memory issues**: Use `--quick` flag for reduced iterations
3. **Stan errors**: Try `Rscript -e "remove.packages('rstan'); install.packages('rstan')"`

### Expected Variations

Results may vary slightly (±3%) due to:
- OpenAlex data updates (new publications indexed daily)
- MCMC sampling variation
- Random seed differences

---

## Citation

If you use this package, please cite:

```bibtex
@article{lipo2026publisher,
  title={Publisher Bias in Widely-Used Scientist Rankings},
  author={Lipo, Carl P. and DiNapoli, Robert J. and Andrus, Benjamin},
  journal={Nature Communications},
  year={2026},
  note={[DOI pending]}
}
```

And the source data:

```bibtex
@dataset{ioannidis2024updated,
  author={Ioannidis, John P.A. and Boyack, Kevin W. and Baas, Jeroen},
  title={Updated science-wide author databases of standardized citation indicators},
  year={2024},
  publisher={Elsevier Data Repository},
  doi={10.17632/btchxktzyw}
}

@article{priem2022openalex,
  author={Priem, Jason and Piwowar, Heather and Orr, Richard},
  title={OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts},
  journal={arXiv preprint arXiv:2205.01833},
  year={2022}
}
```

---

## License

- **Code**: MIT License
- **Data**: CC-BY 4.0
- **Manuscript**: All rights reserved

---

## Contact

Questions about reproducibility? Contact Carl Lipo (clipo@binghamton.edu)

**GitHub**: https://github.com/clipo/2percent

---

**Package created**: February 2026
**Last updated**: February 4, 2026 (Version 4.1 - Clean Reproducibility Package)
