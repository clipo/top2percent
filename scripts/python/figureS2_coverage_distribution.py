#!/usr/bin/env python3
"""
Generate Supplementary Figure S3: Coverage Distribution

Shows histogram of coverage ratios with field-specific distributions.

Output: figureS2_coverage_distribution.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 300

# Load data
data_dir = Path(__file__).parent.parent.parent / "data"
df = pd.read_csv(data_dir / "openalex_comprehensive_data.csv")

# Filter to matched researchers
df = df[df['openalex_found'] == True].copy()

# Clean data
df = df[df['coverage_ratio'].notna() & (df['coverage_ratio'] <= 1.5)]

# Create figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Panel A: Overall distribution
ax1.hist(df['coverage_ratio'], bins=50, color='#0072B2', alpha=0.7, edgecolor='black', linewidth=0.5)
ax1.axvline(df['coverage_ratio'].median(), color='red', linestyle='--', linewidth=2, label=f'Median: {df["coverage_ratio"].median():.1%}')
ax1.axvline(1.0, color='gray', linestyle=':', linewidth=2, label='100% coverage')
ax1.set_xlabel('Coverage Ratio (Scopus/OpenAlex)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Researchers', fontsize=12, fontweight='bold')
ax1.set_title('(a) Overall Coverage Distribution', fontsize=13, fontweight='bold', loc='left', pad=15)
ax1.legend(fontsize=11)
ax1.set_xlim(0, 1.5)

# Add text with statistics
stats_text = f"n = {len(df)}\nMedian = {df['coverage_ratio'].median():.1%}\nMean = {df['coverage_ratio'].mean():.1%}\nSD = {df['coverage_ratio'].std():.2f}"
ax1.text(0.98, 0.97, stats_text, transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Panel B: By field type
field_types = ['book_heavy', 'mixed', 'journal_heavy']
field_labels = ['Book-heavy', 'Mixed', 'Journal-heavy']
colors = ['#D55E00', '#E69F00', '#0072B2']

for ft, label, color in zip(field_types, field_labels, colors):
    data_subset = df[df['field_type'] == ft]['coverage_ratio']
    ax2.hist(data_subset, bins=30, alpha=0.5, label=f'{label} (median={data_subset.median():.1%}, n={len(data_subset)})',
             color=color, edgecolor='black', linewidth=0.5)

ax2.axvline(1.0, color='gray', linestyle=':', linewidth=2, label='100% coverage')
ax2.set_xlabel('Coverage Ratio (Scopus/OpenAlex)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Researchers', fontsize=12, fontweight='bold')
ax2.set_title('(b) Coverage Distribution by Field Type', fontsize=13, fontweight='bold', loc='left', pad=15)
ax2.legend(fontsize=10, loc='upper right')
ax2.set_xlim(0, 1.5)

plt.tight_layout()

# Save
output_path = Path(__file__).parent.parent.parent / "figures" / "FigureS3_Coverage_Distribution.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure S3 saved: {output_path}")

# Print summary
print(f"\nCoverage Statistics by Field:")
for ft, label in zip(field_types, field_labels):
    data_subset = df[df['field_type'] == ft]['coverage_ratio']
    print(f"  {label:15s}: median={data_subset.median():.1%}, mean={data_subset.mean():.1%}, n={len(data_subset)}")

plt.close()
