#!/usr/bin/env python3
"""
Run all analyses and generate all figures for the reproducibility package.

This script:
1. Verifies package integrity
2. Runs statistical analysis
3. Generates all figures (via R and Python)
4. Creates summary report

Usage:
    python3 run_all_analyses.py
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def run_command(cmd, description, shell=False):
    """Run a command and report success/failure."""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print()

    try:
        if shell:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print("Error output:", e.stderr)
        return False
    except FileNotFoundError as e:
        print(f"✗ Command not found: {e}")
        print(f"   Make sure all dependencies are installed")
        return False

def main():
    """Run all reproducibility analyses."""
    
    start_time = datetime.now()
    
    print("="*80)
    print("REPRODUCIBILITY PACKAGE - COMPLETE ANALYSIS PIPELINE")
    print("="*80)
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Change to package directory
    package_dir = Path(__file__).parent
    os.chdir(package_dir)
    print(f"Working directory: {package_dir}")

    results = {}

    # Step 1: Verify setup
    results['verify'] = run_command(
        [sys.executable, 'verify_setup.py'],
        "Step 1: Verifying package integrity"
    )

    if not results['verify']:
        print("\n⚠️  Package verification failed. Please fix errors before continuing.")
        return 1

    # Step 2: Run statistical analysis
    print("\n" + "="*80)
    print("Step 2: Running statistical analysis")
    print("="*80)

    with open('ANALYSIS_SUMMARY_n600.txt', 'w') as f:
        try:
            result = subprocess.run(
                [sys.executable, 'scripts/python/analyze_coverage_bias.py'],
                check=True,
                capture_output=True,
                text=True
            )
            f.write(result.stdout)
            if result.stderr and 'FutureWarning' not in result.stderr:
                f.write("\n\nWarnings:\n")
                f.write(result.stderr)
            print(result.stdout[-2000:])  # Last 2000 chars
            print(f"\n✓ Analysis saved to: ANALYSIS_SUMMARY_n600.txt")
            results['analysis'] = True
        except subprocess.CalledProcessError as e:
            print(f"✗ Analysis failed: {e}")
            f.write(f"Analysis failed: {e}\n")
            f.write(e.stderr)
            results['analysis'] = False

    # Step 3: Generate Figures 1-3 (R)
    results['figures_1_3'] = run_command(
        ['Rscript', 'scripts/R/figures_1_2_3_coverage_analysis.R'],
        "Step 3: Generating Figures 1-3 (R)"
    )

    # Step 4: Generate Figure 4 (Python)
    results['figure_4'] = run_command(
        [sys.executable, 'scripts/python/figure_4_university_adoption.py'],
        "Step 4: Generating Figure 4 (Python)"
    )

    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "="*80)
    print("REPRODUCIBILITY PIPELINE COMPLETE")
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
        ('ANALYSIS_SUMMARY_n600.txt', 'Statistical analysis report'),
        ('figures/Figure1_Coverage_by_Field.png', 'Figure 1'),
        ('figures/Figure2_Elsevier_vs_Coverage.png', 'Figure 2'),
        ('figures/Figure3_Books_vs_Coverage.png', 'Figure 3'),
        ('figures/Figure4_university_adoption.png', 'Figure 4'),
        ('figures/Table1_Summary.csv', 'Summary table'),
    ]

    for filepath, description in outputs:
        path = Path(filepath)
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✓ {description}: {filepath} ({size_kb:.1f} KB)")
        else:
            print(f"  ✗ {description}: {filepath} (NOT FOUND)")

    print()
    
    all_success = all(results.values())
    if all_success:
        print("🎉 All analyses completed successfully!")
        print()
        print("Next steps:")
        print("  1. Review ANALYSIS_SUMMARY_n600.txt for statistical results")
        print("  2. Check figures/ directory for publication-ready figures")
        print("  3. Compare results to manuscript for consistency")
        return 0
    else:
        print("⚠️  Some analyses failed. Please review error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
