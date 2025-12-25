#!/usr/bin/env python3
"""
Generate taxonomy-proposals.json containing per-post title, current and proposed category/tags.
Appends a short summary to taxonomy-apply.log.
"""
from pathlib import Path
import json
import importlib.util
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
AUDIT_LOG = ROOT / 'taxonomy-apply.log'
OUT_JSON = ROOT / 'taxonomy-proposals.json'

# import taxonomy_audit
spec = importlib.util.spec_from_file_location('taxonomy_audit', str(ROOT / 'scripts' / 'taxonomy_audit.py'))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

files, per_file, cat_counts, tag_counts = mod.audit()
updates = mod.propose_updates(per_file, cat_counts, tag_counts)

proposals = []
for f, old_c, old_t, new_c, new_t in updates:
    try:
        post = mod.load_post(f)
        title = post.get('title') or ''
    except Exception:
        title = ''
    proposals.append({
        'path': str(f.relative_to(ROOT)),
        'title': title,
        'current_categories': old_c,
        'current_tags': old_t,
        'proposed_categories': new_c,
        'proposed_tags': new_t
    })

# write JSON
OUT_JSON.write_text(json.dumps({'generated_at': datetime.utcnow().isoformat(), 'proposals': proposals}, indent=2), encoding='utf-8')

# append summary
with AUDIT_LOG.open('a', encoding='utf-8') as fh:
    fh.write('\n\n# Taxonomy proposals JSON written\n')
    fh.write(f'Written: {datetime.utcnow().isoformat()} UTC\n')
    fh.write(f'Proposals count: {len(proposals)}\n')

print('Wrote', OUT_JSON)

