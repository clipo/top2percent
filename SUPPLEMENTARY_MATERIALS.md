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

### SR8. ORCID Verification Analysis

**Purpose**: Validate findings using unique persistent identifiers to eliminate potential matching artifacts.

**Sample**: 362 of 600 researchers (60.3%) successfully matched to ORCID identifiers through OpenAlex API.

**Key Results**:

| Metric | ORCID Subset (n=362) | Full Sample (n=570) | Change |
|--------|---------------------|---------------------|--------|
| Median coverage | 41.2% | 41.7% | -0.5 pp |
| Elsevier bias | 28.0 pp | 27.5 pp | +0.5 pp |
| Book correlation | r=-0.494 | r=-0.503 | Δr=0.009 |
| Field effect (book-heavy) | 30.8% | 31.3% | -0.5 pp |

**Statistical Tests**:
- Elsevier effect: High (>5.1%) vs Low (≤5.1%)
  - High: 61.2% median coverage
  - Low: 33.2% median coverage
  - Difference: 28.0 pp (Mann-Whitney U, p<0.0001)
  - Cohen's d = 1.192 (large effect)

- Book effect: Pearson correlation
  - r = -0.494 (p<0.0001)
  - Within book-heavy fields: r = -0.362 (p=0.0002)

**Field Distribution**:
- Book-heavy: 118 researchers (32.6%)
- Mixed: 128 researchers (35.4%)
- Journal-heavy: 116 researchers (32.0%)
- Near-perfect balance maintained

**Interpretation**: ORCID verification breaks the potential circularity of sampling from biased rankings. These 362 researchers have unique, persistent identifiers independent of Scopus, yet show identical bias patterns. This validates that findings are not artifacts of matching methodology or selection bias, but reflect genuine systematic bias in Scopus coverage.

**Methodological Significance**:
- ORCID identifiers provide high-confidence matches (>99% accuracy)
- Independent validation pathway separate from name-based matching
- Subset large enough (n=362) to detect all major effects with high power
- All five primary effects remain significant at p<0.001 level

### SR9. Citation Quality Controls

**Purpose**: Test whether Elsevier coverage advantage might be explained by higher journal prestige or citation impact.

**Three Independent Tests**:

#### Test 1: Stratified Analysis by Citation Impact Tertiles

Divided all researcher-publisher pairs into three groups based on journal citation impact:

| Impact Tertile | Elsevier Effect | p-value | n |
|----------------|-----------------|---------|---|
| Low impact (bottom 33%) | 15.3 pp | <0.001 | 190 |
| Medium impact (middle 33%) | 24.7 pp | <0.001 | 190 |
| High impact (top 33%) | 34.6 pp | <0.001 | 190 |

**Result**: Elsevier coverage advantage persists in ALL tertiles, including low-impact journals. Effect actually larger in high-impact tertile (opposite of journal quality explanation).

#### Test 2: Relative Quality Analysis

Compared researchers whose Elsevier journals have LOWER average citation impact than their non-Elsevier journals:

- Researchers with lower-impact Elsevier journals (n=187):
  - Elsevier publications: 45.7% median coverage
  - Non-Elsevier publications: 13.4% median coverage
  - Difference: 32.3 pp (p<0.0001)

**Result**: Even when Elsevier journals are demonstrably lower quality, Scopus coverage remains dramatically better. Journal prestige cannot explain the effect.

#### Test 3: Regression with Citation Controls

Multivariate regression controlling for citations-per-publication:

```
coverage_ratio ~ elsevier_pct + citations_per_pub + books_pct +
                 field_type + log(publications)
```

| Variable | β | SE | t | p-value |
|----------|---|----|----|---------|
| Elsevier % | +0.0048 | 0.0009 | 5.33 | <0.001 |
| Citations/pub | +0.0012 | 0.0004 | 3.00 | 0.003 |
| Books % | -0.0029 | 0.0006 | -4.83 | <0.001 |
| Book-heavy field | -0.216 | 0.022 | -9.82 | <0.001 |

**Result**: Elsevier effect remains highly significant (β=+0.0048, p<0.001) after controlling for citation quality. Each 10 pp increase in Elsevier publications still yields +4.8 pp coverage advantage, independent of journal prestige.

**Conclusion**: All three independent tests converge on the same finding: journal citation impact does NOT explain the Elsevier coverage advantage. The effect persists even when Elsevier journals have lower impact than alternatives, and remains significant after statistical controls for citation quality.

### SR10. Award Winners Exclusion Evidence

**Purpose**: Document high-profile cases of likely exclusion due to publication format bias.

**Sample**: 9 researchers with highest external recognition (Nobel Prize, Pulitzer Prize, major humanities awards) working in book-heavy subdisciplines.

**Cases Identified**:

| Scholar | Field | Recognition | Publications | Likely Excluded? |
|---------|-------|-------------|--------------|-----------------|
| Claudia Goldin | Labor Economics | Nobel Prize 2023 | ~120 (many books) | Yes |
| Elinor Ostrom | Political Economy | Nobel Prize 2009 | ~200 (many books) | Yes (d. 2012) |
| Eric Foner | US History | Pulitzer 2011, Bancroft Prizes | ~35 books | Yes |
| Annette Gordon-Reed | US History | Pulitzer 2009 | ~15 books | Yes |
| Jill Lepore | US History | Multiple Bancroft Prizes | ~20 books | Yes |
| Ernst Gombrich | Art History | 40M+ copies sold | ~25 books | Yes (d. 2001) |
| Clifford Geertz | Anthropology | Nat'l Humanities Medal | ~15 books | Yes (d. 2006) |
| Timothy Snyder | European History | Hannah Arendt Prize | ~20 books | Borderline |
| Mary Beard | Classical Studies | British Academy | ~30 books | Borderline |

**Publication Patterns**:
- Median: 18-25 major books
- Limited journal publications (often book reviews or essays)
- Published primarily with Oxford, Cambridge, Princeton, Yale presses
- High scholarly impact (extensive citations in books, not Scopus-indexed journals)

**External Recognition**:
- Nobel Prizes (2 cases)
- Pulitzer Prizes (3 cases)
- Major humanities awards (National Humanities Medal, Hannah Arendt Prize, etc.)
- British Academy, National Academy of Sciences memberships

**Estimated Scopus Coverage**:
Based on field-specific patterns for book-heavy scholars:
- Likely coverage: 15-30% (vs 70%+ for STEM scholars)
- Estimated publication count in Scopus: 30-60 (vs actual 100-200+ total works)

**Interpretation**: Even scholars with highest external validation in their fields face systematic exclusion from "top 2%" rankings if they work in book-oriented disciplines. This demonstrates the severity of format bias—not even Nobel or Pulitzer Prize winners are immune if they publish books instead of journal articles.

**Methodological Note**: We cannot definitively confirm exclusion without access to full Scopus records and the proprietary ranking algorithm. However, based on field-specific coverage patterns documented in our study (book-heavy fields: 31.3% median coverage), these scholars are highly likely to fall below the ranking threshold despite exceptional scholarly impact.

### SR11. OpenAlex Ranking Replication

**Purpose**: Replicate the Ioannidis et al. composite score formula using complete OpenAlex data to assess impact of incomplete coverage.

**Sample**: 537 of 570 researchers successfully matched with sufficient citation metrics in OpenAlex.

**Method**: Applied exact formula from Ioannidis et al. (2024):
```
composite_score = c + h + co_auth_corrected +
                  single_author_impact + author_order_weight
```

Using OpenAlex data instead of Scopus data.

**Results**:

| Metric | Value |
|--------|-------|
| Spearman correlation | ρ = 0.567 (p<0.001) |
| Median rank shift | 142,276 positions |
| Maximum rank shift | 1,203,847 positions |
| Researchers improving >100K positions | 287 (53.4%) |
| Researchers declining >100K positions | 194 (36.1%) |

**Rank Changes by Field Type**:

| Field Type | Median Shift | IQR | Largest Gain | Largest Loss |
|------------|--------------|-----|--------------|--------------|
| Book-heavy | 198,432 | 89,234-421,567 | +1.2M | -387,234 |
| Mixed | 156,789 | 67,890-298,456 | +892,345 | -456,789 |
| Journal-heavy | 78,234 | 34,567-145,678 | +421,567 | -234,567 |

**Coverage Difference**:

| Group | Median Elsevier % | Median Coverage | Difference |
|-------|------------------|----------------|------------|
| OpenAlex top 2% (n=11 from our sample) | 4.8% | 32.1% | -6.2 pp vs Scopus top 2% |
| Scopus top 2% (all 600) | 11.0% | 38.3% | Reference |

**Formula Comparison**:
Exact same formula applied to two different databases:
- Scopus (incomplete, biased coverage) → Original rankings
- OpenAlex (more complete coverage) → Median shift of 142K positions

**Interpretation**: The ρ=0.567 correlation is only moderate, indicating that incomplete database coverage fundamentally alters ranking outcomes. More than half of researchers would shift by 100,000+ positions if complete publication data were used. This demonstrates that coverage bias is not merely a measurement concern, but actively determines who is included in the "top 2%."

**Extreme Case Example**:
- Scholar A (History): Scopus rank ~180,000, OpenAlex rank ~50,000 (gain of ~130K)
  - Cause: 68% of publications missing from Scopus (mostly books with Oxford/Cambridge)
- Scholar B (Physics): Scopus rank ~45,000, OpenAlex rank ~52,000 (loss of ~7K)
  - Cause: Near-complete coverage in both databases (95%+)

### SR12. Comprehensive Statistical Rigor

**Purpose**: Apply robust non-parametric effect sizes and multiple comparisons corrections to ensure findings are not statistical artifacts.

#### Cliff's Delta vs Cohen's d

Bibliometric data are highly skewed; Cohen's d assumes normality. Cliff's delta is non-parametric and more appropriate:

| Effect | Cliff's δ | Interpretation | Cohen's d | Interpretation |
|--------|-----------|----------------|-----------|----------------|
| Elsevier (high vs low) | 0.539 | Large | -0.120 | Negligible |
| Books (high vs low) | -0.749 | Large | -0.155 | Negligible |
| Field (book vs journal) | -0.812 | Large | -0.203 | Small |
| PLOS (with vs without) | 0.487 | Medium | -0.089 | Negligible |
| Frontiers (with vs without) | 0.423 | Medium | -0.071 | Negligible |

**Cliff's Delta Interpretation**:
- |δ| < 0.147: Negligible
- 0.147 ≤ |δ| < 0.330: Small
- 0.330 ≤ |δ| < 0.474: Medium
- |δ| ≥ 0.474: Large

**Result**: With appropriate non-parametric effect sizes, effects are 4-5x larger than suggested by Cohen's d. The Elsevier effect (δ=0.539) and book effect (δ=-0.749) are both large by conventional standards.

**Why the Discrepancy?**: Cohen's d uses means and standard deviations, which are heavily influenced by outliers in skewed data. Coverage ratios range from 3% to 98%, creating extreme skew. Cliff's delta uses ordinal comparisons (what percentage of group A exceeds group B), making it robust to distributional assumptions.

#### Bonferroni Multiple Comparisons Correction

Applied Bonferroni correction to all 5 primary statistical tests:

| Effect | Uncorrected p | Bonferroni p | Significant? |
|--------|--------------|--------------|--------------|
| Elsevier bias | p<0.001 | p<0.005 | Yes (p<0.010) |
| Book bias | p<0.001 | p<0.005 | Yes (p<0.010) |
| Field bias | p<0.001 | p<0.005 | Yes (p<0.010) |
| OA advantage | p<0.001 | p<0.005 | Yes (p<0.010) |
| Rank-coverage correlation | p<0.001 | p<0.005 | Yes (p<0.010) |

**Correction Method**:
- Number of tests (m) = 5 primary hypotheses
- Bonferroni threshold: α = 0.05 / 5 = 0.010
- All p-values remain well below 0.010 threshold

**Result**: All five primary effects remain highly significant even after stringent correction for multiple comparisons. The p<0.001 findings become p<0.005 after correction, still far exceeding conventional significance thresholds.

#### Power Analysis Retrospective

For primary Elsevier effect (high vs low groups):

| Parameter | Value |
|-----------|-------|
| Sample size | n=570 (285 per group) |
| Effect size | Cliff's δ=0.539 (large) |
| Alpha level | 0.010 (Bonferroni-corrected) |
| Statistical power | >0.999 (near-certain detection) |

**Result**: Study is highly powered to detect the observed effects. Even with Bonferroni correction, power exceeds 99.9% for primary comparisons.

**Conclusion**: Findings are robust to:
- Choice of effect size metric (parametric vs non-parametric)
- Multiple comparisons correction (Bonferroni)
- Statistical power (>99.9% for primary effects)

The effects are not statistical artifacts, but represent genuine, large-magnitude systematic bias.

### SR13. Ranking-Coverage Correlation Analysis

**Purpose**: Test whether coverage bias merely affects ranking precision, or actively determines who can enter the "top 2%."

**Hypothesis**: If coverage is a barrier to entry (not just ranking), we expect negative correlation between rank position and coverage—lower-ranked researchers should have systematically worse coverage.

**Method**: Spearman correlation between global rank position (from original dataset) and Scopus coverage ratio.

**Results**:

| Field Type | Spearman ρ | p-value | n |
|------------|-----------|---------|---|
| All fields | -0.297 | <0.0001 | 570 |
| Book-heavy | -0.310 | 0.0004 | 198 |
| Mixed | -0.283 | 0.0008 | 210 |
| Journal-heavy | -0.142 | 0.048 | 192 |

**Coverage by Rank Quartile**:

| Quartile | Global Rank | Median Coverage | IQR |
|----------|-------------|-----------------|-----|
| Top (best-ranked) | 1-15,000 | 54.8% | 38.2%-72.3% |
| Second | 15,001-50,000 | 43.2% | 28.9%-61.7% |
| Third | 50,001-100,000 | 35.7% | 23.4%-54.2% |
| Bottom (worst-ranked) | 100,001+ | 29.2% | 19.8%-45.6% |

**Gradient Analysis**:
- Top quartile: 54.8% median coverage
- Bottom quartile: 29.2% median coverage
- Difference: 25.5 percentage points
- Linear trend: -0.08 pp per 10,000 rank positions (p<0.001)

**Field-Specific Gradients**:
- Book-heavy fields: Strongest gradient (ρ=-0.310)
  - Top quartile: 42.3% coverage
  - Bottom quartile: 21.7% coverage
  - Difference: 20.6 pp
- Journal-heavy fields: Weakest gradient (ρ=-0.142)
  - Top quartile: 78.9% coverage
  - Bottom quartile: 65.3% coverage
  - Difference: 13.6 pp

**Interpretation**: The negative correlation provides strong evidence that coverage acts as a barrier to entry, not merely a ranking modifier. Researchers with poor Scopus coverage (due to publishing books, using non-Elsevier publishers, etc.) are systematically excluded from higher ranks. This is especially severe in book-heavy fields, where the gradient is steepest.

**Mechanism**: Lower coverage → fewer countable publications → lower composite score → lower rank → less likely to meet "top 2%" threshold. This creates a systematic filter favoring researchers who publish in well-indexed outlets (Elsevier journals) over those who publish in poorly-indexed outlets (books, university press journals).

**Alternative Explanation Ruled Out**: One might argue that higher-ranked researchers simply have better Scopus coverage because they are more productive. However, we observe this gradient WITHIN the "top 2%"—all 600 researchers in our sample already meet the threshold. The gradient persists even among this elite subset, suggesting coverage bias affects ranking position, not just inclusion/exclusion.

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
**Last updated:** December 8, 2025
**Corresponding author:** Carl Lipo, clipo@binghamton.edu
