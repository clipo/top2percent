#!/usr/bin/env python3
"""
Generate Supplementary Figure S4: Regression Diagnostics

Shows diagnostic plots for the multivariate regression model.

Output: figureS4_regression_diagnostics.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import statsmodels.api as sm
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

# Prepare regression variables
df['book_heavy'] = (df['field_type'] == 'book_heavy').astype(int)
df['mixed'] = (df['field_type'] == 'mixed').astype(int)

# Create independent variables
X = pd.DataFrame({
    'elsevier_pct': df['elsevier_pct'].fillna(0),
    'book_pct': df['books_pct'].fillna(0),
    'book_heavy': df['book_heavy'],
    'mixed': df['mixed'],
    'log_publications': np.log1p(df['total_works'])
})

# Add constant
X = sm.add_constant(X)

# Dependent variable
y = df['coverage_ratio']

# Fit model
model = sm.OLS(y, X).fit()

# Get predictions and residuals
predictions = model.predict(X)
residuals = model.resid
standardized_residuals = (residuals - residuals.mean()) / residuals.std()

# Create figure with 4 panels
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Panel A: Residuals vs Fitted
ax1 = axes[0, 0]
ax1.scatter(predictions, residuals, alpha=0.5, s=20, color='#0072B2', edgecolors='none')
ax1.axhline(0, color='red', linestyle='--', linewidth=2)
ax1.set_xlabel('Fitted Values', fontsize=11, fontweight='bold')
ax1.set_ylabel('Residuals', fontsize=11, fontweight='bold')
ax1.set_title('A. Residuals vs Fitted Values', fontsize=12, fontweight='bold', pad=15)

# Add loess smooth
from scipy.signal import savgol_filter
sorted_indices = np.argsort(predictions)
sorted_predictions = predictions.iloc[sorted_indices]
sorted_residuals = residuals.iloc[sorted_indices]
if len(sorted_residuals) > 51:
    smoothed = savgol_filter(sorted_residuals, window_length=51, polyorder=3)
    ax1.plot(sorted_predictions, smoothed, color='blue', linewidth=2)

# Panel B: Q-Q Plot
ax2 = axes[0, 1]
stats.probplot(standardized_residuals, dist="norm", plot=ax2)
ax2.set_title('B. Normal Q-Q Plot', fontsize=12, fontweight='bold', pad=15)
ax2.set_xlabel('Theoretical Quantiles', fontsize=11, fontweight='bold')
ax2.set_ylabel('Standardized Residuals', fontsize=11, fontweight='bold')

# Panel C: Scale-Location
ax3 = axes[1, 0]
sqrt_abs_resid = np.sqrt(np.abs(standardized_residuals))
ax3.scatter(predictions, sqrt_abs_resid, alpha=0.5, s=20, color='#0072B2', edgecolors='none')
ax3.set_xlabel('Fitted Values', fontsize=11, fontweight='bold')
ax3.set_ylabel('√|Standardized Residuals|', fontsize=11, fontweight='bold')
ax3.set_title('C. Scale-Location Plot', fontsize=12, fontweight='bold', pad=15)

# Add loess smooth
sorted_sqrt_resid = sqrt_abs_resid.iloc[sorted_indices]
if len(sorted_sqrt_resid) > 51:
    smoothed_sqrt = savgol_filter(sorted_sqrt_resid, window_length=51, polyorder=3)
    ax3.plot(sorted_predictions, smoothed_sqrt, color='red', linewidth=2)

# Panel D: Residuals Histogram
ax4 = axes[1, 1]
ax4.hist(standardized_residuals, bins=50, color='#0072B2', alpha=0.7, edgecolor='black', linewidth=0.5)
ax4.axvline(0, color='red', linestyle='--', linewidth=2)
x_range = np.linspace(standardized_residuals.min(), standardized_residuals.max(), 100)
ax4.plot(x_range, stats.norm.pdf(x_range) * len(standardized_residuals) *
         (standardized_residuals.max() - standardized_residuals.min()) / 50,
         color='red', linewidth=2, label='Normal distribution')
ax4.set_xlabel('Standardized Residuals', fontsize=11, fontweight='bold')
ax4.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax4.set_title('D. Distribution of Residuals', fontsize=12, fontweight='bold', pad=15)
ax4.legend(fontsize=9)

plt.tight_layout()

# Save
output_path = Path(__file__).parent.parent.parent / "figures" / "FigureS4_regression_diagnostics.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure S4 saved: {output_path}")

# Print regression summary
print(f"\nRegression Model Summary:")
print(f"  R²: {model.rsquared:.3f}")
print(f"  Adjusted R²: {model.rsquared_adj:.3f}")
print(f"  F-statistic: {model.fvalue:.2f} (p < 0.001)")
print(f"\nCoefficients:")
for var in X.columns:
    if var != 'const':
        coef = model.params[var]
        pval = model.pvalues[var]
        print(f"  {var:20s}: β = {coef:+.4f}, p = {pval:.4f}")

plt.close()
