"""
Fetch Composite Score Metrics for All 550 Matched Researchers
This will take approximately 3-4 hours (550 researchers × ~25 seconds each)

Progress will be saved incrementally so we can resume if interrupted.
"""
import pandas as pd
import numpy as np
import requests
import time
import json
from pathlib import Path

def calculate_h_index(citations_list):
    if not citations_list or len(citations_list) == 0:
        return 0
    sorted_cites = sorted(citations_list, reverse=True)
    h = 0
    for i, cites in enumerate(sorted_cites, 1):
        if cites >= i:
            h = i
        else:
            break
    return h

def calculate_hm_index(citations_list, num_authors_list):
    if not citations_list or len(citations_list) == 0:
        return 0
    adjusted_cites = []
    for cites, n_authors in zip(citations_list, num_authors_list):
        if n_authors > 0:
            adjusted_cites.append(cites / n_authors)
        else:
            adjusted_cites.append(0)
    return calculate_h_index(adjusted_cites)

def fetch_author_metrics(openalex_id, max_works=200):
    """Fetch metrics for one author"""
    if 'openalex.org' in str(openalex_id):
        author_id = str(openalex_id).split('/')[-1]
    else:
        author_id = str(openalex_id)

    works_url = f"https://api.openalex.org/works?filter=author.id:{author_id}&per-page={max_works}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (educational research project)',
        'mailto': 'research@example.edu'
    }

    try:
        response = requests.get(works_url, headers=headers, timeout=30)
        if response.status_code != 200:
            return None

        data = response.json()
        works = data.get('results', [])
        if not works:
            return None

        # Initialize
        total_citations = 0
        single_author_citations = 0
        single_first_author_citations = 0
        single_first_last_author_citations = 0
        all_citations = []
        all_author_counts = []

        for work in works:
            cites = work.get('cited_by_count', 0)
            authorships = work.get('authorships', [])
            n_authors = len(authorships)

            total_citations += cites
            all_citations.append(cites)
            all_author_counts.append(n_authors if n_authors > 0 else 1)

            # Find author's position
            author_position = None
            for j, authorship in enumerate(authorships, 1):
                author_obj = authorship.get('author', {})
                if author_obj.get('id', '').endswith(author_id):
                    author_position = j
                    break

            if author_position is None:
                continue

            # Count by position
            if n_authors == 1:
                single_author_citations += cites
                single_first_author_citations += cites
                single_first_last_author_citations += cites
            elif author_position == 1:
                single_first_author_citations += cites
                single_first_last_author_citations += cites
            elif author_position == n_authors:
                single_first_last_author_citations += cites

        # Calculate indices
        h_index = calculate_h_index(all_citations)
        hm_index = calculate_hm_index(all_citations, all_author_counts)

        return {
            'nc': total_citations,
            'h': h_index,
            'hm': hm_index,
            'ncs': single_author_citations,
            'ncsf': single_first_author_citations,
            'ncsfl': single_first_last_author_citations,
            'n_works': len(works)
        }

    except Exception as e:
        return None

# Output files
OUTPUT_FILE = 'researcher_metrics_all_550.csv'
PROGRESS_FILE = 'fetch_progress.json'
LOG_FILE = 'fetch_all_550.log'

print("="*80)
print("FETCHING METRICS FOR ALL 550 MATCHED RESEARCHERS")
print("="*80)
print(f"\nEstimated time: 3-4 hours")
print(f"Progress saved to: {PROGRESS_FILE}")
print(f"Results saved to: {OUTPUT_FILE}")
print(f"Log saved to: {LOG_FILE}")

# Load data
df = pd.read_csv('reproducibility_package/data/openalex_comprehensive_data.csv')
df_matched = df[df['openalex_found'] == True].copy()

print(f"\nTotal researchers to process: {len(df_matched)}")

# Check for existing progress
existing_data = []
processed_ids = set()

if Path(OUTPUT_FILE).exists():
    print(f"\n✓ Found existing results file")
    existing_df = pd.read_csv(OUTPUT_FILE)
    existing_data = existing_df.to_dict('records')
    processed_ids = set(existing_df['openalex_id'].values)
    print(f"  Already processed: {len(processed_ids)} researchers")
    print(f"  Remaining: {len(df_matched) - len(processed_ids)} researchers")

# Load progress tracking
start_idx = 0
if Path(PROGRESS_FILE).exists():
    with open(PROGRESS_FILE, 'r') as f:
        progress = json.load(f)
        start_idx = progress.get('last_index', 0)
        print(f"  Resuming from index: {start_idx}")

# Start processing
start_time = time.time()
success_count = len(existing_data)
fail_count = 0

log_entries = []

for idx, (_, row) in enumerate(df_matched.iterrows()):
    if idx < start_idx:
        continue

    # Skip if already processed
    if row['openalex_id'] in processed_ids:
        continue

    # Progress update every 10 researchers
    if idx % 10 == 0 and idx > 0:
        elapsed = time.time() - start_time
        rate = elapsed / (idx - start_idx + 1)
        remaining = (len(df_matched) - idx) * rate
        progress_pct = idx / len(df_matched) * 100

        print(f"\n[{time.strftime('%H:%M:%S')}] Progress: {idx}/{len(df_matched)} ({progress_pct:.1f}%)")
        print(f"  Elapsed: {elapsed/60:.1f} min | ETA: {remaining/60:.1f} min")
        print(f"  Success: {success_count} | Failed: {fail_count}")

        # Save progress
        with open(PROGRESS_FILE, 'w') as f:
            json.dump({
                'last_index': idx,
                'success_count': success_count,
                'fail_count': fail_count,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f)

    # Fetch metrics
    metrics = fetch_author_metrics(row['openalex_id'])

    if metrics:
        entry = {
            'openalex_id': row['openalex_id'],
            'authfull': row['authfull'],
            'field': row['field'],
            'field_type': row['field_type'],
            'scopus_pubs': row['scopus_pubs'],
            'scopus_citations': row['scopus_citations'],
            'scopus_h_index': row['scopus_h_index'],
            'elsevier_pct': row.get('elsevier_pct', 0),
            **metrics
        }
        existing_data.append(entry)
        success_count += 1

        log_entries.append(f"[{idx}] SUCCESS: {row['authfull']}")

        # Save incrementally every 50 successful fetches
        if success_count % 50 == 0:
            df_temp = pd.DataFrame(existing_data)
            df_temp.to_csv(OUTPUT_FILE, index=False)
            print(f"  ✓ Saved {success_count} researchers to {OUTPUT_FILE}")
    else:
        fail_count += 1
        log_entries.append(f"[{idx}] FAILED: {row['authfull']}")

    # Rate limiting
    time.sleep(0.25)

# Final save
elapsed = time.time() - start_time

print(f"\n{'='*80}")
print("COMPLETE")
print("="*80)
print(f"\nTotal time: {elapsed/3600:.2f} hours ({elapsed/60:.1f} minutes)")
print(f"Successfully fetched: {success_count}/{len(df_matched)} ({success_count/len(df_matched)*100:.1f}%)")
print(f"Failed: {fail_count}")

if existing_data:
    final_df = pd.DataFrame(existing_data)
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✓ Final results saved to: {OUTPUT_FILE}")

    # Summary statistics
    print(f"\nSummary statistics:")
    print(final_df[['nc', 'h', 'hm', 'ncs', 'ncsf', 'ncsfl']].describe())
else:
    print("\n✗ No metrics fetched")

# Save log
with open(LOG_FILE, 'w') as f:
    f.write('\n'.join(log_entries))
print(f"\n✓ Log saved to: {LOG_FILE}")

# Clean up progress file
if Path(PROGRESS_FILE).exists():
    Path(PROGRESS_FILE).unlink()
    print(f"✓ Cleaned up progress file")

print(f"\nReady for composite score calculation!")
