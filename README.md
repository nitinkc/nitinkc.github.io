# nitinkc.github.io

Personal Jekyll site built on Minimal Mistakes theme.

## Quick Start

### Prerequisites
- Ruby (3.0+)
- Bundler
- macOS with Homebrew (for local setup without sudo)

### Minimal Setup (macOS)

1. **Install rbenv and Ruby** (one-time setup)
   ```bash
   brew install rbenv ruby-build
   echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
   source ~/.zshrc
   rbenv install 3.2.2
   rbenv local 3.2.2
   ```

2. **Install dependencies**
   ```bash
   gem install bundler
   bundle config set path 'vendor/bundle'
   bundle install
   ```

3. **Serve the site**
   ```bash
   bundle exec jekyll serve --livereload
   ```
   
   Open http://localhost:4000

### Common Commands

```bash
# Clean generated files
bundle exec jekyll clean
rm -rf _site

# Build site
bundle exec jekyll build

# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Kill process on port 4000
lsof -P | grep ':4000' | awk '{print $2}' | xargs kill -9
```

### Troubleshooting

**Bundle install fails with native extension errors:**
```bash
xcode-select --install
brew install libxml2 libxslt
export LDFLAGS="-L$(brew --prefix libxml2)/lib -L$(brew --prefix libxslt)/lib"
export CPPFLAGS="-I$(brew --prefix libxml2)/include -I$(brew --prefix libxslt)/include"
bundle install
```

**Package.json not found:**
```bash
rm -rf _site
bundle exec jekyll clean
bundle install
```

## Advanced Setup

### Alternative: User Gem Installation (without rbenv)

If you prefer not to use rbenv:

```bash
# Ensure user gem bin is on PATH
export PATH="$(ruby -r rubygems -e 'print Gem.user_dir')/bin:$PATH"
echo 'export PATH="$(ruby -r rubygems -e "print Gem.user_dir")/bin:$PATH"' >> ~/.zshrc

# Install Jekyll
gem install --user-install jekyll bundler

# Run
jekyll serve --livereload
```

### Automated Setup Script

Run the provided setup script for automated installation:
```bash
./scripts/setup-local-mac.sh
```

## Site Customization

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

## Resources

- [Markdown Reference](_posts/developertools/2022-01-19-markdown-reference.md)
- [Text Symbols Generator](https://fsymbols.com/generators/encool/)
- [Google Sitemap Documentation](https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap)

## Scripts

Helper scripts are available in `scripts/`:
- `setup-local-mac.sh` - Automated setup for macOS