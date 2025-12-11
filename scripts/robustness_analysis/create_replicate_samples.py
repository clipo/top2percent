#!/usr/bin/env python3
"""
Create 5 Independent Replicate Samples
=======================================

Generates 5 independent stratified random samples (n=400 each)
from the full Ioannidis 2024 career rankings.

Stratification matches original study:
- Field type (book-heavy vs journal-heavy)
- Rank percentiles (to ensure range of rankings)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_full_rankings():
    """Load the full 2024 career rankings from Excel."""

    print("Loading full rankings...")
    rankings_path = Path("August 2025 data-update for Updated science-wide a/Table_1_Authors_career_2024_pubs_since_1788_wopp_extracted_202508.xlsx")

    if not rankings_path.exists():
        print(f"✗ Could not find rankings at: {rankings_path}")
        return None

    # Load Excel file (may take a minute - it's 85MB)
    # The data is in the 'Data' sheet, not the default 'Key' sheet
    df = pd.read_excel(rankings_path, sheet_name='Data')

    print(f"✓ Loaded {len(df):,} researchers from full rankings")
    print(f"  Columns: {list(df.columns)[:10]}...")

    return df

def classify_field_type(df):
    """Classify fields as book-heavy or journal-heavy based on discipline."""

    # Book-heavy fields (humanities, social sciences, some arts)
    book_heavy_fields = [
        'Archaeology', 'Architecture', 'Art & Art History', 'Classics',
        'Communication & Textual Studies', 'Historical Studies', 'History & Philosophy Of Science',
        'Literature', 'Music & Musicology', 'Philosophy', 'Religion',
        'Anthropology', 'Economics & Business', 'Education', 'Geography',
        'Law', 'Political Science', 'Public Administration', 'Social Studies',
        'Sociology'
    ]

    # Get field column (might be 'sm-subfield-1' or similar)
    field_col = None
    for col in df.columns:
        if 'field' in col.lower() or 'subfield' in col.lower():
            field_col = col
            break

    if field_col:
        df['field_type'] = df[field_col].apply(
            lambda x: 'book_heavy' if x in book_heavy_fields else 'journal_heavy'
        )
    else:
        # If no field column, create random assignment (not ideal but better than nothing)
        print("  Warning: No field column found, assigning random field types")
        df['field_type'] = np.random.choice(['book_heavy', 'journal_heavy'], size=len(df))

    return df

def create_stratified_sample(df, n=400, random_state=42):
    """Create a stratified random sample."""

    np.random.seed(random_state)

    # Add rank percentiles
    df['rank_percentile'] = pd.qcut(range(len(df)), q=5, labels=['0-20', '20-40', '40-60', '60-80', '80-100'])

    # Classify field types
    df = classify_field_type(df)

    # Stratified sample by field_type × rank_percentile
    sample = df.groupby(['field_type', 'rank_percentile'], group_keys=False).apply(
        lambda x: x.sample(n=max(1, int(len(x) * n / len(df))), random_state=random_state)
    )

    # Ensure exact sample size
    if len(sample) < n:
        remaining = df[~df.index.isin(sample.index)].sample(n=n - len(sample), random_state=random_state)
        sample = pd.concat([sample, remaining])
    elif len(sample) > n:
        sample = sample.sample(n=n, random_state=random_state)

    return sample.reset_index(drop=True)

def create_all_replicates(n_replicates=5, sample_size=400):
    """Create all replicate samples."""

    print("="*80)
    print("CREATING INDEPENDENT REPLICATE SAMPLES")
    print("="*80)

    # Load full rankings
    rankings = load_full_rankings()
    if rankings is None:
        return

    # Create output directory
    output_dir = Path("robustness_analysis/replicates")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nCreating {n_replicates} independent samples (n={sample_size} each)...")

    samples_created = []

    for i in range(n_replicates):
        print(f"\n--- Replicate {i+1}/{n_replicates} ---")

        # Different random seed for each
        random_state = 2000 + i

        # Create sample
        sample = create_stratified_sample(rankings, n=sample_size, random_state=random_state)

        # Add sample ID column
        sample['sample_id'] = range(1, len(sample) + 1)
        sample['replicate'] = i + 1

        # Save
        output_file = output_dir / f"replicate_{i+1}_n{sample_size}.csv"
        sample.to_csv(output_file, index=False)

        print(f"  ✓ Created sample: {len(sample)} researchers")
        print(f"  ✓ Field distribution:")
        print(f"     - Book-heavy: {(sample['field_type']=='book_heavy').sum()}")
        print(f"     - Journal-heavy: {(sample['field_type']=='journal_heavy').sum()}")
        print(f"  ✓ Saved to: {output_file}")

        samples_created.append({
            'replicate': i + 1,
            'n': len(sample),
            'book_heavy': (sample['field_type']=='book_heavy').sum(),
            'journal_heavy': (sample['field_type']=='journal_heavy').sum(),
            'random_seed': random_state
        })

    # Save metadata
    metadata_df = pd.DataFrame(samples_created)
    metadata_df.to_csv(output_dir / "replicate_metadata.csv", index=False)

    print("\n" + "="*80)
    print("✓ ALL REPLICATES CREATED")
    print("="*80)
    print(f"\nSamples saved to: {output_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Match each replicate to OpenAlex (run match_replicates_to_openalex.py)")
    print(f"  2. Calculate effect sizes for each (run analyze_replicates.py)")
    print(f"  3. Compare across replicates (run compare_replicates.py)")

def main():
    """Main execution."""
    create_all_replicates(n_replicates=5, sample_size=400)

if __name__ == "__main__":
    main()
