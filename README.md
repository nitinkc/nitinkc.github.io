# nitinkc.github.io

Clone the code, goto root directory.

Build site using default _config.yml file:

```sh
bundle install 

#Serve site at http://localhost:4000
bundle exec jekyll serve

# if package.json not found exception
rm -r _site | bundle exec jekyll serve 
```

```sh
#Deletes Jekyll generated old ./_site cache folder
bundle exec jekyll clean or 
rm -rf _site 

#Build site into ./_site
bundle exec jekyll build --trace --verbose
bundle exec jekyll build

#Build site as production, default is development
JEKYLL_ENV=production bundle exec jekyll build

#Build site into ./_site and for watch changes
bundle exec jekyll build --watch
```
 
[Text using Symbols](https://fsymbols.com/generators/encool/)

Liquid Templating Language. Add Font matter to the top of the page

---
# front matter tells Jekyll to process Liquid
---

To expand the main content to the right, filling the space of what is normally occupied by the table of contents. Add the following to a post or page’s YAML Front Matter:

classes: wide

sudo bundle install --path vendor/bundle 


added in default.html in navigation and in head.html in include
<!-- Added to allow font awesome icons -->
<script src="https://use.fontawesome.com/releases/v5.0.2/js/all.js"></script>   

kill running process occupying 
```shell
lsof -P | grep ':4000' | awk '{print $2}' | xargs kill -9
```

SiteMap : https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap


pandoc -f docx -t markdown Buying\ a\ bigger\ machine.docx -o x.md  

## Taxonomy and scripts

We added a small Python helper to audit and normalize categories/tags across all posts.

- Location: `scripts/taxonomy_audit.py`
- Requirements: see `requirements.txt`

Quick usage (PowerShell on Windows):

1. Create/activate a virtual environment in the repo root
	- `python -m venv .venv`
	- `./.venv/Scripts/Activate.ps1`
2. Install deps
	- `pip install -r requirements.txt`
3. Dry run audit (prints counts and proposed changes)
	- `python scripts/taxonomy_audit.py audit-tags`
4. Apply changes
	- `python scripts/taxonomy_audit.py audit-tags --apply`

Notes
- Categories are inferred primarily from the top-level folder under `_posts/` and normalized for casing.
- Tags are normalized, low-frequency singletons are dropped, and tags duplicating the primary category are removed.
- Minimal Mistakes supports both string and list formats for `categories`; this script prefers a single canonical category when possible.