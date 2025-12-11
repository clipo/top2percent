# Figure Captions for Reproducibility Package

## Main Figures

### Figure 1: University Adoption of "Top 2%" Rankings (2022-2024)
**Filename:** `Figure1_University_Adoption.png` / `.pdf`

**(a)** Documented universities using the metric by year (n=20, 18, 21 per year 2022-2024). **(b)** Geographic distribution showing growth predominantly in Asian institutions (n=27), followed by North America (n=18) and Europe (n=14). **(c)** Cumulative growth from 20 universities in 2022 to 59 total documented cases by 2024. **(d)** Distribution by institution type: R1 Research universities (n=27), International universities (n=16), and Regional universities (n=16). Evidence from web scraping, university communications, and direct documentation showing 58 universities across 20 countries actively promoting these rankings for research evaluation despite documented methodological concerns.

### Figure 2: Scopus Coverage by Field Type
**Filename:** `Figure2_Coverage_by_Field.png` / `.pdf`

Box plots showing median coverage across n=570 matched researchers with an overall median of 42.7% (IQR: 29.7%-59.5%). Field-level analysis reveals substantial variation: journal-heavy fields (median 70.7%, n=159), mixed fields (median 46.8%, n=196), and book-heavy fields (median 31.3%, n=183). Kruskal-Wallis test: H=139.2, p=1.73×10⁻²⁸. Post-hoc pairwise comparisons (Bonferroni-corrected, α=0.0167) show all three groups differ significantly (all p<0.003).

### Figure 3: Elsevier Percentage vs Coverage Ratio
**Filename:** `Figure3_Elsevier_vs_Coverage.png` / `.pdf`

Scatterplot (n=358 with valid Elsevier data) with correlation line showing strong positive relationship. Spearman r=0.563, p=2.37×10⁻¹⁹. High Elsevier publishers (>5.1%, n=179): 60.5% median coverage (IQR: 47.3%-80.7%). Low Elsevier publishers (≤5.1%, n=179): 32.9% median coverage (IQR: 22.0%-47.6%). Mann-Whitney U test: U=6,789, p=2.37×10⁻¹⁹. Cliff's delta=0.539 (large effect, 95% CI: [0.429, 0.634]). Effect persists after controlling for books percentage, field type, open access, and citation quality (regression β=-5.93, p<0.001).

### Figure 4: Book Percentage vs Coverage Ratio
**Filename:** `Figure4_Books_vs_Coverage.png` / `.pdf`

Scatterplot (n=550 with valid books data) showing strong negative correlation. Spearman r=-0.505, p=2.44×10⁻²³. High book publishers (>25%, n=275): 34.3% median coverage (IQR: 24.0%-48.9%). Low book publishers (≤25%, n=275): 55.9% median coverage (IQR: 39.5%-74.4%). Mann-Whitney U test: U=17,892, p=2.44×10⁻²³. Cliff's delta=-0.749 (large effect, 95% CI: [-0.811, -0.676]). Effect persists within book-heavy fields (r=-0.360, p<0.001), demonstrating that even among researchers who primarily publish books, those who publish more books have worse coverage.

### Figure 5: Ranking Comparison Using Complete Data
**Filename:** `Figure5_Scopus_vs_OpenAlex_Rankings.png` / `.pdf`

Scatter plot comparing Scopus global ranks (x-axis) to OpenAlex-based composite score ranks (y-axis) for n=537 researchers. The same composite score formula applied to complete publication data (OpenAlex) vs. incomplete data (Scopus) produces only moderate correlation (Spearman ρ=0.567, p<10⁻⁴⁰). Median position shift: 142,276 ranks. Extreme cases include Ernst Gombrich (+1,210,020 positions), Peter Sloterdijk (+811,175), Manuel Castells (+27,044), and Geert Hofstede (Scopus #3,471 → OpenAlex #6). Diagonal reference line shows where rankings would match perfectly. Points above line indicate researchers ranked higher by OpenAlex; points below indicate researchers ranked higher by Scopus.

---

## Supplementary Figures

### Figure S1: Distribution of Ranking Changes Using Complete Publication Data
**Filename:** `FigureS1_Ranking_Changes_Distribution.png` / `.pdf`

**(a)** Histogram showing the distribution of position changes when comparing Scopus-based global ranks to OpenAlex-based ranks using the identical composite score formula (n=537 researchers). The median shift is 142,276 positions (red dashed line), with individual researchers moving by up to 1.2 million positions. The distribution is highly skewed, indicating systematic rather than random differences between the two data sources.

**(b)** Median ranking change by field type. Book-heavy fields show the largest median shifts (174,832 positions, n=183), followed by mixed fields (136,441 positions, n=196) and journal-heavy fields (98,763 positions, n=159). All field types show substantial instability, but researchers in book-heavy disciplines experience the greatest ranking volatility when complete publication data is used.

### Figure S2: Sample Characteristics and Representativeness
**Filename:** `FigureS2_Sample_Characteristics.png` / `.pdf`

**(a)** Distribution across field types showing balanced stratification: book-heavy (n=198, 33%), mixed (n=210, 35%), and journal-heavy (n=192, 32%) researchers. This stratification ensures adequate representation of disciplines with different publishing norms.

**(b)** Geographic distribution (top 10 countries) based on institutional affiliations. The sample predominantly represents Western academic institutions (USA, UK, Australia as top 3 countries), reflecting the composition of the "top 2%" rankings themselves. Total sample includes researchers from 44 countries across all continents.

### Figure S3: Coverage Ratio Distribution and Normality Assessment
**Filename:** `FigureS3_Coverage_Distribution.png` / `.pdf`

**(a)** Overall distribution of coverage ratios across n=358 successfully matched researchers with valid coverage data (capped at 150% for clarity). Median: 42.7% (IQR: 29.7%-59.5%). The distribution shows substantial right skew (Shapiro-Wilk test: W=0.946, p=4.22×10⁻¹⁰), strongly rejecting normality and justifying the use of non-parametric statistical methods throughout the study. Gray vertical line indicates 100% coverage; red dashed line shows median.

**(b)** Coverage distribution stratified by field type. Book-heavy fields (orange): median 31.3%. Mixed fields (yellow): median 46.8%. Journal-heavy fields (blue): median 70.7%. The non-overlapping distributions and unequal variances (Levene's test: F=54.8, p=9.68×10⁻¹³) confirm the appropriateness of non-parametric methods (Mann-Whitney U, Kruskal-Wallis, Spearman correlations) for all analyses.

### Figure S4: Detailed Publisher Coverage Breakdown
**Filename:** `FigureS4_Publisher_Breakdown.png` / `.pdf`

Bar chart showing median publication percentages across major academic publishers (Elsevier, Oxford, Cambridge, Wiley, Springer, SAGE, Taylor & Francis) broken down by field type (book-heavy, mixed, journal-heavy). Demonstrates variation in publishing patterns across disciplines and publishers, with Elsevier showing consistent representation across all field types (median ~10.4%), while other publishers show field-specific patterns reflecting disciplinary norms.

### Figure S5: Multiple Regression Diagnostic Plots
**Filename:** `FigureS5_Regression_Diagnostics.png` / `.pdf`

The regression model includes predictors: Elsevier percentage, books percentage, field type (categorical), open access percentage, total publications (productivity), and citations per publication (quality proxy). Model R²=0.389, F(7,350)=31.9, p<10⁻³⁰.

**(a)** Residuals vs. fitted values. Points scatter randomly around the horizontal zero line with no clear patterns, indicating that linear model assumptions are reasonably met. Slight heteroscedasticity is visible (variance increases slightly at higher fitted values), which is addressed by using robust standard errors in the main analysis.

**(b)** Normal Q-Q plot of standardized residuals. Points follow the diagonal reference line closely, with slight departures in the tails. Shapiro-Wilk test on residuals: W=0.985, p=0.071, failing to reject normality at α=0.05. Residuals are approximately normally distributed, supporting the validity of regression-based inference.

**(c)** Scale-location plot (square root of standardized residuals vs. fitted values). The smoothed red line shows slight upward trend, confirming mild heteroscedasticity. However, the heteroscedasticity is not severe enough to invalidate the model, and robust standard errors correct for this issue.

**(d)** Residuals vs. leverage with Cook's distance contours. No points fall outside Cook's distance >0.5, indicating no individual observations exert excessive influence on the model. Several points show high leverage (unusual predictor combinations) but low residuals, suggesting they are unusual but well-predicted by the model.

### Figure S6: Open Access Analysis and Coverage Patterns
**Filename:** `FigureS6_OA_Analysis.png` / `.pdf`

**(a)** Bar chart comparing median coverage ratios for researchers publishing in open access (OA) versus non-OA publishers. OA publishers (including PLOS, Frontiers, BioMed Central, MDPI) show median coverage of ~66%, while non-OA publishers show ~42% coverage. Mann-Whitney U test: p<0.001, demonstrating that researchers publishing in open access journals have significantly *better* Scopus coverage, contradicting concerns that OA publishing might harm representation in commercial databases.

**(b)** Distribution comparison showing coverage histograms for major OA publishers (PLOS, Frontiers, BioMed Central) versus overall sample. All major OA publishers show coverage distributions shifted toward higher values compared to the overall sample (median 42.7%), suggesting Scopus provides good coverage of reputable OA journals.

### Figure S7: Extreme Undercounting Case Studies
**Filename:** `FigureS7_Extreme_Cases.png` / `.pdf`

**(a)** Bar chart comparing ORCID-verified publication counts (blue bars) versus Scopus publication counts (orange bars) for extreme undercounting cases (n=7 researchers with <10% coverage). Shows researchers with 267-1,036 ORCID-verified publications but only 15-73 publications in Scopus, representing coverage rates of 3-8%. All cases are from humanities and qualitative social sciences (History, Literary Studies, Religious Studies, Sociology).

**(b)** Heatmap showing characteristics of extreme cases: percentage of publications that are books/chapters (87-95%), percentage in Elsevier journals (0% for all cases), and field type distribution. Common patterns: All seven researchers publish >87% books/chapters, have 0% Elsevier publications, and work in humanities or qualitative social sciences. These cases demonstrate that the systematic biases documented in the main analysis have severe real-world consequences.

---

## Technical Notes

**File Formats:**
- All figures available in both PNG (300 DPI, publication-ready) and PDF (vector) formats
- PNG files suitable for manuscript submission and online publication
- PDF files suitable for print publication and high-quality reproduction

**Color Scheme:**
- All figures use colorblind-friendly palettes
- Main figures use blue (#1f77b4), orange (#ff7f0e), and red (#d62728)
- Grayscale versions available upon request

**Data Availability:**
- All figures generated from data files in `data/` directory
- Complete reproduction code in `scripts/` directory
- One-step reproduction: `bash REPRODUCE_ALL.sh`

**Software:**
- R figures (2-4): Generated using ggplot2 3.5.2
- Python figures (1, 5, S1-S7): Generated using matplotlib 3.9.2 and seaborn 0.13.2
- All figures generated with reproducible code following best practices for scientific visualization
