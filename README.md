# Complete Reproducibility Package

## Publisher Bias in Widely-Used Scientist Rankings

**Authors**: Carl P. Lipo, Beau DiNapoli, Benjamin Andrus

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
4. Generate all figures (6 main + 13 supplementary + Bayesian diagnostics)

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

- **Correlation**: Spearman ρ = 0.695 (Scopus vs OpenAlex rankings using same formula, n=538)
- **Median shift**: 142,276 positions when using complete data
- **Maximum shift**: 1,210,020 positions (Ernst Gombrich, art history)
- **Implication**: Same formula, different data → dramatically different rankings

### University Adoption

- **123 universities** across **32 countries** (2022-2025) use the rankings in official communications
- No evidence of declining adoption despite scholarly criticism

---

## Directory Structure

```
top2percent/
├── README.md                      # This file
├── LICENSE                        # CC0 1.0 Universal
├── REPRODUCE_ALL.sh               # Master reproduction script
├── ANALYSIS_SUMMARY.txt           # Statistical results summary
├── analysis_results.json          # Machine-readable results
├── requirements.txt               # Python dependencies
├── r_requirements.txt             # R dependencies (including Bayesian)
├── install_r_dependencies.R       # R package installer
│
├── August 2025 data-update.../    # Source Ioannidis dataset (~170MB)
│   ├── Table_1_Authors_career_2024_*.xlsx    # Career-long rankings
│   ├── Table_1_Authors_singleyr_2024_*.xlsx  # Single-year rankings
│   └── Table_2_*, Table_3_*                  # Thresholds and max values
│
├── data/                          # All data files
│   ├── comprehensive_sample.csv              # 600 researchers sample
│   ├── openalex_comprehensive_data.csv       # 564 with valid coverage
│   ├── openalex_data_with_orcid.csv          # ORCID-verified subset (362)
│   ├── openalex_rankings_full.csv            # Ranking replication (541)
│   ├── scopus_vs_openalex_rankings.csv       # Ranking comparison
│   ├── award_winners_case_studies.csv        # Nobel/Pulitzer cases
│   ├── citation_quality_*.csv                # Journal impact controls
│   ├── university_adoption/                  # 123 universities, 32 countries
│   └── robustness_analysis/                  # 5-replicate robustness data
│
├── scripts/                       # Analysis scripts
│   ├── python/                    # Python scripts
│   │   ├── create_stratified_sample.py        # Step 1: Create sample
│   │   ├── fetch_openalex_comprehensive.py    # Step 2: Fetch OpenAlex data
│   │   ├── create_replicate_samples.py        # Step 3: Create replicates
│   │   ├── match_replicates_to_openalex.py    # Step 4: Match replicates
│   │   ├── fix_data_merge.py                  # Fix Scopus data recovery
│   │   ├── comprehensive_statistical_analysis.py
│   │   ├── figure_4_university_adoption.py    # Figure 1
│   │   ├── create_manuscript_visualizations.py # Figure 5
│   │   ├── figureS1_sample_characteristics.py # Figure S1
│   │   ├── figureS2_coverage_distribution.py  # Figure S2
│   │   ├── figureS3_publisher_breakdown.py    # Figure S3
│   │   ├── figureS4_regression_diagnostics.py # Figure S4 (OLS diagnostics)
│   │   ├── figureS5_oa_analysis.py            # Figure S4 (OA analysis)
│   │   ├── figureS6_extreme_cases.py          # Figure S6
│   │   └── ...
│   ├── data_collection/           # Data collection scripts
│   │   ├── create_stratified_sample.py
│   │   └── fetch_openalex_comprehensive.py
│   └── R/                         # R scripts
│       ├── figures_1_2_3_coverage_analysis.R   # Figures 2, 3, 4
│       └── bayesian/              # Bayesian analysis pipeline
│           ├── run_all.R          # Master script
│           ├── 00_install_deps.R
│           ├── 01_data_preparation.R
│           ├── 02_main_regression_model.R
│           ├── 03_hierarchical_field_model.R
│           ├── 04_hypothesis_tests.R
│           ├── 05_model_comparison.R
│           ├── 06_posterior_visualization.R   # Figure 6, Figures S8-S9
│           ├── 07_frequentist_comparison.R    # Figure S11
│           ├── 08_run_all_replicates.R        # Figure S13
│           └── 09_manuscript_tables.R         # Tables B1-B5
│
├── figures/                       # All generated figures
│   ├── main/                      # Main manuscript figures (1-6)
│   │   ├── Figure1_University_Adoption.png/.pdf
│   │   ├── Figure2_Coverage_by_Field.png/.pdf
│   │   ├── Figure3_Elsevier_vs_Coverage.png/.pdf
│   │   ├── Figure4_Books_vs_Coverage.png/.pdf
│   │   ├── Figure5_Scopus_vs_OpenAlex_Rankings.png/.pdf
│   │   └── Figure6_Bayesian_Hypothesis_Tests.png/.pdf
│   ├── supplementary/             # SI Appendix figures (S1-S13)
│   │   ├── FigureS1_Sample_Characteristics.png
│   │   ├── FigureS2_Coverage_Distribution.png
│   │   ├── FigureS3_Publisher_Breakdown.png
│   │   ├── FigureS4_OA_Analysis.png
│   │   ├── FigureS5_Regression_Diagnostics.png
│   │   ├── FigureS6_Extreme_Cases.png
│   │   ├── FigureS7_Ranking_Changes_Distribution.png
│   │   ├── FigureS8_Elsevier_Posterior.png
│   │   ├── FigureS9_Field_Type_Posteriors.png
│   │   ├── FigureS10_MCMC_Diagnostics.png
│   │   ├── FigureS11_Bayesian_vs_Frequentist.png
│   │   ├── FigureS12_Prior_Sensitivity.png
│   │   └── FigureS13_Replicate_Robustness.png
│   └── bayesian/                  # Bayesian diagnostic figures
│       ├── key_hypotheses.png/.pdf
│       ├── Figure_B1_posterior_distributions.png/.pdf
│       ├── Figure_B2_hierarchical_effects.png/.pdf
│       ├── Figure_B4_bayesian_vs_frequentist.png/.pdf
│       ├── rhat_diagnostic.png/.pdf
│       ├── ess_diagnostic.png/.pdf
│       └── replicate_posteriors.png/.pdf
│
├── results/                       # Analysis results
│   └── bayesian/
│       ├── manuscript_tables/     # Tables B1-B5 (CSV)
│       └── model_summaries/       # Detailed model output (10 CSVs)
│
└── tables/                        # Summary tables (CSV)
    ├── Table1_Summary.csv
    ├── table_summary_statistics.csv
    └── extreme_ranking_improvements.csv
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

Key packages: pandas, numpy, scipy, statsmodels, matplotlib, seaborn, requests, openpyxl

### R Packages (Base Analysis)

```bash
Rscript install_r_dependencies.R
```

Key packages: ggplot2, dplyr, tidyr, readr, scales, ggrepel

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

### Option 1: Reproduce from Pre-generated Data (Quick)

Use `REPRODUCE_ALL.sh` to regenerate all figures and analyses from the included data files:

```bash
./REPRODUCE_ALL.sh
```

### Option 2: Full Reproduction from Scratch

To regenerate everything from the original Ioannidis dataset (including new samples and fresh OpenAlex data):

#### Step 1: Source Data (Included)

The Ioannidis "top 2% scientists" dataset is included in the repository:
- **Location**: `August 2025 data-update for Updated science-wide a/`
- **Main file**: `Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx` (~85MB)
- **Source**: [Elsevier Data Repository](https://doi.org/10.17632/btchxktzyw)

#### Step 2: Create Stratified Sample

```bash
python3 scripts/python/create_stratified_sample.py
```

Creates `data/comprehensive_sample.csv` (600 researchers stratified by field type and ranking position).

#### Step 3: Fetch OpenAlex Data

```bash
python3 scripts/python/fetch_openalex_comprehensive.py
```

Queries the OpenAlex API for each researcher (~3-4 hours) and creates `data/openalex_comprehensive_data.csv`.

#### Step 4: Create Replicate Samples (Optional)

```bash
python3 scripts/python/create_replicate_samples.py
python3 scripts/python/match_replicates_to_openalex.py
```

Creates 5 independent samples (n=400 each) for robustness analysis.

#### Step 5: Run Analysis

```bash
./REPRODUCE_ALL.sh
```

---

### Option 3: Step-by-Step Analysis (from pre-generated data)

#### Step 1: Verify Setup

```bash
python3 -c "import pandas; import scipy; import matplotlib; print('Python OK')"
Rscript -e "library(ggplot2); library(dplyr); print('R OK')"
```

#### Step 2: Generate Main Figures (R)

```bash
Rscript scripts/R/figures_1_2_3_coverage_analysis.R
```

Generates: Figures 2, 3, 4 (coverage by field, Elsevier effect, book effect)

#### Step 3: Generate Main Figures (Python)

```bash
python3 scripts/python/figure_4_university_adoption.py     # Figure 1
python3 scripts/python/create_manuscript_visualizations.py  # Figure 5
```

#### Step 4: Generate Supplementary Figures

```bash
python3 scripts/python/figureS1_sample_characteristics.py
python3 scripts/python/figureS2_coverage_distribution.py
python3 scripts/python/figureS3_publisher_breakdown.py
python3 scripts/python/figureS4_regression_diagnostics.py
python3 scripts/python/figureS5_oa_analysis.py
python3 scripts/python/figureS6_extreme_cases.py
```

#### Step 5: Bayesian Analysis (Optional, ~1-2 hours)

```bash
cd scripts/R/bayesian
Rscript run_all.R           # Full analysis (recommended)
# OR
Rscript run_all.R --quick   # Quick mode (~20 min, fewer iterations)
```

Generates:
- Figure 6 (`key_hypotheses.png`) - Bayesian hypothesis tests
- Supplementary Figures S8-S13 (posteriors, MCMC diagnostics, sensitivity, robustness)
- Tables B1-B5 (`results/bayesian/manuscript_tables/`)

---

## Main Figures

| Figure | Description | Script |
|--------|-------------|--------|
| **Figure 1** | University adoption of rankings (2022-2025) | `figure_4_university_adoption.py` |
| **Figure 2** | Scopus coverage by field type (box plots) | `figures_1_2_3_coverage_analysis.R` |
| **Figure 3** | Elsevier % vs coverage ratio (scatterplot) | `figures_1_2_3_coverage_analysis.R` |
| **Figure 4** | Book % vs coverage ratio (scatterplot) | `figures_1_2_3_coverage_analysis.R` |
| **Figure 5** | Scopus vs OpenAlex ranking comparison | `create_manuscript_visualizations.py` |
| **Figure 6** | Bayesian hypothesis tests (posteriors) | `bayesian/06_posterior_visualization.R` |

---

## Supplementary Figures

| Figure | Description | Script |
|--------|-------------|--------|
| **S1** | Sample characteristics (field distribution, geography) | `figureS1_sample_characteristics.py` |
| **S2** | Coverage distribution histograms | `figureS2_coverage_distribution.py` |
| **S3** | Publisher breakdown by field type | `figureS3_publisher_breakdown.py` |
| **S4** | Open access publisher analysis | `figureS5_oa_analysis.py` |
| **S5** | Regression diagnostics (OLS) | `figureS4_regression_diagnostics.py` |
| **S6** | Extreme undercounting cases | `figureS6_extreme_cases.py` |
| **S7** | Ranking changes distribution | `create_manuscript_visualizations.py` |
| **S8** | Posterior distributions for main effects | `bayesian/06_posterior_visualization.R` |
| **S9** | Field-level random effects | `bayesian/06_posterior_visualization.R` |
| **S10** | MCMC convergence diagnostics | `bayesian/06_posterior_visualization.R` |
| **S11** | Bayesian vs frequentist comparison | `bayesian/07_frequentist_comparison.R` |
| **S12** | Prior sensitivity analysis | `bayesian/06_posterior_visualization.R` |
| **S13** | Robustness across 5 independent replicates | `bayesian/08_run_all_replicates.R` |

---

## Data Files

### Primary Data

| File | Description | n |
|------|-------------|---|
| `comprehensive_sample.csv` | Stratified random sample from top 2% dataset | 600 |
| `openalex_comprehensive_data.csv` | Matched to OpenAlex with valid coverage ratios | 564 |
| `openalex_data_with_orcid.csv` | ORCID-verified subset for validation | 362 |
| `scopus_vs_openalex_rankings.csv` | Ranking comparison using same formula | 541 |

### University Adoption Data

| File | Description |
|------|-------------|
| `university_adoption/university_adoption_data.csv` | Aggregated adoption metrics by year (2022-2025) |
| `university_adoption/university_details.csv` | 123 individual university records across 32 countries |

### Robustness Data

| File | Description |
|------|-------------|
| `robustness_analysis/replicates/replicate_*_n400.csv` | 5 independent samples (n=400 each) |
| `robustness_analysis/openalex_matched/replicate_*_openalex_data.csv` | OpenAlex-matched replicate data |

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
- **Warmup**: 1,000 iterations
- **Sampling**: 3,000 iterations per chain
- **Total samples**: 12,000 post-warmup
- **Priors**: Weakly informative Normal(0, 1)

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
  - Elsevier effect: 23.6 pp (vs 30.6 pp full sample)
  - Book bias: ρ = -0.503 (vs ρ = -0.534 full sample)
  - Field-type gap: 32.3 pp (vs 43.6 pp full sample)
- **Conclusion**: Findings not artifacts of name-matching errors

### Robustness Analysis

- **5 independent replicate samples** (n=400 each, unstratified)
- **All replicates**: P(Direction) >= 99.98% for Elsevier effect
- **Pooled Elsevier effect**: mean β = 0.169 (± 0.038 SD), range [0.129, 0.217]
- **Conclusion**: Effects are robust and replicable

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
  author={Lipo, Carl P. and DiNapoli, Beau and Andrus, Benjamin},
  journal={Research Evaluation},
  year={2026},
  note={Under review}
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

---

## Contact

Questions about reproducibility or this code? Contact Carl Lipo (clipo@binghamton.edu)

**GitHub**: https://github.com/clipo/top2percent

---

**Last updated**: March 7, 2026 (Version 6.0 - Research Evaluation Submission)
