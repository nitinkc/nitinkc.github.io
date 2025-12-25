import os
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict
import frontmatter
from ruamel.yaml import YAML
from tabulate import tabulate
import click
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"

yaml = YAML()
yaml.preserve_quotes = True

def find_posts():
    md_files = []
    for p in POSTS_DIR.rglob("*.md"):
        md_files.append(p)
    return md_files

CANON_CATEGORIES = [
    "System Design","Microservices","Java","Python","SQL","Electronics",
    "Machine Learning","Developer tools","Architecture","DevOps","GCP","Git",
    "Health","Finance","Management","Miscellaneous","Photography","Testing","Security","Networks"
]

CATEGORY_BY_FOLDER = {
    "systems_design": "System Design",
    "microservices": "Microservices",
    "Java": "Java",
    "python": "Python",
    "sql": "SQL",
    "science": "Electronics",
    "machineLearning": "Machine Learning",
    "developertools": "Developer tools",
    "architecture": "Architecture",
    "devops": "DevOps",
    "gcp": "GCP",
    "git": "Git",
    "health": "Health",
    "finances": "Finance",
    "management": "Management",
    "misc": "Miscellaneous",
    "Algo": "Algorithms",
    "design-patterns": "Design Patterns",
    "databases": "Database",
}

TAG_NORMALIZATION = {
    # normalize spacing/case
    "system design": "System Design",
    "networks": "Networks",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    "spring microservices": "Microservices",
    "java": "Java",
    "sql": "SQL",
    "electronics": "Electronics",
    "misc": "Miscellaneous",
    "developer tools": "Developer tools",
    "macbook": "MacBook",
    "performance engineering": "Performance Engineering",
    "multithreading": "Multithreading",
    # Additional mappings proposed by user
    "finances": "Finance",
    "finance": "Finance",
    "google cloud platform": "GCP",
    "google cloud": "GCP",
    "gcp": "GCP",
    "gitops": "GitOps",
    "git ops": "GitOps",
    "crud": "CRUD",
    # Treat miscellaneous as drop when it appears as a tag (map to empty string)
    "miscellaneous": "",
}

MERGE_SINGLETONS_INTO = {
    # If a tag appears < MIN_COUNT and exists as category context, map to category
    # We'll decide dynamically when applying
}

MIN_TAG_COUNT = 2
# Max number of tags to keep per post
TAG_CAP = 4

@dataclass
class PostUpdate:
    path: Path
    old_categories: list
    old_tags: list
    new_categories: list
    new_tags: list


def load_post(path: Path):
    try:
        return frontmatter.load(path)
    except Exception:
        text = path.read_text(encoding="utf-8")
        return frontmatter.loads(text)


def normalize_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        # split on commas if looks like CSV, else single
        if "," in value:
            items = [v.strip() for v in value.split(",")]
        else:
            items = [value.strip()]
    elif isinstance(value, list):
        items = [str(v).strip() for v in value]
    else:
        items = [str(value).strip()]
    # remove quotes wrappers like ['SQL'] read as strings sometimes
    items = [re.sub(r"^[\['\"]|[\]'\"]$", "", it).strip() for it in items]
    # title case known normalizations
    normed = []
    for it in items:
        low = it.lower()
        it2 = TAG_NORMALIZATION.get(low, it.strip())
        normed.append(it2)
    # dedupe preserving order
    seen = set()
    result = []
    for it in normed:
        if it and it not in seen:
            seen.add(it)
            result.append(it)
    return result


def infer_category_from_path(path: Path):
    rel = path.relative_to(POSTS_DIR)
    if len(rel.parts) > 1:
        folder = rel.parts[0]
        return CATEGORY_BY_FOLDER.get(folder)
    return None


def audit():
    files = find_posts()
    tag_counts = Counter()
    cat_counts = Counter()
    per_file = []
    for f in files:
        post = load_post(f)
        cats = normalize_list(post.get("categories"))
        tags = normalize_list(post.get("tags"))
        for c in cats:
            cat_counts[c] += 1
        for t in tags:
            tag_counts[t] += 1
        per_file.append((f, cats, tags))

    return files, per_file, cat_counts, tag_counts


def propose_updates(per_file, cat_counts, tag_counts):
    updates = []
    for f, cats, tags in per_file:
        inferred = infer_category_from_path(f)
        new_cats = cats.copy()
        if inferred and inferred not in new_cats:
            # Prefer inferred single category; if existing categories are similar, replace
            new_cats = [inferred]
        elif not new_cats and inferred:
            new_cats = [inferred]
        # otherwise keep existing but normalize to canonical if possible
        new_cats = [TAG_NORMALIZATION.get(c.lower(), c) for c in new_cats]
        # If multiple categories, limit to 1-2 max: main + optional sub if clearly present
        if len(new_cats) > 2:
            new_cats = new_cats[:2]
        # Tags policy:
        # - Normalize and dedupe
        # - Prefer common tags (>= MIN_TAG_COUNT), but never drop to zero
        # - Remove category-as-tag only if other tags remain
        # - Cap total tags to TAG_CAP
        primary = new_cats[0] if new_cats else None
        candidates = normalize_list(tags)

        # If primary appears as a tag and there are other tags, we can drop it later
        # First filter by global frequency, but ensure we don't end up empty
        common = [t for t in candidates if tag_counts.get(t, 0) >= MIN_TAG_COUNT]
        if not common:
            # If nothing meets the threshold, keep the original normalized ones (limited later)
            filtered = candidates.copy()
        else:
            filtered = common

        # Remove category tag only if other tags remain after filtering
        if primary and len(filtered) > 1 and primary in filtered:
            filtered = [t for t in filtered if t != primary]
            if not filtered:
                filtered = [primary]

        # Cap tags
        if len(filtered) > TAG_CAP:
            filtered = filtered[:TAG_CAP]

        # Ensure at least one tag remains; fallback to primary category if needed
        if not filtered and primary:
            filtered = [primary]

        new_tags = filtered

        updates.append((f, cats, tags, new_cats, new_tags))
    return updates


def write_back(updates, dry_run=True):
    changed = []
    for f, old_c, old_t, new_c, new_t in updates:
        if old_c == new_c and old_t == new_t:
            continue
        if dry_run:
            changed.append((f, old_c, old_t, new_c, new_t))
            continue
        post = load_post(f)
        meta = post.metadata
        if new_c:
            meta["categories"] = new_c if len(new_c) > 1 else new_c[0]
        else:
            if "categories" in meta:
                del meta["categories"]
        if new_t:
            meta["tags"] = new_t
        else:
            if "tags" in meta:
                del meta["tags"]
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(frontmatter.dumps(post))
        changed.append((f, old_c, old_t, new_c, new_t))
    return changed


@click.group()
def cli():
    pass


@cli.command()
@click.option("--apply", "apply_changes", is_flag=True, help="Write changes to files")
def audit_tags(apply_changes):
    files, per_file, cat_counts, tag_counts = audit()
    updates = propose_updates(per_file, cat_counts, tag_counts)

    # Summary tables
    cats_table = sorted(cat_counts.items(), key=lambda x: (-x[1], x[0]))
    tags_table = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))

    print("\nCategories (count):\n")
    print(tabulate(cats_table, headers=["Category", "Count"]))
    print("\nTop 40 tags (count):\n")
    print(tabulate(tags_table[:40], headers=["Tag", "Count"]))

    changed = write_back(updates, dry_run=not apply_changes)
    print(f"\nFiles needing changes: {len(changed)} (apply={'yes' if apply_changes else 'no'})")
    for (f, oc, ot, nc, nt) in changed[:30]:
        print(f"- {f.relative_to(ROOT)}: categories {oc} -> {nc}; tags {ot} -> {nt}")
    if len(changed) > 30:
        print(f"... {len(changed)-30} more")


if __name__ == "__main__":
    cli()
