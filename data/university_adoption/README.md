# University Adoption Data

This directory contains data on university adoption of the Stanford/Elsevier "Top 2% Scientists" rankings for institutional marketing and reputation management (2022-2024).

## Data Files

### `university_adoption_data.csv`

Aggregated metrics by year showing adoption trends.

**Columns:**
- `year`: Year of observation (2022, 2023, 2024)
- `metric`: Type of metric measured
  - `total_universities`: Number of universities that year
  - `cumulative_total`: Running total of unique universities
  - `north_america`, `asia`, `europe`: Regional breakdown
  - `r1_research`, `regional`, `international`: Institution type breakdown
- `value`: Numeric value for the metric

**Sample:**
```
year,metric,value
2022,total_universities,20
2023,total_universities,18
2024,total_universities,21
```

### `university_details.csv`

Individual university records with detailed information.

**Columns:**
- `university`: Institution name
- `year`: Year first documented using the metric
- `country`: Country location
- `region`: Geographic region (North America, Asia, Europe)
- `institution_type`: Category (R1 Research, Regional, International, Medical School)
- `faculty_count`: Number of faculty members in "top 2%" (when reported)

**Sample:**
```
university,year,country,region,institution_type,faculty_count
"Texas A&M University Health Science Center",2022,"USA","North America","Medical School",26
"Hong Kong Polytechnic University",2022,"Hong Kong","Asia","R1 Research",21
```

## Data Collection Methodology

**Sources:**
- University press releases and news announcements
- Official university websites (faculty profile pages, research pages)
- Web-searchable English-language announcements

**Search Methods:**
- Google searches: `"top 2% scientists" [university name]`
- University news archives: 2022-2024
- Academic social media monitoring (LinkedIn, Twitter/X)

**Important Limitations:**

1. **Minimum Estimates**: These numbers represent only documented cases found through web-searchable English-language sources. Actual adoption is likely several times higher.

2. **Non-English Sources**: Universities in non-English-speaking countries may announce in local languages not captured by our search.

3. **Internal Use**: Many universities incorporate the metric into:
   - Faculty profile pages (without press releases)
   - Internal tenure/promotion documents
   - Strategic planning reports
   - Grant applications

   These uses are not captured unless publicly announced.

4. **Undercounting**: A university appearing once may use the metric for multiple years; we only count the first documented instance.

5. **Regional Bias**: Asian universities, particularly in Hong Kong and Singapore, issue more English-language press releases, potentially inflating their representation.

## Key Findings

- **59 distinct universities** documented over 2022-2024
- **Persistent adoption**: ~20 universities per year with no decline
- **Geographic expansion**: Growth in Asian institutions (8→10 over period)
- **Institutional diversity**: Spans R1 research universities, regional universities, and international institutions across 20+ countries
- **No evidence of decline**: Despite scholarly criticism of the rankings, institutional adoption shows no signs of decreasing

## Usage

Generate figures from this data:

```bash
# Generate Figure 4 for manuscript
python scripts/generate_figure4_adoption.py

# Specify output directory
python scripts/generate_figure4_adoption.py --output-dir results/figures/

# Generate PDF instead of PNG
python scripts/generate_figure4_adoption.py --format pdf
```

## Citation

If using this adoption data, please cite:

[Citation information for manuscript to be added]

## Related Documentation

- Main manuscript: `MANUSCRIPT_NATURE.md`
- Figure specifications: See manuscript Figure 4 description
- Analysis script: `scripts/generate_figure4_adoption.py`

## Data Updates

This dataset captures adoption through November 2024. To update:

1. Search for recent university announcements
2. Add new records to `university_details.csv`
3. Update aggregated metrics in `university_adoption_data.csv`
4. Re-run analysis script to regenerate figures

## Contact

[Contact information to be added]

---

*Last updated: November 2024*
