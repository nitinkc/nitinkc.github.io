#!/usr/bin/env python3
"""
Refine tags for posts across categories by inferring more granular tags from file path and title.
- Reads existing proposals from taxonomy-proposals.json
- For each post, uses category-specific keyword mappings to infer granular tags
- Updates post front-matter tags (writes changes)
- Updates taxonomy-proposals.json, regenerates reports

Runs in the project root; requires venv with dependencies installed (.venv)
"""
from pathlib import Path
import json
import re
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_JSON = ROOT / 'taxonomy-proposals.json'
if not PROPOSALS_JSON.exists():
    print('taxonomy-proposals.json not found; run save_taxonomy_proposals.py first')
    raise SystemExit(1)

data = json.loads(PROPOSALS_JSON.read_text(encoding='utf-8'))
proposals = data.get('proposals', [])

# Category-specific keyword→tag rules. Keys are lowercase category names.
CATEGORY_RULES = {
    'algorithms': [
        (['tree','trees','avl','b-tree','b+','btree'],'Trees'),
        (['graph','dfs','bfs','dijkstra','shortest path','union-find'],'Graphs'),
        (['dynamic programming','dynamic','dp'],'Dynamic Programming'),
        (['heap','priority queue'],'Heaps'),
        (['stack'],'Stacks'),
        (['queue'],'Queues'),
        (['array','arrays'],'Arrays'),
        (['string','substring','regex'],'Strings'),
        (['hash','hashmap','map','dictionary'],'Hashmaps'),
        (['search','binary search'],'Searching'),
        (['sort','sorting','quicksort','mergesort'],'Sorting'),
        (['bitwise','bitwise operators','bit'],'Bitwise'),
        (['greedy'],'Greedy'),
        (['backtrack','backtracking'],'Backtracking'),
    ],
    'java': [
        (['generics','generic'],'Generics'),
        (['stream','streams'],'Streams'),
        (['jvm','jvm','garbage collection','gc'],'Garbage Collection'),
        (['concurrency','multithreading','thread','threads','concurrent'],'Multithreading'),
        (['lambda','functional'],'Functional'),
        (['serialization'],'Serialization'),
        (['jmh','benchmark','benchmarking'],'Benchmarking'),
    ],
    'microservices': [
        (['spring','spring boot','springboot'],'Spring Boot'),
        (['docker','container','containers'],'Docker'),
        (['kafka'],'Kafka'),
        (['redis','cache'],'Redis'),
        (['security','ssl','tls','keystore'],'Security'),
        (['rest','rest template','restful'],'REST'),
        (['websocket','sse','server-sent'],'Real-time'),
        (['gradle','maven'],'Build Tools'),
    ],
    'system design': [
        (['cache','caching'],'Caching'),
        (['cap theorem','cap'],'CAP Theorem'),
        (['messag','message queue','kafka','rabbitmq'],'Messaging'),
        (['scalab','scaling','scale'],'Scalability'),
        (['consistency','consistency levels'],'Consistency'),
        (['api gateway'],'API Gateway'),
        (['rate limit','rate-limiting'],'Rate Limiting'),
    ],
    'devops': [
        (['kubernetes','k8s','gke'],'Kubernetes'),
        (['terraform'],'Terraform'),
        (['jenkins'],'Jenkins'),
        (['flux','argo','gitops'],'GitOps'),
        (['prometheus','grafana','monitor'],'Monitoring'),
        (['docker'],'Docker'),
    ],
    'gcp': [
        (['bigquery'],'BigQuery'),
        (['spanner'],'Spanner'),
        (['gcp','google cloud'],'GCP'),
        (['stackdriver','logging','logging'],'Logging'),
        (['pubsub'],'Pub/Sub'),
    ],
    'database': [
        (['mysql','mariadb'],'MySQL'),
        (['spanner'],'Spanner'),
        (['migration','harbourbridge'],'Migration'),
        (['sql','queries','joins'],'SQL'),
        (['nosql'],'NoSQL'),
    ],
    'developer tools': [
        (['intellij','idea'],'IntelliJ'),
        (['vscode','code'],'VSCode'),
        (['macbook'],'MacBook'),
        (['terminal','shell'],'Terminal'),
        (['docker','dbeaver','mysql workbench'],'Tools'),
    ],
    'electronics': [
        (['arduino'],'Arduino'),
        (['raspberry','raspberry pi'],'Raspberry Pi'),
        (['led','rgb'],'LED'),
        (['sensor','ultrasonic','ldr'],'Sensors'),
    ],
    'health': [
        (['diet','nutrition','nutrition'],'Nutrition'),
        (['yoga','pranayam','pranayama'],'Yoga'),
        (['workout','training'],'Fitness'),
    ],
    'design patterns': [
        (['factory','builder','singleton','decorator','strategy','iterator'],'Pattern'),
    ],
    # fallback rules for other categories
}

# Generic fallback keyword list across categories
GENERIC_KEYWORDS = [
    (['tutorial','guide','complete guide','how to'],'Guide'),
    (['best practices','best-practices'],'Best Practices'),
    (['example','examples'],'Examples'),
]

# normalize helper
def normalize_tag(tag):
    return tag.strip()

# infer tags for a post given primary category, path and title
def infer_tags_for_post(category, path, title, existing_tags):
    text = (path + ' ' + title + ' ' + ' '.join(existing_tags or [])).lower()
    tags = []
    rules = CATEGORY_RULES.get(category.lower(), [])
    for kws, tag in rules:
        for kw in kws:
            if kw in text and tag not in tags:
                tags.append(normalize_tag(tag))
    # generic rules
    for kws, tag in GENERIC_KEYWORDS:
        for kw in kws:
            if kw in text and tag not in tags:
                tags.append(normalize_tag(tag))
    # always include category name as last tag for context
    if category and category not in tags:
        tags.append(category)
    # if nothing found, fallback to existing tags or category
    if not tags:
        if existing_tags:
            tags = existing_tags
        else:
            tags = [category]
    # dedupe preserving order and cap to 6
    seen = set()
    out = []
    for t in tags:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
        if len(out) >= 6:
            break
    return out

# apply to all proposals
changed = []
for p in proposals:
    path = p.get('path')
    title = p.get('title') or ''
    cur_cats = p.get('current_categories') or p.get('current_category') or []
    if isinstance(cur_cats, str):
        cur_cats = [cur_cats]
    primary = cur_cats[0] if cur_cats else (p.get('proposed_categories')[0] if p.get('proposed_categories') else None)
    if not primary:
        continue
    existing_tags = p.get('current_tags') or []
    new_tags = infer_tags_for_post(primary, path, title, existing_tags)
    # update proposal
    p['proposed_categories'] = p.get('proposed_categories') or cur_cats
    p['proposed_tags'] = new_tags
    # write back to post
    post_file = ROOT / path
    if post_file.exists():
        try:
            import frontmatter
            post = frontmatter.load(post_file)
            post.metadata['tags'] = new_tags
            content = frontmatter.dumps(post)
            with post_file.open('w', encoding='utf-8') as fh:
                fh.write(content)
            changed.append(path)
        except Exception as e:
            print('Failed to write', path, e)
    else:
        print('Missing file', path)

# write back proposals
data['proposals'] = proposals
PROPOSALS_JSON.write_text(json.dumps(data, indent=2), encoding='utf-8')

# regenerate reports
import subprocess
subprocess.run(['./.venv/bin/python', 'scripts/group_taxonomy_and_save.py'])
subprocess.run(['./.venv/bin/python', 'scripts/generate_taxonomy_report.py'])

print('Updated posts:', len(changed))
for p in changed[:200]:
    print('-', p)

# stage and commit changes on the taxonomy/apply-proposals branch
import subprocess
subprocess.run(['git', 'add', '-A'])
commit_msg = f"taxonomy: refine tags across categories ({len(changed)} posts)"
subprocess.run(['git', 'commit', '-m', commit_msg])
print('Committed changes')

