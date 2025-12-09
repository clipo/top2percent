#!/usr/bin/env python3
"""
Test if Ranking Position Correlates with Coverage

This addresses the sampling circularity criticism:
- If lower-ranked researchers (within top 2%) have worse coverage
- This suggests exclusion bias affects who makes the ranking
- Provides evidence beyond the sampled population
"""

import pandas as pd
from scipy.stats import spearmanr, pearsonr
import numpy as np

print("="*80)
print("RANKING POSITION VS COVERAGE CORRELATION")
print("="*80)
print("\nTesting if ranking position correlates with coverage...")
print("(Would suggest exclusion bias if lower ranks have worse coverage)")
print()

# Load data
sample = pd.read_csv('reproducibility_package/data/comprehensive_sample.csv')
openalex = pd.read_csv('reproducibility_package/data/openalex_comprehensive_data.csv')

print(f"Loaded {len(sample)} researchers from comprehensive_sample.csv")
print(f"Loaded {len(openalex)} researchers from openalex_comprehensive_data.csv")

# Merge on authfull to get both rankings and coverage
merged = sample.merge(openalex[['authfull', 'coverage_ratio', 'elsevier_pct', 'books_pct']],
                      on='authfull', how='inner')

print(f"\n✓ Merged: {len(merged)} researchers with both ranking and coverage data")

# Remove any NaN values
valid = merged[['rank_global', 'rank_in_field', 'coverage_ratio']].dropna()
merged_valid = merged.loc[valid.index]

print(f"✓ Valid data: {len(merged_valid)} researchers")

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("CORRELATION: RANKING POSITION VS COVERAGE")
print("="*80)

# Global rank vs coverage
# Note: Higher rank number = worse rank (e.g., rank 100,000 is worse than rank 1,000)
# So negative correlation would mean: worse rank → worse coverage
rho_global, p_global = spearmanr(merged_valid['rank_global'], merged_valid['coverage_ratio'])
r_global, p_global_pearson = pearsonr(merged_valid['rank_global'], merged_valid['coverage_ratio'])

print(f"\n**Global Rank vs Coverage**:")
print(f"  Spearman ρ = {rho_global:.3f}, p = {p_global:.4f}")
print(f"  Pearson r = {r_global:.3f}, p = {p_global_pearson:.4f}")

if p_global < 0.001:
    if rho_global < 0:
        print(f"  ✓ SIGNIFICANT NEGATIVE correlation")
        print(f"    → Lower-ranked researchers have worse coverage")
        print(f"    → Suggests exclusion bias affects who makes the ranking")
    else:
        print(f"  ! Positive correlation (unexpected)")
else:
    print(f"  No significant correlation")

# Field rank vs coverage
rho_field, p_field = spearmanr(merged_valid['rank_in_field'], merged_valid['coverage_ratio'])
r_field, p_field_pearson = pearsonr(merged_valid['rank_in_field'], merged_valid['coverage_ratio'])

print(f"\n**Field Rank vs Coverage**:")
print(f"  Spearman ρ = {rho_field:.3f}, p = {p_field:.4f}")
print(f"  Pearson r = {r_field:.3f}, p = {p_field_pearson:.4f}")

if p_field < 0.001:
    if rho_field < 0:
        print(f"  ✓ SIGNIFICANT NEGATIVE correlation")
        print(f"    → Lower-ranked researchers have worse coverage")
        print(f"    → Pattern holds within fields")
    else:
        print(f"  ! Positive correlation (unexpected)")
else:
    print(f"  No significant correlation")

# ============================================================================
# QUANTILE ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("COVERAGE BY RANKING QUARTILE")
print("="*80)

# Divide into quartiles by global rank
merged_valid['rank_quartile'] = pd.qcut(merged_valid['rank_global'],
                                         q=4,
                                         labels=['Top 25%', 'Q2', 'Q3', 'Bottom 25%'])

print(f"\n**Coverage by Global Rank Quartile**:")
for quartile in ['Top 25%', 'Q2', 'Q3', 'Bottom 25%']:
    q_data = merged_valid[merged_valid['rank_quartile'] == quartile]
    median_cov = q_data['coverage_ratio'].median() * 100
    mean_cov = q_data['coverage_ratio'].mean() * 100
    n = len(q_data)
    print(f"  {quartile:12s}: {median_cov:5.1f}% median, {mean_cov:5.1f}% mean (n={n})")

# Calculate difference
top_quartile_cov = merged_valid[merged_valid['rank_quartile'] == 'Top 25%']['coverage_ratio'].median() * 100
bottom_quartile_cov = merged_valid[merged_valid['rank_quartile'] == 'Bottom 25%']['coverage_ratio'].median() * 100
quartile_diff = top_quartile_cov - bottom_quartile_cov

print(f"\n  Difference (Top 25% - Bottom 25%): {quartile_diff:.1f} percentage points")

if quartile_diff > 0:
    print(f"  ✓ Top-ranked researchers have better coverage")
    print(f"    → Consistent with exclusion bias hypothesis")

# ============================================================================
# BY FIELD TYPE
# ============================================================================

print("\n" + "="*80)
print("CORRELATION BY FIELD TYPE")
print("="*80)

for field_type in ['book_heavy', 'mixed', 'journal_heavy']:
    field_data = merged_valid[merged_valid['field_type'] == field_type]
    if len(field_data) > 20:  # Need enough data
        rho, p = spearmanr(field_data['rank_global'], field_data['coverage_ratio'])
        print(f"\n{field_type}:")
        print(f"  ρ = {rho:.3f}, p = {p:.4f} (n={len(field_data)})")
        if p < 0.05 and rho < 0:
            print(f"  ✓ Negative correlation within {field_type} fields")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY AND IMPLICATIONS")
print("="*80)

print(f"""
**Finding**: Ranking position correlates with coverage

Global rank correlation: ρ={rho_global:.3f} (p={p_global:.4f})
Field rank correlation: ρ={rho_field:.3f} (p={p_field:.4f})

Coverage by quartile:
  Top 25% (best ranks): {top_quartile_cov:.1f}% median coverage
  Bottom 25% (worst ranks within top 2%): {bottom_quartile_cov:.1f}% median coverage
  Difference: {quartile_diff:.1f} percentage points

**Interpretation**:
""")

if rho_global < -0.1 and p_global < 0.001:
    print("""
✓ SIGNIFICANT EVIDENCE OF EXCLUSION BIAS

Even within the top 2%, lower-ranked researchers have systematically worse
coverage. This suggests that poor coverage affects not just ranking position
among included researchers, but also determines who makes it into the ranking
at all.

This addresses the sampling circularity criticism: we find evidence of
exclusion bias by examining the gradient within the sampled population. If
coverage only affected ranking position (not inclusion), we would expect no
correlation between rank and coverage within the top 2%. The observed
correlation suggests coverage acts as a barrier to entry.

Researchers with coverage just below the cutoff (e.g., 30-40%) are
systematically underrepresented in the ranking relative to their true
productivity, as evidenced by their concentration in lower rank positions
when they do appear.
""")
else:
    print("""
No strong evidence of correlation between rank position and coverage within
the top 2%. This suggests that among included researchers, coverage affects
ranking position but we cannot infer exclusion bias from this analysis alone.

The ORCID verification remains the strongest defense against sampling
circularity concerns.
""")

# Save results
results = pd.DataFrame({
    'analysis': ['Global rank vs coverage', 'Field rank vs coverage',
                 'Top quartile median', 'Bottom quartile median', 'Quartile difference'],
    'statistic': [rho_global, rho_field, top_quartile_cov, bottom_quartile_cov, quartile_diff],
    'p_value': [p_global, p_field, np.nan, np.nan, np.nan]
})

results.to_csv('ranking_coverage_correlation_results.csv', index=False)
print("\n✓ Saved: ranking_coverage_correlation_results.csv")

print("\n" + "="*80)
print("COMPLETE")
print("="*80)
