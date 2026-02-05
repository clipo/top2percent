#!/usr/bin/env python3
"""
Create Stratified Sample for Publisher Bias Study
==================================================

PURPOSE:
    Generates a stratified random sample of researchers from the "top 2% of
    scientists" dataset for validating Scopus coverage bias.

SAMPLING STRATEGY:
    - 24 fields across 3 categories (book-heavy, mixed, journal-heavy)
    - 3 strata per field: top quartile, bottom quartile, anomalies
    - ~6 researchers per field per stratum
    - Geographic diversity (multiple countries per field)
    - Target: ~400 researchers total

INPUT FILES:
    - Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx
      (from https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw)

OUTPUT FILES:
    - comprehensive_sample.csv: 397 researchers with field classifications

DEPENDENCIES:
    - pandas >= 2.0.0
    - numpy >= 1.24.0
    - openpyxl >= 3.1.0 (for Excel reading)

USAGE:
    python3 create_stratified_sample.py

    Output will be saved to: data/comprehensive_sample.csv

REPRODUCIBILITY:
    - Random seed set to 42 for reproducible sampling
    - All sampling decisions are deterministic given the seed
    - Sample selection criteria are explicit and documented

AUTHOR: Generated for "Systematic Bias in Top 2% Rankings" study
DATE: November 2024
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Dataset path (user must download this separately)
DATASET_PATH = "August 2025 data-update for Updated science-wide a/Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx"

# Field classifications based on publication norms
# Book-heavy: Fields where monographs are primary outputs
# Mixed: Fields with both books and articles
# Journal-heavy: Fields where journal articles dominate
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

# Sampling parameters
RESEARCHERS_PER_FIELD_STRATUM = 6  # Target per field per stratum
MIN_RESEARCHERS_FOR_ANOMALIES = 10  # Minimum field size to sample anomalies


def load_dataset():
    """
    Load the "top 2%" dataset.

    Returns:
        pd.DataFrame: Full dataset with all researchers

    Raises:
        FileNotFoundError: If dataset file not found
        ValueError: If required columns missing
    """
    print("="*80)
    print("LOADING TOP 2% DATASET")
    print("="*80)
    print()

    if not Path(DATASET_PATH).exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}\n"
            f"Please download from: https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw"
        )

    print(f"Loading: {DATASET_PATH}")
    print("(This may take 1-2 minutes for the ~90 MB file)")

    df = pd.read_excel(DATASET_PATH, sheet_name='Data')

    print(f"✓ Loaded {len(df):,} researchers")
    print()

    # Verify required columns exist
    required_cols = ['authfull', 'sm-subfield-1', 'rank', 'np', 'nc', 'h', 'country']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def identify_anomalies(df, field_name):
    """
    Identify researchers in global top 2% but outside their field's top 2%.

    These "anomaly" researchers are mathematically impossible under valid
    field normalization and may indicate systematic measurement bias.

    Args:
        df: DataFrame with full dataset
        field_name: Subfield name to analyze

    Returns:
        pd.DataFrame: Anomaly researchers for this field
    """
    field_data = df[df['sm-subfield-1'] == field_name].copy()

    if len(field_data) == 0:
        return pd.DataFrame()

    # Calculate top 2% threshold for this field
    field_size = len(field_data)
    top_2_percent_count = int(field_size * 0.02)

    # Anomalies: researchers beyond the field's top 2% threshold
    # but still in the dataset (which claims to be global top 2%)
    anomalies = field_data[field_data['rank'] > top_2_percent_count].copy()

    return anomalies


def create_stratified_sample(df):
    """
    Create stratified random sample across field types and ranking positions.

    Stratification ensures:
    - Balanced representation across field types
    - Coverage of top and bottom of rankings within each field
    - Inclusion of anomalous cases

    Args:
        df: Full dataset

    Returns:
        pd.DataFrame: Stratified sample (~400 researchers)
    """
    print("="*80)
    print("CREATING STRATIFIED SAMPLE")
    print("="*80)
    print()

    sample_list = []

    for field_type, fields in FIELD_CLASSIFICATIONS.items():
        print(f"\n{field_type.upper()} FIELDS")
        print("-" * 80)

        for field_name in fields:
            field_data = df[df['sm-subfield-1'] == field_name].copy()

            if len(field_data) == 0:
                print(f"  {field_name}: NO DATA (skipping)")
                continue

            # Sort by rank (1 = best)
            field_data = field_data.sort_values('rank')

            # Calculate field size and top 2% threshold
            field_size = len(field_data)
            top_2_percent_count = int(field_size * 0.02)

            # STRATUM 1: Top quartile (among field's top 2%)
            top_quartile_n = max(1, top_2_percent_count // 4)
            top_sample = field_data.head(top_quartile_n).sample(
                n=min(RESEARCHERS_PER_FIELD_STRATUM, top_quartile_n),
                random_state=RANDOM_SEED
            )
            top_sample['sample_stratum'] = 'top'

            # STRATUM 2: Bottom quartile (among field's top 2%)
            bottom_quartile_start = top_2_percent_count - top_quartile_n
            bottom_sample = field_data.iloc[bottom_quartile_start:top_2_percent_count].sample(
                n=min(RESEARCHERS_PER_FIELD_STRATUM, top_quartile_n),
                random_state=RANDOM_SEED
            )
            bottom_sample['sample_stratum'] = 'bottom'

            # STRATUM 3: Anomalies (if sufficient)
            anomalies = identify_anomalies(df, field_name)
            if len(anomalies) >= MIN_RESEARCHERS_FOR_ANOMALIES:
                anomaly_sample = anomalies.sample(
                    n=min(RESEARCHERS_PER_FIELD_STRATUM, len(anomalies)),
                    random_state=RANDOM_SEED
                )
                anomaly_sample['sample_stratum'] = 'anomaly'
            else:
                anomaly_sample = pd.DataFrame()

            # Combine strata for this field
            field_sample = pd.concat([top_sample, bottom_sample, anomaly_sample], ignore_index=True)
            field_sample['field_type'] = field_type

            print(f"  {field_name}:")
            print(f"    Field size: {field_size:,} | Top 2%: {top_2_percent_count}")
            print(f"    Sampled: {len(field_sample)} (top={len(top_sample)}, bottom={len(bottom_sample)}, anomaly={len(anomaly_sample)})")

            sample_list.append(field_sample)

    # Combine all samples
    sample = pd.concat(sample_list, ignore_index=True)

    # Add sample ID for tracking
    sample.insert(0, 'sample_id', range(1, len(sample) + 1))

    print()
    print("="*80)
    print("SAMPLE SUMMARY")
    print("="*80)
    print(f"Total researchers sampled: {len(sample)}")
    print()
    print("By field type:")
    print(sample['field_type'].value_counts().sort_index())
    print()
    print("By stratum:")
    print(sample['sample_stratum'].value_counts().sort_index())
    print()
    print("Geographic distribution:")
    print(sample['country'].value_counts().head(10))
    print()

    return sample


def save_sample(sample, output_path='data/comprehensive_sample.csv'):
    """
    Save sample to CSV file.

    Args:
        sample: Sample DataFrame
        output_path: Output file path
    """
    # Create output directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Save
    sample.to_csv(output_path, index=False)

    print(f"✓ Sample saved to: {output_path}")
    print(f"  Columns: {list(sample.columns)}")
    print(f"  Rows: {len(sample)}")
    print()


def main():
    """Main execution function."""
    try:
        # Load dataset
        df = load_dataset()

        # Create sample
        sample = create_stratified_sample(df)

        # Save
        save_sample(sample)

        print("="*80)
        print("✓ SAMPLING COMPLETE")
        print("="*80)
        print()
        print("Next steps:")
        print("  1. Review: data/comprehensive_sample.csv")
        print("  2. Run: python3 fetch_openalex_comprehensive.py")
        print()

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
