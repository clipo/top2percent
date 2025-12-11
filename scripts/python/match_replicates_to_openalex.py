#!/usr/bin/env python3
"""
Match Replicate Samples to OpenAlex
====================================

Matches all 5 independent replicate samples (n=400 each) to OpenAlex.

For each replicate:
1. Loads the sample CSV
2. Searches for each researcher in OpenAlex
3. Fetches all their publications
4. Calculates coverage metrics (Elsevier %, book %, OA %, etc.)
5. Saves results

This enables calculating effect sizes for each independent replicate.
"""

import pandas as pd
import requests
import time
import json
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration
OPENALEX_API_BASE = "https://api.openalex.org"
EMAIL = "research@example.com"
DELAY_BETWEEN_REQUESTS = 0.2
CHECKPOINT_INTERVAL = 50

# Publisher classifications
PUBLISHER_GROUPS = {
    'Elsevier': ['elsevier', 'cell press', 'the lancet', 'academic press'],
    'Wiley': ['wiley', 'john wiley', 'wiley-blackwell', 'blackwell'],
    'Springer Nature': ['springer', 'nature', 'palgrave', 'springer nature', 'bmc'],
    'Taylor & Francis': ['taylor', 'francis', 'routledge', 'crc press', 'informa'],
    'PLOS': ['plos', 'public library of science'],
    'Frontiers': ['frontiers'],
    'MDPI': ['mdpi'],
    'Oxford': ['oxford university press', 'oup'],
    'Cambridge': ['cambridge university press', 'cup'],
    'IEEE': ['ieee', 'institute of electrical'],
    'ACM': ['acm', 'association for computing machinery'],
    'ACS': ['american chemical society', 'acs publications'],
}

def classify_publisher(publisher_name):
    """Classify a publisher into major groups."""
    if not publisher_name or publisher_name == 'Unknown':
        return 'Unknown'

    publisher_lower = publisher_name.lower()

    for group, variants in PUBLISHER_GROUPS.items():
        if any(variant in publisher_lower for variant in variants):
            return group

    return 'Other'

def search_openalex_author(name, institution=None):
    """Search for an author in OpenAlex by name."""
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

        return results[0]

    except Exception as e:
        print(f"    Error searching: {e}")
        return None

def fetch_all_works(author_id):
    """Fetch ALL publications for an author from OpenAlex."""
    if 'openalex.org' in author_id:
        author_id = author_id.split('/')[-1]

    all_works = []
    page = 1
    per_page = 200

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

            meta = data.get('meta', {})
            count = meta.get('count', 0)
            if page * per_page >= count:
                break

            page += 1
            time.sleep(0.1)

        except Exception as e:
            print(f"    Error fetching page {page}: {e}")
            break

    return all_works

def calculate_metrics(works):
    """Calculate comprehensive metrics from publication list."""
    if not works:
        return {
            'total_works': 0,
            'total_citations': 0,
            'books_count': 0,
            'books_pct': 0,
            'articles_count': 0,
            'oa_count': 0,
            'oa_pct': 0,
            'elsevier_count': 0,
            'elsevier_pct': 0,
            'elsevier_citations': 0,
            'elsevier_citations_pct': 0,
            'wiley_count': 0,
            'wiley_pct': 0,
            'springer_count': 0,
            'springer_pct': 0,
            'plos_count': 0,
            'frontiers_count': 0,
            'oa_publisher_count': 0,
            'oa_publisher_pct': 0,
        }

    df = pd.DataFrame(works)

    total_works = len(df)
    total_citations = df['cited_by_count'].sum()

    books = df[df['is_book'] == True]
    articles = df[df['is_book'] == False]

    oa_works = df[df['is_oa'] == True]

    elsevier_works = df[df['publisher_group'] == 'Elsevier']
    elsevier_count = len(elsevier_works)
    elsevier_citations = elsevier_works['cited_by_count'].sum()

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
    }

def process_replicate(replicate_num, replicate_df, output_dir):
    """Process a single replicate sample."""

    print(f"\n{'='*80}")
    print(f"PROCESSING REPLICATE {replicate_num}")
    print(f"{'='*80}")
    print(f"Sample size: {len(replicate_df)} researchers\n")

    results = []
    checkpoint_file = output_dir / f"checkpoint_replicate_{replicate_num}.csv"

    # Load checkpoint if exists
    start_idx = 0
    if checkpoint_file.exists():
        print(f"Found checkpoint file, resuming from {checkpoint_file}")
        checkpoint_df = pd.read_csv(checkpoint_file)
        results = checkpoint_df.to_dict('records')
        start_idx = len(results)
        print(f"Resuming from researcher #{start_idx + 1}\n")

    for idx in range(start_idx, len(replicate_df)):
        row = replicate_df.iloc[idx]

        sample_id = row['sample_id']
        name = row['authfull']
        field = row.get('sm-subfield-1', 'Unknown')
        field_type = row['field_type']
        institution = row.get('inst_name', 'Unknown')

        scopus_pubs = row.get('np6024', 0)
        scopus_citations = row.get('nc9624 (ns)', 0)
        scopus_h = row.get('h24 (ns)', 0)

        print(f"[{idx + 1}/{len(replicate_df)}] {name}")
        print(f"  Field: {field} ({field_type})")
        print(f"  Scopus: {scopus_pubs} pubs, {scopus_citations:,} citations, h={scopus_h}")

        # Search for author
        author_data = search_openalex_author(name, institution)

        if not author_data:
            print(f"  ❌ Not found in OpenAlex")
            results.append({
                'sample_id': sample_id,
                'replicate': replicate_num,
                'authfull': name,
                'field': field,
                'field_type': field_type,
                'institution': institution,
                'scopus_pubs': scopus_pubs,
                'scopus_citations': scopus_citations,
                'scopus_h_index': scopus_h,
                'openalex_found': False,
                'match_quality': 'not_found',
                'total_works': 0,
                'total_citations': 0,
                'books_count': 0,
                'books_pct': 0,
                'articles_count': 0,
                'oa_count': 0,
                'oa_pct': 0,
                'elsevier_count': 0,
                'elsevier_pct': 0,
                'coverage_ratio': 0,
            })
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        # Extract author info
        openalex_id = author_data.get('id', '')
        openalex_name = author_data.get('display_name', '')

        print(f"  ✓ Found: {openalex_name}")

        # Fetch all works
        works = fetch_all_works(openalex_id)

        if not works:
            print(f"  ⚠️  No publications found")
            results.append({
                'sample_id': sample_id,
                'replicate': replicate_num,
                'authfull': name,
                'field': field,
                'field_type': field_type,
                'institution': institution,
                'scopus_pubs': scopus_pubs,
                'scopus_citations': scopus_citations,
                'scopus_h_index': scopus_h,
                'openalex_found': True,
                'openalex_id': openalex_id,
                'openalex_name': openalex_name,
                'match_quality': 'found_no_works',
                'total_works': 0,
                'total_citations': 0,
                'books_count': 0,
                'books_pct': 0,
                'articles_count': 0,
                'oa_count': 0,
                'oa_pct': 0,
                'elsevier_count': 0,
                'elsevier_pct': 0,
                'coverage_ratio': 0,
            })
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        # Calculate metrics
        metrics = calculate_metrics(works)

        openalex_pubs = metrics['total_works']
        openalex_citations = metrics['total_citations']

        coverage_ratio = scopus_pubs / openalex_pubs if openalex_pubs > 0 else 0
        citation_coverage = scopus_citations / openalex_citations if openalex_citations > 0 else 0

        print(f"  ✓ {openalex_pubs} pubs ({metrics['books_count']} books)")
        print(f"  Coverage: {coverage_ratio:.1%} (pubs), {citation_coverage:.1%} (cites)")
        print(f"  Elsevier: {metrics['elsevier_pct']:.1f}%, Books: {metrics['books_pct']:.1f}%, OA: {metrics['oa_pct']:.1f}%")

        # Compile result
        result = {
            'sample_id': sample_id,
            'replicate': replicate_num,
            'authfull': name,
            'field': field,
            'field_type': field_type,
            'institution': institution,
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

        # Checkpoint
        if (idx + 1) % CHECKPOINT_INTERVAL == 0:
            checkpoint_df = pd.DataFrame(results)
            checkpoint_df.to_csv(checkpoint_file, index=False)
            print(f"\n  💾 Checkpoint saved ({len(results)} processed)")

        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save final results
    results_df = pd.DataFrame(results)
    output_file = output_dir / f"replicate_{replicate_num}_openalex_data.csv"
    results_df.to_csv(output_file, index=False)

    # Clean up checkpoint
    if checkpoint_file.exists():
        checkpoint_file.unlink()

    # Summary
    found = results_df[results_df['openalex_found'] == True]
    print(f"\n{'='*80}")
    print(f"REPLICATE {replicate_num} COMPLETE")
    print(f"{'='*80}")
    print(f"Matched: {len(found)}/{len(results_df)} ({len(found)/len(results_df)*100:.1f}%)")
    print(f"Median coverage: {found['coverage_ratio'].median():.1%}")
    print(f"Median Elsevier %: {found['elsevier_pct'].median():.1f}%")
    print(f"Median Books %: {found['books_pct'].median():.1f}%")
    print(f"Median OA %: {found['oa_pct'].median():.1f}%")
    print(f"Saved to: {output_file}")

    return results_df

def match_all_replicates(n_replicates=5):
    """Match all replicate samples to OpenAlex."""

    print("="*80)
    print("MATCH REPLICATE SAMPLES TO OPENALEX")
    print("="*80)

    # Input/output directories
    replicate_dir = Path("robustness_analysis/replicates")
    output_dir = Path("robustness_analysis/openalex_matched")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Estimate time
    est_minutes = n_replicates * 400 * DELAY_BETWEEN_REQUESTS / 60
    print(f"\nEstimated time: {est_minutes:.1f} minutes ({est_minutes/60:.1f} hours)")
    print(f"With checkpointing every {CHECKPOINT_INTERVAL} researchers\n")

    start_time = datetime.now()

    all_results = []

    for i in range(1, n_replicates + 1):
        # Load replicate
        replicate_file = replicate_dir / f"replicate_{i}_n400.csv"

        if not replicate_file.exists():
            print(f"\n⚠️  Replicate {i} not found: {replicate_file}")
            continue

        replicate_df = pd.read_csv(replicate_file)

        # Process replicate
        results_df = process_replicate(i, replicate_df, output_dir)
        all_results.append(results_df)

    # Combine all replicates
    combined_df = pd.concat(all_results, ignore_index=True)
    combined_file = output_dir / "all_replicates_combined.csv"
    combined_df.to_csv(combined_file, index=False)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60

    print(f"\n{'='*80}")
    print(f"✓ ALL REPLICATES MATCHED")
    print(f"{'='*80}")
    print(f"Total time: {duration:.1f} minutes ({duration/60:.1f} hours)")
    print(f"Combined results: {combined_file}")
    print(f"\nNext steps:")
    print(f"  1. Run analyze_all_replicates.py to calculate effect sizes")
    print(f"  2. Run generate_robustness_report.py to create summary")

def main():
    """Main execution."""
    match_all_replicates(n_replicates=5)

if __name__ == "__main__":
    main()
