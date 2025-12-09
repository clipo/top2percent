#!/usr/bin/env python3
"""
Generate Supplementary Figure S1: Sample Characteristics

Shows geographic and field distribution of the n=600 sample.

Output: figureS1_sample_characteristics.png
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
df = pd.read_csv(data_dir / "comprehensive_sample.csv")

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Field distribution
field_counts = df['field_type'].value_counts().sort_index()
colors = ['#D55E00', '#E69F00', '#0072B2']  # Colorblind-safe
labels = ['Book-heavy\n(n=198)', 'Mixed\n(n=210)', 'Journal-heavy\n(n=192)']

ax1.bar(range(len(field_counts)), field_counts.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax1.set_xticks(range(len(field_counts)))
ax1.set_xticklabels(labels, fontsize=11)
ax1.set_ylabel('Number of Researchers', fontsize=12, fontweight='bold')
ax1.set_title('A. Sample Distribution by Field Type', fontsize=13, fontweight='bold', pad=15)
ax1.set_ylim(0, 250)

# Add value labels on bars
for i, v in enumerate(field_counts.values):
    ax1.text(i, v + 5, str(v), ha='center', va='bottom', fontweight='bold', fontsize=11)

# Panel B: Geographic distribution
# Get top 10 countries
country_counts = df['country'].value_counts().head(10)

ax2.barh(range(len(country_counts)), country_counts.values, color='#0072B2', alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.set_yticks(range(len(country_counts)))
ax2.set_yticklabels(country_counts.index, fontsize=10)
ax2.set_xlabel('Number of Researchers', fontsize=12, fontweight='bold')
ax2.set_title('B. Geographic Distribution (Top 10 Countries)', fontsize=13, fontweight='bold', pad=15)
ax2.invert_yaxis()

# Add value labels
for i, v in enumerate(country_counts.values):
    ax2.text(v + 2, i, str(v), va='center', fontsize=10)

plt.tight_layout()

# Save
output_path = Path(__file__).parent.parent.parent / "figures" / "FigureS1_sample_characteristics.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure S1 saved: {output_path}")

# Print summary statistics
print(f"\nSample Summary:")
print(f"  Total: {len(df)} researchers")
print(f"  Field distribution: {dict(field_counts)}")
print(f"  Countries represented: {df['country'].nunique()}")
print(f"  Top 3 countries: {', '.join(country_counts.head(3).index)}")

plt.close()
