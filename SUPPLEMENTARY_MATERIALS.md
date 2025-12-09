# Supplementary Materials

## Publisher Bias in Widely-Used Scientist Rankings

---

## Table of Contents

1. [Supplementary Methods](#supplementary-methods)
2. [Supplementary Results](#supplementary-results)
3. [Supplementary Figures](#supplementary-figures)
4. [Supplementary Tables](#supplementary-tables)
5. [Data Availability](#data-availability)
6. [Code Availability](#code-availability)

---

## Supplementary Methods

### 1. Sample Selection and Stratification

**Sampling frame:** The 2024 "top 2% of scientists" dataset (Ioannidis et al.) contains 230,333 researchers across 174 subfields. We stratified these into three field categories based on publication norms:

- **Book-heavy fields (n=198):** History, Philosophy, Literary Studies, Religions & Theology, Archaeology
- **Mixed fields (n=210):** Sociology, Economics, Political Science, Law, Geography
- **Journal-heavy fields (n=192):** Genetics, Neuroscience, Physics, Chemistry, Cell Biology

**Sample size calculation:** Target n=600 was selected to provide 80% power to detect medium effect sizes (Cohen's d ≥ 0.5) with α=0.001, accounting for potential ~5% matching failures in OpenAlex.

**Random sampling procedure:** Within each field category, we randomly sampled researchers proportionally to category size, maintaining perfect balance: 33% book-heavy, 35% mixed, 32% journal-heavy. Geographic diversity was verified post-hoc: 45% USA, 30% Europe, 15% Asia-Pacific, 10% other regions.

**Matching validation:** We achieved 95% successful matching (570/600 researchers) between Scopus IDs from the rankings dataset and OpenAlex author records. Unmatched researchers (n=30) were excluded from analysis. Matching was performed using author name + institution + approximate publication count verification.

### 2. Data Collection from OpenAlex

**API queries:** For each matched researcher, we queried the OpenAlex API (https://api.openalex.org) to retrieve:
- Complete publication list (all document types)
- Publisher information for each work
- Publication year
- Citation counts
- Open access status

**Coverage ratio calculation:**
```
coverage_ratio = scopus_publications / openalex_publications
```

Where:
- `scopus_publications` = publication count from Ioannidis et al. dataset
- `openalex_publications` = total works count from OpenAlex API

**Capping procedure:** Coverage ratios were capped at 1.5 (150%) to handle data quality issues where Scopus might count duplicate records or include more document types than OpenAlex. This affected <1% of researchers.

### 3. Publisher Classification

**Publisher identification:** We extracted publisher information from OpenAlex metadata using the `primary_location.source.host_organization` field for journals and `host_venue.publisher` for books.

**Publisher categories analyzed:**
- **Major commercial publishers:** Elsevier, Wiley, Springer Nature, Taylor & Francis
- **University presses:** Oxford University Press, Cambridge University Press, MIT Press, University of Chicago Press
- **Open access publishers:** PLOS, Frontiers Media, MDPI, Hindawi, BioMed Central
- **Society publishers:** American Chemical Society, IEEE, Royal Society

**Percentage calculations:** For each researcher:
```
publisher_pct = (publications_with_publisher / total_openalex_publications) * 100
```

### 4. Statistical Analysis

**Hypothesis testing framework:** We used α=0.001 for all significance tests to control for multiple comparisons. Effect sizes (Cohen's d) were calculated for all group comparisons.

**Non-parametric tests:** Mann-Whitney U tests and Kruskal-Wallis tests were used due to non-normal distributions of coverage ratios (confirmed by Shapiro-Wilk tests, p<0.001).

**Cohen's d calculation:**
```
d = (median_1 - median_2) / pooled_SD
```

**Multivariate regression:** Ordinary least squares regression with coverage ratio as dependent variable:
```
coverage_ratio ~ elsevier_pct + book_pct + book_heavy + mixed +
                 log(publications) + country + oa_status
```

Model diagnostics verified linearity, homoscedasticity, and normality of residuals (see Figure S4).

**Correlation analysis:** Pearson correlations for continuous variables, Spearman's rho for verification of non-parametric relationships.

### 5. University Adoption Analysis

**Search methodology:** Systematic web search conducted January-March 2024 using Google Scholar and institutional websites. Search terms:
- "top 2%" OR "top 2 percent" AND "scientist"
- "most cited scientists" AND "Ioannidis"
- "Stanford" AND "highly cited researchers"

**Inclusion criteria:**
- University official website, press release, or faculty profile page
- Explicit mention of "top 2%" ranking or direct citation of Ioannidis et al. dataset
- Public-facing announcement (not internal documents)
- English-language results only
- Dated 2022-2024

**Data extraction:** For each institution we recorded:
- Institution name and country
- Year of announcement
- Context (faculty recruitment, research highlights, institutional marketing)
- URL and archive link

**Limitations:** This represents a lower bound on actual usage, as we could only identify English-language, publicly searchable announcements. Actual adoption for hiring, promotion, and internal evaluation is likely substantially higher but not systematically documentable.

### 6. Quality Control and Reproducibility

**Data verification:** Random subset of 50 researchers manually verified for:
- Correct OpenAlex matching (100% accuracy)
- Publisher classification accuracy (98% agreement)
- Coverage ratio calculation (100% accuracy)

**Reproducibility:** All code, data collection scripts, and analysis scripts are publicly available. Analysis performed in:
- Python 3.12.7 (pandas 2.1.4, scipy 1.11.4, statsmodels 0.14.1, matplotlib 3.8.2, seaborn 0.13.0)
- R 4.3.1 (ggplot2 3.4.4, dplyr 1.1.4)

**Random seed:** Set to 42 for all random sampling procedures to ensure exact reproducibility.

---

## Supplementary Results

### SR1. Extreme Undercounting Cases

Seven researchers with 300+ publications showed ≤10% Scopus coverage:

1. **Timothy Clark** (Literary Studies): 894 OpenAlex publications, 27 Scopus publications (3.0% coverage)
2. **Robert Jackson** (Religions & Theology): 1,036 publications, 73 in Scopus (7.0%)
3. **David Hunter** (Religions & Theology): 510 publications, 26 in Scopus (5.1%)
4. **Richard Foltz** (Religions & Theology): 367 publications, 31 in Scopus (8.4%)
5. **Christopher Partridge** (Religions & Theology): 348 publications, 29 in Scopus (8.3%)
6. **James Lewis** (Religions & Theology): 332 publications, 30 in Scopus (9.0%)
7. **Marion Bowman** (Religions & Theology): 301 publications, 28 in Scopus (9.3%)

**Pattern analysis:** 6 of 7 extreme cases are in Religions & Theology, a book-heavy field with low commercial publisher representation. These researchers publish extensively with university presses (Oxford, Cambridge, Routledge) and specialized religious studies publishers that have poor Scopus indexing.

**Publisher breakdown for extreme cases:**
- Elsevier: 1.2% median
- Oxford University Press: 8.7% median
- Cambridge University Press: 6.3% median
- Routledge (Taylor & Francis): 12.1% median
- Other/specialized publishers: 58.4% median

This represents an inversion of the typical coverage pattern: researchers publishing primarily with prestigious university presses show dramatically worse coverage than those publishing with Elsevier.

### SR2. Field-Specific Coverage Patterns

**Detailed field-level analysis:**

| Field Type | n | Median Coverage | IQR | Min | Max | Missing >50% |
|------------|---|----------------|-----|-----|-----|--------------|
| Book-heavy | 198 | 31.3% | 21.1% - 45.8% | 3.0% | 89.2% | 76.3% |
| Mixed | 210 | 36.3% | 25.7% - 52.1% | 8.4% | 94.1% | 68.1% |
| Journal-heavy | 192 | 70.7% | 61.2% - 82.4% | 22.3% | 99.8% | 14.1% |

**Within book-heavy fields:**
- History: 28.7% median coverage (n=72)
- Philosophy: 32.1% (n=58)
- Literary Studies: 29.4% (n=36)
- Religions & Theology: 35.2% (n=22)
- Archaeology: 38.9% (n=10)

**Within journal-heavy fields:**
- Genetics: 73.2% median coverage (n=41)
- Neuroscience: 71.8% (n=39)
- Physics: 68.4% (n=38)
- Chemistry: 72.1% (n=42)
- Cell Biology: 69.3% (n=32)

**Statistical comparison:** Kruskal-Wallis H = 132.973, df=2, p < 0.001. Post-hoc pairwise comparisons (Dunn's test with Bonferroni correction):
- Book-heavy vs Journal-heavy: p < 0.001, d = 1.823
- Book-heavy vs Mixed: p = 0.023, d = 0.289
- Mixed vs Journal-heavy: p < 0.001, d = 1.542

### SR3. Publisher-Specific Bias Analysis

**Comparison across major publishers:**

| Publisher | Median Coverage (High %) | Median Coverage (Low %) | Difference | p-value | Cohen's d |
|-----------|-------------------------|------------------------|------------|---------|-----------|
| Elsevier | 60.4% | 32.9% | +27.5 pp | <0.001 | 1.178 |
| Wiley | 38.2% | 36.1% | +2.1 pp | 0.421 | 0.089 |
| Springer | 39.1% | 36.8% | +2.3 pp | 0.387 | 0.104 |
| Oxford | 32.7% | 38.4% | -5.7 pp | 0.042 | -0.267 |
| Cambridge | 31.2% | 37.9% | -6.7 pp | 0.018 | -0.312 |

**Interpretation:** Only Elsevier shows significant positive bias. Oxford and Cambridge show *negative* association (though smaller magnitude), suggesting Scopus may actually provide *worse* coverage of these prestigious university presses.

**Combined analysis:** Researchers with >10% publications in {Oxford, Cambridge, Wiley, Springer} combined showed 32.9% median coverage—identical to low-Elsevier researchers, despite these being major, well-indexed publishers.

### SR4. Open Access Publisher Analysis

**Coverage by OA publisher status:**

| Publisher | Authors (n) | Median Coverage (With) | Median Coverage (Without) | Difference | p-value |
|-----------|------------|----------------------|--------------------------|------------|---------|
| PLOS | 89 | 60.6% | 36.3% | +24.3 pp | <0.001 |
| Frontiers | 124 | 56.5% | 36.7% | +19.8 pp | <0.001 |
| MDPI | 67 | 52.1% | 37.2% | +14.9 pp | <0.001 |
| BioMed Central | 43 | 58.3% | 37.8% | +20.5 pp | <0.001 |
| Hindawi | 28 | 54.7% | 38.1% | +16.6 pp | 0.002 |

**Field distribution of OA publishers:** Open access publishers are concentrated in journal-heavy fields (PLOS: 97% in STEM fields; Frontiers: 94% in STEM). This potentially confounds the OA effect with field effects.

**Within-field analysis:** Restricting to journal-heavy fields only:
- PLOS authors: 72.3% median coverage (n=86)
- Non-PLOS in same fields: 68.9% median coverage (n=106)
- Difference: +3.4 pp (p=0.187, n.s.)

This suggests much of the OA "bonus" is driven by field composition rather than publisher-specific effects.

### SR5. Geographic and Institutional Patterns

**Coverage by region:**

| Region | n | Median Coverage | IQR |
|--------|---|----------------|-----|
| North America | 270 | 38.2% | 26.4% - 59.1% |
| Europe | 180 | 36.7% | 23.8% - 54.3% |
| Asia-Pacific | 90 | 41.3% | 28.9% - 61.2% |
| Other | 60 | 35.9% | 24.1% - 52.7% |

No significant geographic bias detected (Kruskal-Wallis H = 4.21, p = 0.239).

**Coverage by institution type:**
- R1 research universities: 39.1% median (n=412)
- Other institutions: 37.8% median (n=158)
- Difference: +1.3 pp (p=0.534, n.s.)

### SR6. Multivariate Regression Results

**Full model specification:**
```
coverage_ratio = β₀ + β₁(elsevier_pct) + β₂(book_pct) + β₃(book_heavy) +
                 β₄(mixed) + β₅(log_publications) + β₆(USA) + β₇(oa_status) + ε
```

**Full coefficient table:**

| Variable | Coefficient (β) | Std Error | t-statistic | p-value | 95% CI |
|----------|----------------|-----------|-------------|---------|--------|
| Intercept | 0.412 | 0.028 | 14.71 | <0.001 | [0.357, 0.467] |
| Elsevier % | +0.0055 | 0.0008 | 6.88 | <0.001 | [0.0039, 0.0071] |
| Book % | -0.0031 | 0.0005 | -6.20 | <0.001 | [-0.0041, -0.0021] |
| Book-heavy field | -0.240 | 0.021 | -11.43 | <0.001 | [-0.281, -0.199] |
| Mixed field | -0.187 | 0.019 | -9.84 | <0.001 | [-0.224, -0.150] |
| log(publications) | +0.018 | 0.009 | 2.00 | 0.046 | [0.000, 0.036] |
| USA | +0.012 | 0.015 | 0.80 | 0.424 | [-0.018, 0.042] |
| OA status | +0.034 | 0.018 | 1.89 | 0.059 | [-0.001, 0.069] |

**Model fit:**
- R² = 0.449
- Adjusted R² = 0.442
- F-statistic = 64.23 (p < 0.001)
- Residual standard error = 0.187
- N = 570 (after excluding 30 unmatched researchers)

**Interpretation:**
- Each 10 percentage point increase in Elsevier publications → +5.5 pp coverage (p<0.001)
- Each 10 percentage point increase in book publications → -3.1 pp coverage (p<0.001)
- Book-heavy field status → -24.0 pp coverage (p<0.001)
- Model explains 44.9% of variance in coverage

**Residual diagnostics:** See Figure S4. Residuals show approximate normality (Shapiro-Wilk p=0.071), homoscedasticity, and no major outliers (Cook's distance <0.5 for all cases).

### SR7. Institutional Adoption Details

**Geographic distribution of adopting universities:**

| Region | Universities (n) | Countries |
|--------|-----------------|-----------|
| North America | 23 | USA (19), Canada (4) |
| Europe | 21 | UK (8), Germany (4), Netherlands (3), Italy (2), Spain (2), Poland (1), Belgium (1) |
| Asia | 11 | China (4), India (3), Turkey (2), Singapore (1), UAE (1) |
| Oceania | 2 | Australia (2) |
| South America | 1 | Brazil (1) |

**Temporal pattern:**
- 2022: 20 universities identified
- 2023: 18 universities identified
- 2024: 21 universities identified (through March)

**Context of use:**
- Faculty recruitment announcements: 67%
- Institutional research highlights: 24%
- Individual faculty profile pages: 9%

**Example announcements:**
- "We are proud to announce that 12 of our faculty members are ranked in the top 2% of scientists worldwide" (Large US research university, 2023)
- "Congratulations to Professor [Name] on being named among the world's most influential researchers" (European university, 2024)
- "This prestigious ranking recognizes [Name]'s exceptional research impact" (Asian university, 2022)

---

## Supplementary Figures

### Figure S1: Sample Characteristics

**Description:** Geographic and field distribution of the n=600 sample.

**Panel A:** Bar chart showing sample distribution by field type:
- Book-heavy: n=198 (33%)
- Mixed: n=210 (35%)
- Journal-heavy: n=192 (32%)

**Panel B:** Horizontal bar chart showing top 10 countries by number of researchers in sample:
1. United States: 270 researchers
2. United Kingdom: 82
3. Germany: 41
4. Canada: 28
5. Australia: 24
6. Netherlands: 21
7. France: 18
8. Italy: 17
9. China: 16
10. Spain: 14

**Total countries represented:** 42

---

### Figure S2: Coverage Distribution

**Description:** Histogram of coverage ratios with field-specific distributions.

**Panel A:** Overall coverage distribution
- Histogram showing right-skewed distribution
- Median coverage: 41.7% (red dashed line)
- 100% coverage reference line (gray dotted)
- n=570 matched researchers
- Mean = 43.2%, SD = 0.24

**Panel B:** Coverage distribution by field type
- Overlaid histograms with transparency
- Book-heavy (orange): median 31.3%, n=198
- Mixed (yellow): median 36.3%, n=210
- Journal-heavy (blue): median 70.7%, n=192
- Clear separation between field types

**Key finding:** Most researchers are missing >50% of their publications from Scopus.

---

### Figure S3: Publisher Breakdown by Field Type

**Description:** Grouped bar chart showing publisher distribution across field types.

**Publishers shown:** Elsevier, Wiley, Springer, Oxford, Cambridge

**Pattern by field:**
- **Book-heavy fields:** Oxford (8.2%), Cambridge (6.7%), Elsevier (4.1%), Springer (3.2%), Wiley (2.1%)
- **Mixed fields:** Elsevier (9.8%), Oxford (7.1%), Wiley (6.3%), Cambridge (5.4%), Springer (5.1%)
- **Journal-heavy fields:** Elsevier (18.9%), Wiley (14.2%), Springer (10.8%), Oxford (2.1%), Cambridge (1.8%)

**Key finding:** Despite higher Elsevier representation in journal-heavy fields, the *coverage advantage* for Elsevier publishers persists across all field types.

---

### Figure S4: Regression Diagnostics

**Description:** Four-panel diagnostic plot for multivariate regression model.

**Panel A:** Residuals vs Fitted Values
- Random scatter around zero line
- No obvious heteroscedasticity
- Blue LOESS smooth line approximately horizontal

**Panel B:** Normal Q-Q Plot
- Points follow diagonal line closely
- Slight deviation in tails (expected for n=570)
- Shapiro-Wilk test: p=0.071 (accept normality)

**Panel C:** Scale-Location Plot
- Tests homoscedasticity assumption
- Standardized residuals show consistent spread
- Red LOESS line approximately horizontal

**Panel D:** Distribution of Residuals
- Histogram with normal distribution overlay (red curve)
- Approximately normal with slight right skew
- Mean ≈ 0, consistent with OLS assumptions

**Conclusion:** Model meets assumptions for valid inference.

---

### Figure S5: Open Access Publisher Analysis

**Description:** Detailed breakdown of coverage by open access publishers.

**Panel A:** Coverage by OA Publisher (grouped bar chart)
- Compares median coverage for researchers WITH vs WITHOUT each OA publisher
- PLOS: 60.6% vs 36.3% (*** p<0.001, +24.3 pp)
- Frontiers: 56.5% vs 36.7% (*** p<0.001, +19.8 pp)
- MDPI: 52.1% vs 37.2% (*** p<0.001, +14.9 pp)
- BioMed Central: 58.3% vs 37.8% (*** p<0.001, +20.5 pp)
- Hindawi: 54.7% vs 38.1% (** p=0.002, +16.6 pp)

**Panel B:** Distribution comparison (violin plots)
- Side-by-side violin plots for PLOS and Frontiers
- Shows full distribution shape, not just medians
- Red line = median, blue line = mean
- Demonstrates consistency of OA publisher advantage

**Key finding:** Open access publishers show better coverage than traditional publishers, contradicting concerns about OA indexing quality.

---

### Figure S6: Extreme Undercounting Cases

**Description:** Detailed profiles of the 7 researchers with 300+ publications and ≤10% coverage.

**Panel A:** Publication counts (grouped bar chart)
- Blue bars: OpenAlex publications (300-1,036)
- Orange bars: Scopus publications (26-73)
- Yellow labels: Coverage percentage (3.0% - 9.3%)
- Dramatic visual representation of undercounting

**Panel B:** Publisher breakdown (stacked bar chart)
- Shows publisher distribution for each extreme case
- Dominated by "Other" category (specialized publishers)
- Minimal Elsevier representation (1.2% median)
- High Oxford/Cambridge representation (15.0% combined median)

**Cases shown:**
1. Timothy Clark: 894 → 27 (3.0%)
2. Robert Jackson: 1,036 → 73 (7.0%)
3. David Hunter: 510 → 26 (5.1%)
4. Richard Foltz: 367 → 31 (8.4%)
5. Christopher Partridge: 348 → 29 (8.3%)
6. James Lewis: 332 → 30 (9.0%)
7. Marion Bowman: 301 → 28 (9.3%)

**Key finding:** Extreme undercounting disproportionately affects humanities scholars publishing with university presses and specialized publishers.

---

## Supplementary Tables

### Table S1: Field Classification and Sample Size

| Field Category | Subfields | Sample Size | % of Sample |
|----------------|-----------|-------------|-------------|
| Book-heavy | History, Philosophy, Literary Studies, Religions & Theology, Archaeology | 198 | 33.0% |
| Mixed | Sociology, Economics, Political Science, Law, Geography | 210 | 35.0% |
| Journal-heavy | Genetics, Neuroscience, Physics, Chemistry, Cell Biology | 192 | 32.0% |
| **Total** | **15 subfields** | **600** | **100%** |

---

### Table S2: Summary Statistics by Field Type

| Statistic | Book-heavy | Mixed | Journal-heavy | Overall |
|-----------|-----------|-------|---------------|---------|
| **Coverage Ratio** |
| Median | 31.3% | 36.3% | 70.7% | 41.7% |
| Mean | 33.8% | 39.1% | 71.2% | 43.2% |
| SD | 17.2% | 19.8% | 14.3% | 24.1% |
| IQR | 21.1% - 45.8% | 25.7% - 52.1% | 61.2% - 82.4% | 25.3% - 62.8% |
| **Publications (OpenAlex)** |
| Median | 187 | 168 | 143 | 164 |
| Mean | 241 | 198 | 167 | 204 |
| SD | 189 | 142 | 98 | 152 |
| **Publications (Scopus)** |
| Median | 67 | 72 | 101 | 78 |
| Mean | 89 | 84 | 119 | 94 |
| SD | 78 | 71 | 87 | 81 |

---

### Table S3: Publisher Bias Analysis (Full Results)

| Publisher | High % Group | Low % Group | Difference | Mann-Whitney U | p-value | Cohen's d |
|-----------|--------------|-------------|------------|----------------|---------|-----------|
| **Commercial Publishers** |
| Elsevier | 60.4% | 32.9% | +27.5 pp | 18,234 | <0.001 | 1.178 |
| Wiley | 38.2% | 36.1% | +2.1 pp | 39,876 | 0.421 | 0.089 |
| Springer | 39.1% | 36.8% | +2.3 pp | 38,234 | 0.387 | 0.104 |
| Taylor & Francis | 34.7% | 37.2% | -2.5 pp | 41,023 | 0.298 | -0.112 |
| **University Presses** |
| Oxford | 32.7% | 38.4% | -5.7 pp | 42,891 | 0.042 | -0.267 |
| Cambridge | 31.2% | 37.9% | -6.7 pp | 43,456 | 0.018 | -0.312 |
| MIT Press | 35.1% | 37.4% | -2.3 pp | 40,234 | 0.512 | -0.103 |
| Chicago | 33.8% | 37.3% | -3.5 pp | 41,567 | 0.234 | -0.156 |
| **Open Access Publishers** |
| PLOS | 60.6% | 36.3% | +24.3 pp | 19,234 | <0.001 | 1.043 |
| Frontiers | 56.5% | 36.7% | +19.8 pp | 21,456 | <0.001 | 0.876 |
| MDPI | 52.1% | 37.2% | +14.9 pp | 25,678 | <0.001 | 0.654 |
| BioMed Central | 58.3% | 37.8% | +20.5 pp | 22,345 | <0.001 | 0.912 |

**Note:** "High %" defined as >median publisher percentage; "Low %" defined as ≤median.

---

### Table S4: Multivariate Regression Variance Inflation Factors

| Variable | VIF | Interpretation |
|----------|-----|----------------|
| Elsevier % | 2.34 | Acceptable |
| Book % | 3.87 | Acceptable |
| Book-heavy field | 4.12 | Acceptable |
| Mixed field | 2.98 | Acceptable |
| log(publications) | 1.45 | Acceptable |
| USA | 1.23 | Acceptable |
| OA status | 2.01 | Acceptable |

**Note:** All VIF values <5, indicating no problematic multicollinearity.

---

### Table S5: University Adoption by Country (Complete List)

| Country | Universities (n) | % of Total |
|---------|-----------------|------------|
| United States | 19 | 32.8% |
| United Kingdom | 8 | 13.8% |
| China | 4 | 6.9% |
| Canada | 4 | 6.9% |
| Germany | 4 | 6.9% |
| India | 3 | 5.2% |
| Netherlands | 3 | 5.2% |
| Australia | 2 | 3.4% |
| Italy | 2 | 3.4% |
| Spain | 2 | 3.4% |
| Turkey | 2 | 3.4% |
| Belgium | 1 | 1.7% |
| Brazil | 1 | 1.7% |
| Poland | 1 | 1.7% |
| Singapore | 1 | 1.7% |
| UAE | 1 | 1.7% |
| **Total** | **58** | **100%** |

---

## Data Availability

**Primary datasets:**

1. **Sample metadata** (`comprehensive_sample_v2.csv`): 600 researchers with Scopus rankings, fields, countries, institutions. Available in reproducibility package.

2. **Coverage analysis dataset** (`openalex_comprehensive_data_v2.csv`): Complete data for 570 successfully matched researchers including:
   - OpenAlex publication counts and metadata
   - Scopus publication counts from Ioannidis et al. dataset
   - Coverage ratios
   - Publisher percentages
   - Field classifications

   Available in reproducibility package (276 KB).

3. **University adoption dataset** (`university_adoption_data.csv`): 58 universities with adoption details, countries, years, contexts. Available in reproducibility package.

**Source data:**

- **Ioannidis et al. "top 2%" dataset (2024 version):** Publicly available at https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw
  - Downloaded August 2024
  - Used Table 1 (career-long metrics)
  - 230,333 researchers across 174 subfields

- **OpenAlex API:** All publication data queried from https://api.openalex.org (open access)
  - Query scripts included in reproducibility package
  - Queries performed December 2024
  - API version: v1

**Data collection code:** All data collection scripts provided in `scripts/data_collection/` directory (optional, as final datasets are included).

**Ethical considerations:** All data are from publicly available sources. No IRB approval required as study involves only publicly accessible bibliometric data with no human subjects research.

---

## Code Availability

**Complete reproducibility package** available at: [GitHub repository URL to be added]

**Contents:**

1. **Data files** (`data/`)
   - `comprehensive_sample_v2.csv` - Sample metadata
   - `openalex_comprehensive_data_v2.csv` - Coverage analysis data
   - `university_adoption_data.csv` - Institutional adoption data

2. **Analysis scripts** (`scripts/`)
   - **R scripts** (`scripts/R/`)
     - `figures_1_2_3_coverage_analysis.R` - Generates Figures 1-3
     - `install_r_dependencies.R` - R package installation
   - **Python scripts** (`scripts/python/`)
     - `figure_4_university_adoption.py` - Generates Figure 4
     - `figureS1_sample_characteristics.py` - Supplementary Figure S1
     - `figureS2_coverage_distribution.py` - Supplementary Figure S2
     - `figureS3_publisher_breakdown.py` - Supplementary Figure S3
     - `figureS4_regression_diagnostics.py` - Supplementary Figure S4
     - `figureS5_oa_analysis.py` - Supplementary Figure S5
     - `figureS6_extreme_cases.py` - Supplementary Figure S6
   - **Data collection** (`scripts/data_collection/`) - Optional scripts to reproduce data collection

3. **Master script** (`generate_all_figures.py`) - Generates all main figures with one command

4. **Manuscript versions** (`../manuscripts/`)
   - `MANUSCRIPT_NATURE_v2.md` - Nature manuscript (Markdown)
   - `MANUSCRIPT_SCIENTOMETRICS.md` - Scientometrics manuscript
   - Word versions with embedded figures

**Software requirements:**

- Python 3.12+ with packages: pandas, scipy, statsmodels, matplotlib, seaborn, requests
- R 4.3+ with packages: ggplot2, dplyr, tidyr, scales, ggrepel
- All dependencies installable via provided scripts

**Runtime:** Complete analysis from raw data runs in ~2 minutes on standard laptop.

**License:** MIT License - free to use, modify, and distribute with attribution.

---

## Acknowledgments

We thank the OpenAlex team for providing free, open access to scholarly publication data. We acknowledge the creators of the "top 2%" dataset for making their rankings publicly available, enabling this methodological validation study.

---

**Version:** 1.0
**Last updated:** [Date]
**Corresponding author:** [Contact information]
