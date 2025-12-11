#!/bin/bash
#
# Rename figures to match manuscript numbering
#
# Manuscript order:
# - Figure 1: University adoption (currently Figure4)
# - Figure 2: Coverage by field (currently Figure1)
# - Figure 3: Elsevier vs Coverage (currently Figure2)
# - Figure 4: Books vs Coverage (currently Figure3)
# - Figure 5: Scopus vs OpenAlex (currently Figure5) - correct
# - Figure S1: Ranking changes distribution (currently Figure6)
# - Figures S2-S7: Currently S1-S6
#

set -e

cd figures/

echo "Renaming figures to match manuscript..."
echo ""

# Create temporary directory to avoid conflicts
mkdir -p .tmp_rename

# Step 1: Move all figures to temp directory with new names
echo "Step 1: Preparing renamed files..."

# Figure 1: University adoption (old Figure4)
if [ -f "Figure4_university_adoption.png" ]; then
    cp "Figure4_university_adoption.png" ".tmp_rename/Figure1_University_Adoption.png"
    echo "  ✓ Figure4_university_adoption.png → Figure1_University_Adoption.png"
fi
if [ -f "Figure4_university_adoption.pdf" ]; then
    cp "Figure4_university_adoption.pdf" ".tmp_rename/Figure1_University_Adoption.pdf"
fi

# Figure 2: Coverage by field (old Figure1)
if [ -f "Figure1_Coverage_by_Field.png" ]; then
    cp "Figure1_Coverage_by_Field.png" ".tmp_rename/Figure2_Coverage_by_Field.png"
    echo "  ✓ Figure1_Coverage_by_Field.png → Figure2_Coverage_by_Field.png"
fi
if [ -f "Figure1_Coverage_by_Field.pdf" ]; then
    cp "Figure1_Coverage_by_Field.pdf" ".tmp_rename/Figure2_Coverage_by_Field.pdf"
fi

# Figure 3: Elsevier vs Coverage (old Figure2)
if [ -f "Figure2_Elsevier_vs_Coverage.png" ]; then
    cp "Figure2_Elsevier_vs_Coverage.png" ".tmp_rename/Figure3_Elsevier_vs_Coverage.png"
    echo "  ✓ Figure2_Elsevier_vs_Coverage.png → Figure3_Elsevier_vs_Coverage.png"
fi
if [ -f "Figure2_Elsevier_vs_Coverage.pdf" ]; then
    cp "Figure2_Elsevier_vs_Coverage.pdf" ".tmp_rename/Figure3_Elsevier_vs_Coverage.pdf"
fi

# Figure 4: Books vs Coverage (old Figure3)
if [ -f "Figure3_Books_vs_Coverage.png" ]; then
    cp "Figure3_Books_vs_Coverage.png" ".tmp_rename/Figure4_Books_vs_Coverage.png"
    echo "  ✓ Figure3_Books_vs_Coverage.png → Figure4_Books_vs_Coverage.png"
fi
if [ -f "Figure3_Books_vs_Coverage.pdf" ]; then
    cp "Figure3_Books_vs_Coverage.pdf" ".tmp_rename/Figure4_Books_vs_Coverage.pdf"
fi

# Figure 5: Scopus vs OpenAlex (already correct)
if [ -f "Figure5_Scopus_vs_OpenAlex_Rankings.png" ]; then
    cp "Figure5_Scopus_vs_OpenAlex_Rankings.png" ".tmp_rename/Figure5_Scopus_vs_OpenAlex_Rankings.png"
    echo "  ✓ Figure5_Scopus_vs_OpenAlex_Rankings.png (unchanged)"
fi
if [ -f "Figure5_Scopus_vs_OpenAlex_Rankings.pdf" ]; then
    cp "Figure5_Scopus_vs_OpenAlex_Rankings.pdf" ".tmp_rename/Figure5_Scopus_vs_OpenAlex_Rankings.pdf"
fi

# Figure S1: Ranking changes (old Figure6)
if [ -f "Figure6_Ranking_Changes_Distribution.png" ]; then
    cp "Figure6_Ranking_Changes_Distribution.png" ".tmp_rename/FigureS1_Ranking_Changes_Distribution.png"
    echo "  ✓ Figure6_Ranking_Changes_Distribution.png → FigureS1_Ranking_Changes_Distribution.png"
fi
if [ -f "Figure6_Ranking_Changes_Distribution.pdf" ]; then
    cp "Figure6_Ranking_Changes_Distribution.pdf" ".tmp_rename/FigureS1_Ranking_Changes_Distribution.pdf"
fi

# Figure S2: Sample characteristics (old S1)
if [ -f "FigureS1_sample_characteristics.png" ]; then
    cp "FigureS1_sample_characteristics.png" ".tmp_rename/FigureS2_Sample_Characteristics.png"
    echo "  ✓ FigureS1_sample_characteristics.png → FigureS2_Sample_Characteristics.png"
fi

# Figure S3: Coverage distribution (old S2)
if [ -f "FigureS2_coverage_distribution.png" ]; then
    cp "FigureS2_coverage_distribution.png" ".tmp_rename/FigureS3_Coverage_Distribution.png"
    echo "  ✓ FigureS2_coverage_distribution.png → FigureS3_Coverage_Distribution.png"
fi

# Figure S4: Publisher breakdown (old S3)
if [ -f "FigureS3_publisher_breakdown.png" ]; then
    cp "FigureS3_publisher_breakdown.png" ".tmp_rename/FigureS4_Publisher_Breakdown.png"
    echo "  ✓ FigureS3_publisher_breakdown.png → FigureS4_Publisher_Breakdown.png"
fi

# Figure S5: Regression diagnostics (old S4)
if [ -f "FigureS4_regression_diagnostics.png" ]; then
    cp "FigureS4_regression_diagnostics.png" ".tmp_rename/FigureS5_Regression_Diagnostics.png"
    echo "  ✓ FigureS4_regression_diagnostics.png → FigureS5_Regression_Diagnostics.png"
fi

# Figure S6: OA analysis (old S5)
if [ -f "FigureS5_oa_analysis.png" ]; then
    cp "FigureS5_oa_analysis.png" ".tmp_rename/FigureS6_OA_Analysis.png"
    echo "  ✓ FigureS5_oa_analysis.png → FigureS6_OA_Analysis.png"
fi

# Figure S7: Extreme cases (old S6)
if [ -f "FigureS6_extreme_cases.png" ]; then
    cp "FigureS6_extreme_cases.png" ".tmp_rename/FigureS7_Extreme_Cases.png"
    echo "  ✓ FigureS6_extreme_cases.png → FigureS7_Extreme_Cases.png"
fi

echo ""
echo "Step 2: Moving renamed files back..."

# Step 2: Move all renamed files back
mv .tmp_rename/* .
rmdir .tmp_rename

echo "  ✓ All figures renamed successfully"
echo ""

# Step 3: Create backup of old files
echo "Step 3: Creating backup of old filenames..."
mkdir -p ../figures_old_names
cp Figure4_university_adoption.* ../figures_old_names/ 2>/dev/null || true
cp Figure1_Coverage_by_Field.* ../figures_old_names/ 2>/dev/null || true
cp Figure2_Elsevier_vs_Coverage.* ../figures_old_names/ 2>/dev/null || true
cp Figure3_Books_vs_Coverage.* ../figures_old_names/ 2>/dev/null || true
cp Figure6_Ranking_Changes_Distribution.* ../figures_old_names/ 2>/dev/null || true
cp FigureS*.* ../figures_old_names/ 2>/dev/null || true

echo "  ✓ Old files backed up to ../figures_old_names/"
echo ""

echo "================================================================================
"
echo "COMPLETE!"
echo "================================================================================
"
echo ""
echo "Figure renaming complete. Current figures:"
ls -1 Figure*.png FigureS*.png 2>/dev/null | sort
echo ""
echo "Old filenames backed up to: ../figures_old_names/"
echo ""
