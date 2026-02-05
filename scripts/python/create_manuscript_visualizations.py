"""
Create Publication-Ready Visualizations and Tables for Manuscript

Generates:
- Figure 5: Scatter plot of Scopus vs OpenAlex rankings
- Figure S1: Distribution of ranking changes
- Tables: Top 10 OpenAlex researchers, summary statistics, extreme cases
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path

# Set publication-quality style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

print("="*80)
print("CREATING MANUSCRIPT VISUALIZATIONS")
print("="*80)

# Set up paths relative to script location
script_dir = Path(__file__).parent
data_dir = script_dir / ".." / ".." / "data"
output_dir = script_dir / ".." / ".." / "figures"
tables_dir = script_dir / ".." / ".." / "tables"
tables_dir.mkdir(exist_ok=True)

# Load data
print("\nLoading comparison data...")
df = pd.read_csv(data_dir / 'scopus_vs_openalex_rankings.csv')
top_2_df = pd.read_csv(data_dir / 'openalex_top_2_percent.csv')

print(f"Total researchers: {len(df)}")
print(f"Top 2%: {len(top_2_df)}")

# =============================================================================
# FIGURE 1: Ranking Correlation Scatter Plot
# =============================================================================
print("\n" + "="*80)
print("FIGURE 1: Scopus vs OpenAlex Rankings")
print("="*80)

fig, ax = plt.subplots(figsize=(8, 6))

# Filter to researchers with both rankings
df_both = df[df['rank_global'].notna()].copy()

# Identify top 2% in each system
top_2_openalex = set(df_both.nsmallest(10, 'rank_openalex')['authfull'])
top_2_scopus = set(df_both[df_both['rank_global'] <= 200000]['authfull'])

# Create categories
df_both['category'] = 'Other'
df_both.loc[df_both['authfull'].isin(top_2_openalex), 'category'] = 'OpenAlex Top 2%'
df_both.loc[df_both['authfull'].isin(top_2_scopus) & ~df_both['authfull'].isin(top_2_openalex), 'category'] = 'Scopus Top 2% Only'

# Plot with log scale
colors = {'OpenAlex Top 2%': '#d62728', 'Scopus Top 2% Only': '#ff7f0e', 'Other': '#1f77b4'}
for category in ['Other', 'Scopus Top 2% Only', 'OpenAlex Top 2%']:
    mask = df_both['category'] == category
    ax.scatter(df_both.loc[mask, 'rank_global'],
              df_both.loc[mask, 'rank_openalex'],
              c=colors[category],
              label=category,
              alpha=0.6,
              s=50 if category == 'OpenAlex Top 2%' else 20)

# Add diagonal reference line (scaled to visible range)
# For different axis scales, show diagonal for equal PERCENTILE, not equal absolute rank
ax.plot([0, 300000], [0, 550], 'k--', alpha=0.5, linewidth=2, label='Equal Ranking', zorder=1)

# Label specific researchers mentioned in manuscript with manual positioning to avoid overlap
specific_researchers = {
    'Hofstede': (-70, -20),      # Top left corner
    'Castells': (10, 15),        # Early, mid-range
    'Fletcher': (-70, 15),       # Mid-range, avoid overlap
    'Buck-Morss': (10, -15),     # Mid-range, below
    'Rosenwein': (-70, 10),      # Right side, upper
    'Butler': (10, 15),          # Right side, mid
    'Crystal': (10, -20)         # Right side, lower
}

for name, text_offset in specific_researchers.items():
    match = df_both[df_both['authfull'].str.contains(name, case=False, na=False)]
    if len(match) > 0:
        row = match.iloc[0]
        ax.scatter(row['rank_global'], row['rank_openalex'],
                  s=120, c='red', marker='*', zorder=5, edgecolors='black', linewidths=1.5)
        # Abbreviate name for less clutter
        display_name = name.split()[-1] if len(name.split()) > 1 else name
        ax.annotate(f"{display_name}\n+{row['rank_change']/1000:.0f}K",
                   xy=(row['rank_global'], row['rank_openalex']),
                   xytext=text_offset, textcoords='offset points',
                   fontsize=6, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.25', facecolor='yellow', alpha=0.8, edgecolor='black', linewidth=0.5),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', lw=0.8, color='black'))

# Add annotation for Gombrich (off-scale)
ax.text(0.98, 0.35, 'Gombrich\n+1.21M\n(off scale →)',
        transform=ax.transAxes, ha='right', va='center',
        fontsize=6, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8, edgecolor='black', linewidth=0.5),
        zorder=10)

ax.set_xlabel('Scopus Global Rank', fontsize=12)
ax.set_ylabel('OpenAlex Rank (Composite Score)', fontsize=12)
ax.set_title('Comparison of Scopus vs OpenAlex-Based Rankings\n(n=537 researchers)', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', framealpha=0.9)
ax.set_xlim(0, 300000)
ax.set_ylim(0, 550)

# Add correlation text
corr = df_both[['rank_global', 'rank_openalex']].corr().iloc[0, 1]
ax.text(0.95, 0.05, f'Spearman ρ = {corr:.3f}',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(output_dir / 'Figure5_Scopus_vs_OpenAlex_Rankings.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'Figure5_Scopus_vs_OpenAlex_Rankings.pdf', bbox_inches='tight')
print("\n✓ Saved: Figure5_Scopus_vs_OpenAlex_Rankings.png")
print("✓ Saved: Figure5_Scopus_vs_OpenAlex_Rankings.pdf")

# =============================================================================
# FIGURE S1: Ranking Changes Distribution
# =============================================================================
print("\n" + "="*80)
print("FIGURE S1: Distribution of Ranking Changes")
print("="*80)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Histogram of rank changes
rank_changes = df_both['rank_change'].dropna()
ax1.hist(rank_changes, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
ax1.axvline(rank_changes.median(), color='red', linestyle='--', linewidth=2, label=f'Median: {rank_changes.median():.0f}')
ax1.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
ax1.set_xlabel('Rank Change (Scopus - OpenAlex)', fontsize=11)
ax1.set_ylabel('Number of Researchers', fontsize=11)
ax1.set_title('(a) Distribution of Ranking Changes', fontsize=12, fontweight='bold', loc='left')
ax1.legend()

# Field type breakdown
field_stats = df_both.groupby('field_type')['rank_change'].agg(['mean', 'median', 'count'])
field_stats = field_stats.sort_values('median', ascending=False)
ax2.barh(field_stats.index, field_stats['median'], color='steelblue', alpha=0.7)
ax2.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
ax2.set_xlabel('Median Rank Change', fontsize=11)
ax2.set_ylabel('Field Type', fontsize=11)
ax2.set_title('(b) Median Ranking Change by Field Type', fontsize=12, fontweight='bold', loc='left')

# Add counts
for i, (idx, row) in enumerate(field_stats.iterrows()):
    ax2.text(row['median'] + 1000, i, f"n={int(row['count'])}",
            va='center', fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / 'FigureS7_Ranking_Changes_Distribution.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'FigureS7_Ranking_Changes_Distribution.pdf', bbox_inches='tight')
print("\n✓ Saved: FigureS7_Ranking_Changes_Distribution.png")
print("✓ Saved: FigureS7_Ranking_Changes_Distribution.pdf")

# =============================================================================
# TABLE 1: Top 10 OpenAlex Researchers (LaTeX)
# =============================================================================
print("\n" + "="*80)
print("TABLE 1: Top 10 OpenAlex Researchers (LaTeX)")
print("="*80)

latex_table = r"""\begin{table}[htbp]
\centering
\caption{Top 10 Researchers by OpenAlex Composite Score}
\label{tab:openalex_top10}
\small
\begin{tabular}{@{}llrrrrr@{}}
\toprule
Researcher & Field & \multicolumn{2}{c}{Ranking} & c-score & Citations & Elsevier \\
           &       & OpenAlex & Scopus & (OA) & (OA) & \% \\
\midrule
"""

for idx, (_, row) in enumerate(top_2_df.iterrows(), 1):
    name = row['authfull']
    # Shorten field names for table
    field = row['field'].replace(' & ', ' \\& ')
    if len(field) > 25:
        field = field[:22] + '...'

    rank_oa = int(row['rank_openalex'])
    rank_sc = f"{int(row['rank_global']):,}" if pd.notna(row['rank_global']) else "---"
    c_score = row['c_score_openalex']
    citations = f"{int(row['nc']):,}"
    elsevier_pct = row['elsevier_pct']

    # Calculate rank change
    if pd.notna(row['rank_global']):
        change = int(row['rank_global'] - row['rank_openalex'])
        change_str = f"(+{change:,})" if change > 0 else f"({change:,})"
    else:
        change_str = ""

    latex_table += f"{name} & {field} & {rank_oa} & {rank_sc} {change_str} & {c_score:.2f} & {citations} & {elsevier_pct:.1f}\\% \\\\\n"

latex_table += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\small
\item Note: Ranking change shows positions gained (+) or lost (-) relative to Scopus.
\item c-score calculated using Ioannidis formula applied to OpenAlex data.
\item Elsevier \% indicates proportion of publications in Elsevier-owned journals.
\end{tablenotes}
\end{table}
"""

with open(tables_dir / 'table_openalex_top10.tex', 'w') as f:
    f.write(latex_table)

print("\n✓ Saved: table_openalex_top10.tex")
print("\nPreview:")
print(latex_table)

# =============================================================================
# TABLE 2: Summary Statistics (CSV + LaTeX)
# =============================================================================
print("\n" + "="*80)
print("TABLE 2: Summary Statistics")
print("="*80)

summary_stats = pd.DataFrame({
    'Metric': [
        'Total Researchers',
        'Mean Scopus Rank',
        'Mean OpenAlex Rank',
        'Median Rank Change',
        'Mean Rank Change',
        'Max Rank Improvement',
        'Ranking Correlation (ρ)',
        '',
        'Top 2% OpenAlex (n=10):',
        '  Mean Elsevier %',
        '  Mean Citations',
        '  Mean h-index',
        '',
        'Overall Sample:',
        '  Mean Elsevier %',
        '  Mean Citations',
        '  Mean h-index'
    ],
    'Value': [
        f"{len(df_both)}",
        f"{df_both['rank_global'].mean():,.0f}",
        f"{df_both['rank_openalex'].mean():.0f}",
        f"{df_both['rank_change'].median():,.0f}",
        f"{df_both['rank_change'].mean():,.0f}",
        f"{df_both['rank_change'].max():,.0f} ({df_both.loc[df_both['rank_change'].idxmax(), 'authfull']})",
        f"{corr:.3f}",
        "",
        "",
        f"{top_2_df['elsevier_pct'].mean():.1f}%",
        f"{top_2_df['nc'].mean():,.0f}",
        f"{top_2_df['h'].mean():.0f}",
        "",
        "",
        f"{df_both['elsevier_pct'].mean():.1f}%",
        f"{df_both['nc'].mean():,.0f}",
        f"{df_both['h'].mean():.0f}"
    ]
})

summary_stats.to_csv(tables_dir / 'table_summary_statistics.csv', index=False)
print("\n✓ Saved: table_summary_statistics.csv")
print("\nSummary Statistics:")
print(summary_stats.to_string(index=False))

# =============================================================================
# EXTREME CASES ANALYSIS
# =============================================================================
print("\n" + "="*80)
print("EXTREME CASES: Largest Ranking Improvements")
print("="*80)

extreme_df = df_both.nlargest(10, 'rank_change')[['authfull', 'field', 'rank_openalex',
                                                    'rank_global', 'rank_change',
                                                    'c_score_openalex', 'elsevier_pct',
                                                    'nc', 'h']]

extreme_df.to_csv(tables_dir / 'extreme_ranking_improvements.csv', index=False)
print("\n✓ Saved: extreme_ranking_improvements.csv")
print("\nTop 10 Ranking Improvements:")
for idx, (_, row) in enumerate(extreme_df.iterrows(), 1):
    print(f"\n{idx}. {row['authfull']}")
    print(f"   Field: {row['field']}")
    print(f"   Scopus rank: #{row['rank_global']:,.0f} → OpenAlex rank: #{row['rank_openalex']:.0f}")
    print(f"   Improvement: +{row['rank_change']:,.0f} positions")
    print(f"   Elsevier %: {row['elsevier_pct']:.1f}%")
    print(f"   Citations: {row['nc']:,} | h-index: {row['h']:.0f}")

# =============================================================================
# FIELD ANALYSIS
# =============================================================================
print("\n" + "="*80)
print("FIELD DISTRIBUTION ANALYSIS")
print("="*80)

# Compare field types in top 2% vs overall
print("\nField Type Distribution:")
print("\nTop 2% OpenAlex:")
top_2_fields = top_2_df['field_type'].value_counts()
for ft, count in top_2_fields.items():
    pct = count / len(top_2_df) * 100
    print(f"  {ft}: {count} ({pct:.1f}%)")

print("\nOverall Sample:")
overall_fields = df_both['field_type'].value_counts()
for ft, count in overall_fields.items():
    pct = count / len(df_both) * 100
    print(f"  {ft}: {count} ({pct:.1f}%)")

# Elsevier analysis
print("\n" + "="*80)
print("ELSEVIER COVERAGE ANALYSIS")
print("="*80)

print(f"\nTop 2% mean Elsevier %: {top_2_df['elsevier_pct'].mean():.1f}%")
print(f"Overall mean Elsevier %: {df_both['elsevier_pct'].mean():.1f}%")
print(f"Difference: {df_both['elsevier_pct'].mean() - top_2_df['elsevier_pct'].mean():.1f} percentage points")

# T-test
from scipy import stats
t_stat, p_val = stats.ttest_ind(top_2_df['elsevier_pct'], df_both['elsevier_pct'])
print(f"\nt-test: t={t_stat:.3f}, p={p_val:.4f}")

# =============================================================================
# SAVE ALL FIGURES
# =============================================================================
print("\n" + "="*80)
print("COMPLETE")
print("="*80)

print("\nGenerated files:")
print("  Figures:")
print("    - figure_scopus_vs_openalex_rankings.png/pdf")
print("    - figure_ranking_changes.png/pdf")
print("\n  Tables:")
print("    - table_openalex_top10.tex")
print("    - table_summary_statistics.csv")
print("    - extreme_ranking_improvements.csv")

print("\nAll visualizations ready for manuscript!")
