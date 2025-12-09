#!/usr/bin/env python3
"""
Generate All Figures for Reproducibility Package

This script generates all 6 publication-ready figures in one command:
- Figures 1-3: Scopus coverage analysis (via R)
- Figure 4: University adoption visualization (via Python)
- Figures 5-6: OpenAlex ranking replication (via Python)

Usage:
    python3 generate_all_figures.py

Output:
    figures/Figure1_Coverage_by_Field.png
    figures/Figure2_Elsevier_vs_Coverage.png
    figures/Figure3_Books_vs_Coverage.png
    figures/Figure4_university_adoption.png
    figures/Figure5_Scopus_vs_OpenAlex_Rankings.png
    figures/Figure6_Ranking_Changes_Distribution.png
    figures/Table1_Summary.csv

Expected runtime: ~20 seconds
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_script(command, description):
    """Run a script and report success/failure."""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}")
    print(f"Command: {' '.join(command)}")
    print()

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr and 'FutureWarning' not in result.stderr:
            print("Warnings:", result.stderr)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print("Error output:", e.stderr)
        return False
    except FileNotFoundError as e:
        print(f"✗ Command not found: {e}")
        print("   Make sure R and Python are installed")
        return False

def main():
    """Generate all figures."""
    start_time = datetime.now()

    print("="*80)
    print("GENERATE ALL FIGURES - REPRODUCIBILITY PACKAGE")
    print("="*80)
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Ensure we're in the package directory
    package_dir = Path(__file__).parent
    print(f"Working directory: {package_dir}")

    results = {}

    # Generate Figures 1-3 (R)
    results['figures_1_3'] = run_script(
        ['Rscript', 'scripts/R/figures_1_2_3_coverage_analysis.R'],
        "Generating Figures 1-3 (R)"
    )

    # Generate Figure 4 (Python)
    results['figure_4'] = run_script(
        [sys.executable, 'scripts/python/figure_4_university_adoption.py'],
        "Generating Figure 4 (Python)"
    )

    # Generate Figures 5-6 (Python - OpenAlex rankings)
    results['figures_5_6'] = run_script(
        [sys.executable, 'scripts/python/create_manuscript_visualizations.py'],
        "Generating Figures 5-6 (Python)"
    )

    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "="*80)
    print("FIGURE GENERATION COMPLETE")
    print("="*80)
    print(f"Duration: {duration:.1f} seconds")
    print()
    print("Results:")
    for step, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {status}: {step}")

    print()
    print("Output files:")

    # Check for output files
    outputs = [
        ('figures/Figure1_Coverage_by_Field.png', 'Figure 1 - Coverage by Field'),
        ('figures/Figure2_Elsevier_vs_Coverage.png', 'Figure 2 - Elsevier vs Coverage'),
        ('figures/Figure3_Books_vs_Coverage.png', 'Figure 3 - Books vs Coverage'),
        ('figures/Figure4_university_adoption.png', 'Figure 4 - University Adoption'),
        ('figures/Figure5_Scopus_vs_OpenAlex_Rankings.png', 'Figure 5 - Ranking Comparison'),
        ('figures/Figure6_Ranking_Changes_Distribution.png', 'Figure 6 - Ranking Changes'),
        ('figures/Table1_Summary.csv', 'Summary table'),
    ]

    all_files_exist = True
    for filepath, description in outputs:
        path = Path(filepath)
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✓ {description}: {filepath} ({size_kb:.1f} KB)")
        else:
            print(f"  ✗ {description}: {filepath} (NOT FOUND)")
            all_files_exist = False

    print()

    if all(results.values()) and all_files_exist:
        print("🎉 All figures generated successfully!")
        print()
        print("Next steps:")
        print("  1. Check figures/ directory for publication-ready figures")
        print("  2. Verify figure quality (300 DPI, publication-ready)")
        return 0
    else:
        print("⚠️  Some figures failed to generate. Please review error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
