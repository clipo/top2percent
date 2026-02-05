#!/usr/bin/env python3
"""
Statistical Analysis of Scopus Coverage Bias
============================================

PURPOSE:
    Tests four pre-specified hypotheses about systematic bias in Scopus coverage
    using data from 570 researchers matched between Scopus and OpenAlex (n=600 sample).

HYPOTHESES:
    H1: Publisher bias - Does Elsevier % predict better Scopus coverage?
    H2: Book bias - Do researchers with more books have worse coverage?
    H3: Open access penalty - Does OA publishing predict worse coverage?
    H4: Field bias - Do book-heavy fields have worse coverage than STEM?

INPUT FILES:
    - data/openalex_comprehensive_data.csv (600-researcher sample with OpenAlex data)

OUTPUT FILES:
    - ANALYSIS_SUMMARY.txt (console output redirect)
    - analysis_results.json (machine-readable results)

STATISTICAL METHODS:
    - Pearson correlation (linear relationships)
    - Mann-Whitney U (non-parametric group comparisons)
    - Kruskal-Wallis H (non-parametric 3+ group comparisons)
    - Cohen's d (effect sizes)
    - OLS regression (multivariate analysis)

EXPECTED RESULTS:
    - H1: r=0.564, p<0.001, d=1.178 (27.5 pp difference)
    - H2: r=-0.503, p<0.001 (39.4 pp field difference)
    - H3: r=+0.251, p<0.001 (NO PENALTY - positive correlation)
    - H4: H=132.973, p<0.001 (large field differences)
    - Multivariate R²=0.449

DEPENDENCIES:
    - pandas >= 2.0.0
    - numpy >= 1.24.0
    - scipy >= 1.11.0
    - statsmodels >= 0.14.0

USAGE:
    python3 analyze_coverage_bias.py > ANALYSIS_SUMMARY.txt

REPRODUCIBILITY:
    - No randomness - all tests deterministic
    - Results should match manuscript exactly
    - Expect ±3% variation if OpenAlex data updated

AUTHOR: Generated for "Systematic Bias in Top 2% Rankings" study
DATE: November 2024
"""

import pandas as pd
import numpy as np
from scipy import stats
import json

def load_data(filename='data/openalex_comprehensive_data.csv'):
    """Load the comprehensive evidence table (n=600 sample)."""
    df = pd.read_csv(filename)

    # Filter to successfully matched researchers
    df = df[df['openalex_found'] == True].copy()

    # Clean data: drop NaN values and cap unrealistic coverage ratios
    initial_n = len(df)
    df = df.dropna(subset=['coverage_ratio', 'elsevier_pct', 'books_pct', 'oa_publisher_pct'])

    # Cap coverage ratio at 1.5 (150%) to exclude obvious name mismatches
    # (Coverage >150% suggests Scopus matched wrong person)
    df = df[df['coverage_ratio'] <= 1.5]

    excluded = initial_n - len(df)
    if excluded > 0:
        print(f"Excluded {excluded} researchers due to missing data or extreme coverage (>150%)")

    print(f"Loaded {len(df)} researchers with OpenAlex matches")
    print(f"  Book-heavy: {len(df[df['field_type'] == 'book_heavy'])}")
    print(f"  Mixed: {len(df[df['field_type'] == 'mixed'])}")
    print(f"  Journal-heavy: {len(df[df['field_type'] == 'journal_heavy'])}")

    return df


def test_hypothesis_1_publisher_bias(df):
    """
    H1: Researchers with higher Elsevier % have better Scopus coverage.

    Test: Correlation and group comparison.
    """
    print("\n" + "=" * 80)
    print("HYPOTHESIS 1: PUBLISHER BIAS")
    print("=" * 80)
    print("\nDo researchers who publish more in Elsevier journals have better")
    print("Scopus coverage?")

    # Overall correlation
    correlation = df[['elsevier_pct', 'coverage_ratio']].corr().iloc[0, 1]
    n = len(df)

    # Pearson correlation test
    r, p_value = stats.pearsonr(df['elsevier_pct'], df['coverage_ratio'])

    print(f"\n--- Overall Correlation ---")
    print(f"Correlation (Elsevier % vs Coverage): r = {r:.3f}")
    print(f"Sample size: n = {n}")
    print(f"p-value: {p_value:.6f}")

    if p_value < 0.001:
        print("*** HIGHLY SIGNIFICANT (p < 0.001) ***")
    elif p_value < 0.01:
        print("** SIGNIFICANT (p < 0.01) **")
    elif p_value < 0.05:
        print("* SIGNIFICANT (p < 0.05) *")
    else:
        print("Not significant (p >= 0.05)")

    # Group comparison: High vs Low Elsevier
    median_elsevier = df['elsevier_pct'].median()
    high_elsevier = df[df['elsevier_pct'] > median_elsevier]
    low_elsevier = df[df['elsevier_pct'] <= median_elsevier]

    print(f"\n--- Group Comparison ---")
    print(f"High Elsevier group (>{median_elsevier:.1f}%): n={len(high_elsevier)}")
    print(f"  Median coverage: {high_elsevier['coverage_ratio'].median():.2%}")
    print(f"  Mean coverage: {high_elsevier['coverage_ratio'].mean():.2%}")

    print(f"\nLow Elsevier group (≤{median_elsevier:.1f}%): n={len(low_elsevier)}")
    print(f"  Median coverage: {low_elsevier['coverage_ratio'].median():.2%}")
    print(f"  Mean coverage: {low_elsevier['coverage_ratio'].mean():.2%}")

    # Mann-Whitney U test
    stat, p_mw = stats.mannwhitneyu(
        high_elsevier['coverage_ratio'],
        low_elsevier['coverage_ratio'],
        alternative='greater'
    )

    diff = high_elsevier['coverage_ratio'].median() - low_elsevier['coverage_ratio'].median()
    print(f"\nDifference: {diff:.2%} (High - Low)")
    print(f"Mann-Whitney U test: p = {p_mw:.6f}")

    if p_mw < 0.05 and diff > 0:
        print("⚠️  BIAS DETECTED: High-Elsevier researchers have better coverage!")
    else:
        print("✓ No significant bias detected")

    # Effect size (Cohen's d)
    mean_diff = high_elsevier['coverage_ratio'].mean() - low_elsevier['coverage_ratio'].mean()
    pooled_std = np.sqrt(
        (high_elsevier['coverage_ratio'].std()**2 + low_elsevier['coverage_ratio'].std()**2) / 2
    )
    cohens_d = mean_diff / pooled_std
    print(f"Effect size (Cohen's d): {cohens_d:.3f}")

    if abs(cohens_d) > 0.8:
        print("  (Large effect)")
    elif abs(cohens_d) > 0.5:
        print("  (Medium effect)")
    elif abs(cohens_d) > 0.2:
        print("  (Small effect)")

    return {
        'correlation': r,
        'p_value': p_value,
        'median_diff': diff,
        'p_mann_whitney': p_mw,
        'cohens_d': cohens_d,
        'significant': p_value < 0.05 and r > 0
    }


def test_hypothesis_2_book_bias(df):
    """
    H2: Researchers with higher book % have worse Scopus coverage.

    Test: Correlation, controlling for field type.
    """
    print("\n" + "=" * 80)
    print("HYPOTHESIS 2: BOOK BIAS")
    print("=" * 80)
    print("\nDo researchers who publish more books have worse Scopus coverage?")

    # Overall correlation
    r, p_value = stats.pearsonr(df['books_pct'], df['coverage_ratio'])

    print(f"\n--- Overall Correlation ---")
    print(f"Correlation (Book % vs Coverage): r = {r:.3f}")
    print(f"p-value: {p_value:.6f}")

    if p_value < 0.05:
        if r < 0:
            print("⚠️  BIAS DETECTED: More books = worse coverage")
        else:
            print("Unexpected positive correlation")
    else:
        print("✓ No significant correlation")

    # Within field types
    print(f"\n--- Within Field Types ---")

    for field_type in ['book_heavy', 'mixed', 'journal_heavy']:
        subset = df[df['field_type'] == field_type]
        if len(subset) < 10:
            continue

        r_field, p_field = stats.pearsonr(subset['books_pct'], subset['coverage_ratio'])

        print(f"\n{field_type.upper()}:")
        print(f"  n = {len(subset)}")
        print(f"  Correlation: r = {r_field:.3f}, p = {p_field:.4f}")
        print(f"  Median book %: {subset['books_pct'].median():.1f}%")
        print(f"  Median coverage: {subset['coverage_ratio'].median():.2%}")

    # Group comparison within book-heavy fields
    book_heavy = df[df['field_type'] == 'book_heavy']
    if len(book_heavy) > 20:
        median_books = book_heavy['books_pct'].median()
        high_books = book_heavy[book_heavy['books_pct'] > median_books]
        low_books = book_heavy[book_heavy['books_pct'] <= median_books]

        if len(high_books) > 5 and len(low_books) > 5:
            stat, p_mw = stats.mannwhitneyu(
                high_books['coverage_ratio'],
                low_books['coverage_ratio'],
                alternative='less'
            )

            print(f"\n--- Book-Heavy Fields Only ---")
            print(f"High book % (>{median_books:.1f}%): coverage = {high_books['coverage_ratio'].median():.2%}")
            print(f"Low book % (≤{median_books:.1f}%): coverage = {low_books['coverage_ratio'].median():.2%}")
            print(f"Mann-Whitney U test: p = {p_mw:.4f}")

    return {
        'correlation': r,
        'p_value': p_value,
        'significant': p_value < 0.05 and r < 0
    }


def test_hypothesis_3_oa_penalty(df):
    """
    H3: Researchers with higher OA % have worse Scopus coverage.

    Test: Correlation and comparison.
    """
    print("\n" + "=" * 80)
    print("HYPOTHESIS 3: OPEN ACCESS PENALTY")
    print("=" * 80)
    print("\nDo researchers who publish more in OA venues have worse coverage?")

    # Correlation
    r, p_value = stats.pearsonr(df['oa_publisher_pct'], df['coverage_ratio'])

    print(f"\n--- Overall Correlation ---")
    print(f"Correlation (OA Publisher % vs Coverage): r = {r:.3f}")
    print(f"p-value: {p_value:.6f}")

    if p_value < 0.05:
        if r < 0:
            print("⚠️  PENALTY DETECTED: More OA = worse coverage")
        else:
            print("✓ Positive correlation (OA publishers well-indexed)")
    else:
        print("✓ No significant correlation")

    # Specific OA publishers
    print(f"\n--- Specific OA Publishers ---")
    print(f"PLOS:")
    print(f"  Researchers publishing in PLOS: {len(df[df['plos_count'] > 0])}")
    if len(df[df['plos_count'] > 0]) > 5:
        plos_pubs = df[df['plos_count'] > 0]
        no_plos = df[df['plos_count'] == 0]
        print(f"  Median coverage (PLOS authors): {plos_pubs['coverage_ratio'].median():.2%}")
        print(f"  Median coverage (non-PLOS): {no_plos['coverage_ratio'].median():.2%}")

    print(f"\nFrontiers:")
    print(f"  Researchers publishing in Frontiers: {len(df[df['frontiers_count'] > 0])}")
    if len(df[df['frontiers_count'] > 0]) > 5:
        frontiers_pubs = df[df['frontiers_count'] > 0]
        no_frontiers = df[df['frontiers_count'] == 0]
        print(f"  Median coverage (Frontiers authors): {frontiers_pubs['coverage_ratio'].median():.2%}")
        print(f"  Median coverage (non-Frontiers): {no_frontiers['coverage_ratio'].median():.2%}")

    return {
        'correlation': r,
        'p_value': p_value,
        'significant': p_value < 0.05 and r < 0
    }


def test_hypothesis_4_field_bias(df):
    """
    H4: Book-heavy fields have systematically worse coverage than journal-heavy fields.

    Test: Kruskal-Wallis H test across field types.
    """
    print("\n" + "=" * 80)
    print("HYPOTHESIS 4: FIELD-LEVEL BIAS")
    print("=" * 80)
    print("\nDo book-heavy fields have worse coverage than journal-heavy fields?")

    # Summary by field type
    print(f"\n--- Coverage by Field Type ---")

    field_stats = {}
    for field_type in ['book_heavy', 'mixed', 'journal_heavy']:
        subset = df[df['field_type'] == field_type]
        field_stats[field_type] = {
            'n': len(subset),
            'median': subset['coverage_ratio'].median(),
            'mean': subset['coverage_ratio'].mean(),
            'std': subset['coverage_ratio'].std(),
        }

        print(f"\n{field_type.upper()}:")
        print(f"  n = {field_stats[field_type]['n']}")
        print(f"  Median coverage: {field_stats[field_type]['median']:.2%}")
        print(f"  Mean coverage: {field_stats[field_type]['mean']:.2%}")
        print(f"  Std dev: {field_stats[field_type]['std']:.3f}")

    # Kruskal-Wallis H test
    book_heavy = df[df['field_type'] == 'book_heavy']['coverage_ratio']
    mixed = df[df['field_type'] == 'mixed']['coverage_ratio']
    journal_heavy = df[df['field_type'] == 'journal_heavy']['coverage_ratio']

    h_stat, p_value = stats.kruskal(book_heavy, mixed, journal_heavy)

    print(f"\n--- Statistical Test ---")
    print(f"Kruskal-Wallis H test: H = {h_stat:.3f}, p = {p_value:.6f}")

    if p_value < 0.05:
        print("*** SIGNIFICANT FIELD DIFFERENCES DETECTED ***")

        # Post-hoc pairwise comparisons
        print(f"\n--- Post-hoc Pairwise Comparisons ---")

        # Book-heavy vs Journal-heavy
        stat_bj, p_bj = stats.mannwhitneyu(book_heavy, journal_heavy, alternative='less')
        diff_bj = book_heavy.median() - journal_heavy.median()
        print(f"\nBook-heavy vs Journal-heavy:")
        print(f"  Median difference: {diff_bj:.2%}")
        print(f"  p-value: {p_bj:.6f}")
        if p_bj < 0.05:
            print("  ⚠️  Book-heavy fields significantly worse!")

        # Book-heavy vs Mixed
        stat_bm, p_bm = stats.mannwhitneyu(book_heavy, mixed, alternative='less')
        diff_bm = book_heavy.median() - mixed.median()
        print(f"\nBook-heavy vs Mixed:")
        print(f"  Median difference: {diff_bm:.2%}")
        print(f"  p-value: {p_bm:.6f}")

        # Mixed vs Journal-heavy
        stat_mj, p_mj = stats.mannwhitneyu(mixed, journal_heavy, alternative='less')
        diff_mj = mixed.median() - journal_heavy.median()
        print(f"\nMixed vs Journal-heavy:")
        print(f"  Median difference: {diff_mj:.2%}")
        print(f"  p-value: {p_mj:.6f}")
    else:
        print("✓ No significant field differences")

    return {
        'h_statistic': h_stat,
        'p_value': p_value,
        'field_stats': field_stats,
        'significant': p_value < 0.05
    }


def multivariate_analysis(df):
    """
    Multivariate regression: coverage ~ elsevier_pct + books_pct + oa_pct + field_type

    This controls for confounds.
    """
    print("\n" + "=" * 80)
    print("MULTIVARIATE ANALYSIS")
    print("=" * 80)
    print("\nRegression: Coverage ~ Elsevier% + Books% + OA% + Field")

    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import StandardScaler

        # Prepare data
        X = df[['elsevier_pct', 'books_pct', 'oa_publisher_pct']].copy()

        # Add field type dummies
        X['is_book_heavy'] = (df['field_type'] == 'book_heavy').astype(int)
        X['is_mixed'] = (df['field_type'] == 'mixed').astype(int)

        y = df['coverage_ratio'].values

        # Fit model
        model = LinearRegression()
        model.fit(X, y)

        r_squared = model.score(X, y)

        print(f"\nModel R²: {r_squared:.3f}")
        print(f"\nCoefficients:")
        for i, col in enumerate(X.columns):
            coef = model.coef_[i]
            print(f"  {col:25s}: {coef:+.4f}")
            if col == 'elsevier_pct' and coef > 0.001:
                print(f"    → 10% more Elsevier = {coef*10:.2%} better coverage")
            elif col == 'books_pct' and coef < -0.001:
                print(f"    → 10% more books = {abs(coef*10):.2%} worse coverage")

        print(f"\nIntercept: {model.intercept_:.4f}")

        return {
            'r_squared': r_squared,
            'coefficients': dict(zip(X.columns, model.coef_)),
            'intercept': model.intercept_
        }

    except ImportError:
        print("\nSkipping (sklearn not installed)")
        print("Install with: pip install scikit-learn")
        return None


def generate_summary_table(df, results):
    """
    Create publication-ready summary table.
    """
    print("\n" + "=" * 80)
    print("PUBLICATION-READY SUMMARY")
    print("=" * 80)

    summary = {
        'Sample size': len(df),
        'Median coverage ratio': f"{df['coverage_ratio'].median():.1%}",
        'Median Elsevier %': f"{df['elsevier_pct'].median():.1f}%",
        'Median book %': f"{df['books_pct'].median():.1f}%",
        'Median OA %': f"{df['oa_publisher_pct'].median():.1f}%",
        '': '',
        'H1 (Publisher bias)': 'DETECTED' if results['h1']['significant'] else 'Not detected',
        'H1 correlation': f"r = {results['h1']['correlation']:.3f}, p = {results['h1']['p_value']:.4f}",
        'H1 effect size': f"d = {results['h1']['cohens_d']:.3f}",
        ' ': '',
        'H2 (Book bias)': 'DETECTED' if results['h2']['significant'] else 'Not detected',
        'H2 correlation': f"r = {results['h2']['correlation']:.3f}, p = {results['h2']['p_value']:.4f}",
        '  ': '',
        'H3 (OA penalty)': 'DETECTED' if results['h3']['significant'] else 'Not detected',
        'H3 correlation': f"r = {results['h3']['correlation']:.3f}, p = {results['h3']['p_value']:.4f}",
        '   ': '',
        'H4 (Field bias)': 'DETECTED' if results['h4']['significant'] else 'Not detected',
        'H4 test': f"H = {results['h4']['h_statistic']:.3f}, p = {results['h4']['p_value']:.4f}",
    }

    print("\nSUMMARY TABLE")
    print("-" * 80)
    for key, value in summary.items():
        if key.strip() == '':
            print()
        else:
            print(f"{key:30s} {value}")

    # Save to file
    with open('ANALYSIS_SUMMARY.txt', 'w') as f:
        f.write("SCOPUS COVERAGE BIAS ANALYSIS - RESULTS SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        for key, value in summary.items():
            if key.strip() == '':
                f.write("\n")
            else:
                f.write(f"{key:30s} {value}\n")

    print("\n✓ Summary saved to: ANALYSIS_SUMMARY.txt")


def main():
    """
    Main analysis execution.
    """
    print("=" * 80)
    print("COMPREHENSIVE COVERAGE BIAS ANALYSIS")
    print("=" * 80)

    # Load data
    df = load_data()

    # Test all hypotheses
    results = {
        'h1': test_hypothesis_1_publisher_bias(df),
        'h2': test_hypothesis_2_book_bias(df),
        'h3': test_hypothesis_3_oa_penalty(df),
        'h4': test_hypothesis_4_field_bias(df),
    }

    # Multivariate analysis
    mv_results = multivariate_analysis(df)
    if mv_results:
        results['multivariate'] = mv_results

    # Generate summary
    generate_summary_table(df, results)

    # Save results to JSON
    # Convert numpy types to Python types for JSON serialization
    def convert_types(obj):
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_types(item) for item in obj]
        else:
            return obj

    results_clean = convert_types(results)

    with open('analysis_results.json', 'w') as f:
        json.dump(results_clean, f, indent=2)

    print(f"\n✓ Detailed results saved to: analysis_results.json")

    # Final verdict
    print("\n" + "=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)

    significant_hypotheses = [
        h for h, r in [
            ('Publisher bias (H1)', results['h1']['significant']),
            ('Book bias (H2)', results['h2']['significant']),
            ('OA penalty (H3)', results['h3']['significant']),
            ('Field bias (H4)', results['h4']['significant']),
        ] if r
    ]

    if significant_hypotheses:
        print("\n⚠️  SYSTEMATIC BIAS DETECTED")
        print("\nSignificant findings:")
        for h in significant_hypotheses:
            print(f"  • {h}")
        print("\nThe 'top 2%' rankings are SYSTEMATICALLY BIASED and should")
        print("NOT be used for hiring, promotion, or funding decisions.")
        print("\nRecommendation: Multi-database rankings required (Scopus + OpenAlex + others)")
    else:
        print("\n✓ No systematic bias detected")
        print("\nSingle-source rankings may be acceptable, though multi-database")
        print("approaches are still recommended for completeness.")


if __name__ == "__main__":
    main()
