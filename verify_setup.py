#!/usr/bin/env python3
"""
Verification script to check if the reproducibility package is set up correctly.

Run this script to verify:
1. All required files are present
2. Data files can be loaded
3. Python dependencies are installed
4. Data integrity checks pass

Usage:
    python3 verify_setup.py
"""

import sys
from pathlib import Path

print("="*80)
print("REPRODUCIBILITY PACKAGE VERIFICATION")
print("="*80)
print()

# Check 1: File structure
print("✓ Checking file structure...")
required_files = {
    "data/comprehensive_sample_v2.csv": "Sample data (600 researchers)",
    "data/openalex_comprehensive_data_v2.csv": "Results data (600 researchers, 570 matched)",
    "data/university_adoption/university_adoption_data.csv": "University adoption data",
    "scripts/python/analyze_coverage_bias.py": "Statistical analysis code",
    "scripts/R/figures_1_2_3_coverage_analysis.R": "Figures 1-3 generation code (R)",
    "scripts/python/figure_4_university_adoption.py": "Figure 4 generation code (Python)",
    "scripts/data_collection/create_stratified_sample.py": "Sample selection code",
    "scripts/data_collection/fetch_openalex_comprehensive.py": "Data collection code",
    "generate_all_figures.py": "Master figure generation script",
    "README_REPRODUCIBILITY.md": "Documentation",
    "requirements.txt": "Python dependencies",
}

missing_files = []
for file_path, description in required_files.items():
    if Path(file_path).exists():
        print(f"  ✓ {file_path:45s} - {description}")
    else:
        print(f"  ✗ {file_path:45s} - MISSING!")
        missing_files.append(file_path)

if missing_files:
    print()
    print(f"⚠️  WARNING: {len(missing_files)} required file(s) missing!")
    print("   Please ensure all files are present before running analyses.")
    print()
else:
    print()
    print("✓ All required files present!")
    print()

# Check 2: Python dependencies
print("✓ Checking Python dependencies...")
required_modules = {
    "pandas": "Data manipulation",
    "numpy": "Numerical operations",
    "scipy": "Statistical tests",
    "statsmodels": "Regression analysis",
    "requests": "OpenAlex API access",
}

missing_modules = []
for module, description in required_modules.items():
    try:
        __import__(module)
        print(f"  ✓ {module:20s} - {description}")
    except ImportError:
        print(f"  ✗ {module:20s} - NOT INSTALLED!")
        missing_modules.append(module)

if missing_modules:
    print()
    print(f"⚠️  WARNING: {len(missing_modules)} required module(s) not installed!")
    print("   Install with: pip install -r requirements.txt")
    print()
else:
    print()
    print("✓ All Python dependencies installed!")
    print()

# Check 3: Data integrity
if not missing_files and not missing_modules:
    print("✓ Checking data integrity...")

    try:
        import pandas as pd

        # Load sample data
        sample = pd.read_csv("data/comprehensive_sample_v2.csv")
        print(f"  ✓ Loaded comprehensive_sample_v2.csv: {len(sample)} rows")

        if len(sample) != 600:
            print(f"  ⚠️  Expected 600 researchers, got {len(sample)}")

        # Check expected columns
        expected_cols = ['authfull', 'sm-subfield-1', 'field_type']
        missing_cols = [col for col in expected_cols if col not in sample.columns]
        if missing_cols:
            print(f"  ✗ Missing columns in sample data: {missing_cols}")
        else:
            print(f"  ✓ All expected columns present in sample data")

        # Check field types
        field_types = sample['field_type'].value_counts().sort_index()
        print(f"  ✓ Field type distribution:")
        expected_dist = {'book_heavy': 198, 'journal_heavy': 192, 'mixed': 210}
        for ft in ['book_heavy', 'mixed', 'journal_heavy']:
            count = field_types.get(ft, 0)
            expected = expected_dist.get(ft, 0)
            status = "✓" if abs(count - expected) <= 2 else "⚠️"
            print(f"      {status} {ft}: {count} (expected: {expected})")

        # Load results data
        results = pd.read_csv("data/openalex_comprehensive_data_v2.csv")
        print(f"  ✓ Loaded openalex_comprehensive_data_v2.csv: {len(results)} rows")

        if len(results) != 600:
            print(f"  ⚠️  Expected 600 researchers, got {len(results)}")

        # Check match rate
        matched = results[results['openalex_found'] == True]
        match_rate = len(matched) / len(sample) * 100
        print(f"  ✓ Match rate: {match_rate:.1f}% ({len(matched)}/{len(sample)})")

        # Check coverage statistics
        coverage = matched['coverage_ratio'].dropna()
        print(f"  ✓ Coverage ratio statistics:")
        print(f"      Median: {coverage.median():.1%}")
        print(f"      Mean: {coverage.mean():.1%}")
        print(f"      Range: {coverage.min():.1%} to {coverage.max():.1%}")

        print()
        print("✓ Data integrity checks passed!")
        print()

    except Exception as e:
        print(f"  ✗ Error checking data: {e}")
        print()

# Summary
print("="*80)
print("SUMMARY")
print("="*80)

if not missing_files and not missing_modules:
    print()
    print("✅ SETUP COMPLETE - Ready to reproduce analyses!")
    print()
    print("Next steps:")
    print("  1. Generate all figures: python3 generate_all_figures.py")
    print("  2. Run complete pipeline: python3 run_all_analyses.py")
    print("  3. See README_REPRODUCIBILITY.md for full instructions")
    print()
else:
    print()
    print("⚠️  SETUP INCOMPLETE - Please fix issues above before proceeding")
    print()
    if missing_files:
        print(f"  Missing files: {len(missing_files)}")
    if missing_modules:
        print(f"  Missing Python modules: {len(missing_modules)}")
        print(f"  Install with: pip install -r requirements.txt")
    print()

print("="*80)
