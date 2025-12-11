#!/usr/bin/env python3
"""
Generate Supplementary Figure S7: Extreme Undercounting Cases

Detailed profiles of the 7 researchers with 300+ publications and ≤10% coverage.

Output: figureS6_extreme_cases.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

# Load data
data_dir = Path(__file__).parent.parent.parent / "data"
df = pd.read_csv(data_dir / "openalex_comprehensive_data.csv")

# Filter to matched researchers
df = df[df['openalex_found'] == True].copy()

# Identify extreme cases: 300+ publications, ≤10% coverage
extreme_cases = df[
    (df['total_works'] >= 300) &
    (df['coverage_ratio'] <= 0.10)
].copy()

# Sort by number of publications (descending)
extreme_cases = extreme_cases.sort_values('total_works', ascending=False)

print(f"\nFound {len(extreme_cases)} extreme cases (300+ pubs, ≤10% coverage)")

# Create figure with 2 panels
fig = plt.figure(figsize=(14, 10))

# Panel A: Bar chart showing publication counts
ax1 = plt.subplot(2, 1, 1)

if len(extreme_cases) > 0:
    # Create labels with name and field
    labels = []
    for _, row in extreme_cases.iterrows():
        name = row['authfull'] if 'authfull' in row else row.get('name', 'Unknown')
        field = row.get('sm-subfield-1', row.get('field', 'Unknown'))
        labels.append(f"{name}\n({field})")

    x = np.arange(len(extreme_cases))
    width = 0.35

    # OpenAlex publications
    bars1 = ax1.bar(x - width/2, extreme_cases['total_works'], width,
                    label='OpenAlex Publications', color='#0072B2', alpha=0.8,
                    edgecolor='black', linewidth=1.5)

    # Scopus publications
    bars2 = ax1.bar(x + width/2, extreme_cases['scopus_pubs'], width,
                    label='Scopus Publications', color='#D55E00', alpha=0.8,
                    edgecolor='black', linewidth=1.5)

    ax1.set_xlabel('Researcher', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Publications', fontsize=12, fontweight='bold')
    ax1.set_title('(a) Publication Counts for Extreme Undercounting Cases', fontsize=13, fontweight='bold', loc='left', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=9, rotation=0, ha='center')
    ax1.legend(fontsize=11, loc='upper right')
    ax1.set_ylim(0, extreme_cases['total_works'].max() * 1.1)

    # Add coverage percentage labels on Scopus bars
    for i, (idx, row) in enumerate(extreme_cases.iterrows()):
        coverage = row['coverage_ratio'] * 100
        ax1.text(i + width/2, row['scopus_pubs'] + 20, f"{coverage:.1f}%",
                ha='center', va='bottom', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

    # Add value labels on bars
    for i, (idx, row) in enumerate(extreme_cases.iterrows()):
        # OpenAlex
        ax1.text(i - width/2, row['total_works'] + 10,
                str(int(row['total_works'])),
                ha='center', va='bottom', fontsize=8)
        # Scopus
        ax1.text(i + width/2, row['scopus_pubs'] + 10,
                str(int(row['scopus_pubs'])),
                ha='center', va='bottom', fontsize=8, color='#D55E00')

# Panel B: Stacked bar showing publisher breakdown
ax2 = plt.subplot(2, 1, 2)

if len(extreme_cases) > 0:
    # Get publisher percentages
    publishers = ['elsevier', 'wiley', 'springer', 'oxford', 'cambridge']
    publisher_labels = ['Elsevier', 'Wiley', 'Springer', 'Oxford', 'Cambridge']
    colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#CC79A7']

    # Create stacked data
    bottom = np.zeros(len(extreme_cases))

    for pub, label, color in zip(publishers, publisher_labels, colors):
        pct_col = f'{pub}_pct'
        if pct_col in extreme_cases.columns:
            values = extreme_cases[pct_col].fillna(0).values * 100  # Convert to percentage
            ax2.bar(x, values, width=0.7, bottom=bottom, label=label,
                   color=color, alpha=0.8, edgecolor='black', linewidth=1)
            bottom += values

    # Add "Other" category
    other = 100 - bottom
    ax2.bar(x, other, width=0.7, bottom=bottom, label='Other',
           color='#999999', alpha=0.6, edgecolor='black', linewidth=1)

    ax2.set_xlabel('Researcher', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Publisher Distribution (%)', fontsize=12, fontweight='bold')
    ax2.set_title('(b) Publisher Breakdown for Extreme Cases', fontsize=13, fontweight='bold', loc='left', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9, rotation=0, ha='center')
    ax2.legend(fontsize=9, loc='upper right', ncol=2)
    ax2.set_ylim(0, 100)

plt.tight_layout()

# Save
output_path = Path(__file__).parent.parent.parent / "figures" / "FigureS6_Extreme_Cases.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure S7 saved: {output_path}")

# Print detailed table
print(f"\nExtreme Undercounting Cases (300+ publications, ≤10% coverage):")
print("=" * 100)

if len(extreme_cases) > 0:
    for idx, row in extreme_cases.iterrows():
        name = row['authfull'] if 'authfull' in row else row.get('name', 'Unknown')
        field = row.get('field', 'Unknown')
        oa_pubs = int(row['total_works'])
        scopus_pubs = int(row['scopus_pubs'])
        coverage = row['coverage_ratio'] * 100

        print(f"\n{name} ({field})")
        print(f"  OpenAlex: {oa_pubs:,} publications")
        print(f"  Scopus: {scopus_pubs:,} publications")
        print(f"  Coverage: {coverage:.1f}%")

        # Publisher breakdown
        print(f"  Publisher breakdown:")
        for pub, label in zip(publishers, publisher_labels):
            pct_col = f'{pub}_pct'
            if pct_col in row and pd.notna(row[pct_col]) and row[pct_col] > 0:
                print(f"    {label}: {row[pct_col]*100:.1f}%")
else:
    print("No extreme cases found matching criteria.")

plt.close()
