# nitinkc.github.io

Personal Jekyll site built on Minimal Mistakes theme.

## Quick Reference

### Most Common Commands

```bash
# Start developing (clean & serve with live reload)
rm -rf ./_site && bundle exec jekyll serve --livereload
```

Open [http://localhost:4000](http://localhost:4000) in your browser.

### Other Frequent Commands

```bash
# Build the site
bundle exec jekyll build

# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Clean generated files
rm -rf _site

# Kill process on port 4000 if it's stuck
lsof -P | grep ':4000' | awk '{print $2}' | xargs kill -9
```

---

## Setup (Choose Your Path)

**First time?** Pick one setup method below:

| Method               | Best For                            | Requirements        | Time      |
|:---------------------|:------------------------------------|:--------------------|:----------|
| **Automated Script** | Everyone                            | Homebrew + macOS    | 5-10 min  |
| **rbenv + Homebrew** | Users with admin access or Homebrew | Homebrew, Xcode CLT | 10-15 min |
| **User Gems**        | Users without admin access          | System Ruby 2.6+    | 5-10 min  |

### Option 1: Automated Setup (Recommended)

Run the provided setup script—handles everything:

```bash
./scripts/setup-local-mac.sh
```

Then start developing:
```bash
bundle exec jekyll serve --livereload
```

**Features:**
- Installs rbenv and Ruby (if needed)
- Configures gems locally in `vendor/bundle`
- Works with `zsh` and auto-initializes your shell
- Supports `--dry-run` flag to preview changes

**When to use:** You have Homebrew installed and want a hands-off setup.

### Option 2: rbenv + Homebrew (Manual)

For step-by-step control or if the script encounters issues:

1. **Install rbenv and Ruby**
   ```bash
   brew install rbenv ruby-build
   echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
   source ~/.zshrc
   rbenv install 3.2.2
   rbenv local 3.2.2
   ```

2. **Install project dependencies**
   ```bash
   gem install bundler
   bundle config set path 'vendor/bundle'
   bundle install
   ```

3. **Start developing**
   ```bash
   bundle exec jekyll serve --livereload
   ```

**When to use:** You prefer manual setup, have Homebrew, or need to debug the process.

### Option 3: User Gems (No Admin Access)

For Macs without Homebrew or admin access—uses your system Ruby:

1. **Add user gem directory to your PATH**
   ```bash
   export PATH="$(ruby -r rubygems -e 'print Gem.user_dir')/bin:$PATH"
   echo 'export PATH="$(ruby -r rubygems -e "print Gem.user_dir")/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

2. **Verify system Ruby version** (must be 2.6 or higher)
   ```bash
   ruby --version
   ```

3. **Install gems for your user account**
   ```bash
   gem install --user-install bundler jekyll
   bundle config set path 'vendor/bundle'
   bundle install
   ```

4. **Start developing**
   ```bash
   bundle exec jekyll serve --livereload
   ```

**When to use:** You don't have admin access, Homebrew is unavailable, or you prefer using system Ruby.

**Note:** System Ruby on macOS is typically older (2.6–2.7). If you need Ruby 3.0+, use Option 1 or 2.

---

## Troubleshooting

### Bundle install fails with native extension errors

Install Xcode command-line tools and dependencies:

```bash
xcode-select --install
brew install libxml2 libxslt
export LDFLAGS="-L$(brew --prefix libxml2)/lib -L$(brew --prefix libxslt)/lib"
export CPPFLAGS="-I$(brew --prefix libxml2)/include -I$(brew --prefix libxslt)/include"
bundle install
```

**Applies to:** rbenv + Homebrew (Option 2)

### "bundle: command not found"

If you used Option 3 (User Gems), ensure your PATH was updated and sourced:

```bash
source ~/.zshrc
which bundle
```

If still not found, reinstall bundler:
```bash
gem install --user-install bundler
gem install --user-install jekyll
```

### Package.json not found or build errors

Clean and rebuild:

```bash
rm -rf _site
bundle exec jekyll clean
bundle install
```

### Port 4000 already in use

Kill the existing process:
```bash
lsof -P | grep ':4000' | awk '{print $2}' | xargs kill -9
```

---

## Setup Details & Advanced Options

### Setup Script Details (`scripts/setup-local-mac.sh`)

The automated setup script provides:
- **Idempotent execution** — Safe to run multiple times; skips already-installed items
- **Dry-run mode** — Preview changes before applying: `./scripts/setup-local-mac.sh --dry-run`
- **Homebrew integration** — Requires Homebrew; fails gracefully if unavailable
- **Shell initialization** — Automatically updates `~/.zshrc` with rbenv paths
- **Local rbenv configuration** — Sets `.rbenv-version` in the repo so each machine can use a different Ruby if needed

See [scripts/setup-local-mac.sh](scripts/setup-local-mac.sh) for full source.

### Alternative Setup: bash shell

If you use `bash` instead of `zsh`, adjust the shell init lines:

**With rbenv/brew:**
```bash
echo 'eval "$(rbenv init - bash)"' >> ~/.bashrc
```

**With user gems:**
```bash
echo 'export PATH="$(ruby -r rubygems -e 'print Gem.user_dir')/bin:$PATH"' >> ~/.bashrc
```

Then:
```bash
source ~/.bashrc
```

### Vendor Directory & Bundle Configuration

Gems are installed locally to `vendor/bundle` (not system-wide) to avoid:
- Needing elevated privileges
- Conflicts with other projects
- Cluttering your system Ruby

View or modify bundle settings:
```bash
bundle config list
```

---

## Site Customization

### Search Features

Three search providers available (configured in `_config.yml`):

| Provider | Setup | Quality | Notes |
|----------|-------|---------|-------|
| **Lunr** (default) | None | Basic | Client-side, works offline |
| **Google** | Requires CSE | Excellent | Auto-indexed by Google |
| **Algolia** | Requires account + indexing | Excellent | Advanced features, may need SSL fixes |

**Quick switch:** Edit `_config.yml` and change `search_provider` to `lunr`, `google`, or `algolia`

<details>
<summary>Configuration examples</summary>

**Lunr (default):**
```yaml
search_provider: lunr
```

**Google Custom Search:**
```yaml
search_provider: google
google:
  search_engine_id: YOUR_SEARCH_ENGINE_ID
```
Setup: https://programmablesearchengine.google.com/

**Algolia:**
```yaml
search_provider: algolia
algolia:
  application_id: YOUR_APPLICATION_ID
  index_name: YOUR_INDEX_NAME
  search_only_api_key: YOUR_SEARCH_ONLY_API_KEY
```

Index content:
```bash
ALGOLIA_API_KEY='admin_key' bundle exec jekyll algolia
```
</details>

### Front Matter Options

Expand content width (removes TOC sidebar):
```yaml
---
classes: wide
---
```

### Vendor Font Awesome Locally (Optional)

To use a local copy instead of CDN:
```bash
mkdir -p assets/vendor/fontawesome/js
curl -L -o assets/vendor/fontawesome/js/all.js https://use.fontawesome.com/releases/v5.0.2/js/all.js
```

---

## Resources

- [Markdown Reference](_posts/developertools/2022-01-19-markdown-reference.md)
- [Text Symbols Generator](https://fsymbols.com/generators/encool/)
- [Google Sitemap Documentation](https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap)

---

## Link Checking

### Quick Link Check

Visit [https://nitinkc.github.io/sitemap.xml](https://nitinkc.github.io/sitemap.xml) to see all published links.

**Comprehensive broken link check:**
1. Go to [deadlinkchecker.com](https://deadlinkchecker.com)
2. Enter `https://nitinkc.github.io`
3. Wait for crawl results

This tool will find all broken links on the site without needing the sitemap URL.
