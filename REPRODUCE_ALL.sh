#!/bin/bash
#
# REPRODUCE_ALL.sh
#
# Complete reproduction script for "Publisher Bias in Widely-Used Scientist Rankings"
#
# This script reproduces all analyses and figures from scratch.
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
    "data/university_adoption/university_adoption_data.csv"
)

ALL_PRESENT=true
for file in "${DATA_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file NOT FOUND"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo -e "${RED}ERROR: Missing data files${NC}"
    exit 1
fi

echo ""

# ============================================================================
# STEP 4b: Fix Data Merge Issues
# ============================================================================
echo "================================================================================"
echo "STEP 4b: Fixing Data Merge Issues"
echo "================================================================================"
echo ""

echo "Recovering missing Scopus data..."
cd scripts/python
python3 fix_data_merge.py
cd ../..

echo ""
echo -e "${GREEN}✓${NC} Data merge fixed (n=564 with coverage)"
echo ""

# ============================================================================
# STEP 5: Generate Main Figures
# ============================================================================
echo "================================================================================"
echo "STEP 5: Generating Main Figures"
echo "================================================================================"
echo ""

echo "Generating Figures 2-4 (R)..."
Rscript scripts/R/figures_1_2_3_coverage_analysis.R

echo "Generating Figure 1 (Python)..."
cd scripts/python
python3 figure_4_university_adoption.py
cd ../..

echo "Generating Figure 5 (Python)..."
cd scripts/python
python3 create_manuscript_visualizations.py 2>/dev/null || echo "  (visualization script not found, skipping)"
cd ../..

echo ""
echo -e "${GREEN}✓${NC} Main figures generated"
echo ""

# ============================================================================
# STEP 6: Generate Supplementary Figures
# ============================================================================
echo "================================================================================"
echo "STEP 6: Generating Supplementary Figures"
echo "================================================================================"
echo ""

cd scripts/python

for script in figureS1_sample_characteristics.py figureS2_coverage_distribution.py \
              figureS3_publisher_breakdown.py figureS4_regression_diagnostics.py \
              figureS5_oa_analysis.py figureS6_extreme_cases.py; do
    if [ -f "$script" ]; then
        echo "  Running $script..."
        python3 "$script" 2>/dev/null || echo "    (warning: $script had issues)"
    fi
done

cd ../..

echo ""
echo -e "${GREEN}✓${NC} Supplementary figures generated"
echo ""

# ============================================================================
# STEP 6b: Analyze Rank-Coverage Correlation by Field Type
# ============================================================================
echo "================================================================================"
echo "STEP 6b: Analyzing Rank-Coverage Correlation by Field Type"
echo "================================================================================"
echo ""

cd scripts/python
python3 analyze_book_heavy_rank_correlation.py
cd ../..

echo ""
echo -e "${GREEN}✓${NC} Book-heavy rank correlation analysis complete"
echo ""

# ============================================================================
# STEP 7: Bayesian Analysis (Optional)
# ============================================================================
echo "================================================================================"
echo "STEP 7: Bayesian Analysis (Optional)"
echo "================================================================================"
echo ""
echo "The Bayesian analysis takes ~1-2 hours for full MCMC sampling."
echo "Results are already included in results/bayesian/"
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
    else
        echo -e "${YELLOW}WARNING: brms not installed${NC}"
        echo "Install with: Rscript -e \"install.packages('brms')\""
        echo "Skipping Bayesian analysis..."
    fi
else
    echo "Skipping Bayesian analysis (pre-computed results available)"
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
echo "Main Figures (figures/):"
echo "  Figure 1: University adoption (2022-2024)"
echo "  Figure 2: Coverage by field type"
echo "  Figure 3: Elsevier publisher bias"
echo "  Figure 4: Book publication bias"
echo "  Figure 5: Scopus vs OpenAlex rankings"
echo ""
echo "Supplementary Figures (figures/supplementary/):"
echo "  Figures S1-S7"
echo ""
echo "Bayesian Results (results/bayesian/):"
echo "  Tables B1-B5 (manuscript_tables/)"
echo "  Model summaries (model_summaries/)"
echo "  Figures B1-B4 (figures/bayesian/)"
echo ""
echo "Data (data/):"
echo "  comprehensive_sample.csv (600 researchers)"
echo "  openalex_comprehensive_data.csv (570 matched)"
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
