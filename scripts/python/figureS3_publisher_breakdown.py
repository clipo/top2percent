#!/usr/bin/env python3
"""
Generate Supplementary Figure S3: Publisher Breakdown by Field

Shows publisher distribution across field types.

Output: figureS3_publisher_breakdown.png
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

# Calculate publisher percentages by field type
publishers = ['elsevier', 'wiley', 'springer', 'oxford', 'cambridge']
field_types = ['book_heavy', 'mixed', 'journal_heavy']
field_labels = ['Book-heavy', 'Mixed', 'Journal-heavy']

# Create summary data
summary_data = []
for field in field_types:
    field_data = df[df['field_type'] == field]
    for pub in publishers:
        pct_col = f'{pub}_pct'
        if pct_col in field_data.columns:
            median_pct = field_data[pct_col].median()
            summary_data.append({
                'field': field,
                'publisher': pub.capitalize(),
                'median_pct': median_pct
            })

summary_df = pd.DataFrame(summary_data)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Pivot for grouped bar chart
pivot_df = summary_df.pivot(index='publisher', columns='field', values='median_pct')
pivot_df = pivot_df.reindex(['Elsevier', 'Wiley', 'Springer', 'Oxford', 'Cambridge'])

# Create bar chart
x = np.arange(len(pivot_df.index))
width = 0.25
colors = ['#D55E00', '#E69F00', '#0072B2']

for i, (field, label, color) in enumerate(zip(field_types, field_labels, colors)):
    offset = width * (i - 1)
    values = pivot_df[field].values
    bars = ax.bar(x + offset, values, width, label=label, color=color, alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        if height > 0.5:  # Only label if visible
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

ax.set_xlabel('Publisher', fontsize=12, fontweight='bold')
ax.set_ylabel('Median % of Publications', fontsize=12, fontweight='bold')
ax.set_title('Publisher Distribution by Field Type', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(pivot_df.index, fontsize=11)
ax.legend(title='Field Type', fontsize=10, title_fontsize=11)
ax.set_ylim(0, max(pivot_df.max()) * 1.2)

plt.tight_layout()

# Save
output_path = Path(__file__).parent.parent.parent / "figures" / "FigureS3_publisher_breakdown.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure S3 saved: {output_path}")

# Print summary table
print(f"\nPublisher Distribution by Field (Median %):")
print(pivot_df.to_string())

plt.close()
