# Code Documentation and Reproducibility Guide

This document provides comprehensive documentation for all analysis scripts in the reproducibility package.

---

## Overview

The analysis consists of 6 scripts that must be run in sequence:

1. **create_stratified_sample.py** - Sample selection from "top 2%" dataset
2. **fetch_openalex_comprehensive.py** - Data collection from OpenAlex API
3. **analyze_coverage_bias.py** - Statistical hypothesis testing
4. **create_comprehensive_figures.R** - Publication-quality figure generation
5. **analyze_interdisciplinary_bias.py** - Publisher diversity analysis (optional)
6. **investigate_field_assignment.py** - Field classification analysis (optional)

---

## 1. create_stratified_sample.py

### Purpose
Generates a stratified random sample of ~400 researchers from the "top 2%" dataset for validating Scopus coverage bias.

### Reproducibility Features
- **Random seed**: Set to 42 (line 49-50)
- **Deterministic**: Same seed produces identical sample
- **Documented**: All sampling decisions explicit

### Input
- `Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx`
  - Source: https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw
  - Size: ~90 MB
  - Contains: 230,333 researchers

### Output
- `data/comprehensive_sample.csv`
  - 397 researchers
  - Columns: sample_id, authfull, sm-subfield-1, field_type, sample_stratum, rank, np, nc, h, country, institution

### Sampling Strategy
1. **Field Classification**: 24 fields × 3 categories
   - Book-heavy: 8 fields (Archaeology, History, Philosophy, etc.)
   - Mixed: 8 fields (Sociology, Economics, Law, etc.)
   - Journal-heavy: 8 fields (Genetics, Physics, Chemistry, etc.)

2. **Stratification**: 3 strata per field
   - **Top quartile**: Best-ranked researchers in field's top 2%
   - **Bottom quartile**: Lowest-ranked researchers in field's top 2%
   - **Anomalies**: In global top 2% but OUTSIDE field's top 2% (mathematically impossible cases)

3. **Sample Size**: ~6 researchers per field per stratum

### Dependencies
```python
pandas >= 2.0.0
numpy >= 1.24.0
openpyxl >= 3.1.0  # For Excel reading
```

### Runtime
- 1-2 minutes (Excel loading is slow)

### Usage
```bash
python3 create_stratified_sample.py
```

### Error Handling
- Checks for missing input file (provides download link)
- Validates required columns exist
- Handles fields with insufficient data

---

## 2. fetch_openalex_comprehensive.py

### Purpose
Collects publication data from OpenAlex API for all sampled researchers to compare against Scopus.

### Reproducibility Features
- **Checkpointing**: Saves progress every 50 researchers
- **Resumable**: Can restart from checkpoint if interrupted
- **Rate limiting**: Respects OpenAlex API guidelines
- **Logging**: Detailed progress output

### Input
- `data/comprehensive_sample.csv` (from step 1)
- OpenAlex API: https://api.openalex.org (free, no auth required)

### Output
- `data/evidence_summary_table.csv`: Main results file
  - One row per researcher
  - Columns: all from sample + openalex_found, openalex_pubs, coverage_ratio, elsevier_pct, wiley_pct, springer_pct, books_pct, oa_publisher_pct, etc.

- `openalex_works/`: Individual publication lists
  - One CSV per researcher (397 files)
  - Detailed publication metadata
  - Used for validation and detailed analysis

### API Usage
- **Endpoint**: https://api.openalex.org/authors
- **Rate limit**: ~10 requests/second for polite users
- **Delay**: 0.2 seconds between requests (line 25)
- **Polite pool**: Requires email in User-Agent header (line 24)

### Publisher Classification
The script classifies publishers into 12 major groups:

1. **Elsevier** (includes Cell Press, Lancet, Academic Press)
2. **Wiley** (includes Wiley-Blackwell)
3. **Springer Nature** (includes BMC, Palgrave)
4. **Taylor & Francis** (includes Routledge, CRC Press)
5. **PLOS** (open access)
6. **Frontiers** (open access)
7. **MDPI** (open access)
8. **Oxford University Press**
9. **Cambridge University Press**
10. **IEEE**
11. **ACM**
12. **American Chemical Society**

### Matching Strategy
1. **Author search**: By name
2. **Verification**: Check h-index within ±20% of Scopus value
3. **Fallback**: If h-index mismatch, try citation count match
4. **Rejection**: If neither matches, mark as not found

### Coverage Ratio Calculation
```
coverage_ratio = scopus_pubs / openalex_pubs
```

Where:
- `scopus_pubs`: Publication count from "top 2%" dataset
- `openalex_pubs`: Publication count from OpenAlex API
- Ratio > 1.0 means Scopus has more (unusual, suggests name mismatch)
- Ratio < 0.5 means Scopus has less than half (strong undercounting)

### Dependencies
```python
pandas >= 2.0.0
requests >= 2.31.0
```

### Runtime
- 15-20 minutes for 397 researchers
- ~2-3 seconds per researcher (API call + processing)

### Usage
```bash
python3 fetch_openalex_comprehensive.py
```

### Error Handling
- Checkpoint recovery: Resume from last saved position
- API errors: Retry with exponential backoff
- Name matching failures: Logged and marked as not found
- Network errors: Graceful failure with informative messages

### Important Notes
- **Match rate**: Expect ~90-91% (361 of 397 researchers)
- **Coverage validation**: Results >150% coverage are excluded as probable mismatches
- **Data freshness**: OpenAlex updates weekly; slight variations possible over time

---

## 3. analyze_coverage_bias.py

### Purpose
Statistical analysis testing four hypotheses about systematic bias in Scopus coverage.

### Reproducibility Features
- **No randomness**: All tests are deterministic
- **Complete output**: All statistics printed to console and saved to file
- **JSON export**: Results saved in machine-readable format

### Input
- `data/evidence_summary_table.csv` (from step 2)

### Output
- Console: Detailed statistical results
- `ANALYSIS_SUMMARY.txt`: Complete analysis text
- `analysis_results.json`: Machine-readable results

### Hypotheses Tested

#### H1: Publisher Bias
**Question**: Do researchers publishing more in Elsevier journals have better Scopus coverage?

**Tests**:
- Pearson correlation (elsevier_pct vs coverage_ratio)
- Mann-Whitney U test (high vs low Elsevier groups)
- Cohen's d (effect size)

**Expected Results**:
- r ≈ 0.564, p < 0.001
- High Elsevier: 60.4% coverage
- Low Elsevier: 32.9% coverage
- d ≈ 1.178 (large effect)

#### H2: Book Bias
**Question**: Do researchers with more books have worse Scopus coverage?

**Tests**:
- Pearson correlation (books_pct vs coverage_ratio)
- Correlation within book-heavy fields
- Mann-Whitney U within fields

**Expected Results**:
- Overall: r ≈ -0.503, p < 0.001
- Within book-heavy: r ≈ -0.349, p < 0.001

#### H3: Open Access Penalty
**Question**: Do researchers publishing more in OA venues have worse coverage?

**Tests**:
- Pearson correlation (oa_publisher_pct vs coverage_ratio)
- Group comparisons (PLOS vs non-PLOS, Frontiers vs non-Frontiers)

**Expected Results**:
- r ≈ +0.251, p < 0.001 (POSITIVE correlation - no penalty)
- PLOS: 60.6% vs non-PLOS: 36.3%

#### H4: Field-Level Bias
**Question**: Do book-heavy fields have systematically worse coverage?

**Tests**:
- Kruskal-Wallis H test (3 field types)
- Post-hoc pairwise Mann-Whitney U tests

**Expected Results**:
- Book-heavy: 31.3% median coverage
- Mixed: 36.3%
- Journal-heavy: 70.7%
- H ≈ 132.973, p < 0.001

### Multivariate Regression
**Model**:
```
coverage_ratio ~ elsevier_pct + books_pct + oa_pct + field_type + country
```

**Expected Results**:
- R² ≈ 0.449 (explains 45% of variance)
- Elsevier %: β ≈ +0.0055, p < 0.001
- Book %: β ≈ -0.0018, p < 0.01
- Book-heavy field: β ≈ -0.240, p < 0.001

### Statistical Methods

All tests appropriate for the data:

1. **Pearson correlation**: Tests linear relationships (robust with n=361)
2. **Mann-Whitney U**: Non-parametric test for 2 groups (no normality assumption)
3. **Kruskal-Wallis H**: Non-parametric test for 3+ groups (equivalent to non-parametric ANOVA)
4. **Cohen's d**: Standard effect size measure ((mean1 - mean2) / pooled_sd)
5. **OLS regression**: Multivariate analysis with multiple predictors

### Data Cleaning
- Filters to `openalex_found == True` (361 of 397)
- Excludes coverage > 150% (probable name mismatches)
- Drops rows with missing values in key variables

### Dependencies
```python
pandas >= 2.0.0
numpy >= 1.24.0
scipy >= 1.11.0
statsmodels >= 0.14.0  # For multivariate regression
sklearn >= 1.3.0  # For regression (alternative)
```

### Runtime
- 10-15 seconds

### Usage
```bash
python3 analyze_coverage_bias.py > ANALYSIS_SUMMARY.txt
```

---

## 4. create_comprehensive_figures.R

### Purpose
Generates publication-quality figures (300 DPI) for the manuscript.

### Reproducibility Features
- **Seed set**: R's random seed for jitter positioning
- **Deterministic colors**: Fixed color palette
- **High resolution**: 300 DPI for publication
- **Same data cleaning**: Matches Python analysis exactly

### Input
- `data/evidence_summary_table.csv` (same as Python analysis)

### Output
All saved to `figures/` directory:

1. **Figure1_Coverage_by_Field.png** (300 DPI, ~387 KB)
   - Boxplots showing coverage by field type
   - Shows median, quartiles, outliers
   - Jittered points for all observations

2. **Figure2_Elsevier_vs_Coverage.png** (300 DPI, ~485 KB)
   - Scatterplot with regression line
   - Colored by field type
   - Correlation coefficient annotated

3. **Figure3_Books_vs_Coverage.png** (300 DPI, ~554 KB)
   - Scatterplot showing negative correlation
   - Same format as Figure 2

4. **Table1_Summary.csv**
   - Summary statistics by field type
   - Median coverage, Elsevier %, book %

### Color Palette
- Book-heavy: Orange (#D55E00)
- Mixed: Yellow-orange (#E69F00)
- Journal-heavy: Blue (#0072B2)
- Colorblind-friendly palette

### Dependencies
```R
ggplot2 >= 3.4.0
dplyr >= 1.1.0
tidyr >= 1.3.0
scales >= 1.2.0
```

### Runtime
- 20-30 seconds

### Usage
```bash
Rscript create_comprehensive_figures.R
```

### Auto-installation
The script automatically installs missing packages on first run.

---

## 5. analyze_interdisciplinary_bias.py (Optional)

### Purpose
Analyzes whether researchers with diverse publisher portfolios face bias.

### Method
Uses Herfindahl-Hirschman Index (HHI) to measure publisher concentration:

```
HHI = sum(share_i^2) for all publishers

where share_i = publications with publisher i / total publications
```

- HHI = 1.0: All publications with one publisher (monopoly)
- HHI → 0: Publications evenly distributed across many publishers

### Key Finding
174 researchers (48% of sample) have diverse portfolios (HHI < 0.5).
Overall, these show better coverage (59.8% vs 33.2%), but extreme cases
exist (3-7% coverage despite 300-1000+ publications).

### Usage
```bash
python3 analyze_interdisciplinary_bias.py
```

### Output
- Console output with statistics
- `interdisciplinary_disadvantaged.csv`: Researchers with diverse portfolios and low coverage

---

## 6. investigate_field_assignment.py (Optional)

### Purpose
Examines how interdisciplinary researchers are assigned to single fields.

### Method
Identifies researchers publishing across multiple major publishers
(Elsevier, Wiley, Springer, Oxford, Cambridge, etc.) as likely interdisciplinary.

### Usage
```bash
python3 investigate_field_assignment.py
```

### Output
- Console output with examples
- `potentially_interdisciplinary_researchers.csv`: Candidates for further investigation

---

## Complete Reproduction Workflow

### Option 1: Use Our Data (Recommended)

```bash
# Step 1: Verify setup
python3 verify_setup.py

# Step 2: Run statistical analysis
python3 code/analyze_coverage_bias.py > ANALYSIS_SUMMARY.txt

# Step 3: Generate figures
Rscript code/create_comprehensive_figures.R

# Step 4: Optional analyses
python3 code/analyze_interdisciplinary_bias.py
python3 code/investigate_field_assignment.py
```

**Expected runtime**: 1-2 minutes total

### Option 2: Reproduce From Scratch

```bash
# Step 1: Download "top 2%" dataset
# Go to: https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw
# Download: Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx
# Place in: August 2025 data-update for Updated science-wide a/

# Step 2: Create sample
python3 code/create_stratified_sample.py

# Step 3: Fetch OpenAlex data (15-20 minutes)
python3 code/fetch_openalex_comprehensive.py

# Step 4: Run analysis
python3 code/analyze_coverage_bias.py > ANALYSIS_SUMMARY.txt

# Step 5: Generate figures
Rscript code/create_comprehensive_figures.R

# Step 6: Optional analyses
python3 code/analyze_interdisciplinary_bias.py
python3 code/investigate_field_assignment.py
```

**Expected runtime**: ~25-30 minutes total

---

## Troubleshooting

### OpenAlex API Issues

**Problem**: Rate limit errors
**Solution**: Script includes 0.2s delay; OpenAlex allows ~10/sec. If errors persist, wait 10 minutes.

**Problem**: Network timeouts
**Solution**: Script has checkpointing. If interrupted, just rerun - it will resume from last checkpoint.

**Problem**: Match rate lower than expected
**Solution**: 90-91% is normal. Failures due to name variations or missing OpenAlex records.

### Statistical Results Don't Match

**Problem**: Coverage ratios differ by ±3%
**Explanation**: OpenAlex updates weekly. New publications indexed. Normal variation.

**Problem**: Match rate differs by ±2%
**Explanation**: OpenAlex author matching improves over time. Normal variation.

**Problem**: Results substantially different
**Action**: Contact authors. Check data file versions.

### R Package Installation

**Problem**: Package installation fails
**Solution**:
```R
install.packages(c("ggplot2", "dplyr", "tidyr", "scales"))
```

**Problem**: Permission errors on Linux
**Solution**: Install packages to user library or use conda environment

### Python Dependencies

**Problem**: Import errors
**Solution**:
```bash
pip install pandas numpy scipy statsmodels requests openpyxl
```

**Problem**: Version conflicts
**Solution**: Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Data Provenance

### Source Data
- **"Top 2%" dataset**: Ioannidis et al. (2024), licensed CC-BY 4.0
- **OpenAlex**: Priem et al. (2022), licensed CC0 (public domain)

### Our Data
- **comprehensive_sample.csv**: Our selection, CC-BY 4.0
- **evidence_summary_table.csv**: Our analysis, CC-BY 4.0

### Modifications
- Field classifications: Based on domain expert knowledge
- Publisher groupings: Based on corporate ownership and brand families
- Coverage calculations: Our methodology

---

## Quality Assurance

### Verification Steps

1. **Sample representativeness**: Compare field distributions to full dataset
2. **Match quality**: Manual verification of 20 random matches
3. **Coverage calculation**: Spot-check 10 researchers manually
4. **Publisher classification**: Verify top 50 most common publishers
5. **Statistical assumptions**: Check regression diagnostics

### Known Limitations

1. **Name matching**: ~9% fail to match (name variations, missing records)
2. **Coverage extremes**: Exclude >150% (probable mismatches)
3. **OpenAlex completeness**: May miss older works, non-English works
4. **Publisher classification**: "Other" category is heterogeneous
5. **Temporal changes**: OpenAlex updates weekly; exact results may vary

---

## Citation

If you use this code or data, please cite:

Carl P. Lipo, Robert J. DiNapoli, Ben Andrus. (In Review). Systematic Bias in "Top 2% of Scientists" Rankings:
Evidence from Multi-Database Comparison. *Nature Communications*

And cite the source data:

Ioannidis JPA, Boyack KW, Baas J. (2024). Updated August 2024 data for
"Updated science-wide author databases of standardized citation indicators".
Elsevier Data Repository. https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw

Priem J, Piwowar H, Orr R. (2022). OpenAlex: A fully-open index of scholarly
works, authors, venues, institutions, and concepts. arXiv:2205.01833.

---

**Last updated**: November 2025
**Code version**: 1.0
**Contact**: Carl Lipo clipo@binghamton.edu
