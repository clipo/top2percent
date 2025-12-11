#!/bin/bash
#
# REPRODUCE_ALL.sh
#
# One-command script to reproduce all analyses and figures from scratch.
# This script:
# 1. Checks for Python and R
# 2. Installs all dependencies
# 3. Verifies package integrity
# 4. Runs all analyses
# 5. Generates all figures
#
# Usage:
#   bash REPRODUCE_ALL.sh
#
# Or make it executable and run directly:
#   chmod +x REPRODUCE_ALL.sh
#   ./REPRODUCE_ALL.sh
#

set -e  # Exit on error

echo "================================================================================"
echo "REPRODUCIBILITY PACKAGE - COMPLETE ONE-STEP REPRODUCTION"
echo "================================================================================"
echo ""
echo "This script will:"
echo "  1. Check system requirements (Python 3.12+, R 4.3+)"
echo "  2. Install all Python dependencies"
echo "  3. Install all R dependencies"
echo "  4. Verify package integrity"
echo "  5. Generate all main figures (1-5)"
echo "  6. Generate all supplementary figures (S1-S7)"
echo "  7. Run statistical analyses"
echo ""
echo "Estimated time: 2-5 minutes"
echo ""
read -p "Press ENTER to continue or Ctrl+C to cancel..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo ""

# ============================================================================
# STEP 1: Check system requirements
# ============================================================================
echo "================================================================================"
echo "STEP 1: Checking System Requirements"
echo "================================================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ ERROR: Python 3 not found"
    echo "  Please install Python 3.12 or later from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python found: $PYTHON_VERSION"

# Check R
if ! command -v Rscript &> /dev/null; then
    echo "✗ ERROR: R not found"
    echo "  Please install R 4.3 or later from https://www.r-project.org/"
    exit 1
fi

R_VERSION=$(Rscript --version 2>&1 | head -n 1)
echo "✓ R found: $R_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠  WARNING: pip3 not found, using python3 -m pip instead"
    PIP_CMD="python3 -m pip"
else
    PIP_CMD="pip3"
    echo "✓ pip3 found"
fi

echo ""

# ============================================================================
# STEP 2: Install Python dependencies
# ============================================================================
echo "================================================================================"
echo "STEP 2: Installing Python Dependencies"
echo "================================================================================"
echo ""

echo "Installing Python packages from requirements.txt..."
$PIP_CMD install -q --upgrade pip
$PIP_CMD install -q -r requirements.txt

echo "✓ Python dependencies installed"
echo ""

# Verify key packages
echo "Verifying installation:"
python3 -c "import pandas; print(f'  ✓ pandas {pandas.__version__}')"
python3 -c "import scipy; print(f'  ✓ scipy {scipy.__version__}')"
python3 -c "import matplotlib; print(f'  ✓ matplotlib {matplotlib.__version__}')"
python3 -c "import seaborn; print(f'  ✓ seaborn {seaborn.__version__}')"
echo ""

# ============================================================================
# STEP 3: Install R dependencies
# ============================================================================
echo "================================================================================"
echo "STEP 3: Installing R Dependencies"
echo "================================================================================"
echo ""

echo "Installing R packages (this may take 1-2 minutes on first run)..."
Rscript install_r_dependencies.R

if [ $? -eq 0 ]; then
    echo "✓ R dependencies installed"
else
    echo "✗ WARNING: R dependency installation had issues"
    echo "  Continuing anyway - some figures may fail"
fi
echo ""

# ============================================================================
# STEP 4: Verify package integrity
# ============================================================================
echo "================================================================================"
echo "STEP 4: Verifying Package Integrity"
echo "================================================================================"
echo ""

python3 verify_setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ ERROR: Package verification failed"
    echo "  Please fix the issues above before continuing"
    exit 1
fi

echo ""

# ============================================================================
# STEP 5: Generate all figures
# ============================================================================
echo "================================================================================"
echo "STEP 5: Generating All Figures"
echo "================================================================================"
echo ""

echo "Generating main figures (1-5) and supplementary figures (S1-S7)..."
echo "This will take about 15-30 seconds..."
echo ""

python3 generate_all_figures.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ All figures generated successfully"
else
    echo ""
    echo "✗ ERROR: Figure generation failed"
    echo "  See error messages above"
    exit 1
fi

echo ""

# ============================================================================
# STEP 6: Summary
# ============================================================================
echo "================================================================================"
echo "REPRODUCTION COMPLETE!"
echo "================================================================================"
echo ""
echo "✅ All analyses and figures successfully generated!"
echo ""
echo "Generated outputs:"
echo ""
echo "Main Figures (figures/):"
echo "  • Figure 1: University adoption"
echo "  • Figure 2: Coverage by field type"
echo "  • Figure 3: Elsevier publisher bias"
echo "  • Figure 4: Book publication bias"
echo "  • Figure 5: Scopus vs OpenAlex rankings"
echo ""
echo "Supplementary Figures (figures/):"
echo "  • Figure S1: Ranking change distribution"
echo "  • Figure S2: Sample characteristics"
echo "  • Figure S3: Coverage distribution"
echo "  • Figure S4: Publisher breakdown"
echo "  • Figure S5: Regression diagnostics"
echo "  • Figure S6: Open access analysis"
echo "  • Figure S7: Extreme undercounting cases"
echo ""
echo "Data files (data/):"
echo "  • comprehensive_sample.csv (600 researchers)"
echo "  • openalex_comprehensive_data.csv (570 matched)"
echo "  • All supplementary analysis files"
echo "  • Robustness analysis replicates (2,000 researchers)"
echo ""
echo "Next steps:"
echo "  1. Check figures/ directory for all generated figures"
echo "  2. Compare results to manuscript for consistency"
echo "  3. See README.md for detailed documentation"
echo ""
echo "Figures are saved in both PNG (300 DPI) and PDF (vector) formats."
echo "All results should match the values reported in the manuscript."
echo ""
echo "================================================================================"
echo ""

# Optional: Open figures directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open figures directory in Finder? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open figures/
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    read -p "Open figures directory? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open figures/ 2>/dev/null || echo "Please check the figures/ directory manually"
    fi
fi

echo "Done!"
echo ""
