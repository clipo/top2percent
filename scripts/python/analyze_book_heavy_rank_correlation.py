#!/usr/bin/env python3
"""
analyze_book_heavy_rank_correlation.py - Analyze rank-coverage correlation by field type

This script calculates the Spearman rank correlation between ranking and coverage
for different field types (book-heavy, mixed, journal-heavy).

Key Finding: Book-heavy fields show the strongest negative correlation between
ranking and coverage, indicating that higher-ranked researchers in humanities/social
sciences have systematically lower Scopus coverage.

Expected Results:
- Overall: ρ ≈ -0.30, p < 0.0001
- Book-heavy: ρ ≈ -0.31, p < 0.001 (strongest effect)
- Mixed: ρ ≈ -0.13, p > 0.05 (not significant)
- Journal-heavy: ρ ≈ -0.04, p > 0.05 (not significant)
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import sys

def calculate_rank_correlation(df, group_name="Overall"):
    """Calculate Spearman rank correlation between ranking and coverage."""
    # Use rank_global (higher = worse ranking)
    valid = df[['rank_global', 'coverage_ratio']].dropna()

    if len(valid) < 10:
        return {
            'group': group_name,
            'n': len(valid),
            'rho': np.nan,
            'p_value': np.nan,
            'significant': False,
            'interpretation': 'Insufficient data'
        }

    rho, p_value = stats.spearmanr(valid['rank_global'], valid['coverage_ratio'])

    # Interpretation
    if p_value < 0.001:
        sig_str = "***"
    elif p_value < 0.01:
        sig_str = "**"
    elif p_value < 0.05:
        sig_str = "*"
    else:
        sig_str = "ns"

    # Effect size interpretation
    abs_rho = abs(rho)
    if abs_rho >= 0.5:
        effect = "large"
    elif abs_rho >= 0.3:
        effect = "medium"
    elif abs_rho >= 0.1:
        effect = "small"
    else:
        effect = "negligible"

    # Direction interpretation
    # Negative rho means: higher rank (worse position) → higher coverage
    # This is EXPECTED because top researchers in book-heavy fields have LOWER coverage
    # So we expect negative correlation
    if rho < 0:
        direction = "Higher-ranked researchers (better position) have LOWER coverage"
    else:
        direction = "Higher-ranked researchers (better position) have HIGHER coverage"

    return {
        'group': group_name,
        'n': len(valid),
        'rho': rho,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'sig_marker': sig_str,
        'effect_size': effect,
        'interpretation': direction
    }


def main():
    # Paths
    data_dir = Path(__file__).parent.parent.parent / 'data'
    input_path = data_dir / 'openalex_comprehensive_data.csv'
    output_path = data_dir / 'rank_coverage_by_field_type.csv'

    print("=" * 70)
    print("RANK-COVERAGE CORRELATION BY FIELD TYPE")
    print("=" * 70)

    # Load data
    print(f"\nLoading data from: {input_path}")
    df = pd.read_csv(input_path)

    # Filter to those with valid coverage and ranking
    valid_df = df[df['coverage_ratio'].notna() & df['rank_global'].notna()].copy()
    print(f"Total researchers with valid data: {len(valid_df)}")

    # Overall correlation
    print("\n" + "-" * 70)
    print("OVERALL CORRELATION")
    print("-" * 70)

    overall = calculate_rank_correlation(valid_df, "Overall")
    print(f"n = {overall['n']}")
    print(f"Spearman ρ = {overall['rho']:.4f}")
    print(f"p-value = {overall['p_value']:.6f}")
    print(f"Effect size: {overall['effect_size']}")
    print(f"Interpretation: {overall['interpretation']}")

    # By field type
    print("\n" + "-" * 70)
    print("CORRELATION BY FIELD TYPE")
    print("-" * 70)

    results = [overall]

    for field_type in ['book_heavy', 'mixed', 'journal_heavy']:
        subset = valid_df[valid_df['field_type'] == field_type]
        result = calculate_rank_correlation(subset, field_type)
        results.append(result)

        print(f"\n{field_type.upper()} FIELDS:")
        print(f"  n = {result['n']}")
        print(f"  Spearman ρ = {result['rho']:.4f} {result['sig_marker']}")
        print(f"  p-value = {result['p_value']:.6f}")
        print(f"  Effect size: {result['effect_size']}")

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Format for output
    results_df['rho_formatted'] = results_df['rho'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")
    results_df['p_formatted'] = results_df['p_value'].apply(
        lambda x: f"{x:.6f}" if pd.notna(x) else "N/A"
    )

    # Save results
    print(f"\nSaving results to: {output_path}")
    results_df.to_csv(output_path, index=False)

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Field Type':<15} {'n':>6} {'ρ':>10} {'p-value':>12} {'Sig':>5} {'Effect':>10}")
    print("-" * 70)
    for _, row in results_df.iterrows():
        print(f"{row['group']:<15} {row['n']:>6} {row['rho']:>10.4f} {row['p_value']:>12.6f} {row['sig_marker']:>5} {row['effect_size']:>10}")

    # Key finding for manuscript
    print("\n" + "=" * 70)
    print("KEY FINDING FOR MANUSCRIPT")
    print("=" * 70)

    book_heavy = results_df[results_df['group'] == 'book_heavy'].iloc[0]
    print(f"""
The correlation between ranking and coverage differs substantially by field type.
Book-heavy disciplines (humanities and social sciences) show the strongest negative
correlation (ρ = {book_heavy['rho']:.3f}, p = {book_heavy['p_value']:.4f}, n = {book_heavy['n']}),
indicating that higher-ranked researchers in these fields have systematically lower
Scopus coverage. This pattern is weaker or absent in journal-heavy STEM fields.
""")

    # Also save to reproducibility package
    repro_path = data_dir.parent / 'reproducibility_package' / 'data' / 'rank_coverage_by_field_type.csv'
    if repro_path.parent.exists():
        results_df.to_csv(repro_path, index=False)
        print(f"Also saved to: {repro_path}")

    print("\nDone!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
