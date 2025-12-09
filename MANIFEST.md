# Reproducibility Package Manifest

**Version**: 2.0  
**Date**: November 19, 2024  
**Sample Size**: 600 researchers (570 matched to OpenAlex)

---

## Directory Structure

```
reproducibility_package/
├── data/                      # Research data
│   ├── comprehensive_sample.csv           # 600 researcher sample
│   ├── openalex_comprehensive_data.csv    # Coverage analysis (570 matched)
│   ├── evidence_summary_table.csv         # Statistical evidence
│   └── university_adoption/               # Institutional adoption data
│       ├── university_adoption_data.csv
│       └── university_details.csv
├── scripts/                   # Analysis scripts (organized by language)
│   ├── R/                     # R scripts
│   │   ├── figures_1_2_3_coverage_analysis.R
│   │   └── install_r_dependencies.R
│   ├── python/                # Python scripts
│   │   ├── analyze_coverage_bias.py
│   │   ├── figure_4_university_adoption.py
│   │   ├── figureS1_sample_characteristics.py
│   │   ├── figureS2_coverage_distribution.py
│   │   ├── figureS3_publisher_breakdown.py
│   │   ├── figureS4_regression_diagnostics.py
│   │   ├── figureS5_oa_analysis.py
│   │   └── figureS6_extreme_cases.py
│   └── data_collection/       # Data collection scripts (optional)
│       ├── create_stratified_sample.py
│       └── fetch_openalex_comprehensive.py
├── figures/                   # Generated output (created by scripts)
│   ├── Figure1_Coverage_by_Field.png
│   ├── Figure2_Elsevier_vs_Coverage.png
│   ├── Figure3_Books_vs_Coverage.png
│   ├── Figure4_university_adoption.png
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

**University adoption data** (`data/university_adoption/`):
- [x] `university_adoption_data.csv` - Yearly adoption metrics
- [x] `university_details.csv` - Institution details
- [x] `README.md` - Data documentation

### Analysis Scripts (`scripts/`)

**Master scripts:**
- [x] `generate_all_figures.py` - Generate all 4 figures in one command
  - Runs both R and Python figure generation
  - Output: All 4 figures + summary table
  - Runtime: ~5 seconds

**Python scripts (`scripts/python/`):**
- [x] `analyze_coverage_bias.py` - Main statistical analysis
  - Hypothesis testing (H1-H4)
  - Correlation analysis
  - Effect size calculations
  - Multivariate regression
  - Output: ANALYSIS_SUMMARY_n600.txt
- [x] `figure_4_university_adoption.py` - Figure 4: University adoption
  - University adoption visualization over time
  - Output: figures/Figure4_university_adoption.png

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

**Publication-ready figures:**
- [x] `Figure1_Coverage_by_Field.png` (3000×2100 px, 300 DPI, ~375 KB)
- [x] `Figure2_Elsevier_vs_Coverage.png` (3000×2100 px, 300 DPI, ~475 KB)
- [x] `Figure3_Books_vs_Coverage.png` (3000×2100 px, 300 DPI, ~540 KB)
- [x] `Figure4_university_adoption.png` (3000×2100 px, 300 DPI, ~460 KB)
- [x] `Table1_Summary.csv` - Summary statistics table

**Analysis output:**
- [x] `ANALYSIS_SUMMARY_n600.txt` - Complete statistical analysis report

---

## File Size Summary

| Category | Size |
|----------|------|
| Data files | ~350 KB |
| Code files | ~150 KB |
| Figures | ~1.9 MB |
| Documentation | ~50 KB |
| **Total** | **~2.5 MB** |

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

**Package validated**: November 19, 2024  
**Test environment**: macOS 14.x, Python 3.12, R 4.3  
**Status**: ✅ All components functional
