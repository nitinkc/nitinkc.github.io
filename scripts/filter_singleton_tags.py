#!/usr/bin/env python3
"""
Remove singleton tags (used only once) from taxonomy-proposals.csv.
Keeps only tags that appear 2+ times across all posts to reduce noise.
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_IN = ROOT / 'taxonomy-proposals.csv'
CSV_OUT = ROOT / 'taxonomy-proposals-filtered.csv'

# First pass: count tag usage
tag_counts = Counter()
rows = []

with CSV_IN.open('r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)
        tags = [t.strip() for t in (row.get('proposed_tags') or '').split(';') if t.strip()]
        for tag in tags:
            tag_counts[tag] += 1

# Find low-frequency tags (used 3 or fewer times)
singletons = {tag for tag, count in tag_counts.items() if count <= 3}
print(f'Found {len(singletons)} low-frequency tags (used 3 or fewer times)')
print(f'Total unique tags: {len(tag_counts)}')
print(f'Tags to keep (4+ uses): {len(tag_counts) - len(singletons)}')

# Second pass: filter out singletons
posts_modified = 0
tags_removed = 0

with CSV_OUT.open('w', encoding='utf-8', newline='') as f:
    fieldnames = ['path', 'title', 'current_categories', 'current_tags', 'proposed_categories', 'proposed_tags']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for row in rows:
        original_tags = [t.strip() for t in (row.get('proposed_tags') or '').split(';') if t.strip()]
        filtered_tags = [t for t in original_tags if t not in singletons]

        if len(filtered_tags) != len(original_tags):
            posts_modified += 1
            tags_removed += len(original_tags) - len(filtered_tags)

        # If no tags remain after filtering, use the category as tag
        if not filtered_tags:
            proposed_cats = [c.strip() for c in (row.get('proposed_categories') or '').split(';') if c.strip()]
            if proposed_cats:
                filtered_tags = [proposed_cats[0]]

        row['proposed_tags'] = ';'.join(filtered_tags) if filtered_tags else ''
        writer.writerow(row)

print(f'\nPosts modified: {posts_modified}')
print(f'Tags removed: {tags_removed}')
print(f'Output written to: {CSV_OUT}')

# Show some examples of removed tags
print('\nExample low-frequency tags removed (first 30):')
for i, tag in enumerate(sorted(list(singletons))[:30], 1):
    print(f'  {i}. {tag}')
if len(singletons) > 30:
    print(f'  ... and {len(singletons) - 30} more')

