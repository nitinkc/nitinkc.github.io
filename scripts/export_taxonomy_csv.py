#!/usr/bin/env python3
"""
Export taxonomy proposals (taxonomy-proposals.json) to a CSV file for human review.
Generates taxonomy-proposals.csv with columns:
  path,title,current_categories,current_tags,proposed_categories,proposed_tags

Run:
  python scripts/export_taxonomy_csv.py
"""
from pathlib import Path
import json
import csv

ROOT = Path(__file__).resolve().parents[1]
JSON_IN = ROOT / 'taxonomy-proposals.json'
CSV_OUT = ROOT / 'taxonomy-proposals.csv'

if not JSON_IN.exists():
    print('Error: taxonomy-proposals.json not found. Run save_taxonomy_proposals.py first.')
    raise SystemExit(1)

data = json.loads(JSON_IN.read_text(encoding='utf-8'))
proposals = data.get('proposals', [])

with CSV_OUT.open('w', encoding='utf-8', newline='') as fh:
    writer = csv.writer(fh)
    writer.writerow(['path','title','current_categories','current_tags','proposed_categories','proposed_tags'])
    for p in proposals:
        path = p.get('path','')
        title = p.get('title','')
        cur_cats = p.get('current_categories') or p.get('current_category') or []
        if isinstance(cur_cats, list):
            cur_cats_s = ';'.join(cur_cats)
        else:
            cur_cats_s = str(cur_cats)
        cur_tags = p.get('current_tags') or []
        cur_tags_s = ';'.join(cur_tags) if isinstance(cur_tags, list) else str(cur_tags)
        prop_cats = p.get('proposed_categories') or []
        prop_cats_s = ';'.join(prop_cats) if isinstance(prop_cats, list) else str(prop_cats)
        prop_tags = p.get('proposed_tags') or []
        prop_tags_s = ';'.join(prop_tags) if isinstance(prop_tags, list) else str(prop_tags)
        writer.writerow([path, title, cur_cats_s, cur_tags_s, prop_cats_s, prop_tags_s])

print('Wrote', CSV_OUT)

