# Script Index and Documentation

Complete guide to all analysis scripts in the reproducibility package.

## Quick Reference

### One-Command Reproducibility
```bash
python generate_all_figures.py    # Generate all 6 main figures
python run_all_analyses.py        # Run complete analysis pipeline
```

---

## Main Figure Generation Scripts

### figures_1_2_3_coverage_analysis.R
**Location**: `scripts/R/`
**Language**: R (version 4.0+)
**Purpose**: Generate main Figures 1-3 (coverage analysis)

**Inputs**:
- `data/comprehensive_sample.csv` (600 researchers)
- `data/openalex_comprehensive_data.csv` (coverage ratios)

**Outputs**:
- `figures/Figure1_Coverage_by_Field.png` - Box plots by field type
- `figures/Figure2_Elsevier_vs_Coverage.png` - Scatterplot with regression line
- `figures/Figure3_Books_vs_Coverage.png` - Scatterplot with regression line
- `figures/Table1_Summary.csv` - Summary statistics

**Dependencies**:
- ggplot2, dplyr, tidyr, readr, broom, ggpubr

**Runtime**: ~5-10 seconds

**Usage**:
```bash
Rscript scripts/R/figures_1_2_3_coverage_analysis.R
```

---

### figure_4_university_adoption.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Generate Figure 4 (university adoption 2022-2024)

**Inputs**:
- `data/university_adoption/university_adoption_data.csv` (58 universities)
- `data/university_adoption/university_details.csv` (geographic/type data)

**Outputs**:
- `figures/Figure4_university_adoption.png` - Multi-panel visualization

**Dependencies**:
- pandas, matplotlib, numpy

**Runtime**: ~2 seconds

**Usage**:
```bash
python scripts/python/figure_4_university_adoption.py
```

---

### create_manuscript_visualizations.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Generate Figures 5-6 (OpenAlex ranking comparison)

**Inputs**:
- `data/scopus_vs_openalex_rankings.csv` (537 researcher comparisons)
- `data/openalex_rankings_full.csv` (complete ranking data)
- `data/comprehensive_sample.csv` (field type information)

**Outputs**:
- `figures/Figure5_Scopus_vs_OpenAlex_Rankings.png` - Scatterplot comparison (ρ=0.567)
- `figures/Figure6_Ranking_Changes_Distribution.png` - Distribution analysis

**Dependencies**:
- pandas, matplotlib, numpy, scipy

**Runtime**: ~3 seconds

**Usage**:
```bash
python scripts/python/create_manuscript_visualizations.py
```

---

## Validation and Robustness Analyses

### create_replicate_samples.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Generate 5 independent stratified random samples for robustness testing

**Inputs**:
- Full 2024 rankings Excel file (230,333 researchers)

**Outputs**:
- `data/robustness_analysis/replicates/replicate_1_n400.csv` - Replicate 1 sample
- `data/robustness_analysis/replicates/replicate_2_n400.csv` - Replicate 2 sample
- `data/robustness_analysis/replicates/replicate_3_n400.csv` - Replicate 3 sample
- `data/robustness_analysis/replicates/replicate_4_n400.csv` - Replicate 4 sample
- `data/robustness_analysis/replicates/replicate_5_n400.csv` - Replicate 5 sample
- `data/robustness_analysis/replicate_metadata.csv` - Sample metadata

**Dependencies**:
- pandas, openpyxl

**Runtime**: ~2 seconds

**Usage**:
```bash
python scripts/python/create_replicate_samples.py
```

**Details**: Creates 5 independent samples (n=400 each) using stratified random sampling by rank percentile (5 bins) and field type (book-heavy/mixed/journal-heavy). Uses different random seeds (2000-2004) to ensure independence.

---

### match_replicates_to_openalex.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Match all 2,000 researchers from 5 replicates to OpenAlex

**Inputs**:
- `data/robustness_analysis/replicates/replicate_*_n400.csv` (5 files)

**Outputs**:
- `data/robustness_analysis/openalex_matched/replicate_*_openalex_data.csv` (5 files)
- `data/robustness_analysis/openalex_matched/all_replicates_combined.csv` (2,000 researchers)

**Dependencies**:
- pandas, requests, time

**Runtime**: ~87 minutes (2,000 API calls with 0.5s delays)

**Usage**:
```bash
python scripts/python/match_replicates_to_openalex.py
```

**Details**: For each of 2,000 researchers:
1. Searches OpenAlex by name and institution
2. Fetches complete publication history
3. Calculates publisher percentages (Elsevier, Wiley, Springer, Oxford, Cambridge)
4. Calculates books percentage
5. Calculates OA publisher percentage (PLOS, Frontiers, MDPI)
6. Determines coverage ratio (Scopus pubs / OpenAlex total works)

Match rates: 87.8-94.2% (mean: 91.5%)

---

### analyze_all_replicates.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Calculate effect sizes across all 5 replicates to test robustness

**Inputs**:
- `data/robustness_analysis/openalex_matched/replicate_*_openalex_data.csv` (5 files)
- `data/robustness_analysis/replicates/replicate_*_n400.csv` (5 files)

**Outputs**:
- `data/robustness_analysis/replicate_effect_sizes.csv` - Effect sizes for each replicate
- `data/robustness_analysis/replicate_summary_statistics.csv` - Summary statistics (means/SDs)

**Dependencies**:
- pandas, numpy, scipy

**Runtime**: ~30 seconds

**Usage**:
```bash
python scripts/python/analyze_all_replicates.py
```

**Details**: For each replicate, calculates:
- **H1 (Elsevier effect)**: Cohen's d, Pearson r, mean difference, p-value
- **H2 (Book penalty)**: Cliff's delta, Pearson r, mean difference, p-value (where applicable)
- **H3 (Field bias)**: Cohen's d, mean difference, p-value (where applicable)

Then computes summary statistics across all 5 replicates:
- Mean effect size ± SD
- Range (min to max)
- Tests stability (SD < 0.10 indicates excellent stability)

**Key findings**:
- Elsevier effect: d=0.58±0.09 (highly stable), all p<0.001
- Book penalty: δ=-0.08±0.01 (very stable where detected)
- Demonstrates findings do NOT depend on sample selection

---

### extract_orcid_validation.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: ORCID verification analysis - validate findings with unique identifiers

**Inputs**:
- `data/openalex_comprehensive_data.csv` (matched OpenAlex data)

**Outputs**:
- `data/openalex_data_with_orcid.csv` (362 ORCID-verified researchers)
- `orcid_validation_summary.json` (statistical summary)
- Console output with validation statistics

**Key Findings**:
- 362/600 researchers (60.3%) have ORCID
- Elsevier bias persists: 28.0 pp (p<0.0001)
- Book bias persists: r=-0.494 (p<0.0001)

**Dependencies**:
- pandas, requests, scipy, json

**Runtime**: ~5-10 minutes (API calls)

**Usage**:
```bash
python scripts/python/extract_orcid_validation.py
```

---

### test_ranking_coverage_correlation.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Test if ranking position correlates with coverage (exclusion bias test)

**Inputs**:
- `data/comprehensive_sample.csv` (with rank_global, rank_in_field)
- `data/openalex_comprehensive_data.csv` (coverage ratios)

**Outputs**:
- `ranking_coverage_correlation_results.csv` (statistical results)
- Console output with correlation analysis

**Key Findings**:
- Spearman ρ=-0.297 (p<0.0001)
- Top quartile: 54.8% median coverage
- Bottom quartile: 29.2% median coverage
- 25.5 pp gradient suggests coverage acts as barrier to entry

**Dependencies**:
- pandas, scipy, numpy

**Runtime**: ~2 seconds

**Usage**:
```bash
python scripts/python/test_ranking_coverage_correlation.py
```

---

### award_winners_case_studies.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Analyze exclusion of high-profile award winners (Nobel, Pulitzer) due to book bias

**Inputs**:
- `data/comprehensive_sample.csv` (field classifications)
- Manual curation of award winners in book-heavy fields

**Outputs**:
- `data/award_winners_case_studies.csv` (9 high-profile cases)
- Console output with exclusion evidence

**Key Findings**:
- 9 researchers with highest external recognition likely excluded
- Nobel laureates: Claudia Goldin (Economics 2023), Elinor Ostrom (Economics 2009)
- Pulitzer Prize winners: Eric Foner, Annette Gordon-Reed, Jill Lepore
- Major scholars: Ernst Gombrich (40M+ copies), Clifford Geertz (Nat'l Humanities Medal)
- Pattern: Even top scholars in book-heavy fields face systematic exclusion

**Dependencies**:
- pandas, numpy

**Runtime**: ~2 seconds

**Usage**:
```bash
python scripts/python/award_winners_case_studies.py
```

---

### citation_quality_analysis.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Test whether journal citation impact explains Elsevier coverage advantage

**Inputs**:
- `data/openalex_comprehensive_data.csv` (coverage and publisher data)
- OpenAlex API (journal citation impact metrics)

**Outputs**:
- `data/citation_quality_stratified.csv` (tertile analysis)
- `data/citation_quality_relative.csv` (relative quality comparison)
- `data/citation_quality_regression.csv` (regression with controls)
- Console output with three independent tests

**Key Findings**:
- **Stratified analysis**: Effect persists in ALL tertiles (low: 15.3 pp, medium: 24.7 pp, high: 34.6 pp)
- **Relative quality**: Effect remains when Elsevier journals have LOWER impact (32.3 pp, p<0.0001)
- **Regression**: Effect significant (β=-6.05, p=0.0065) controlling for citations-per-publication
- **Conclusion**: Journal prestige does NOT explain Elsevier advantage

**Dependencies**:
- pandas, scipy, statsmodels, requests

**Runtime**: ~10-15 minutes (API calls for journal metrics)

**Usage**:
```bash
python scripts/python/citation_quality_analysis.py
```

---

### comprehensive_statistical_analysis.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Apply robust non-parametric effect sizes and multiple comparisons corrections

**Inputs**:
- `data/openalex_comprehensive_data.csv` (coverage analysis)

**Outputs**:
- `data/effect_sizes_comparison.csv` (Cliff's delta vs Cohen's d)
- `data/comprehensive_statistics.csv` (Bonferroni corrections)
- Console output with power analysis

**Key Findings**:
- **Cliff's delta vs Cohen's d**:
  - Elsevier: δ=0.539 (large) vs d=-0.120 (negligible)
  - Books: δ=-0.749 (large) vs d=-0.155 (negligible)
- **Bonferroni correction**: All 5 primary effects remain p<0.010
- **Power analysis**: >99.9% power for primary effects
- **Conclusion**: Effects 4-5x larger with appropriate non-parametric measures

**Dependencies**:
- pandas, scipy, numpy

**Runtime**: ~3 seconds

**Usage**:
```bash
python scripts/python/comprehensive_statistical_analysis.py
```

---

## OpenAlex Ranking Replication Pipeline

### fetch_all_550_researchers.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Fetch complete publication data from OpenAlex for ranking replication

**Inputs**:
- `data/comprehensive_sample.csv` (researcher names and affiliations)

**Outputs**:
- `researcher_metrics_all_550.csv` (complete OpenAlex metrics)

**Dependencies**:
- pandas, requests, time

**Runtime**: ~30-60 minutes (API rate limits)

**Usage**:
```bash
python scripts/python/fetch_all_550_researchers.py
```

**Note**: Rate-limited to respect OpenAlex API guidelines (10 requests/second)

---

### create_openalex_top2percent.py
**Location**: `scripts/python/`
**Language**: Python 3.8+
**Purpose**: Calculate composite scores using Ioannidis formula with OpenAlex data

**Inputs**:
- `researcher_metrics_all_550.csv` (from fetch script)
- `data/comprehensive_sample.csv` (original Scopus ranks)

**Outputs**:
- `data/openalex_rankings_full.csv` (537 researchers with composite scores)
- `data/openalex_top_2_percent.csv` (top 10 by OpenAlex score)
- `data/scopus_vs_openalex_rankings.csv` (side-by-side comparison)

**Key Findings**:
- Spearman ρ=0.567 correlation with Scopus rankings
- Median shift: 142,276 positions
- Extreme case: 1.2 million position change

**Dependencies**:
- pandas, numpy, scipy

**Runtime**: ~5 seconds

**Usage**:
```bash
python scripts/python/create_openalex_top2percent.py
```

---

## Supplementary Figure Scripts

### figureS1_sample_characteristics.py
**Purpose**: Sample characteristics (field distribution, stratification)
**Output**: `figures/FigureS1_sample_characteristics.png`

### figureS2_coverage_distribution.py
**Purpose**: Coverage distribution histograms and statistics
**Output**: `figures/FigureS2_coverage_distribution.png`

### figureS3_publisher_breakdown.py
**Purpose**: Publisher composition analysis
**Output**: `figures/FigureS3_publisher_breakdown.png`

### figureS4_regression_diagnostics.py
**Purpose**: Regression model diagnostics (residuals, Q-Q plots)
**Output**: `figures/FigureS4_regression_diagnostics.png`

### figureS5_oa_analysis.py
**Purpose**: Open access analysis (no OA penalty found)
**Output**: `figures/FigureS5_oa_analysis.png`

### figureS6_extreme_cases.py
**Purpose**: Extreme undercounting cases (300-1000+ publications)
**Output**: `figures/FigureS6_extreme_cases.png`

**All supplementary scripts**:
- Runtime: ~2-3 seconds each
- Dependencies: pandas, matplotlib, seaborn, scipy

---

## Helper Scripts

### analyze_coverage_bias.py
**Location**: `scripts/python/`
**Purpose**: Core statistical analysis (used by other scripts)
**Functions**: Correlation tests, group comparisons, effect sizes

### install_r_dependencies.R
**Location**: `scripts/R/`
**Purpose**: Install required R packages
**Usage**: `Rscript scripts/R/install_r_dependencies.R`

---

## Master Scripts

### generate_all_figures.py
**Location**: `reproducibility_package/`
**Purpose**: Generate all 6 main figures in one command

**Workflow**:
1. Run R script for Figures 1-3
2. Run Python script for Figure 4
3. Run Python script for Figures 5-6
4. Verify all outputs created

**Runtime**: ~20 seconds total

**Usage**:
```bash
cd reproducibility_package
python generate_all_figures.py
```

---

### run_all_analyses.py
**Location**: `reproducibility_package/`
**Purpose**: Run complete analysis pipeline

**Workflow**:
1. Verify data files present
2. Generate all figures (main + supplementary)
3. Run validation analyses
4. Generate summary report

**Runtime**: ~1-2 minutes

**Usage**:
```bash
cd reproducibility_package
python run_all_analyses.py
```

---

## Data Collection Scripts (Optional)

### create_stratified_sample.py
**Location**: `scripts/data_collection/`
**Purpose**: Create stratified sample from raw rankings

### fetch_openalex_comprehensive.py
**Location**: `scripts/data_collection/`
**Purpose**: Fetch OpenAlex data for comprehensive sample

**Note**: Data collection scripts are optional as pre-collected data is provided.

---

## Complete Analysis Pipeline

### From Scratch (with API calls):
```bash
# 1. Install dependencies
pip install -r requirements.txt
Rscript scripts/R/install_r_dependencies.R

# 2. Generate figures (uses provided data)
python generate_all_figures.py

# 3. Run validation analyses
python scripts/python/extract_orcid_validation.py
python scripts/python/test_ranking_coverage_correlation.py

# 4. Optional: Replicate OpenAlex rankings (slow - API calls)
python scripts/python/fetch_all_550_researchers.py      # 30-60 min
python scripts/python/create_openalex_top2percent.py    # 5 sec
python scripts/python/create_manuscript_visualizations.py # 3 sec
```

### Quick Validation (using provided data):
```bash
# 1. Install dependencies
pip install -r requirements.txt
Rscript scripts/R/install_r_dependencies.R

# 2. Run complete analysis
python run_all_analyses.py
```

---

## Script Dependencies

### Python Requirements (requirements.txt):
- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.11.0
- statsmodels >= 0.14.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- requests >= 2.31.0
- python-docx >= 0.8.11

### R Requirements (install_r_dependencies.R):
- ggplot2
- dplyr
- tidyr
- readr
- broom
- ggpubr
- scales

---

## Output Verification

All scripts include verification steps:
- File existence checks
- File size validation (> 0 bytes)
- Dimension checks for data outputs
- Statistical result validation

Expected output sizes:
- PNG figures: 150-700 KB each (300 DPI)
- CSV data files: 10-300 KB depending on content
- Total package: ~15 MB with all outputs

---

## Troubleshooting

### Common Issues:

**R script fails**: Install R dependencies
```bash
Rscript scripts/R/install_r_dependencies.R
```

**Python script fails**: Install Python dependencies
```bash
pip install -r requirements.txt
```

**File not found**: Ensure running from `reproducibility_package/` directory
```bash
cd reproducibility_package
python generate_all_figures.py
```

**API rate limits**: If fetching OpenAlex data, script respects rate limits automatically
- Max 10 requests/second
- Runtime: 30-60 minutes for 550 researchers

---

## Contact and Support

For issues reproducing results:
1. Check `README.md` for quick start guide
2. Review `SUPPLEMENTARY_MATERIALS.md` for detailed methods
3. Check `CODE_DOCUMENTATION.md` for implementation details
4. Verify all dependencies installed correctly

---

Last updated: December 2025
