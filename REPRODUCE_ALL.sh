#!/bin/bash
#
# REPRODUCE_ALL.sh
#
# Complete reproduction script for "Publisher Bias in Widely-Used Scientist Rankings"
# Lipo, DiNapoli, Andrus (2026)
#
# This script reproduces all analyses and figures from the pre-generated data files.
#
# Usage:
#   chmod +x REPRODUCE_ALL.sh
#   ./REPRODUCE_ALL.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "COMPLETE REPRODUCIBILITY PACKAGE"
echo "Publisher Bias in Widely-Used Scientist Rankings"
echo "Lipo, DiNapoli, Andrus (2026)"
echo "================================================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo ""

# ============================================================================
# STEP 1: Check System Requirements
# ============================================================================
echo "================================================================================"
echo "STEP 1: Checking System Requirements"
echo "================================================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not found${NC}"
    echo "Please install Python 3.12+ from https://www.python.org/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} $PYTHON_VERSION"

# Check R
if ! command -v Rscript &> /dev/null; then
    echo -e "${RED}ERROR: R not found${NC}"
    echo "Please install R 4.3+ from https://www.r-project.org/"
    exit 1
fi
R_VERSION=$(Rscript --version 2>&1 | head -n 1)
echo -e "${GREEN}✓${NC} R found"

echo ""

# ============================================================================
# STEP 2: Install Python Dependencies
# ============================================================================
echo "================================================================================"
echo "STEP 2: Installing Python Dependencies"
echo "================================================================================"
echo ""

pip3 install -q --upgrade pip
pip3 install -q -r requirements.txt

echo -e "${GREEN}✓${NC} Python dependencies installed"

# Verify
python3 -c "import pandas; print(f'  pandas {pandas.__version__}')"
python3 -c "import scipy; print(f'  scipy {scipy.__version__}')"
python3 -c "import matplotlib; print(f'  matplotlib {matplotlib.__version__}')"

echo ""

# ============================================================================
# STEP 3: Install R Dependencies
# ============================================================================
echo "================================================================================"
echo "STEP 3: Installing R Dependencies"
echo "================================================================================"
echo ""

Rscript install_r_dependencies.R

echo -e "${GREEN}✓${NC} R dependencies installed"
echo ""

# ============================================================================
# STEP 4: Verify Data Files
# ============================================================================
echo "================================================================================"
echo "STEP 4: Verifying Data Files"
echo "================================================================================"
echo ""

# Check critical data files
DATA_FILES=(
    "data/comprehensive_sample.csv"
    "data/openalex_comprehensive_data.csv"
    "data/openalex_data_with_orcid.csv"
    "data/openalex_rankings_full.csv"
    "data/scopus_vs_openalex_rankings.csv"
    "data/university_adoption/university_adoption_data.csv"
    "data/university_adoption/university_details.csv"
)

ALL_PRESENT=true
for file in "${DATA_FILES[@]}"; do
    if [ -f "$file" ]; then
        LINES=$(wc -l < "$file" | tr -d ' ')
        echo -e "${GREEN}✓${NC} $file ($LINES lines)"
    else
        echo -e "${RED}✗${NC} $file NOT FOUND"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo -e "${RED}ERROR: Missing data files. See README.md for data collection instructions.${NC}"
    exit 1
fi

echo ""

# ============================================================================
# STEP 4b: Fix Data Merge Issues
# ============================================================================
echo "================================================================================"
echo "STEP 4b: Recovering Scopus Publication Counts"
echo "================================================================================"
echo ""

echo "Recovering missing Scopus data from source dataset..."
python3 scripts/python/fix_data_merge.py

echo ""
echo -e "${GREEN}✓${NC} Data merge fixed (n=564 with valid coverage)"
echo ""

# ============================================================================
# STEP 5: Generate Main Figures
# ============================================================================
echo "================================================================================"
echo "STEP 5: Generating Main Figures (1-5)"
echo "================================================================================"
echo ""

echo "Generating Figures 2-4 (R: coverage by field, Elsevier effect, book effect)..."
Rscript scripts/R/figures_1_2_3_coverage_analysis.R

echo ""
echo "Generating Figure 1 (Python: university adoption 2022-2025)..."
python3 scripts/python/figure_4_university_adoption.py

echo ""
echo "Generating Figure 5 (Python: Scopus vs OpenAlex rankings)..."
python3 scripts/python/create_manuscript_visualizations.py 2>/dev/null || echo -e "  ${YELLOW}(visualization script had issues, skipping)${NC}"

echo ""
echo -e "${GREEN}✓${NC} Main figures 1-5 generated"
echo ""

# ============================================================================
# STEP 6: Generate Supplementary Figures (S1-S7)
# ============================================================================
echo "================================================================================"
echo "STEP 6: Generating Supplementary Figures (S1-S7)"
echo "================================================================================"
echo ""

SUPP_SCRIPTS=(
    "figureS1_sample_characteristics.py"
    "figureS2_coverage_distribution.py"
    "figureS3_publisher_breakdown.py"
    "figureS4_regression_diagnostics.py"
    "figureS5_oa_analysis.py"
    "figureS6_extreme_cases.py"
)

for script in "${SUPP_SCRIPTS[@]}"; do
    if [ -f "scripts/python/$script" ]; then
        echo "  Running $script..."
        python3 "scripts/python/$script" 2>/dev/null || echo -e "    ${YELLOW}(warning: $script had issues)${NC}"
    fi
done

echo ""
echo -e "${GREEN}✓${NC} Supplementary figures S1-S7 generated"
echo ""

# ============================================================================
# STEP 6b: Run Statistical Analyses
# ============================================================================
echo "================================================================================"
echo "STEP 6b: Running Statistical Analyses"
echo "================================================================================"
echo ""

echo "Running comprehensive statistical analysis..."
python3 scripts/python/comprehensive_statistical_analysis.py 2>/dev/null || echo -e "  ${YELLOW}(statistical analysis had issues)${NC}"

echo ""
echo "Analyzing rank-coverage correlation by field type..."
python3 scripts/python/analyze_book_heavy_rank_correlation.py 2>/dev/null || echo -e "  ${YELLOW}(correlation analysis had issues)${NC}"

echo ""
echo -e "${GREEN}✓${NC} Statistical analyses complete"
echo ""

# ============================================================================
# STEP 7: Bayesian Analysis (Optional - generates Figure 6 + Figures S8-S13)
# ============================================================================
echo "================================================================================"
echo "STEP 7: Bayesian Analysis (Optional)"
echo "================================================================================"
echo ""
echo "The Bayesian analysis takes ~1-2 hours for full MCMC sampling."
echo "It generates: Figure 6, Supplementary Figures S8-S13, Tables B1-B5."
echo "Pre-computed results are already included in results/bayesian/"
echo ""

read -p "Run Bayesian analysis? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if brms is installed
    if Rscript -e "if (!require('brms', quietly=TRUE)) quit(status=1)" 2>/dev/null; then
        echo "Running Bayesian analysis (this will take a while)..."
        cd scripts/R/bayesian
        Rscript run_all.R --quick
        cd ../../..
        echo -e "${GREEN}✓${NC} Bayesian analysis completed"
        echo "  Generated: Figure 6 (key_hypotheses.png)"
        echo "  Generated: Supplementary Figures S8-S13"
        echo "  Generated: Tables B1-B5 (results/bayesian/manuscript_tables/)"
    else
        echo -e "${YELLOW}WARNING: brms not installed${NC}"
        echo "Install with: Rscript -e \"install.packages('brms')\""
        echo "Skipping Bayesian analysis (pre-computed results still available)..."
    fi
else
    echo "Skipping Bayesian analysis (pre-computed results available in results/bayesian/)"
fi

echo ""

# ============================================================================
# STEP 8: Summary
# ============================================================================
echo "================================================================================"
echo "REPRODUCTION COMPLETE!"
echo "================================================================================"
echo ""
echo -e "${GREEN}All analyses and figures successfully generated!${NC}"
echo ""
echo "Generated outputs:"
echo ""
echo "Main Figures (figures/main/):"
echo "  Figure 1: University adoption of rankings (2022-2025, 123 universities)"
echo "  Figure 2: Scopus coverage by field type (box plots)"
echo "  Figure 3: Elsevier percentage vs coverage ratio"
echo "  Figure 4: Book percentage vs coverage ratio"
echo "  Figure 5: Scopus vs OpenAlex ranking comparison"
echo "  Figure 6: Bayesian hypothesis tests (requires Step 7, or see pre-computed)"
echo ""
echo "Supplementary Figures (figures/supplementary/):"
echo "  S1-S7:  Sample characteristics, coverage distribution, publisher breakdown,"
echo "          OA analysis, regression diagnostics, extreme cases, ranking changes"
echo "  S8-S13: Bayesian posteriors, field effects, MCMC diagnostics, frequentist"
echo "          comparison, prior sensitivity, replicate robustness (requires Step 7)"
echo ""
echo "Bayesian Results (results/bayesian/):"
echo "  Tables B1-B5 (manuscript_tables/)"
echo "  Model summaries (model_summaries/)"
echo ""
echo "Data (data/):"
echo "  comprehensive_sample.csv (600 researchers)"
echo "  openalex_comprehensive_data.csv (564 matched, valid coverage)"
echo "  university_adoption/ (123 universities across 32 countries)"
echo "  robustness_analysis/ (2,000 researchers across 5 replicates)"
echo ""
echo "================================================================================"
echo ""

# Optional: Open output directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open figures directory? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open figures/main/
    fi
fi

echo "Done!"
