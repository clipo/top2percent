#!/usr/bin/env python3
"""
Generate Supplementary Figure S5: Open Access Publisher Analysis

Detailed breakdown of coverage by open access publishers.

Output: figureS5_oa_analysis.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from scipy import stats

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

# Load data
data_dir = Path(__file__).parent.parent.parent / "data"
df = pd.read_csv(data_dir / "openalex_comprehensive_data.csv")

# Filter to matched researchers
df = df[df['openalex_found'] == True].copy()

# Clean data
df = df[df['coverage_ratio'].notna() & (df['coverage_ratio'] <= 1.5)]

# Create figure with 2 panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel A: OA Publisher Comparison
oa_publishers = [
    ('plos', 'PLOS'),
    ('frontiers', 'Frontiers'),
    ('mdpi', 'MDPI')
]

comparison_data = []
for pub_col, label in oa_publishers:
    count_col = f'{pub_col}_count'
    if count_col in df.columns:
        # Define high vs low threshold (has any publications)
        has_pub = df[df[count_col] > 0]
        no_pub = df[df[count_col] == 0]

        if len(has_pub) > 10 and len(no_pub) > 10:
            median_with = has_pub['coverage_ratio'].median()
            median_without = no_pub['coverage_ratio'].median()
            diff = median_with - median_without

            # Statistical test
            u_stat, p_val = stats.mannwhitneyu(has_pub['coverage_ratio'],
                                               no_pub['coverage_ratio'],
                                               alternative='two-sided')

            comparison_data.append({
                'Publisher': label,
                'With Publisher': median_with,
                'Without Publisher': median_without,
                'Difference': diff,
                'p_value': p_val,
                'n_with': len(has_pub),
                'n_without': len(no_pub)
            })

comp_df = pd.DataFrame(comparison_data)

# Add overall OA analysis
if 'oa_publisher_pct' in df.columns:
    has_oa = df[df['oa_publisher_pct'] > 0]
    no_oa = df[df['oa_publisher_pct'] == 0]
    if len(has_oa) > 10 and len(no_oa) > 10:
        u_stat, p_val = stats.mannwhitneyu(has_oa['coverage_ratio'],
                                           no_oa['coverage_ratio'],
                                           alternative='two-sided')
        comp_df = pd.concat([comp_df, pd.DataFrame([{
            'Publisher': 'Any OA Publisher',
            'With Publisher': has_oa['coverage_ratio'].median(),
            'Without Publisher': no_oa['coverage_ratio'].median(),
            'Difference': has_oa['coverage_ratio'].median() - no_oa['coverage_ratio'].median(),
            'p_value': p_val,
            'n_with': len(has_oa),
            'n_without': len(no_oa)
        }])], ignore_index=True)

# Create grouped bar chart
x = np.arange(len(comp_df))
width = 0.35

bars1 = ax1.bar(x - width/2, comp_df['With Publisher'], width,
                label='With Publisher', color='#009E73', alpha=0.8,
                edgecolor='black', linewidth=1)
bars2 = ax1.bar(x + width/2, comp_df['Without Publisher'], width,
                label='Without Publisher', color='#D55E00', alpha=0.8,
                edgecolor='black', linewidth=1)

ax1.set_xlabel('Open Access Publisher', fontsize=12, fontweight='bold')
ax1.set_ylabel('Median Coverage Ratio', fontsize=12, fontweight='bold')
ax1.set_title('A. Coverage by Open Access Publisher', fontsize=13, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(comp_df['Publisher'], fontsize=10)
ax1.legend(fontsize=10)
ax1.set_ylim(0, max(comp_df['With Publisher'].max(), comp_df['Without Publisher'].max()) * 1.15)

# Add significance stars
for i, row in comp_df.iterrows():
    if row['p_value'] < 0.001:
        sig = '***'
    elif row['p_value'] < 0.01:
        sig = '**'
    elif row['p_value'] < 0.05:
        sig = '*'
    else:
        sig = 'n.s.'

    y_pos = max(row['With Publisher'], row['Without Publisher']) + 0.03
    ax1.text(i, y_pos, sig, ha='center', va='bottom', fontweight='bold', fontsize=11)

# Add difference labels
for i, row in comp_df.iterrows():
    diff_text = f"+{row['Difference']:.1%}" if row['Difference'] > 0 else f"{row['Difference']:.1%}"
    ax1.text(i, 0.02, diff_text, ha='center', va='bottom', fontsize=8,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))

# Panel B: Distribution comparison for PLOS and Frontiers
if 'plos_count' in df.columns and 'frontiers_count' in df.columns:
    # PLOS
    plos_yes = df[df['plos_count'] > 0]['coverage_ratio']
    plos_no = df[df['plos_count'] == 0]['coverage_ratio']

    # Frontiers
    frontiers_yes = df[df['frontiers_count'] > 0]['coverage_ratio']
    frontiers_no = df[df['frontiers_count'] == 0]['coverage_ratio']

    # Create violin plots
    positions = [1, 2, 4, 5]
    data_to_plot = [plos_yes, plos_no, frontiers_yes, frontiers_no]
    colors = ['#009E73', '#D55E00', '#009E73', '#D55E00']

    parts = ax2.violinplot(data_to_plot, positions=positions, widths=0.7,
                           showmeans=True, showmedians=True)

    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[i])
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')

    # Customize median and mean lines
    parts['cmedians'].set_color('red')
    parts['cmedians'].set_linewidth(2)
    parts['cmeans'].set_color('blue')
    parts['cmeans'].set_linewidth(1.5)

    ax2.set_xticks([1.5, 4.5])
    ax2.set_xticklabels(['PLOS', 'Frontiers'], fontsize=11, fontweight='bold')
    ax2.set_ylabel('Coverage Ratio', fontsize=12, fontweight='bold')
    ax2.set_title('B. Distribution Comparison for Major OA Publishers', fontsize=13, fontweight='bold', pad=15)
    ax2.axhline(1.0, color='gray', linestyle=':', linewidth=1.5, alpha=0.5, label='100% coverage')

    # Add custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#009E73', lw=4, label='With Publisher'),
        Line2D([0], [0], color='#D55E00', lw=4, label='Without Publisher'),
        Line2D([0], [0], color='red', lw=2, label='Median'),
        Line2D([0], [0], color='blue', lw=1.5, label='Mean')
    ]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=9)

plt.tight_layout()

# Save
output_path = Path(__file__).parent.parent.parent / "figures" / "FigureS5_oa_analysis.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure S5 saved: {output_path}")

# Print summary table
print(f"\nOpen Access Publisher Analysis:")
print(comp_df[['Publisher', 'With Publisher', 'Without Publisher', 'Difference', 'p_value', 'n_with']].to_string(index=False))
print(f"\n*** p < 0.001, ** p < 0.01, * p < 0.05, n.s. = not significant")

plt.close()
