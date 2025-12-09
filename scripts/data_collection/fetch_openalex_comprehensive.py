"""
Fetch comprehensive publication data from OpenAlex for all sampled researchers.

This script:
1. Loads the comprehensive sample (397 researchers)
2. Searches for each researcher in OpenAlex
3. Fetches all their publications with publisher information
4. Categorizes publications by type (book, article, chapter, etc.)
5. Identifies publishers (Elsevier, Wiley, PLOS, Springer, etc.)
6. Saves detailed results for bias analysis

OpenAlex API: https://api.openalex.org (free, no auth required)
"""

import pandas as pd
import requests
import time
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os

# Configuration
OPENALEX_API_BASE = "https://api.openalex.org"
EMAIL = "research@example.com"  # Required for polite pool (faster response)
DELAY_BETWEEN_REQUESTS = 0.2  # Be polite
CHECKPOINT_INTERVAL = 50  # Save progress every N researchers

# Publisher classifications
PUBLISHER_GROUPS = {
    'Elsevier': [
        'elsevier',
        'cell press',
        'the lancet',
        'academic press',
    ],
    'Wiley': [
        'wiley',
        'john wiley',
        'wiley-blackwell',
        'blackwell'
    ],
    'Springer Nature': [
        'springer',
        'nature',
        'palgrave',
        'springer nature',
        'bmc',
    ],
    'Taylor & Francis': [
        'taylor',
        'francis',
        'routledge',
        'crc press',
        'informa'
    ],
    'PLOS': [
        'plos',
        'public library of science'
    ],
    'Frontiers': [
        'frontiers'
    ],
    'MDPI': [
        'mdpi'
    ],
    'Oxford': [
        'oxford university press',
        'oup'
    ],
    'Cambridge': [
        'cambridge university press',
        'cup'
    ],
    'IEEE': [
        'ieee',
        'institute of electrical'
    ],
    'ACM': [
        'acm',
        'association for computing machinery'
    ],
    'ACS': [
        'american chemical society',
        'acs publications'
    ],
}


def classify_publisher(publisher_name: str) -> str:
    """Classify a publisher into major groups."""
    if not publisher_name or publisher_name == 'Unknown':
        return 'Unknown'

    publisher_lower = publisher_name.lower()

    for group, variants in PUBLISHER_GROUPS.items():
        if any(variant in publisher_lower for variant in variants):
            return group

    return 'Other'


def search_openalex_author(name: str, institution: str = None) -> Optional[Dict]:
    """
    Search for an author in OpenAlex by name.

    Returns the best match based on name similarity and institution.
    """
    # Clean name for search
    search_name = name.replace(',', '').strip()

    url = f"{OPENALEX_API_BASE}/authors"
    params = {
        'search': search_name,
        'per_page': 10,
        'mailto': EMAIL
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        results = data.get('results', [])
        if not results:
            return None

        # Return first result (could be improved with institution matching)
        return results[0]

    except Exception as e:
        print(f"    Error searching: {e}")
        return None


def fetch_all_works(author_id: str) -> List[Dict]:
    """
    Fetch ALL publications for an author from OpenAlex.

    Handles pagination to get complete publication list.
    """
    # Clean author ID
    if 'openalex.org' in author_id:
        author_id = author_id.split('/')[-1]

    all_works = []
    page = 1
    per_page = 200  # Max allowed

    while True:
        url = f"{OPENALEX_API_BASE}/works"
        params = {
            'filter': f'author.id:{author_id}',
            'per_page': per_page,
            'page': page,
            'mailto': EMAIL
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            results = data.get('results', [])
            if not results:
                break

            for work in results:
                # Extract key information
                primary_location = work.get('primary_location', {}) or {}
                source = primary_location.get('source', {}) or {}

                publisher_raw = source.get('host_organization_name', 'Unknown')
                publisher_group = classify_publisher(publisher_raw)

                work_type = work.get('type', 'unknown')
                is_book = work_type in ['book', 'book-chapter', 'monograph', 'edited-book']

                oa_status = work.get('open_access', {}) or {}
                is_oa = oa_status.get('is_oa', False)

                all_works.append({
                    'work_id': work.get('id', ''),
                    'title': work.get('title', 'Unknown'),
                    'year': work.get('publication_year'),
                    'type': work_type,
                    'is_book': is_book,
                    'cited_by_count': work.get('cited_by_count', 0),
                    'venue': source.get('display_name', 'Unknown'),
                    'publisher_raw': publisher_raw,
                    'publisher_group': publisher_group,
                    'is_oa': is_oa,
                    'doi': work.get('doi'),
                })

            # Check if there are more pages
            meta = data.get('meta', {})
            count = meta.get('count', 0)
            if page * per_page >= count:
                break

            page += 1
            time.sleep(0.1)  # Brief delay between pages

        except Exception as e:
            print(f"    Error fetching page {page}: {e}")
            break

    return all_works


def calculate_metrics(works: List[Dict]) -> Dict:
    """
    Calculate comprehensive metrics from publication list.
    """
    if not works:
        return {
            'total_works': 0,
            'total_citations': 0,
        }

    df = pd.DataFrame(works)

    # Overall counts
    total_works = len(df)
    total_citations = df['cited_by_count'].sum()

    # By type
    books = df[df['is_book'] == True]
    articles = df[df['is_book'] == False]

    # By publisher
    publisher_counts = df['publisher_group'].value_counts().to_dict()

    # Open access
    oa_works = df[df['is_oa'] == True]

    # Elsevier-specific
    elsevier_works = df[df['publisher_group'] == 'Elsevier']
    elsevier_count = len(elsevier_works)
    elsevier_citations = elsevier_works['cited_by_count'].sum()

    # Non-Elsevier major publishers
    wiley_count = len(df[df['publisher_group'] == 'Wiley'])
    springer_count = len(df[df['publisher_group'] == 'Springer Nature'])
    plos_count = len(df[df['publisher_group'] == 'PLOS'])
    frontiers_count = len(df[df['publisher_group'] == 'Frontiers'])
    oa_publisher_count = plos_count + frontiers_count + len(df[df['publisher_group'] == 'MDPI'])

    return {
        'total_works': total_works,
        'total_citations': total_citations,
        'books_count': len(books),
        'books_pct': len(books) / total_works * 100 if total_works > 0 else 0,
        'articles_count': len(articles),
        'oa_count': len(oa_works),
        'oa_pct': len(oa_works) / total_works * 100 if total_works > 0 else 0,
        'elsevier_count': elsevier_count,
        'elsevier_pct': elsevier_count / total_works * 100 if total_works > 0 else 0,
        'elsevier_citations': elsevier_citations,
        'elsevier_citations_pct': elsevier_citations / total_citations * 100 if total_citations > 0 else 0,
        'wiley_count': wiley_count,
        'wiley_pct': wiley_count / total_works * 100 if total_works > 0 else 0,
        'springer_count': springer_count,
        'springer_pct': springer_count / total_works * 100 if total_works > 0 else 0,
        'plos_count': plos_count,
        'frontiers_count': frontiers_count,
        'oa_publisher_count': oa_publisher_count,
        'oa_publisher_pct': oa_publisher_count / total_works * 100 if total_works > 0 else 0,
        'publisher_counts': json.dumps(publisher_counts),
    }


def process_sample(sample_df: pd.DataFrame, checkpoint_file: str = 'fetch_checkpoint.csv') -> pd.DataFrame:
    """
    Fetch OpenAlex data for all researchers in the sample.

    Includes checkpointing to resume if interrupted.
    """
    results = []

    # Load checkpoint if exists
    start_idx = 0
    if os.path.exists(checkpoint_file):
        print(f"Found checkpoint file: {checkpoint_file}")
        checkpoint_df = pd.read_csv(checkpoint_file)
        results = checkpoint_df.to_dict('records')
        start_idx = len(results)
        print(f"Resuming from researcher #{start_idx + 1}")

    for idx in range(start_idx, len(sample_df)):
        row = sample_df.iloc[idx]

        sample_id = row['sample_id']
        name = row['authfull']
        field = row['sm-subfield-1']
        field_type = row['field_type']
        stratum = row['sample_stratum']
        institution = row.get('institution', 'Unknown')

        scopus_pubs = row['scopus_pubs']
        scopus_citations = row['scopus_citations']
        scopus_h = row['scopus_h_index']

        print(f"\n[{idx + 1}/{len(sample_df)}] {name}")
        print(f"  Field: {field} ({field_type}, {stratum})")
        print(f"  Scopus: {scopus_pubs} pubs, {scopus_citations:,} citations, h={scopus_h}")

        # Search for author
        author_data = search_openalex_author(name, institution)

        if not author_data:
            print(f"  ❌ Not found in OpenAlex")
            results.append({
                'sample_id': sample_id,
                'authfull': name,
                'field': field,
                'field_type': field_type,
                'sample_stratum': stratum,
                'scopus_pubs': scopus_pubs,
                'scopus_citations': scopus_citations,
                'scopus_h_index': scopus_h,
                'openalex_found': False,
                'match_quality': 'not_found',
            })
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        # Extract author info
        openalex_id = author_data.get('id', '')
        openalex_name = author_data.get('display_name', '')
        openalex_summary = author_data.get('summary_stats', {}) or {}

        print(f"  ✓ Found: {openalex_name}")
        print(f"  OpenAlex ID: {openalex_id}")

        # Fetch all works
        print(f"  Fetching publications...")
        works = fetch_all_works(openalex_id)

        if not works:
            print(f"  ⚠️  No publications found")
            results.append({
                'sample_id': sample_id,
                'authfull': name,
                'field': field,
                'field_type': field_type,
                'sample_stratum': stratum,
                'scopus_pubs': scopus_pubs,
                'scopus_citations': scopus_citations,
                'scopus_h_index': scopus_h,
                'openalex_found': True,
                'openalex_id': openalex_id,
                'openalex_name': openalex_name,
                'openalex_pubs': 0,
                'match_quality': 'found_no_works',
            })
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        # Calculate metrics
        metrics = calculate_metrics(works)

        openalex_pubs = metrics['total_works']
        openalex_citations = metrics['total_citations']

        # Coverage ratios
        coverage_ratio = scopus_pubs / openalex_pubs if openalex_pubs > 0 else 0
        citation_coverage = scopus_citations / openalex_citations if openalex_citations > 0 else 0

        print(f"  ✓ Found {openalex_pubs} publications ({metrics['books_count']} books)")
        print(f"  Coverage: {coverage_ratio:.1%} (publications), {citation_coverage:.1%} (citations)")
        print(f"  Publishers: Elsevier {metrics['elsevier_pct']:.1f}%, Wiley {metrics['wiley_pct']:.1f}%, "
              f"OA {metrics['oa_publisher_pct']:.1f}%")

        # Save individual works to separate file
        works_df = pd.DataFrame(works)
        works_file = f"works_{sample_id:03d}_{name.replace(', ', '_').replace(' ', '_')[:50]}.csv"
        works_df.to_csv(f"openalex_works/{works_file}", index=False)

        # Compile result
        result = {
            'sample_id': sample_id,
            'authfull': name,
            'field': field,
            'field_type': field_type,
            'sample_stratum': stratum,
            'scopus_pubs': scopus_pubs,
            'scopus_citations': scopus_citations,
            'scopus_h_index': scopus_h,
            'openalex_found': True,
            'openalex_id': openalex_id,
            'openalex_name': openalex_name,
            'openalex_pubs': openalex_pubs,
            'openalex_citations': openalex_citations,
            'coverage_ratio': coverage_ratio,
            'citation_coverage': citation_coverage,
            'match_quality': 'good',
            **metrics
        }

        results.append(result)

        # Checkpoint every N researchers
        if (idx + 1) % CHECKPOINT_INTERVAL == 0:
            checkpoint_df = pd.DataFrame(results)
            checkpoint_df.to_csv(checkpoint_file, index=False)
            print(f"\n  💾 Checkpoint saved ({len(results)} researchers processed)")

        time.sleep(DELAY_BETWEEN_REQUESTS)

    return pd.DataFrame(results)


def main():
    """
    Main execution: Fetch OpenAlex data for comprehensive sample.
    """
    print("=" * 80)
    print("OPENALEX DATA COLLECTION - COMPREHENSIVE SAMPLE")
    print("=" * 80)

    # Load sample
    sample_file = 'comprehensive_sample.csv'
    if not os.path.exists(sample_file):
        print(f"\n❌ Sample file not found: {sample_file}")
        print("Run create_stratified_sample.py first!")
        return

    sample_df = pd.read_csv(sample_file)
    print(f"\n✓ Loaded sample: {len(sample_df)} researchers")

    # Create output directory for individual works
    os.makedirs('openalex_works', exist_ok=True)

    # Estimate time
    estimated_minutes = len(sample_df) * DELAY_BETWEEN_REQUESTS * 1.5 / 60
    print(f"\nEstimated time: {estimated_minutes:.1f} minutes")
    print(f"With checkpointing every {CHECKPOINT_INTERVAL} researchers\n")

    start_time = datetime.now()

    # Process all researchers
    results_df = process_sample(sample_df)

    # Save final results
    output_file = 'evidence_summary_table.csv'
    results_df.to_csv(output_file, index=False)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60

    print(f"\n{'=' * 80}")
    print(f"✓ DATA COLLECTION COMPLETE")
    print(f"{'=' * 80}")
    print(f"\nResults saved to: {output_file}")
    print(f"Individual works saved to: openalex_works/ directory")
    print(f"Total time: {duration:.1f} minutes")

    # Summary statistics
    found = results_df[results_df['openalex_found'] == True]
    not_found = results_df[results_df['openalex_found'] == False]

    print(f"\n{'=' * 80}")
    print(f"SUMMARY")
    print(f"{'=' * 80}")
    print(f"\nMatching:")
    print(f"  Found in OpenAlex: {len(found)} ({len(found) / len(results_df) * 100:.1f}%)")
    print(f"  Not found: {len(not_found)} ({len(not_found) / len(results_df) * 100:.1f}%)")

    if len(found) > 0:
        print(f"\nCoverage (n={len(found)}):")
        print(f"  Median publication coverage: {found['coverage_ratio'].median():.1%}")
        print(f"  Median citation coverage: {found['citation_coverage'].median():.1%}")
        print(f"  Mean publication coverage: {found['coverage_ratio'].mean():.1%}")

        print(f"\nPublisher Distribution:")
        print(f"  Median Elsevier %: {found['elsevier_pct'].median():.1f}%")
        print(f"  Median Wiley %: {found['wiley_pct'].median():.1f}%")
        print(f"  Median Springer Nature %: {found['springer_pct'].median():.1f}%")
        print(f"  Median OA publishers %: {found['oa_publisher_pct'].median():.1f}%")

        print(f"\nPublication Types:")
        print(f"  Median book %: {found['books_pct'].median():.1f}%")
        print(f"  Median open access %: {found['oa_pct'].median():.1f}%")

        # By field type
        print(f"\n{'=' * 80}")
        print(f"BY FIELD TYPE")
        print(f"{'=' * 80}")

        for field_type in ['book_heavy', 'mixed', 'journal_heavy']:
            subset = found[found['field_type'] == field_type]
            if len(subset) > 0:
                print(f"\n{field_type.upper()} (n={len(subset)}):")
                print(f"  Coverage ratio: {subset['coverage_ratio'].median():.1%}")
                print(f"  Book %: {subset['books_pct'].median():.1f}%")
                print(f"  Elsevier %: {subset['elsevier_pct'].median():.1f}%")

        # Clean up checkpoint file
        if os.path.exists('fetch_checkpoint.csv'):
            os.remove('fetch_checkpoint.csv')
            print(f"\n✓ Checkpoint file removed")

    print(f"\nNext step: Run analysis scripts to test for bias")
    print(f"  python3 analyze_coverage_bias.py")


if __name__ == "__main__":
    main()
