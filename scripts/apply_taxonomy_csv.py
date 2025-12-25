#!/usr/bin/env python3
"""
Apply taxonomy edits from taxonomy-proposals.csv.
CSV columns expected:
  path,title,current_categories,current_tags,proposed_categories,proposed_tags

Behavior:
 - Reads the CSV and for each row updates the post front matter categories/tags to the CSV's proposed values.
 - Creates a backup of each modified post at <post>.bak before writing.
 - Prints a summary at the end.

Run:
  python scripts/apply_taxonomy_csv.py
"""
from pathlib import Path
import csv
import frontmatter

ROOT = Path(__file__).resolve().parents[1]
CSV_IN = ROOT / 'taxonomy-proposals.csv'
if not CSV_IN.exists():
    print('Error: taxonomy-proposals.csv not found. Run export script first.')
    raise SystemExit(1)

changed = []
with CSV_IN.open('r', encoding='utf-8', newline='') as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        path = ROOT / row['path']
        if not path.exists():
            print('Missing file, skipping:', path)
            continue
        # parse proposed categories/tags split by ';'
        prop_cats = [c for c in (row.get('proposed_categories') or '').split(';') if c]
        prop_tags = [t for t in (row.get('proposed_tags') or '').split(';') if t]
        # load post
        post = frontmatter.load(path)
        meta = post.metadata
        # backup
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_bytes(path.read_bytes())
        # apply
        if prop_cats:
            meta['categories'] = prop_cats if len(prop_cats)>1 else prop_cats[0]
        else:
            meta.pop('categories', None)
        if prop_tags:
            meta['tags'] = prop_tags
        else:
            meta.pop('tags', None)
        # write
        path.write_text(frontmatter.dumps(post), encoding='utf-8')
        changed.append(str(path))

print('Applied changes to', len(changed), 'files')
for p in changed[:200]:
    print('-', p)

