#!/usr/bin/env python3
"""
Link Audit Script for Jekyll Blog
Finds internal links that should be converted to {% post_url %} format
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# Base directory
BASE_DIR = Path(__file__).parent.parent
POSTS_DIR = BASE_DIR / "_posts"

def get_all_posts():
    """Get all posts with their metadata"""
    posts = {}
    for md_file in POSTS_DIR.rglob("*.md"):
        relative_path = md_file.relative_to(POSTS_DIR)
        # Extract date and slug from filename
        filename = md_file.stem
        match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)', filename)
        if match:
            date, slug = match.groups()
            # Get the subfolder path for post_url reference
            parent = relative_path.parent
            if parent == Path('.'):
                post_url_path = f"/{filename}"
            else:
                post_url_path = f"/{parent}/{filename}"

            posts[slug.lower()] = {
                'file': str(md_file),
                'relative_path': str(relative_path),
                'date': date,
                'slug': slug,
                'post_url_path': post_url_path,
                'filename': filename
            }
    return posts


def find_internal_links(file_path):
    """Find all internal links in a file that should be converted"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    links = []

    # Pattern 1: Full URLs like https://nitinkc.github.io/category/slug/
    # Matches: [text](https://nitinkc.github.io/path/to/article/)
    full_url_pattern = r'\[([^\]]+)\]\((https://nitinkc\.github\.io/[^)#\s]+)([#][^)]+)?\)'
    for match in re.finditer(full_url_pattern, content):
        link_text = match.group(1)
        url = match.group(2)
        anchor = match.group(3) or ""
        full_match = match.group(0)
        line_num = content[:match.start()].count('\n') + 1

        # Skip asset links (images, pdfs, etc.)
        if '/assets/' in url:
            continue

        links.append({
            'type': 'full_url',
            'text': link_text,
            'url': url,
            'anchor': anchor,
            'full_match': full_match,
            'line': line_num
        })

    # Pattern 2: Site baseurl style (already good but could be simplified)
    # [Link]({{ site.baseurl }}{% post_url ... %})
    baseurl_pattern = r'\[([^\]]+)\]\(\{\{\s*site\.baseurl\s*\}\}\{\%\s*post_url\s+([^\%]+)\s*\%\}\)'
    for match in re.finditer(baseurl_pattern, content):
        link_text = match.group(1)
        post_ref = match.group(2).strip()
        full_match = match.group(0)
        line_num = content[:match.start()].count('\n') + 1

        links.append({
            'type': 'baseurl_post_url',
            'text': link_text,
            'post_ref': post_ref,
            'full_match': full_match,
            'line': line_num
        })

    return links

def url_to_slug(url):
    """Convert a URL to a slug for matching"""
    # Remove trailing slash and extract the last part
    url = url.rstrip('/')
    # Handle URL encoded spaces
    url = url.replace('%20', '-')
    # Get the last segment
    parts = url.split('/')
    if parts:
        return parts[-1].lower()
    return None

def match_url_to_post(url, posts):
    """Try to match a URL to a post"""
    slug = url_to_slug(url)
    if not slug:
        return None

    # Direct match
    if slug in posts:
        return posts[slug]

    # Try matching with hyphens replaced
    slug_normalized = slug.replace('-', '').replace('_', '')
    for post_slug, post_data in posts.items():
        if post_slug.replace('-', '').replace('_', '') == slug_normalized:
            return post_data

    # Try partial match
    for post_slug, post_data in posts.items():
        if slug in post_slug or post_slug in slug:
            return post_data

    return None

def generate_report():
    """Generate a comprehensive link audit report"""
    posts = get_all_posts()

    report = []
    report.append("# Internal Link Audit Report")
    report.append("=" * 60)
    report.append("")
    report.append("This report identifies internal links that should be converted")
    report.append("to the robust `{% post_url %}` format for better maintainability.")
    report.append("")
    report.append("## Target Format")
    report.append("```")
    report.append("[Link Title]({% post_url /category/YYYY-MM-DD-slug %})")
    report.append("```")
    report.append("")

    all_changes = []
    files_with_issues = defaultdict(list)

    for md_file in POSTS_DIR.rglob("*.md"):
        links = find_internal_links(md_file)

        for link in links:
            if link['type'] == 'full_url':
                matched_post = match_url_to_post(link['url'], posts)

                change = {
                    'file': str(md_file),
                    'relative_file': str(md_file.relative_to(BASE_DIR)),
                    'line': link['line'],
                    'original': link['full_match'],
                    'link_text': link['text'],
                    'url': link['url'],
                    'anchor': link['anchor'],
                    'matched_post': matched_post
                }

                if matched_post:
                    if link['anchor']:
                        change['suggested'] = f"[{link['text']}]({{% post_url {matched_post['post_url_path']} %}}{link['anchor']})"
                    else:
                        change['suggested'] = f"[{link['text']}]({{% post_url {matched_post['post_url_path']} %}})"
                else:
                    change['suggested'] = f"⚠️ No matching post found for: {link['url']}"

                all_changes.append(change)
                files_with_issues[str(md_file)].append(change)

            elif link['type'] == 'baseurl_post_url':
                # These are already using post_url but with site.baseurl
                # Suggest removing site.baseurl
                change = {
                    'file': str(md_file),
                    'relative_file': str(md_file.relative_to(BASE_DIR)),
                    'line': link['line'],
                    'original': link['full_match'],
                    'link_text': link['text'],
                    'post_ref': link['post_ref'],
                    'suggested': f"[{link['text']}]({{% post_url {link['post_ref']} %}})"
                }
                all_changes.append(change)
                files_with_issues[str(md_file)].append(change)

    # Summary
    report.append("## Summary")
    report.append(f"- Total links to convert: {len(all_changes)}")
    report.append(f"- Files affected: {len(files_with_issues)}")
    report.append("")

    # Detailed changes by file
    report.append("## Detailed Changes")
    report.append("")

    for file_path, changes in sorted(files_with_issues.items()):
        rel_path = Path(file_path).relative_to(BASE_DIR)
        report.append(f"### {rel_path}")
        report.append("")

        for change in changes:
            report.append(f"**Line {change['line']}:**")
            report.append("")
            report.append("Current:")
            report.append(f"```")
            report.append(change['original'])
            report.append(f"```")
            report.append("")
            report.append("Suggested:")
            report.append(f"```")
            report.append(change['suggested'])
            report.append(f"```")
            report.append("")

        report.append("---")
        report.append("")

    # Output as both text and CSV
    report_text = "\n".join(report)
    print(report_text)

    # Write to file
    report_file = BASE_DIR / "scripts" / "link_audit_report.md"
    with open(report_file, 'w') as f:
        f.write(report_text)

    # Also create CSV for easier processing
    csv_file = BASE_DIR / "scripts" / "link_changes.csv"
    with open(csv_file, 'w') as f:
        f.write("file,line,original,suggested\n")
        for change in all_changes:
            original = change['original'].replace('"', '""')
            suggested = change['suggested'].replace('"', '""')
            f.write(f'"{change["relative_file"]}",{change["line"]},"{original}","{suggested}"\n')

    print(f"\n\nReport written to: {report_file}")
    print(f"CSV written to: {csv_file}")

    return all_changes

if __name__ == "__main__":
    generate_report()

