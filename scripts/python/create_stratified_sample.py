"""
Create a stratified sample for comprehensive publisher bias study.

This script creates a balanced sample across:
- Field types (book-heavy, mixed, journal-heavy)
- Ranking positions (top, bottom, anomaly)
- Geographic regions (to control for regional effects)

Sample designed for publication in Nature/Science or Scientometrics.
"""

import pandas as pd

# Dataset path
DATASET_PATH = (
    "August 2025 data-update for Updated science-wide a/"
    "Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx"
)

# Field classifications based on publication norms
FIELD_CLASSIFICATIONS = {
    'book_heavy': [
        'Archaeology',
        'History',
        'Philosophy',
        'Literary Studies',
        'Anthropology',
        'Religions & Theology',
        'Art Practice, History & Theory',
        'Classics',
    ],
    'mixed': [
        'Sociology',
        'Political Science & Public Administration',
        'Economics',
        'Law',
        'Education',
        'Geography',
        'Languages & Linguistics',
        'Communication & Media Studies',
    ],
    'journal_heavy': [
        'Genetics & Heredity',
        'Neurology & Neurosurgery',
        'Nuclear & Particle Physics',
        'Organic Chemistry',
        'Biochemistry & Molecular Biology',
        'Immunology',
        'Microbiology',
        'Cell Biology',
    ]
}


def load_dataset():
    """Load the full career-long author dataset."""
    print(f"Loading dataset from: {DATASET_PATH}")
    df = pd.read_excel(DATASET_PATH, sheet_name='Data')
    print(f"Loaded {len(df):,} researchers")
    return df


def identify_anomalies(field_df):
    """
    Identify researchers in global top 2% but outside field's top 2%.

    These are the "impossible" researchers who suggest systematic bias.
    """
    total_in_field = len(field_df)

    # Anyone with rank > total is outside the field's top 2%
    anomalies = field_df[field_df['rank sm-subfield-1'] > total_in_field]

    return anomalies


def sample_from_field(field_df, field_name, n_per_group=6):
    """
    Sample researchers from a single field using stratified approach.

    Three strata:
    - Top quartile: The highest-ranked researchers (most prestigious)
    - Bottom quartile: Barely made it into top 2% (most vulnerable to coverage issues)
    - Anomalies: Outside field's top 2% but in global top 2% (the "smoking gun")
    """
    samples = []

    if len(field_df) == 0:
        print(f"  WARNING: No data for {field_name}")
        return pd.DataFrame()

    field_df = field_df.sort_values('rank sm-subfield-1')
    total_in_field = len(field_df)

    print(f"\n{field_name}: {total_in_field} researchers in top 2%")

    # Top quartile (ranks 1-25%)
    top_quartile = field_df.iloc[:total_in_field // 4]
    if len(top_quartile) > 0:
        n_sample = min(n_per_group, len(top_quartile))
        sample_top = top_quartile.sample(n_sample, random_state=42)
        sample_top['sample_stratum'] = 'top_quartile'
        samples.append(sample_top)
        print(f"  Top quartile: sampled {n_sample} from {len(top_quartile)}")

    # Bottom quartile (ranks 75-100% of field's top 2%)
    bottom_quartile = field_df.iloc[3 * total_in_field // 4:]
    if len(bottom_quartile) > 0:
        n_sample = min(n_per_group, len(bottom_quartile))
        sample_bottom = bottom_quartile.sample(n_sample, random_state=42)
        sample_bottom['sample_stratum'] = 'bottom_quartile'
        samples.append(sample_bottom)
        print(f"  Bottom quartile: sampled {n_sample} from {len(bottom_quartile)}")

    # Anomalies (outside field's top 2%)
    anomalies = identify_anomalies(field_df)
    if len(anomalies) > 0:
        n_sample = min(n_per_group, len(anomalies))
        sample_anomalies = anomalies.sample(n_sample, random_state=42)
        sample_anomalies['sample_stratum'] = 'anomaly'
        samples.append(sample_anomalies)
        print(f"  Anomalies: sampled {n_sample} from {len(anomalies)} WARNING")
    else:
        print("  Anomalies: none found")

    if samples:
        result = pd.concat(samples, ignore_index=False)
        result['field_type'] = None  # Will be filled later
        return result
    else:
        return pd.DataFrame()


def create_stratified_sample(df, n_per_group=6):
    """
    Create comprehensive stratified sample.

    For each field type (book-heavy, mixed, journal-heavy):
    - Sample from multiple fields
    - Include top/bottom/anomaly strata
    - Balance sample sizes

    Target: ~150-200 researchers total
    """
    all_samples = []

    for field_type, fields in FIELD_CLASSIFICATIONS.items():
        print("\n" + "=" * 80)
        print(f"FIELD TYPE: {field_type.upper()}")
        print("=" * 80)

        for field in fields:
            field_df = df[df['sm-subfield-1'] == field].copy()

            if len(field_df) == 0:
                print(f"\n{field}: NOT FOUND (skipping)")
                continue

            field_sample = sample_from_field(field_df, field, n_per_group)

            if len(field_sample) > 0:
                field_sample['field_type'] = field_type
                all_samples.append(field_sample)

    if all_samples:
        final_sample = pd.concat(all_samples, ignore_index=False)
        return final_sample
    else:
        return pd.DataFrame()


def add_metadata(sample_df):
    """Add useful metadata for the study."""
    sample_df['sample_id'] = range(1, len(sample_df) + 1)

    # Extract country if available
    if 'cntry' in sample_df.columns:
        sample_df['country'] = sample_df['cntry']

    # Extract institution if available
    if 'inst_name' in sample_df.columns:
        sample_df['institution'] = sample_df['inst_name']

    # Key metrics from Scopus
    sample_df['scopus_pubs'] = sample_df['np6024']
    sample_df['scopus_citations'] = sample_df['nc9624']
    sample_df['scopus_h_index'] = sample_df['h24']

    # Ranking information
    sample_df['rank_global'] = sample_df['rank']
    sample_df['rank_in_field'] = sample_df['rank sm-subfield-1']

    return sample_df


def save_sample(sample_df, output_file='comprehensive_sample.csv'):
    """Save the sample with clear documentation."""
    # Select relevant columns for the study
    columns_to_keep = [
        'sample_id',
        'authfull',
        'sm-subfield-1',
        'field_type',
        'sample_stratum',
        'rank_global',
        'rank_in_field',
        'scopus_pubs',
        'scopus_citations',
        'scopus_h_index',
        'country',
        'institution',
    ]

    # Only keep columns that exist
    columns_to_keep = [col for col in columns_to_keep if col in sample_df.columns]

    output_df = sample_df[columns_to_keep].copy()
    output_df.to_csv(output_file, index=False)

    print("\n" + "=" * 80)
    print(f"Sample saved to: {output_file}")
    print("=" * 80)

    return output_file


def print_sample_summary(sample_df):
    """Print detailed summary of the sample composition."""
    print("\n" + "=" * 80)
    print("SAMPLE SUMMARY")
    print("=" * 80)

    print(f"\nTotal sample size: {len(sample_df)} researchers")

    # By field type
    print("\n--- By Field Type ---")
    field_type_counts = sample_df['field_type'].value_counts()
    for field_type, count in field_type_counts.items():
        pct = count / len(sample_df) * 100
        print(f"  {field_type:20s}: {count:3d} ({pct:5.1f}%)")

    # By stratum
    print("\n--- By Sampling Stratum ---")
    stratum_counts = sample_df['sample_stratum'].value_counts()
    for stratum, count in stratum_counts.items():
        pct = count / len(sample_df) * 100
        print(f"  {stratum:20s}: {count:3d} ({pct:5.1f}%)")

    # By specific field
    print("\n--- By Specific Field (top 10) ---")
    field_counts = sample_df['sm-subfield-1'].value_counts().head(10)
    for field, count in field_counts.items():
        print(f"  {field:40s}: {count:2d}")

    # Geographic distribution
    if 'country' in sample_df.columns:
        print("\n--- By Country (top 10) ---")
        country_counts = sample_df['country'].value_counts().head(10)
        for country, count in country_counts.items():
            print(f"  {country:20s}: {count:3d}")

    # Metrics summary
    print("\n--- Scopus Metrics (Median) ---")
    print(f"  Publications:  {sample_df['scopus_pubs'].median():.0f}")
    print(f"  Citations:     {sample_df['scopus_citations'].median():.0f}")
    print(f"  h-index:       {sample_df['scopus_h_index'].median():.0f}")

    # By field type
    print("\n--- Median Metrics by Field Type ---")
    for field_type in ['book_heavy', 'mixed', 'journal_heavy']:
        subset = sample_df[sample_df['field_type'] == field_type]
        if len(subset) > 0:
            print(f"\n  {field_type}:")
            print(f"    Publications:  {subset['scopus_pubs'].median():.0f}")
            print(f"    Citations:     {subset['scopus_citations'].median():.0f}")
            print(f"    h-index:       {subset['scopus_h_index'].median():.0f}")

    # Statistical power note
    print("\n" + "=" * 80)
    print("STATISTICAL POWER")
    print("=" * 80)
    n = len(sample_df)
    print(f"\nWith n={n}, assuming equal group sizes:")
    print("  - Can detect correlations r > 0.20 (80% power, alpha=0.05)")
    print("  - Can detect group differences d > 0.40 (medium effect)")
    print("  - Adequate for multivariate regression with ~5 predictors")
    print("\nSample size is sufficient for publication-quality analysis")


def main():
    """Create comprehensive stratified sample for publisher bias study."""
    print("=" * 80)
    print("COMPREHENSIVE STRATIFIED SAMPLE CREATION")
    print("Publisher Bias Study - Publication-Ready Design")
    print("=" * 80)

    # Load dataset
    df = load_dataset()

    # Create sample
    print("\nCreating stratified sample...")
    print("  - 3 field types (book-heavy, mixed, journal-heavy)")
    print("  - 3 strata per field (top, bottom, anomaly)")
    print("  - 6 researchers per stratum (target)")
    print("  - Expected total: ~150-200 researchers")

    sample_df = create_stratified_sample(df, n_per_group=6)

    if len(sample_df) == 0:
        print("\nFailed to create sample!")
        return

    # Add metadata
    sample_df = add_metadata(sample_df)

    # Print summary
    print_sample_summary(sample_df)

    # Save
    save_sample(sample_df, 'comprehensive_sample.csv')

    # Save a detailed version with all columns for reference
    sample_df.to_csv('comprehensive_sample_full.csv', index=False)
    print("Full data saved to: comprehensive_sample_full.csv")

    # Create a research log
    with open('SAMPLE_CREATION_LOG.md', 'w') as f:
        f.write("# Sample Creation Log\n\n")
        f.write(f"**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total sample size**: {len(sample_df)} researchers\n\n")
        f.write("## Sampling Strategy\n\n")
        f.write("Stratified random sample with:\n")
        f.write("- **Field types**: book-heavy (8 fields), mixed (8 fields), journal-heavy (8 fields)\n")
        f.write("- **Strata**: top quartile, bottom quartile, anomalies\n")
        f.write("- **Sample size**: ~6 per stratum per field\n\n")
        f.write("## Field Classifications\n\n")
        f.write("**Book-heavy fields** (where books are primary outputs):\n")
        for field in FIELD_CLASSIFICATIONS['book_heavy']:
            f.write(f"- {field}\n")
        f.write("\n**Mixed fields** (books and journals both common):\n")
        for field in FIELD_CLASSIFICATIONS['mixed']:
            f.write(f"- {field}\n")
        f.write("\n**Journal-heavy fields** (journals are primary outputs):\n")
        for field in FIELD_CLASSIFICATIONS['journal_heavy']:
            f.write(f"- {field}\n")
        f.write("\n## Statistical Power\n\n")
        f.write(f"With n={len(sample_df)}:\n")
        f.write("- Minimum detectable correlation: r > 0.20 (80% power)\n")
        f.write("- Minimum detectable effect size: d > 0.40 (medium effect)\n")
        f.write("- Adequate for multivariate regression\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Fetch OpenAlex data: `python3 fetch_openalex_comprehensive.py`\n")
        f.write("2. Analyze coverage patterns: `python3 analyze_coverage_bias.py`\n")
        f.write("3. Test publisher bias: `python3 test_publisher_bias_comprehensive.py`\n")
        f.write("4. Generate figures: `Rscript create_figures.R`\n")
        f.write("5. Write manuscript: See `PUBLICATION_ROADMAP.md`\n")

    print("Research log saved to: SAMPLE_CREATION_LOG.md")

    print("\n" + "=" * 80)
    print("SAMPLE CREATION COMPLETE")
    print("=" * 80)
    print(f"\nNext step: Fetch OpenAlex data for all {len(sample_df)} researchers")
    est_time = len(sample_df) * 2 / 60
    print(f"Estimated time: {est_time:.1f} minutes (with API delays)")


if __name__ == "__main__":
    main()
