#!/usr/bin/env python3
"""
Group taxonomy proposals by proposed category and write a human-readable Markdown and
add a grouped field into taxonomy-proposals.json.
"""
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_JSON = ROOT / 'taxonomy-proposals.json'
OUT_MD = ROOT / 'taxonomy-by-category.md'

if not PROPOSALS_JSON.exists():
    print('taxonomy-proposals.json not found. Run save_taxonomy_proposals.py first.')
    raise SystemExit(1)

data = json.loads(PROPOSALS_JSON.read_text(encoding='utf-8'))
proposals = data.get('proposals', [])

# Group by proposed category (first one if list)
from collections import defaultdict
grouped = defaultdict(list)
for p in proposals:
    # proposed_categories may be list or empty
    pc = p.get('proposed_categories') or []
    if isinstance(pc, list) and len(pc) > 0:
        key = pc[0]
    elif isinstance(pc, str) and pc:
        key = pc
    else:
        key = 'Uncategorized'
    grouped[key].append(p)

# Write markdown
lines = []
lines.append('# Taxonomy: Posts grouped by proposed category')
lines.append(f'Generated: {datetime.utcnow().isoformat()} UTC')
lines.append('')
for cat in sorted(grouped.keys()):
    lines.append(f'## {cat} ({len(grouped[cat])})')
    lines.append('')
    for p in sorted(grouped[cat], key=lambda x: x.get('title') or ''):
        title = p.get('title') or ''
        path = p.get('path')
        tags = p.get('proposed_tags') or []
        tag_str = ', '.join(tags) if tags else ''
        lines.append(f'- **{title}** — `{path}` — Tags: {tag_str}')
    lines.append('')

OUT_MD.write_text('\n'.join(lines), encoding='utf-8')

# Update the JSON with grouped mapping
data['grouped_by_category'] = {k: v for k, v in grouped.items()}
PROPOSALS_JSON.write_text(json.dumps(data, indent=2), encoding='utf-8')

print('Wrote', OUT_MD)
print('Updated', PROPOSALS_JSON)

