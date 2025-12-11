#!/usr/bin/env python3
"""
Analyze All Replicate Samples
==============================

Calculates effect sizes for each of the 5 independent replicate samples.

For each replicate, calculates:
- H1 (Elsevier): Cohen's d, Pearson r, p-value
- H2 (Books): Cliff's δ, Pearson r, p-value
- H3 (Field type): Cohen's d, p-value
- H4 (OA): Pearson r, p-value

Compares effect sizes across replicates to demonstrate robustness.
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def cohens_d(group1, group2):
    """Calculate Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std if pooled_std > 0 else 0

def cliffs_delta(group1, group2):
    """Calculate Cliff's delta effect size."""
    comparisons = []
    for x in group1:
        for y in group2:
            if x > y:
                comparisons.append(1)
            elif x < y:
                comparisons.append(-1)
            else:
                comparisons.append(0)
    return np.mean(comparisons) if comparisons else 0

def analyze_replicate(replicate_num, df):
    """Analyze a single replicate and calculate all effect sizes."""

    print(f"\n{'='*80}")
    print(f"ANALYZING REPLICATE {replicate_num}")
    print(f"{'='*80}")

    # Coverage binary (1 = matched, 0 = not matched)
    df['coverage'] = df['openalex_found'].astype(int) * 100

    # Filter to matched researchers only
    df_matched = df[df['openalex_found'] == True].copy()

    n_total = len(df)
    n_matched = len(df_matched)
    match_rate = n_matched / n_total * 100

    print(f"\nSample size: {n_total} researchers")
    print(f"Matched to OpenAlex: {n_matched} ({match_rate:.1f}%)")

    if n_matched < 50:
        print(f"⚠️  WARNING: Too few matches for reliable analysis")
        return None

    results = {
        'replicate': replicate_num,
        'n_total': n_total,
        'n_matched': n_matched,
        'match_rate': match_rate
    }

    # H1: Elsevier Effect
    print(f"\n--- H1: Elsevier Effect ---")

    # Split by median Elsevier %
    median_elsevier = df_matched['elsevier_pct'].median()
    high_elsevier = df[df['elsevier_pct'] >= median_elsevier]['coverage']
    low_elsevier = df[df['elsevier_pct'] < median_elsevier]['coverage']

    if len(high_elsevier) > 0 and len(low_elsevier) > 0:
        results['h1_cohens_d'] = cohens_d(high_elsevier, low_elsevier)
        results['h1_mean_diff'] = high_elsevier.mean() - low_elsevier.mean()
        results['h1_correlation'], results['h1_pvalue'] = stats.pearsonr(
            df['elsevier_pct'].fillna(0),
            df['coverage'].fillna(0)
        )

        print(f"  Cohen's d: {results['h1_cohens_d']:.3f}")
        print(f"  Mean difference: {results['h1_mean_diff']:.1f} pp")
        print(f"  Correlation r: {results['h1_correlation']:.3f}")
        print(f"  p-value: {results['h1_pvalue']:.6f}")

    # H2: Book Effect
    print(f"\n--- H2: Book Effect ---")

    high_books = df[df['books_pct'] >= 50]['coverage']
    low_books = df[df['books_pct'] < 50]['coverage']

    if len(high_books) > 5 and len(low_books) > 5:
        results['h2_cliffs_delta'] = cliffs_delta(low_books, high_books)
        results['h2_mean_diff'] = low_books.mean() - high_books.mean()
        results['h2_correlation'], results['h2_pvalue'] = stats.pearsonr(
            df['books_pct'].fillna(0),
            df['coverage'].fillna(0)
        )

        print(f"  Cliff's δ: {results['h2_cliffs_delta']:.3f}")
        print(f"  Mean difference: {results['h2_mean_diff']:.1f} pp")
        print(f"  Correlation r: {results['h2_correlation']:.3f}")
        print(f"  p-value: {results['h2_pvalue']:.6f}")

    # H3: Field Type Effect
    print(f"\n--- H3: Field Type Effect ---")

    journal_heavy = df[df['field_type'] == 'journal_heavy']['coverage']
    book_heavy = df[df['field_type'] == 'book_heavy']['coverage']

    if len(journal_heavy) > 5 and len(book_heavy) > 5:
        results['h3_cohens_d'] = cohens_d(journal_heavy, book_heavy)
        results['h3_mean_diff'] = journal_heavy.mean() - book_heavy.mean()
        _, results['h3_pvalue'] = stats.ttest_ind(journal_heavy, book_heavy)

        print(f"  Cohen's d: {results['h3_cohens_d']:.3f}")
        print(f"  Mean difference: {results['h3_mean_diff']:.1f} pp")
        print(f"  p-value: {results['h3_pvalue']:.6f}")

    # H4: OA Effect
    print(f"\n--- H4: OA Effect ---")

    if 'oa_pct' in df_matched.columns:
        results['h4_correlation'], results['h4_pvalue'] = stats.pearsonr(
            df_matched['oa_pct'].fillna(0),
            df_matched['coverage'].fillna(0)
        )

        print(f"  Correlation r: {results['h4_correlation']:.3f}")
        print(f"  p-value: {results['h4_pvalue']:.6f}")

    # Summary statistics for matched researchers
    print(f"\n--- Summary Statistics (n={n_matched}) ---")
    print(f"  Median Elsevier %: {df_matched['elsevier_pct'].median():.1f}%")
    print(f"  Median Books %: {df_matched['books_pct'].median():.1f}%")
    print(f"  Median OA %: {df_matched['oa_pct'].median():.1f}%")
    print(f"  Median coverage: {df_matched['coverage_ratio'].median():.1%}")

    return results

def main():
    """Analyze all replicates."""

    print("="*80)
    print("ROBUSTNESS ANALYSIS: EFFECT SIZES ACROSS REPLICATES")
    print("="*80)

    # Load all replicates
    data_dir = Path("robustness_analysis/openalex_matched")
    output_dir = Path("robustness_analysis")

    all_results = []

    for i in range(1, 6):
        replicate_file = data_dir / f"replicate_{i}_openalex_data.csv"

        if not replicate_file.exists():
            print(f"\n⚠️  Replicate {i} not found: {replicate_file}")
            continue

        # Load data
        df = pd.read_csv(replicate_file)

        # Analyze
        results = analyze_replicate(i, df)

        if results:
            all_results.append(results)

    # Combine results
    results_df = pd.DataFrame(all_results)

    # Save individual results
    results_df.to_csv(output_dir / "replicate_effect_sizes.csv", index=False)

    # Calculate summary statistics
    print(f"\n{'='*80}")
    print("SUMMARY ACROSS ALL REPLICATES")
    print(f"{'='*80}")

    summary_stats = {}

    for col in results_df.columns:
        if col not in ['replicate', 'n_total', 'n_matched']:
            values = results_df[col].dropna()
            if len(values) > 0:
                summary_stats[col] = {
                    'mean': values.mean(),
                    'std': values.std(),
                    'min': values.min(),
                    'max': values.max(),
                    'range': values.max() - values.min()
                }

    # Print comparison table
    print(f"\n{'Replicate':<12} {'H1_d':<8} {'H1_r':<8} {'H1_p':<10} {'H2_δ':<8} {'H2_r':<8} {'H2_p':<10}")
    print("-" * 80)

    for _, row in results_df.iterrows():
        rep = int(row['replicate'])
        h1_d = row.get('h1_cohens_d', np.nan)
        h1_r = row.get('h1_correlation', np.nan)
        h1_p = row.get('h1_pvalue', np.nan)
        h2_d = row.get('h2_cliffs_delta', np.nan)
        h2_r = row.get('h2_correlation', np.nan)
        h2_p = row.get('h2_pvalue', np.nan)

        p_str1 = f"<0.001" if h1_p < 0.001 else f"{h1_p:.4f}"
        p_str2 = f"<0.001" if h2_p < 0.001 else f"{h2_p:.4f}"

        print(f"{rep:<12} {h1_d:>7.3f} {h1_r:>7.3f} {p_str1:>9} {h2_d:>7.3f} {h2_r:>7.3f} {p_str2:>9}")

    # Summary row
    print("-" * 80)
    h1_d_mean = summary_stats.get('h1_cohens_d', {}).get('mean', np.nan)
    h1_d_std = summary_stats.get('h1_cohens_d', {}).get('std', np.nan)
    h1_r_mean = summary_stats.get('h1_correlation', {}).get('mean', np.nan)
    h1_r_std = summary_stats.get('h1_correlation', {}).get('std', np.nan)
    h2_d_mean = summary_stats.get('h2_cliffs_delta', {}).get('mean', np.nan)
    h2_d_std = summary_stats.get('h2_cliffs_delta', {}).get('std', np.nan)
    h2_r_mean = summary_stats.get('h2_correlation', {}).get('mean', np.nan)
    h2_r_std = summary_stats.get('h2_correlation', {}).get('std', np.nan)

    print(f"{'Mean ± SD':<12} {h1_d_mean:.2f}±{h1_d_std:.2f} {h1_r_mean:.2f}±{h1_r_std:.2f} {'ALL':<9} {h2_d_mean:.2f}±{h2_d_std:.2f} {h2_r_mean:.2f}±{h2_r_std:.2f} {'ALL':<9}")

    # Save summary
    summary_df = pd.DataFrame(summary_stats).T
    summary_df.to_csv(output_dir / "replicate_summary_statistics.csv")

    print(f"\n{'='*80}")
    print("ROBUSTNESS ASSESSMENT")
    print(f"{'='*80}")

    # Check if effects are stable (SD < 0.10)
    stable_effects = []
    unstable_effects = []

    for effect in ['h1_cohens_d', 'h1_correlation', 'h2_cliffs_delta', 'h2_correlation']:
        if effect in summary_stats:
            std = summary_stats[effect]['std']
            if std < 0.10:
                stable_effects.append(f"{effect}: ±{std:.3f}")
            else:
                unstable_effects.append(f"{effect}: ±{std:.3f}")

    print(f"\n✓ STABLE EFFECTS (SD < 0.10):")
    for effect in stable_effects:
        print(f"    {effect}")

    if unstable_effects:
        print(f"\n⚠️  UNSTABLE EFFECTS (SD >= 0.10):")
        for effect in unstable_effects:
            print(f"    {effect}")

    # Check if all p-values < 0.001
    all_sig = True
    for col in ['h1_pvalue', 'h2_pvalue', 'h3_pvalue', 'h4_pvalue']:
        if col in results_df.columns:
            max_p = results_df[col].max()
            if max_p >= 0.001:
                all_sig = False
                print(f"\n⚠️  {col}: max p-value = {max_p:.4f}")

    if all_sig:
        print(f"\n✓ ALL p-values < 0.001 across all replicates")

    print(f"\n{'='*80}")
    print("FILES CREATED")
    print(f"{'='*80}")
    print(f"  • {output_dir}/replicate_effect_sizes.csv")
    print(f"  • {output_dir}/replicate_summary_statistics.csv")

    print(f"\n✓ ROBUSTNESS ANALYSIS COMPLETE")
    print(f"\nNext step: Run generate_robustness_report.py to create manuscript-ready report")

if __name__ == "__main__":
    main()
