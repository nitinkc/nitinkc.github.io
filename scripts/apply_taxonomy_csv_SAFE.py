#!/usr/bin/env python3
"""
SAFE taxonomy CSV application - updates ONLY front matter, preserves all post content.
"""
from pathlib import Path
import csv
import frontmatter

ROOT = Path(__file__).resolve().parents[1]
CSV_IN = ROOT / 'taxonomy-proposals.csv'

if not CSV_IN.exists():
    print('Error: taxonomy-proposals.csv not found')
    raise SystemExit(1)

changed = []
with CSV_IN.open('r', encoding='utf-8', newline='') as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        path = ROOT / row['path']
        if not path.exists():
            print('Missing file, skipping:', path)
            continue

        # Parse proposed categories/tags
        prop_cats = [c.strip() for c in (row.get('proposed_categories') or '').split(';') if c.strip()]
        prop_tags = [t.strip() for t in (row.get('proposed_tags') or '').split(';') if t.strip()]

        # Load post WITH CONTENT
        post = frontmatter.load(path)

        # Store original content
        original_content = post.content

        # Update ONLY metadata
        meta = post.metadata
        if prop_cats:
            meta['categories'] = prop_cats if len(prop_cats) > 1 else prop_cats[0]
        else:
            meta.pop('categories', None)

        if prop_tags:
            meta['tags'] = prop_tags
        else:
            meta.pop('tags', None)

        # Restore content (frontmatter.dumps preserves it)
        post.content = original_content

        # Write back
        with path.open('w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        changed.append(str(path))

print('Updated', len(changed), 'files (front matter only, content preserved)')
for p in changed[:20]:
    print('-', p)
if len(changed) > 20:
    print(f'... and {len(changed) - 20} more')

