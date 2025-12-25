## Repository Purpose
This repository is a personal Jekyll site built on the "Minimal Mistakes" theme. Primary developer workflows are locally building/serving the site with Bundler/Jekyll, editing Liquid templates in `_includes`, `_layouts`, and posts under `_posts/`.

## What an AI assistant should know
- Site generator: Jekyll (run via `bundle exec jekyll serve` / `bundle exec jekyll build`). See `Gemfile` and `README.md` for recommended commands.
- Theme: Minimal Mistakes (local theme files live in the repo). `package.json` version is used in `Rakefile` tasks.
- Config: `_config.yml` contains site-wide settings (permalinks, plugins, processors like mermaid/plantuml). Modify this for global changes.
- Templates: HTML/Liquid templates are under `_includes/` and `_layouts/`. Small helper partials are used widely (e.g., `head.html`, `scripts.html`).

## Common tasks and commands (examples)
- Install Ruby deps: `bundle install` (use `bundle exec` to run Jekyll)
- Serve when developing: `bundle exec jekyll serve` (kills on port 4000: `lsof -P | grep ':4000' | awk '{print $2}' | xargs kill -9`)
- Full build: `JEKYLL_ENV=production bundle exec jekyll build` (output in `_site`)
- Clean generated site: `bundle exec jekyll clean` or `rm -rf _site`
- Theme-related dev tasks: `rake js`, `rake preview`, and other Rake tasks defined in `Rakefile`.

## Project-specific conventions and patterns
- Posts: `_posts/` subfolders indicate primary categories; the codebase prefers a single canonical category per post (see `scripts/taxonomy_audit.py`).
- Permalinks: set in `_config.yml` as `/:categories/:title/` — avoid changing post paths without updating redirects.
- Includes/layouts: small modular partials are used. Follow existing classes and `site`/`page` Liquid variables rather than introducing new global variables.
- JS building: `assets/js/main.min.js` is produced by `rake js` using `npx uglifyjs`. Edit source files under `assets/js/plugins/` or `_main.js`.

## Integration points and external dependencies
- External scripts are referenced in `_config.yml` (`mermaid`, `mathjax`) — don't remove unless testing locally with the same network access.
- Search: default client-side `lunr` is used; Algolia keys are not configured.
- Comments providers are configurable in `_config.yml` (disqus, staticman, utterances) — treat as optional integrations.

## Tests and helper scripts
- There are no automated unit tests in the repo. The main helper script is `scripts/taxonomy_audit.py` (uses `requirements.txt`). Run it via a Python venv: `python -m venv .venv && ./.venv/bin/pip install -r requirements.txt && python scripts/taxonomy_audit.py audit-tags`.

## When editing templates or content
- Small UI changes: edit `_includes/*` or `_layouts/*`. Preview with `bundle exec jekyll serve` and validate markup under `_site`.
- Large refactors: update `Rakefile` tasks if build outputs change (e.g., JS target path) and update `README.md` accordingly.
- Front-matter conventions: use `layout`, `author_profile`, `read_time`, `comments`, and `related` fields as shown in `_config.yml` defaults.

## Examples to reference in code changes
- Change header/analytics: `_includes/head.html` and `_includes/analytics.html`.
- Add/remove footer links: `_config.yml` -> `footer.links` and `_includes/footer.html`.
- Update copyright generation: `Rakefile` creates `_includes/copyright.*` files from `package.json`.

## Helpful in-repo reference
- Markdown reference: `_posts/developertools/2022-01-19-markdown-reference.md` — useful for examples of front-matter, classes (e.g., `wide`), and common Markdown/Liquid patterns used across posts.

## Safety and style
- Keep Liquid logic simple in templates; heavy logic should go into small Ruby/Jekyll plugins or the `scripts/` helpers.
- Preserve existing HTML structure and CSS class names to avoid breaking layout inherited from Minimal Mistakes.
