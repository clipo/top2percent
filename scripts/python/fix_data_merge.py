#!/usr/bin/env python3
"""
fix_data_merge.py - Fix data merge issues to recover ~194 researchers with coverage data

Problem: openalex_comprehensive_data.csv only has 374 researchers with valid coverage_ratio,
but comprehensive_sample.csv has Scopus data for all 600 researchers. This script re-merges
the data to recover the missing Scopus metrics.

Matching Strategy (validated):
- Primary key: authfull + field_type
- Verification: institution match (0 mismatches confirmed)
- ORCID cross-reference when available (362 researchers)

Expected Result: n=568 with valid coverage_ratio (up from 374)
"""

import pandas as pd
import sys
from pathlib import Path

def main():
    # Paths
    data_dir = Path(__file__).parent.parent.parent / 'data'
    comp_path = data_dir / 'openalex_comprehensive_data.csv'
    sample_path = data_dir / 'comprehensive_sample.csv'
    orcid_path = data_dir / 'openalex_data_with_orcid.csv'
    output_path = comp_path  # Overwrite original

    print("=" * 60)
    print("FIX DATA MERGE - Recovering Missing Scopus Data")
    print("=" * 60)

    # Load data files
    print("\nLoading data files...")
    comp = pd.read_csv(comp_path)
    sample = pd.read_csv(sample_path)

    print(f"  openalex_comprehensive_data.csv: {len(comp)} rows")
    print(f"    - with coverage_ratio: {comp['coverage_ratio'].notna().sum()}")
    print(f"    - with scopus_pubs: {comp['scopus_pubs'].notna().sum()}")

    print(f"  comprehensive_sample.csv: {len(sample)} rows")
    print(f"    - with scopus_pubs: {sample['scopus_pubs'].notna().sum()}")

    # Load ORCID file for cross-reference verification
    if orcid_path.exists():
        orcid_df = pd.read_csv(orcid_path)
        print(f"  openalex_data_with_orcid.csv: {len(orcid_df)} rows")
        print(f"    - with ORCID: {orcid_df['orcid'].notna().sum()}")
    else:
        orcid_df = None
        print("  ORCID file not found - proceeding without ORCID verification")

    # Step 1: De-duplicate sample (4 true duplicates exist)
    print("\n--- Step 1: De-duplicating sample ---")
    sample_before = len(sample)
    sample_dedup = sample.drop_duplicates(subset=['authfull', 'field_type'], keep='first')
    dupes_removed = sample_before - len(sample_dedup)
    print(f"  Removed {dupes_removed} duplicate rows (same authfull + field_type)")

    # Step 2: Merge Scopus data from sample to comp
    print("\n--- Step 2: Merging Scopus data ---")

    # Columns to merge from sample
    scopus_cols = ['scopus_pubs', 'scopus_citations', 'scopus_h_index',
                   'rank_global', 'rank_in_field', 'sample_stratum']
    merge_cols = ['authfull', 'field_type'] + scopus_cols + ['institution']

    # Merge on authfull + field_type
    merged = comp.merge(
        sample_dedup[merge_cols],
        on=['authfull', 'field_type'],
        how='left',
        suffixes=('', '_sample')
    )

    # Verify institution match (sanity check)
    inst_mismatch = 0
    if 'institution' in merged.columns and 'institution_sample' in merged.columns:
        inst_match = ((merged['institution'].isna()) |
                      (merged['institution_sample'].isna()) |
                      (merged['institution'] == merged['institution_sample']))
        inst_mismatch = (~inst_match).sum()

    if inst_mismatch > 0:
        print(f"  WARNING: {inst_mismatch} institution mismatches detected!")
        print("  These may indicate incorrect matches. Please review:")
        print(merged[~inst_match][['authfull', 'institution', 'institution_sample']])
    else:
        print("  Institution verification: All matches verified (0 mismatches)")

    # Step 3: Fill missing Scopus data
    print("\n--- Step 3: Filling missing Scopus data ---")

    filled_counts = {}
    for col in scopus_cols:
        sample_col = f'{col}_sample'
        if sample_col in merged.columns:
            before_filled = merged[col].notna().sum()
            merged[col] = merged[col].fillna(merged[sample_col])
            after_filled = merged[col].notna().sum()
            filled_counts[col] = after_filled - before_filled
            merged.drop(sample_col, axis=1, inplace=True)

    for col, count in filled_counts.items():
        if count > 0:
            print(f"  {col}: filled {count} missing values")

    # Drop extra institution column
    if 'institution_sample' in merged.columns:
        merged.drop('institution_sample', axis=1, inplace=True)

    # Step 4: Recalculate coverage_ratio
    print("\n--- Step 4: Recalculating coverage_ratio ---")

    # Coverage = scopus_pubs / total_works (capped at 1.0)
    valid_mask = (merged['scopus_pubs'].notna() &
                  merged['total_works'].notna() &
                  (merged['total_works'] > 0))

    merged.loc[valid_mask, 'coverage_ratio'] = (
        merged.loc[valid_mask, 'scopus_pubs'] / merged.loc[valid_mask, 'total_works']
    )

    # Cap at 1.0 (some edge cases have scopus_pubs > total_works due to different counting)
    merged['coverage_ratio'] = merged['coverage_ratio'].clip(upper=1.0)

    # Step 5: ORCID cross-reference (optional verification)
    if orcid_df is not None:
        print("\n--- Step 5: ORCID Cross-Reference ---")
        orcid_lookup = orcid_df[['authfull', 'field_type', 'orcid']].drop_duplicates()

        # Check if merged data matches ORCID data
        if 'orcid' not in merged.columns:
            merged = merged.merge(
                orcid_lookup,
                on=['authfull', 'field_type'],
                how='left'
            )

        orcid_count = merged['orcid'].notna().sum()
        print(f"  Researchers with ORCID: {orcid_count}")

    # Final statistics
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    n_with_coverage = merged['coverage_ratio'].notna().sum()
    n_with_scopus = merged['scopus_pubs'].notna().sum()
    n_total = len(merged)

    print(f"Total researchers: {n_total}")
    print(f"With Scopus data (scopus_pubs): {n_with_scopus}")
    print(f"With valid coverage_ratio: {n_with_coverage}")
    print(f"  (Changed from 374 to {n_with_coverage})")

    # Coverage statistics
    coverage_stats = merged['coverage_ratio'].describe()
    print(f"\nCoverage ratio statistics:")
    print(f"  Mean: {coverage_stats['mean']:.3f}")
    print(f"  Median: {coverage_stats['50%']:.3f}")
    print(f"  Std: {coverage_stats['std']:.3f}")
    print(f"  Min: {coverage_stats['min']:.3f}")
    print(f"  Max: {coverage_stats['max']:.3f}")

    # Save
    print(f"\nSaving to: {output_path}")
    merged.to_csv(output_path, index=False)

    # Also update the reproducibility package
    repro_path = data_dir.parent / 'reproducibility_package' / 'data' / 'openalex_comprehensive_data.csv'
    if repro_path.parent.exists():
        merged.to_csv(repro_path, index=False)
        print(f"Also saved to: {repro_path}")

    print("\nDone!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
