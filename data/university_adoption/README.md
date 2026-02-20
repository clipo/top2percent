# University Adoption Data

This directory contains data on university adoption of the Stanford/Elsevier "Top 2% Scientists" rankings for institutional marketing and reputation management (2022-2025).

## Data Files

### `university_adoption_data.csv`

Aggregated metrics by year showing adoption trends.

**Columns:**
- `year`: Year of observation (2022, 2023, 2024, 2025)
- `metric`: Type of metric measured
  - `total_universities`: Number of universities that year
  - `cumulative_total`: Running total of unique universities
  - `north_america`, `asia`, `europe`: Regional breakdown
  - `r1_research`, `regional`, `international`: Institution type breakdown
- `value`: Numeric value for the metric

### `university_details.csv`

Individual university records with detailed information.

**Columns:**
- `university`: Institution name
- `year`: Year first documented using the metric
- `country`: Country location
- `region`: Geographic region (North America, Asia, Europe)
- `institution_type`: Category (R1 Research, Regional, International, Medical School, Research Institute, Business School)
- `faculty_count`: Number of faculty members in "top 2%" (when reported)

## Data Collection Methodology

**Sources:**
- University press releases and news announcements
- Official university websites (faculty profile pages, research pages)
- Verified institutional news outlets

**Search Methods:**
- Phase 1 (January-March 2024): Initial dataset establishment
- Phase 2 (January 2026): Expanded coverage including 2025 announcements
- Google searches: `"top 2% scientists" [university name]`
- University news archives: 2022-2025

**Important Limitations:**

1. **Minimum Estimates**: These numbers represent only documented cases found through web-searchable English-language sources. Actual adoption is likely several times higher.

2. **Non-English Sources**: Universities in non-English-speaking countries may announce in local languages not captured by our search.

3. **Internal Use**: Many universities incorporate the metric into faculty profiles, tenure/promotion documents, strategic planning reports, and grant applications without public announcements.

4. **Undercounting**: A university appearing once may use the metric for multiple years; we only count the first documented instance.

5. **Regional Bias**: Asian universities, particularly in Hong Kong and Singapore, issue more English-language press releases, potentially inflating their representation.

## Key Findings

- **123 distinct universities** documented across **32 countries** (2022-2025)
- **Persistent adoption**: Consistent ~20-40 universities per year with no decline
- **Geographic expansion**: Growth across North America, Asia, and Europe
- **Institutional diversity**: Spans R1 research universities (68), regional universities (16), international institutions (25), medical schools (8), research institutes (4), and business schools (2)
- **No evidence of decline**: Despite scholarly criticism, institutional adoption continues to grow

## Usage

Generate Figure 1 (university adoption) from this data:

```bash
python scripts/python/figure_4_university_adoption.py
```

## Contact

Carl P. Lipo (clipo@binghamton.edu)

---

*Last updated: February 2026*
