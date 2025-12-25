#!/usr/bin/env python3
"""
Refine tags for posts in the Algorithms category by inferring granular tags
from the file path and title, apply the changes to the post frontmatter, and
update taxonomy-proposals.json and reports.

This script runs safe edits and writes changes to files. It should be run
from the repository root with the project's venv active (or using ./.venv/bin/python).
"""
from pathlib import Path
import json
import re
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_JSON = ROOT / 'taxonomy-proposals.json'

if not PROPOSALS_JSON.exists():
    print('taxonomy-proposals.json not found; run save_taxonomy_proposals.py first')
    raise SystemExit(1)

data = json.loads(PROPOSALS_JSON.read_text(encoding='utf-8'))
proposals = data.get('proposals', [])

# heuristics: map keywords to tags
KEYWORD_TAGS = [
    (['tree', 'trees', 'avl', 'b-tree', 'b+', 'b+','b trees','b+'], 'Trees'),
    (['graph', 'graphs', 'dfs', 'bfs', 'shortest path','dijkstra','union-find','unionfind','union'], 'Graphs'),
    (['dynamic','dynamic programming','dp','dp-','dynamic-programming','dynamic_programming'], 'Dynamic Programming'),
    (['heap','heaps','priority queue','priority-queue'], 'Heaps'),
    (['stack','stacks'], 'Stacks'),
    (['queue','queues'], 'Queues'),
    (['array','arrays'], 'Arrays'),
    (['string','strings','substring','regex','parsing'], 'Strings'),
    (['map','maps','hash','hashmap','hashmaps','dictionary'], 'Hashmaps'),
    (['search','binary search','binary-search','binary_search'], 'Searching'),
    (['sort','sorting','quicksort','mergesort','bubblesort'], 'Sorting'),
    (['union find','union-find','disjoint set'], 'Union Find'),
    (['iterator'], 'Iterator'),
    (['math','maths','number theory','combinatorics'], 'Math'),
    (['bitwise','bit','bits'], 'Bitwise'),
    (['dp','dynamic'], 'Dynamic Programming'),
    (['data structures','data-structures','data_structures'], 'Data Structures'),
    (['greedy','greedy algorithm'], 'Greedy'),
    (['backtracking','backtrack'], 'Backtracking'),
    (['bfs','dfs'], 'BFS/DFS'),
]

# helper to infer tags from path/title

def infer_tags_from_text(path: str, title: str):
    text = (path + ' ' + title).lower()
    tags = []
    for kws, tag in KEYWORD_TAGS:
        for kw in kws:
            if kw in text:
                if tag not in tags:
                    tags.append(tag)
    # ensure if no specific tag found, fallback to 'Algorithms'
    if not tags:
        tags = ['Algorithms']
    # keep order and cap at 4
    return tags[:4]

# Now process proposals and update posts
changed = []
for p in proposals:
    proposed_cats = p.get('proposed_categories') or []
    # support both string and list
    if isinstance(proposed_cats, str):
        cats = [proposed_cats]
    else:
        cats = proposed_cats
    if not cats:
        continue
    primary = cats[0]
    if primary != 'Algorithms':
        continue
    path = p.get('path')
    title = p.get('title') or ''
    new_tags = infer_tags_from_text(path, title)
    # Update proposals entry
    p['proposed_tags'] = new_tags
    # Update the actual post frontmatter
    post_file = ROOT / path
    if post_file.exists():
        try:
            import frontmatter
            post = frontmatter.load(post_file)
            # write tags as list (script expects list)
            post.metadata['tags'] = new_tags
            # Keep categories as-is
            # Use dumps to get a string and write using text mode
            content = frontmatter.dumps(post)
            with post_file.open('w', encoding='utf-8') as fh:
                fh.write(content)
            changed.append({'path': path, 'title': title, 'new_tags': new_tags})
        except Exception as e:
            print('Failed to update', path, e)
    else:
        print('Post file missing:', path)

# write back updated proposals json
data['proposals'] = proposals
PROPOSALS_JSON.write_text(json.dumps(data, indent=2), encoding='utf-8')

# regenerate grouped md and report using existing scripts
import subprocess
subprocess.run(['./.venv/bin/python', 'scripts/group_taxonomy_and_save.py'])
subprocess.run(['./.venv/bin/python', 'scripts/generate_taxonomy_report.py'])

print(f'Updated {len(changed)} posts with refined Algorithm tags')
for c in changed[:50]:
    print('-', c['path'], '->', c['new_tags'])
