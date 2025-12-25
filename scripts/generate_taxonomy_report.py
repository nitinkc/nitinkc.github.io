#!/usr/bin/env python3
"""
Generate a human-readable taxonomy report using the same logic as scripts/taxonomy_audit.py
Outputs:
 - taxonomy-report.md (detailed per-post table)
 - Appends a short summary to taxonomy-apply.log

Usage:
  python scripts/generate_taxonomy_report.py
"""
from pathlib import Path
import importlib.util
import sys
import frontmatter

ROOT = Path(__file__).resolve().parents[1]
AUDIT_LOG = ROOT / 'taxonomy-apply.log'
REPORT_MD = ROOT / 'taxonomy-report.md'

# Import taxonomy_audit.py as module
spec = importlib.util.spec_from_file_location('taxonomy_audit', str(ROOT / 'scripts' / 'taxonomy_audit.py'))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Run audit and propose updates
files, per_file, cat_counts, tag_counts = mod.audit()
updates = mod.propose_updates(per_file, cat_counts, tag_counts)

# Build report content
lines = []
lines.append('# Taxonomy Report')
lines.append('')
from datetime import datetime
lines.append(f'Generated: {datetime.utcnow().isoformat()} UTC')
lines.append('')
lines.append('## Summary')
lines.append('')
lines.append('Category counts (top 20):')
lines.append('')
for c, cnt in sorted(cat_counts.items(), key=lambda x: (-x[1], x[0]))[:20]:
    lines.append(f'- **{c}**: {cnt}')
lines.append('')
lines.append('Top tags (top 40):')
lines.append('')
for t, cnt in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))[:40]:
    lines.append(f'- **{t}**: {cnt}')

lines.append('')
lines.append('## Proposed per-post taxonomy')
lines.append('')
lines.append('| Post path | Title | Current categories | Current tags | Proposed categories | Proposed tags |')
lines.append('|---|---|---|---|---|---|')

changed_rows = []
for f, old_c, old_t, new_c, new_t in updates:
    # load title
    try:
        post = mod.load_post(f)
        title = post.get('title') or ''
    except Exception:
        title = ''
    # Format values as inline lists
    def fmt(x):
        if not x:
            return ''
        if isinstance(x, list):
            return ', '.join(x)
        return str(x)
    row = f'| {f.relative_to(ROOT)} | {title} | {fmt(old_c)} | {fmt(old_t)} | {fmt(new_c)} | {fmt(new_t)} |'
    lines.append(row)
    # track changed
    if old_c != new_c or old_t != new_t:
        changed_rows.append((f, old_c, old_t, new_c, new_t))

# If no changes proposed, note that
if not updates:
    lines.append('*No posts found.*')

# Write report
REPORT_MD.write_text('\n'.join(lines), encoding='utf-8')

# Also append summary to taxonomy-apply.log
with AUDIT_LOG.open('a', encoding='utf-8') as fh:
    fh.write('\n\n# Taxonomy report summary appended\n')
    fh.write(f'Generated: {datetime.utcnow().isoformat()} UTC\n')
    fh.write(f'Proposed changes (count): {len([1 for f,oc,ot,nc,nt in updates if oc!=nc or ot!=nt])}\n')
    for f, oc, ot, nc, nt in updates:
        if oc!=nc or ot!=nt:
            fh.write(f'- {f.relative_to(ROOT)}: categories {oc} -> {nc}; tags {ot} -> {nt}\n')

print('Report written to', REPORT_MD)
print('Summary appended to', AUDIT_LOG)

