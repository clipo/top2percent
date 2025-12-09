# Reproducibility Package Manifest

**Version**: 3.0
**Date**: December 8, 2025
**Sample Size**: 600 researchers (570 matched to OpenAlex, 362 ORCID-verified)

---

## Directory Structure

```
reproducibility_package/
├── data/                      # Research data
│   ├── comprehensive_sample.csv           # 600 researcher sample
│   ├── openalex_comprehensive_data.csv    # Coverage analysis (570 matched)
│   ├── openalex_data_with_orcid.csv       # ORCID-verified subset (362 researchers)
│   ├── openalex_rankings_full.csv         # OpenAlex ranking replication (537 researchers)
│   ├── openalex_top_2_percent.csv         # Top 10 by OpenAlex composite score
│   ├── scopus_vs_openalex_rankings.csv    # Ranking comparison (ρ=0.567)
│   ├── ranking_coverage_correlation_results.csv # Rank-coverage analysis
│   ├── evidence_summary_table.csv         # Statistical evidence
│   ├── award_winners_case_studies.csv     # Nobel/Pulitzer winner case studies
│   ├── citation_quality_stratified.csv    # Citation impact tertile analysis
│   ├── citation_quality_relative.csv      # Relative quality analysis
│   ├── citation_quality_regression.csv    # Regression with citation controls
│   ├── comprehensive_statistics.csv       # Bonferroni corrections
│   ├── effect_sizes_comparison.csv        # Cliff's delta vs Cohen's d
│   └── university_adoption/               # Institutional adoption data
│       ├── university_adoption_data.csv
│       └── university_details.csv
├── scripts/                   # Analysis scripts (organized by language)
│   ├── R/                     # R scripts
│   │   ├── figures_1_2_3_coverage_analysis.R
│   │   └── install_r_dependencies.R
│   ├── python/                # Python scripts
│   │   ├── figure_4_university_adoption.py
│   │   ├── create_manuscript_visualizations.py # Figures 5-6 (OpenAlex)
│   │   ├── fetch_all_550_researchers.py        # Fetch OpenAlex data
│   │   ├── create_openalex_top2percent.py      # Calculate OpenAlex rankings
│   │   ├── extract_orcid_validation.py         # ORCID verification analysis
│   │   ├── test_ranking_coverage_correlation.py # Ranking-coverage gradient
│   │   ├── award_winners_case_studies.py       # Nobel/Pulitzer case studies
│   │   ├── citation_quality_analysis.py        # Journal impact controls
│   │   ├── comprehensive_statistical_analysis.py # Effect sizes & corrections
│   │   ├── figureS1_sample_characteristics.py
│   │   ├── figureS2_coverage_distribution.py
│   │   ├── figureS3_publisher_breakdown.py
│   │   ├── figureS4_regression_diagnostics.py
│   │   ├── figureS5_oa_analysis.py
│   │   └── figureS6_extreme_cases.py
│   └── data_collection/       # Data collection scripts (optional)
│       ├── create_stratified_sample.py
│       └── fetch_openalex_comprehensive.py
├── figures/                   # Generated output (PNG + PDF formats)
│   ├── Figure1_Coverage_by_Field.png/.pdf
│   ├── Figure2_Elsevier_vs_Coverage.png/.pdf
│   ├── Figure3_Books_vs_Coverage.png/.pdf
│   ├── Figure4_university_adoption.png/.pdf
│   ├── Figure5_Scopus_vs_OpenAlex_Rankings.png/.pdf
│   ├── Figure6_Ranking_Changes_Distribution.png/.pdf
│   ├── FigureS1_sample_characteristics.png
│   ├── FigureS2_coverage_distribution.png
│   ├── FigureS3_publisher_breakdown.png
│   ├── FigureS4_regression_diagnostics.png
│   ├── FigureS5_oa_analysis.png
│   ├── FigureS6_extreme_cases.png
│   └── Table1_Summary.csv
├── generate_all_figures.py    # Master script: generate all figures
├── run_all_analyses.py        # Master script: complete pipeline
├── verify_setup.py            # Verification script
├── install_r_dependencies.R   # R package installer
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── SUPPLEMENTARY_MATERIALS.md # Detailed supplementary information
├── CODE_DOCUMENTATION.md      # Technical documentation
├── MANIFEST.md                # This file
├── ANALYSIS_SUMMARY.txt       # Statistical results summary
├── analysis_results.json      # Machine-readable results
├── LICENSE.txt                # License information
└── CITATION.txt               # Citation information
```

---

## Package Contents Checklist

### Documentation Files
- [x] `README.md` - Main documentation (comprehensive guide)
- [x] `SUPPLEMENTARY_MATERIALS.md` - Detailed supplementary information
- [x] `CODE_DOCUMENTATION.md` - Technical code documentation
- [x] `MANIFEST.md` - This file (package contents)
- [x] `LICENSE.txt` - License information
- [x] `CITATION.txt` - Citation information
- [x] `requirements.txt` - Python dependencies
- [x] `install_r_dependencies.R` - R package installer

### Setup & Verification Scripts
- [x] `verify_setup.py` - Package integrity verification script
- [x] `run_all_analyses.py` - Master script to run complete pipeline

### Data Files (`data/`)

**Primary analysis data:**
- [x] `openalex_comprehensive_data.csv` (600 researchers, 570 matched)
  - Size: ~276 KB
  - Rows: 600
  - Columns: 35+ (coverage metrics, publisher data, field info)

**Sample metadata:**
- [x] `comprehensive_sample.csv` (600 researchers with Scopus rankings)
  - Size: ~74 KB
  - Contains: names, fields, rankings, institutions, countries

**Evidence summary:**
- [x] `evidence_summary_table.csv` - Statistical evidence summary table

**ORCID verification data** (NEW):
- [x] `openalex_data_with_orcid.csv` (362 ORCID-verified researchers)
  - Size: ~185 KB
  - High-confidence subset for validation

**OpenAlex ranking replication** (NEW):
- [x] `openalex_rankings_full.csv` (537 researchers with complete data)
  - Rankings using complete OpenAlex publication data
  - Same composite score formula as Ioannidis et al.
- [x] `openalex_top_2_percent.csv` - Top 10 by OpenAlex ranking
- [x] `scopus_vs_openalex_rankings.csv` - Side-by-side comparison (ρ=0.567)
- [x] `ranking_coverage_correlation_results.csv` - Rank-coverage gradient analysis

**Citation quality controls** (NEW):
- [x] `citation_quality_stratified.csv` - Analysis by citation impact tertiles
- [x] `citation_quality_relative.csv` - Relative journal quality comparison
- [x] `citation_quality_regression.csv` - Regression model with quality controls

**Award winners case studies** (NEW):
- [x] `award_winners_case_studies.csv` - Nobel/Pulitzer winners likely excluded

**Comprehensive statistics** (NEW):
- [x] `comprehensive_statistics.csv` - Bonferroni corrections
- [x] `effect_sizes_comparison.csv` - Cliff's delta vs Cohen's d

**University adoption data** (`data/university_adoption/`):
- [x] `university_adoption_data.csv` - Yearly adoption metrics
- [x] `university_details.csv` - Institution details
- [x] `README.md` - Data documentation

### Analysis Scripts (`scripts/`)

**Master scripts:**
- [x] `generate_all_figures.py` - Generate all 6 main figures in one command
  - Runs both R and Python figure generation
  - Output: All 6 figures (PNG + PDF) + summary table
  - Runtime: ~10 seconds

**Python scripts (`scripts/python/`):**
- [x] `figure_4_university_adoption.py` - Figure 4: University adoption
  - University adoption visualization over time
  - Output: figures/Figure4_university_adoption.png/.pdf
- [x] `create_manuscript_visualizations.py` - Figures 5-6: OpenAlex rankings
  - Figure 5: Scopus vs OpenAlex ranking comparison
  - Figure 6: Ranking changes distribution
  - Output: figures/Figure5_*.png/.pdf, Figure6_*.png/.pdf
- [x] `fetch_all_550_researchers.py` - Fetch OpenAlex metrics for 537 researchers
  - Retrieves complete publication data from OpenAlex API
  - Output: researcher_metrics_all_550.csv
- [x] `create_openalex_top2percent.py` - Calculate OpenAlex-based rankings
  - Replicates Ioannidis composite score formula
  - Output: openalex_rankings_full.csv, openalex_top_2_percent.csv
- [x] `extract_orcid_validation.py` - ORCID verification analysis
  - Identifies high-confidence matches using ORCID
  - Tests bias persistence in verified subset
  - Output: openalex_data_with_orcid.csv
- [x] `test_ranking_coverage_correlation.py` - Ranking-coverage gradient analysis
  - Tests correlation between rank position and coverage
  - Output: ranking_coverage_correlation_results.csv
- [x] `award_winners_case_studies.py` - Nobel/Pulitzer winner case studies
  - Identifies high-profile researchers likely excluded
  - Output: award_winners_case_studies.csv
- [x] `citation_quality_analysis.py` - Journal citation impact controls
  - Stratified analysis by citation tertiles
  - Relative quality comparison
  - Regression with quality controls
  - Output: citation_quality_*.csv files
- [x] `comprehensive_statistical_analysis.py` - Effect sizes & corrections
  - Cliff's delta calculations
  - Bonferroni corrections for multiple comparisons
  - Output: comprehensive_statistics.csv, effect_sizes_comparison.csv

**R scripts (`scripts/R/`):**
- [x] `figures_1_2_3_coverage_analysis.R` - Figures 1-3: Coverage analysis
  - Figure 1: Coverage by field type
  - Figure 2: Elsevier % vs coverage
  - Figure 3: Book % vs coverage
  - Output: figures/*.png (300 DPI)

**Data collection scripts (`scripts/data_collection/`):**
- [x] `fetch_openalex_comprehensive.py` - OpenAlex data collection
- [x] `create_stratified_sample.py` - Sample selection methodology

### Output Files (`figures/`)

**Publication-ready figures (PNG + PDF):**
- [x] `Figure1_Coverage_by_Field.png/.pdf` (3000×2100 px, 300 DPI / vector)
- [x] `Figure2_Elsevier_vs_Coverage.png/.pdf` (3000×2100 px, 300 DPI / vector)
- [x] `Figure3_Books_vs_Coverage.png/.pdf` (3000×2100 px, 300 DPI / vector)
- [x] `Figure4_university_adoption.png/.pdf` (3000×2100 px, 300 DPI / vector)
- [x] `Figure5_Scopus_vs_OpenAlex_Rankings.png/.pdf` (2369×1768 px, 300 DPI / vector) (NEW)
- [x] `Figure6_Ranking_Changes_Distribution.png/.pdf` (3563×1470 px, 300 DPI / vector) (NEW)
- [x] `FigureS1-S6_*.png` - Supplementary figures (PNG only)
- [x] `Table1_Summary.csv` - Summary statistics table

**Analysis output:**
- [x] `ANALYSIS_SUMMARY_n600.txt` - Complete statistical analysis report

---

## File Size Summary

| Category | Size |
|----------|------|
| Data files | ~1.2 MB |
| Code files | ~200 KB |
| Figures | ~2.5 MB (PNG + PDF) |
| Documentation | ~80 KB |
| **Total** | **~4 MB** |

---

## Dependencies Summary

**Python packages:**
- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.11.0
- statsmodels >= 0.14.0
- matplotlib >= 3.7.0
- requests >= 2.31.0

**R packages:**
- ggplot2 >= 3.4.0
- dplyr >= 1.1.0
- tidyr >= 1.3.0
- scales >= 1.2.0

---

## Reproduction Checklist

### Initial Setup
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Install R dependencies: `Rscript install_r_dependencies.R`
- [ ] Verify setup: `python3 verify_setup.py`

### Generate All Results
- [ ] Run complete pipeline: `python3 run_all_analyses.py`

OR run components individually:

### Quick Figure Generation
- [ ] Generate all figures: `python3 generate_all_figures.py`
  - Generates all 4 figures in one command (~5 seconds)

### Statistical Analysis
- [ ] Run analysis: `python3 scripts/python/analyze_coverage_bias.py > ANALYSIS_SUMMARY_n600.txt`
- [ ] Verify output: Check ANALYSIS_SUMMARY_n600.txt for key statistics
  - [ ] H1 (Publisher bias): r=0.563, d=1.171
  - [ ] H2 (Book bias): r=-0.505
  - [ ] H3 (OA): r=+0.250
  - [ ] H4 (Field bias): H=131.112, 39.9pp difference

### Figure Generation (Individual)
- [ ] Generate Figures 1-3: `Rscript scripts/R/figures_1_2_3_coverage_analysis.R`
- [ ] Generate Figure 4: `python3 scripts/python/figure_4_university_adoption.py`
- [ ] Verify figures exist in `figures/` directory
- [ ] Check figure quality (300 DPI, publication-ready)

### Validation
- [ ] Compare results to manuscript values
- [ ] Verify figure aesthetics match manuscript
- [ ] Check all correlation coefficients match (±0.002)
- [ ] Verify effect sizes match (±0.01)
- [ ] Confirm p-values are all <0.001 for main effects

---

## Expected Runtime

| Task | Time |
|------|------|
| Package verification | <1 second |
| Generate all figures | ~5 seconds |
| Statistical analysis | ~5 seconds |
| Complete pipeline | ~7 seconds |
| **Individual components:** |
| - Figures 1-3 (R) | ~3 seconds |
| - Figure 4 (Python) | ~2 seconds |

---

## Known Issues & Solutions

**Issue**: Different statistics than manuscript  
**Solution**: OpenAlex data may have been updated. Expected variation: ±3% in coverage ratios. Core findings (correlations, effect sizes) should remain robust within 0.01.

**Issue**: Figures not generated  
**Solution**: Ensure working directory is `reproducibility_package/`. R script creates `figures/` directory automatically.

**Issue**: Missing Python modules  
**Solution**: Run `pip install -r requirements.txt`

**Issue**: Missing R packages  
**Solution**: Run `Rscript install_r_dependencies.R`

---

## Quality Assurance

**Data integrity:**
- [x] 600 researchers total
- [x] 570 matched to OpenAlex (95%)
- [x] Perfect field balance: 198/210/192 (33%/35%/32%)
- [x] No duplicate researchers
- [x] All required columns present

**Code quality:**
- [x] All scripts have documentation headers
- [x] Functions have docstrings
- [x] Clear variable names
- [x] Comments explain methodology
- [x] Namespace usage documented

**Reproducibility:**
- [x] Deterministic analyses (no randomness)
- [x] All dependencies specified
- [x] Version requirements documented
- [x] Expected outputs documented
- [x] Verification script included

---

## Support

For questions or issues:
1. Check `README_REPRODUCIBILITY.md` for detailed instructions
2. Run `python3 verify_setup.py` to diagnose issues
3. Ensure all dependencies are installed
4. Check expected runtime and file sizes

---

**Package validated**: December 8, 2025
**Test environment**: macOS 14.x (Darwin 25.2.0), Python 3.12, R 4.4
**Status**: ✅ All components functional (6 main figures + 6 supplementary + 10 new analyses)
