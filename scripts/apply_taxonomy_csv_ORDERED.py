#!/usr/bin/env python3
"""
SAFE taxonomy CSV application with custom YAML ordering.
Enforces field order: title, date, categories, tags, then other fields.
"""
from pathlib import Path
import csv
import frontmatter
from collections import OrderedDict
import yaml

ROOT = Path(__file__).resolve().parents[1]
CSV_IN = ROOT / 'taxonomy-proposals.csv'

if not CSV_IN.exists():
    print('Error: taxonomy-proposals.csv not found')
    raise SystemExit(1)

def ordered_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    """Custom YAML dumper that preserves OrderedDict order"""
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

changed = []
with CSV_IN.open('r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
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

        # Get existing metadata
        old_meta = post.metadata.copy()

        # Create new ordered metadata: title, date, categories, tags, then others
        new_meta = OrderedDict()

        # 1. Title (if exists)
        if 'title' in old_meta:
            new_meta['title'] = old_meta['title']

        # 2. Date (if exists)
        if 'date' in old_meta:
            new_meta['date'] = old_meta['date']

        # 3. Categories (always as array)
        if prop_cats:
            new_meta['categories'] = prop_cats

        # 4. Tags
        if prop_tags:
            new_meta['tags'] = prop_tags

        # 5. Add any other fields that weren't already processed
        for key, value in old_meta.items():
            if key not in ['title', 'date', 'categories', 'tags']:
                new_meta[key] = value

        # Write back manually with custom YAML
        with path.open('w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(ordered_dump(new_meta, default_flow_style=False, allow_unicode=True))
            f.write('---\n\n')
            f.write(original_content)

        changed.append(str(path))

print('Updated', len(changed), 'files (front matter only, content preserved)')
for p in changed[:20]:
    print('-', p)
if len(changed) > 20:
    print(f'... and {len(changed) - 20} more')

