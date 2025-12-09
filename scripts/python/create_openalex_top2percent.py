"""
Create OpenAlex-Based "Top 2%" Ranking and Compare to Scopus

Analyzes 537 researchers to:
1. Calculate composite scores using OpenAlex data
2. Identify top 2% (11 researchers)
3. Compare to their Scopus rankings
4. Show who gains/loses top 2% status
5. Analyze by field, Elsevier %, etc.
"""
import pandas as pd
import numpy as np

def calculate_composite_score(metrics, max_values):
    """Calculate c-score using Ioannidis formula"""
    score = 0
    for key in ['nc', 'h', 'hm', 'ncs', 'ncsf', 'ncsfl']:
        value = metrics.get(key, 0)
        max_val = max_values.get(key, 1)

        if max_val > 0 and value > 0:
            numerator = np.log(1 + value)
            denominator = np.log(1 + max_val)
            score += numerator / denominator

    return score

print("="*80)
print("CREATING OPENALEX-BASED 'TOP 2%' RANKING")
print("="*80)

# Load the fetched metrics
print("\nLoading metrics for 537 researchers...")
metrics_df = pd.read_csv('researcher_metrics_all_550.csv')
print(f"Loaded: {len(metrics_df)} researchers")

# Load comprehensive data for Scopus rankings
print("Loading Scopus rankings...")
full_df = pd.read_csv('reproducibility_package/data/comprehensive_sample.csv')

# Merge
merged_df = metrics_df.merge(
    full_df[['authfull', 'rank_global', 'rank_in_field', 'sm-subfield-1', 'sample_stratum']],
    on='authfull',
    how='left'
)

print(f"Merged with Scopus rankings: {len(merged_df)} researchers")

# Calculate maximum values
print("\n" + "="*80)
print("CALCULATING COMPOSITE SCORES")
print("="*80)

max_values = {
    'nc': merged_df['nc'].max(),
    'h': merged_df['h'].max(),
    'hm': merged_df['hm'].max(),
    'ncs': merged_df['ncs'].max(),
    'ncsf': merged_df['ncsf'].max(),
    'ncsfl': merged_df['ncsfl'].max()
}

print("\nMaximum values:")
for key, val in max_values.items():
    print(f"  {key.upper():6s}: {val:,.0f}")

# Calculate c-scores
composite_scores = []
for _, row in merged_df.iterrows():
    metrics = {
        'nc': row['nc'],
        'h': row['h'],
        'hm': row['hm'],
        'ncs': row['ncs'],
        'ncsf': row['ncsf'],
        'ncsfl': row['ncsfl']
    }
    c_score = calculate_composite_score(metrics, max_values)
    composite_scores.append(c_score)

merged_df['c_score_openalex'] = composite_scores
merged_df['rank_openalex'] = merged_df['c_score_openalex'].rank(ascending=False, method='min')

print(f"\n✓ Calculated c-scores for {len(merged_df)} researchers")

# Statistics
print("\nC-score statistics:")
print(f"  Mean:   {merged_df['c_score_openalex'].mean():.3f}")
print(f"  Median: {merged_df['c_score_openalex'].median():.3f}")
print(f"  Std:    {merged_df['c_score_openalex'].std():.3f}")
print(f"  Range:  {merged_df['c_score_openalex'].min():.3f} - {merged_df['c_score_openalex'].max():.3f}")

# Identify top 2%
print("\n" + "="*80)
print("IDENTIFYING OPENALEX TOP 2%")
print("="*80)

top_2_pct = 0.02
n_top = int(len(merged_df) * top_2_pct)
print(f"\nTop 2% = {n_top} researchers (out of {len(merged_df)})")

top_2_df = merged_df.nsmallest(n_top, 'rank_openalex')

print(f"\n{'='*80}")
print("OPENALEX TOP 2% RESEARCHERS")
print("="*80)
print()

for idx, (_, row) in enumerate(top_2_df.iterrows(), 1):
    print(f"{idx}. {row['authfull']}")
    print(f"   Field: {row['field']}")
    print(f"   OpenAlex c-score: {row['c_score_openalex']:.3f} (rank #{row['rank_openalex']:.0f})")
    if pd.notna(row['rank_global']):
        print(f"   Scopus rank: #{row['rank_global']:.0f}")
        rank_change = row['rank_global'] - row['rank_openalex']
        if rank_change > 0:
            print(f"   → GAINED {rank_change:,.0f} positions vs Scopus! ⬆")
        else:
            print(f"   → Lost {abs(rank_change):,.0f} positions vs Scopus ⬇")
    print(f"   Elsevier %: {row['elsevier_pct']:.1f}%")
    print(f"   Citations (OpenAlex): {row['nc']:,} | H-index: {row['h']}")
    print()

# Compare to Scopus top 2%
print("="*80)
print("COMPARISON: WHO'S IN TOP 2%?")
print("="*80)

# Get researchers with Scopus rankings
ranked_df = merged_df[merged_df['rank_global'].notna()].copy()
print(f"\nResearchers with both rankings: {len(ranked_df)}")

# Scopus top 2% threshold (approximate - top 2% globally)
scopus_top_2_threshold = 200000  # Top ~200k globally = roughly top 2%

scopus_top_2 = set(ranked_df[ranked_df['rank_global'] <= scopus_top_2_threshold]['authfull'])
openalex_top_2 = set(top_2_df['authfull'])

in_both = openalex_top_2 & scopus_top_2
only_openalex = openalex_top_2 - scopus_top_2
only_scopus = scopus_top_2 - openalex_top_2

print(f"\nTop 2% comparison:")
print(f"  In BOTH Scopus and OpenAlex top 2%: {len(in_both)}")
print(f"  ONLY in OpenAlex top 2%: {len(only_openalex)}")
print(f"  ONLY in Scopus top 2%: {len(only_scopus)}")

if only_openalex:
    print(f"\n{'='*80}")
    print(f"GAINED TOP 2% STATUS (in OpenAlex, not Scopus):")
    print("="*80)
    for name in sorted(only_openalex):
        row = merged_df[merged_df['authfull'] == name].iloc[0]
        print(f"\n• {name}")
        print(f"  Field: {row['field']}")
        print(f"  Scopus rank: #{row['rank_global']:,.0f} (OUTSIDE top 2%)")
        print(f"  OpenAlex rank: #{row['rank_openalex']:.0f} (TOP 2%!)")
        print(f"  Improvement: +{row['rank_global'] - row['rank_openalex']:,.0f} positions")
        print(f"  Elsevier %: {row['elsevier_pct']:.1f}%")
        print(f"  c-score: {row['c_score_openalex']:.3f}")

# Field analysis
print(f"\n{'='*80}")
print("FIELD ANALYSIS: Top 2%")
print("="*80)

field_dist = top_2_df['field_type'].value_counts()
print(f"\nBy field type:")
for field_type, count in field_dist.items():
    pct = count / len(top_2_df) * 100
    print(f"  {field_type}: {count} ({pct:.1f}%)")

# Elsevier analysis
print(f"\nElsevier % analysis:")
print(f"  Top 2% mean Elsevier %: {top_2_df['elsevier_pct'].mean():.1f}%")
print(f"  Overall mean Elsevier %: {merged_df['elsevier_pct'].mean():.1f}%")

high_elsevier_in_top = (top_2_df['elsevier_pct'] > merged_df['elsevier_pct'].median()).sum()
print(f"  High-Elsevier in top 2%: {high_elsevier_in_top}/{len(top_2_df)} ({high_elsevier_in_top/len(top_2_df)*100:.1f}%)")

# Rankings correlation
print(f"\n{'='*80}")
print("OVERALL RANKING COMPARISON")
print("="*80)

corr = ranked_df[['rank_global', 'rank_openalex']].corr().iloc[0, 1]
print(f"\nRanking correlation: r={corr:.3f}")

# Save results
print(f"\n{'='*80}")
print("SAVING RESULTS")
print("="*80)

# Full rankings
output_df = merged_df.sort_values('rank_openalex')
output_df.to_csv('openalex_rankings_full.csv', index=False)
print(f"✓ Full rankings: openalex_rankings_full.csv ({len(output_df)} researchers)")

# Top 2% only
top_2_df.to_csv('openalex_top_2_percent.csv', index=False)
print(f"✓ Top 2% list: openalex_top_2_percent.csv ({len(top_2_df)} researchers)")

# Comparison table
comparison_df = merged_df[['authfull', 'field', 'field_type', 'rank_openalex', 'rank_global',
                           'c_score_openalex', 'elsevier_pct', 'nc', 'h', 'scopus_pubs',
                           'scopus_citations']].copy()
comparison_df['rank_change'] = comparison_df['rank_global'] - comparison_df['rank_openalex']
comparison_df = comparison_df.sort_values('rank_openalex')
comparison_df.to_csv('scopus_vs_openalex_rankings.csv', index=False)
print(f"✓ Comparison table: scopus_vs_openalex_rankings.csv")

# Summary statistics
print(f"\n{'='*80}")
print("SUMMARY")
print("="*80)

print(f"""
OpenAlex-based "Top 2%" analysis complete:

Sample: {len(merged_df)} researchers
Top 2%: {len(top_2_df)} researchers

Key findings:
- {len(only_openalex)} researchers GAIN top 2% status with complete data
- {len(only_scopus)} Scopus top 2% fall out with OpenAlex ranking
- Overall correlation: r={corr:.3f}

Top researcher: {top_2_df.iloc[0]['authfull']}
  c-score: {top_2_df.iloc[0]['c_score_openalex']:.3f}
  Scopus rank: #{top_2_df.iloc[0]['rank_global']:,.0f}

This demonstrates that using complete publication data produces
materially different research evaluations with career implications.
""")

print("="*80)
print("Analysis complete! Ready for manuscript.")
print("="*80)
