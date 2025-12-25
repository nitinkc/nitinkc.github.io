#!/usr/bin/env python3
"""
Fix broken bold markdown patterns where ** is separated by a line break.
Pattern: **text\n** becomes **text**
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / '_posts'

# Pattern to find: ** followed by content, then newline, then **
# This matches cases like:
# **Some text
# ** [link]
pattern = re.compile(r'\*\*([^\*\n]+)\n\*\*', re.MULTILINE)

def fix_file(file_path):
    """Fix broken bold markdown in a single file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Replace pattern: **text\n** with **text**
        content = pattern.sub(r'**\1**', content)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f'Error processing {file_path}: {e}')
        return False

# Find and fix all markdown files
fixed_files = []
for md_file in POSTS_DIR.rglob('*.md'):
    if fix_file(md_file):
        fixed_files.append(str(md_file.relative_to(ROOT)))

print(f'Fixed {len(fixed_files)} files:')
for f in fixed_files[:30]:
    print(f'  - {f}')
if len(fixed_files) > 30:
    print(f'  ... and {len(fixed_files) - 30} more')

