# Publisher Bias in Widely-Used Scientist Rankings

Complete reproducibility package for our study documenting systematic publisher, book, and field bias in the "top 2% of scientists" rankings (Ioannidis et al., 2024).

## Contents

```
top2percent/
├── README.md                          # This file
├── SUPPLEMENTARY_MATERIALS.md         # Detailed supplementary information
├── data/                              # Data files
│   ├── comprehensive_sample.csv       # Sample of 600 researchers
│   ├── openalex_comprehensive_data.csv # Coverage analysis (570 matched)
│   ├── openalex_data_with_orcid.csv   # ORCID-verified subset (362 researchers)
│   ├── openalex_rankings_full.csv     # OpenAlex ranking replication (537 researchers)
│   ├── openalex_top_2_percent.csv     # Top 10 by OpenAlex composite score
│   ├── scopus_vs_openalex_rankings.csv # Ranking comparison (ρ=0.567)
│   ├── ranking_coverage_correlation_results.csv # Rank-coverage analysis
│   ├── evidence_summary_table.csv     # Statistical evidence summary
│   └── university_adoption/           # Institutional adoption evidence
│       ├── university_adoption_data.csv
│       └── university_details.csv
├── scripts/                           # Analysis and figure generation
│   ├── R/                            # R scripts
│   │   ├── figures_1_2_3_coverage_analysis.R  # Main figures 1-3
│   │   └── install_r_dependencies.R           # R package installation
│   ├── python/                       # Python scripts
│   │   ├── figure_4_university_adoption.py    # Main figure 4
│   │   ├── extract_orcid_validation.py        # ORCID verification analysis
│   │   ├── test_ranking_coverage_correlation.py # Ranking-coverage gradient
│   │   ├── create_manuscript_visualizations.py # Figures 5-6 (OpenAlex)
│   │   ├── fetch_all_550_researchers.py       # Fetch OpenAlex data
│   │   ├── create_openalex_top2percent.py     # Calculate OpenAlex rankings
│   │   ├── figureS1_sample_characteristics.py # Supplementary figures
│   │   ├── figureS2_coverage_distribution.py
│   │   ├── figureS3_publisher_breakdown.py
│   │   ├── figureS4_regression_diagnostics.py
│   │   ├── figureS5_oa_analysis.py
│   │   └── figureS6_extreme_cases.py
│   └── data_collection/              # Optional: reproduce data collection
│       └── (data collection scripts)
└── figures/                           # Generated figures
    ├── Figure1_Coverage_by_Field.png
    ├── Figure2_Elsevier_vs_Coverage.png
    ├── Figure3_Books_vs_Coverage.png
    ├── Figure4_university_adoption.png
    ├── Figure5_Scopus_vs_OpenAlex_Rankings.png
    ├── Figure6_Ranking_Changes_Distribution.png
    ├── FigureS1_sample_characteristics.png
    ├── FigureS2_coverage_distribution.png
    ├── FigureS3_publisher_breakdown.png
    ├── FigureS4_regression_diagnostics.png
    ├── FigureS5_oa_analysis.png
    └── FigureS6_extreme_cases.png
```

---

## Key Findings

### Extreme Undercounting Cases
**NEW**: We identified 7 researchers with 300-1,000+ publications showing only 3-10% Scopus coverage:
- Timothy Clark (Literary Studies): 894 publications, 3.0% coverage
- Robert Jackson (Religions & Theology): 1,036 publications, 7.0% coverage
- David Hunter (Religions & Theology): 510 publications, 5.1% coverage

### Systematic Bias
- **Publisher bias**: 27.5 pp better coverage for high Elsevier publishers (r=0.563, d=1.178, p<0.001)
- **Book bias**: 39.9 pp worse coverage for book-heavy fields (r=-0.503, p<0.001)
- **Field bias**: Humanities 31.3% vs STEM 70.7% median coverage
- **Elsevier-specific**: Persists despite 33.4% in Oxford/Cambridge/Wiley/Springer vs 11.3% in Elsevier
- **No OA penalty**: Open access shows 24.3 pp better coverage (PLOS: p<0.001)

### Institutional Adoption
- **58 universities** across 20 countries actively promoting these rankings (2022-2024)
- **Persistent use**: No decline despite documented methodological concerns
- **Geographic expansion**: Asia leading (27 universities), North America (18), Europe (14)

### ORCID Verification (NEW)
- **362 researchers (60.3%)** verified with unique persistent identifiers
- **Bias persists in ORCID subset**: Elsevier bias 28.0 pp (p<0.0001), book bias r=-0.494 (p<0.0001)
- **Independent validation**: Findings not artifacts of matching methodology
- **Breaks sampling circularity**: High-confidence subset validates main results

### Ranking-Coverage Correlation (NEW)
- **Significant negative correlation** between rank position and coverage (ρ=-0.297, p<0.0001)
- **Top quartile**: 54.8% median coverage vs **bottom quartile**: 29.2% median coverage
- **25.5 pp gradient**: Evidence that coverage acts as barrier to entry, not just ranking
- **Strongest in book-heavy fields**: ρ=-0.310 (p=0.0004)

### OpenAlex Ranking Replication (NEW)
- **ρ=0.567 correlation** between Scopus and OpenAlex rankings (same formula, complete data)
- **Median shift**: 142,276 positions when using complete publication data
- **Extreme cases**: Individual researchers shift up to 1.2 million positions
- **Top 2% divergence**: OpenAlex top 2% have 6.2 pp lower Elsevier coverage

### Sample
- **n=600 researchers** from "top 2%" dataset
- **570 matched** to OpenAlex (95% match rate)
- **Perfect stratification**: 198 book-heavy, 210 mixed, 192 journal-heavy
- **~100,000 publications** analyzed

---

## Quick Start

### Generate All Figures (Main + Supplementary)

**Option 1: From project root**
```bash
cd /path/to/2percent/
python3 generate_all_figures.py
```

**Option 2: Individual figure scripts**
```bash
cd reproducibility_package/

# Main figures 1-3 (R)
Rscript scripts/R/figures_1_2_3_coverage_analysis.R

# Main figure 4 (Python)
python3 scripts/python/figure_4_university_adoption.py

# Supplementary figures (Python)
python3 scripts/python/figureS1_sample_characteristics.py
python3 scripts/python/figureS2_coverage_distribution.py
python3 scripts/python/figureS3_publisher_breakdown.py
python3 scripts/python/figureS4_regression_diagnostics.py
python3 scripts/python/figureS5_oa_analysis.py
python3 scripts/python/figureS6_extreme_cases.py
```

All figures saved to `figures/` directory at 300 DPI.

---

## Software Requirements

### Python
- **Version**: Python 3.12+
- **Required packages**:
  ```bash
  pip install pandas scipy statsmodels matplotlib seaborn requests
  ```

### R
- **Version**: R 4.3+
- **Required packages**:
  ```bash
  Rscript scripts/R/install_r_dependencies.R
  ```
  Or manually:
  ```R
  install.packages(c("ggplot2", "dplyr", "tidyr", "scales", "ggrepel"))
  ```

---

## Data Files

### comprehensive_sample_v2.csv (600 researchers)
Stratified random sample from "top 2%" dataset with perfect field balance.

**Key columns**:
- `sample_id`: Unique identifier
- `authfull`: Researcher name
- `field`: Subfield classification (e.g., "History", "Genetics")
- `field_type`: book_heavy / mixed / journal_heavy
- `rank`: Global rank in original dataset
- `scopus_pubs`, `scopus_citations`, `scopus_h_index`: Metrics from Scopus
- `country`, `institution`: Geographic/institutional information

### openalex_comprehensive_data_v2.csv (570 matched researchers)
Complete coverage analysis with publisher breakdowns.

**Key columns**:
- All columns from `comprehensive_sample_v2.csv`
- `openalex_found`: Boolean (match success)
- `total_works`: Total publications in OpenAlex
- `coverage_ratio`: scopus_pubs / total_works (PRIMARY OUTCOME)
- `elsevier_pct`: % publications in Elsevier journals
- `wiley_pct`, `springer_pct`, `oxford_pct`, `cambridge_pct`: Other publishers
- `books_pct`: % that are books/book chapters
- `oa_publisher_pct`: % in open access publishers (PLOS, Frontiers, MDPI)
- `openalex_citations`, `citation_coverage`: Citation metrics

### university_adoption_data.csv (58 universities)
Evidence of institutional use in public marketing (2022-2024).

**Columns**:
- `university`: Institution name
- `country`: Country code
- `year`: Year of announcement (2022, 2023, or 2024)
- `context`: Usage context (recruitment, research highlights, profiles)
- `url`: Source URL
- `archived_date`: Archive.org capture date

---

## Main Figures

### Figure 1: Scopus Coverage by Field Type
**Script**: `scripts/R/figures_1_2_3_coverage_analysis.R`

Box plots showing dramatic coverage differences:
- Book-heavy: 31.3% median
- Mixed: 36.3% median
- Journal-heavy: 70.7% median
- Statistical test: Kruskal-Wallis H=132.973, p<0.001

### Figure 2: Publisher Bias (Elsevier vs Coverage)
**Script**: `scripts/R/figures_1_2_3_coverage_analysis.R`

Scatterplot with regression showing strong positive correlation:
- r = 0.563, p < 0.001
- High Elsevier (>5.1%): 60.4% coverage
- Low Elsevier (≤5.1%): 32.9% coverage
- Cohen's d = 1.178 (large effect)

### Figure 3: Book Bias (Books vs Coverage)
**Script**: `scripts/R/figures_1_2_3_coverage_analysis.R`

Scatterplot showing negative correlation:
- r = -0.503, p < 0.001
- Persists within book-heavy fields (r=-0.349)

### Figure 4: University Adoption (2022-2024)
**Script**: `scripts/python/figure_4_university_adoption.py`

Geographic distribution and temporal trends:
- 58 universities across 20 countries
- Years: 2022 (20 unis), 2023 (18), 2024 (21)
- Regions: North America, Europe, Asia, Oceania, South America
- Demonstrates persistent adoption despite known bias

---

## Supplementary Figures

### Figure S1: Sample Characteristics
2-panel figure showing:
- (A) Field distribution: 198/210/192 perfect balance
- (B) Geographic distribution: 44 countries, USA (270), UK (82), Germany (41)

### Figure S2: Coverage Distribution
Histograms showing:
- (A) Overall distribution (median 41.7%, most researchers missing >50%)
- (B) Field-specific distributions with clear separation

### Figure S3: Publisher Breakdown by Field
Grouped bar chart comparing Elsevier, Wiley, Springer, Oxford, Cambridge across field types.

### Figure S4: Regression Diagnostics
4-panel diagnostic plot for multivariate model:
- (A) Residuals vs Fitted
- (B) Q-Q Plot
- (C) Scale-Location
- (D) Residuals histogram
Confirms model assumptions valid.

### Figure S5: Open Access Publisher Analysis
Coverage comparison for PLOS, Frontiers, MDPI:
- PLOS: +24.3 pp advantage (p<0.001)
- Frontiers: +19.8 pp (p<0.001)
- Violin plots showing full distributions

### Figure S6: Extreme Undercounting Cases
Profiles of 7 researchers with 300-1,000+ publications showing 3-10% coverage:
- (A) Publication counts (OpenAlex vs Scopus)
- (B) Publisher breakdown showing low Elsevier, high Oxford/Cambridge

---

## Statistical Analysis

### Multivariate Regression
**Model**: coverage_ratio ~ elsevier_pct + books_pct + field_type + log(publications)

**Results** (R² = 0.548):
- Elsevier %: β = +0.0052, p < 0.001
- Books %: β = -0.0016, p = 0.024
- Book-heavy field: β = -0.290, p < 0.001
- Mixed field: β = -0.235, p < 0.001
- log(publications): β = -0.116, p < 0.001

**Interpretation**: Each 10 pp increase in Elsevier publications → +5.2 pp coverage, controlling for all other factors.

---

## Source Data

### Included in This Package
- ✅ `comprehensive_sample_v2.csv` (600 researchers)
- ✅ `openalex_comprehensive_data_v2.csv` (570 matched)
- ✅ `university_adoption_data.csv` (58 institutions)

### Download Separately (only if reproducing from scratch)
1. **"Top 2%" dataset**:
   - URL: https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw
   - File: `Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx`
   - Size: ~89 MB
   - License: CC-BY 4.0

2. **OpenAlex**:
   - Automatically fetched via API (no download needed)
   - URL: https://openalex.org
   - License: CC0 (public domain)

---

## Reproduction From Scratch

### Step 1: Create Sample
```bash
# Requires "top 2%" Excel file in parent directory
python3 scripts/data_collection/create_stratified_sample_v2.py
```
Creates `comprehensive_sample_v2.csv` with 600 researchers.

### Step 2: Fetch OpenAlex Data
```bash
# WARNING: ~30 minutes, 600 API calls
python3 scripts/data_collection/fetch_openalex_comprehensive_v2.py
```
Creates `openalex_comprehensive_data_v2.csv` with coverage ratios.

### Step 3: Generate Figures
```bash
# From project root
python3 generate_all_figures.py
```
Generates all 10 figures (4 main + 6 supplementary) in ~5 seconds.

---

## Expected Results

When you reproduce the analysis, you should obtain:

### Coverage Statistics
| Field Type | n | Median | IQR | Missing >50% |
|------------|---|--------|-----|--------------|
| Book-heavy | 198 | 31.3% | 21.1%-45.8% | 76.3% |
| Mixed | 210 | 36.3% | 25.7%-52.1% | 68.1% |
| Journal-heavy | 192 | 70.7% | 61.2%-82.4% | 14.1% |

### Publisher Bias (Elsevier)
| Metric | Value |
|--------|-------|
| Correlation | r = 0.563, p < 0.001 |
| High Elsevier coverage | 60.4% |
| Low Elsevier coverage | 32.9% |
| Difference | 27.5 pp |
| Effect size | d = 1.178 |

### Book Bias
| Metric | Value |
|--------|-------|
| Correlation | r = -0.503, p < 0.001 |
| Within book-heavy | r = -0.349, p < 0.001 |

### Open Access
| Publisher | With | Without | Difference | p-value |
|-----------|------|---------|------------|---------|
| PLOS | 60.6% | 36.3% | +24.3 pp | <0.001 |
| Frontiers | 56.5% | 36.7% | +19.8 pp | <0.001 |

---

## Troubleshooting

### Figure Generation Issues
**Problem**: R script fails with missing packages
**Solution**:
```bash
Rscript scripts/R/install_r_dependencies.R
```

**Problem**: Python script fails with missing modules
**Solution**:
```bash
pip install pandas scipy statsmodels matplotlib seaborn
```

### Data Access Issues
**Problem**: OpenAlex API rate limits
**Solution**: Scripts include 0.5s delays. If you hit limits, wait 10 minutes.

**Problem**: Different OpenAlex results
**Solution**: OpenAlex adds new publications daily. Results within ±3% are expected.

### Path Issues
All scripts use relative paths from their script location. Run from:
- R scripts: any directory (they auto-detect paths)
- Python scripts: `reproducibility_package/` directory
- Master script: project root

---

## File Formats

All data files are CSV (comma-separated values):
- UTF-8 encoding
- Comma delimiters
- Header row included
- Missing values: empty string or "NA"

All figures are PNG:
- 300 DPI (publication quality)
- RGB color space
- Colorblind-safe palettes (where applicable)

---

## Licenses

### Our Data and Code
- **Data files** (`data/*.csv`): CC-BY 4.0
- **Scripts** (`scripts/*`): MIT License
- Free to use, modify, distribute with attribution

### Source Data
- **"Top 2%" dataset**: CC-BY 4.0 (Ioannidis et al.)
- **OpenAlex**: CC0 (public domain)

---

## Citation

If you use this reproducibility package, please cite:

Lipo, Carl, Robert DiNapoli, and Ben Andrus. (2025). Publisher Bias in Widely-Used Scientist Rankings. [**Journal], [Volume], [Pages]**.

And cite the source data:

Ioannidis JPA, Boyack KW, Baas J. (2024). Updated science-wide author databases of standardized citation indicators. Elsevier Data Repository. https://doi.org/10.17632/btchxktzyw

Priem J, Piwowar H, Orr R. (2022). OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts. arXiv:2205.01833.

---

## Supplementary Materials

For extended methods, additional analyses, supplementary tables, and data availability statements, see:

**[SUPPLEMENTARY_MATERIALS.md](SUPPLEMENTARY_MATERIALS.md)**

Includes:
- Detailed sampling methodology
- Publisher classification procedures
- Complete statistical analysis protocols
- Quality control procedures
- Supplementary results
- Supplementary tables
- Data and code availability

---

## Version History

**Version 2.0** (November 2025)
- Expanded sample: n=600 (from n=397)
- Perfect field stratification: 198/210/192
- 95% match rate (570/600)
- **NEW**: Extreme undercounting cases (7 researchers, 300-1,000+ pubs, 3-10% coverage)
- **NEW**: Supplementary materials with 6 additional figures
- **NEW**: University adoption analysis (58 universities, 20 countries)
- Updated regression model (R²=0.548)
- Reorganized directory structure (scripts/R/, scripts/python/)

**Version 1.0** (November 2025)
- Initial release
- Sample: n=361 matched researchers
- Four hypothesis tests
- Three main figures

---

## Contact

Questions about reproducibility? Issues with code? Contact Carl Lipo, clipo@binghamton.edu.

Expected small variations in results due to:
- OpenAlex data updates (new publications indexed daily)
- Match rates (±2% variation normal)
- Coverage ratios (±3% variation acceptable)

If results differ substantially, please report.

---

## Acknowledgments

- **OpenAlex team**: Free, open scholarly data
- **Ioannidis et al.**: Publicly available rankings enabling this validation

---

**Last updated**: January 2025
