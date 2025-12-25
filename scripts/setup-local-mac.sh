#!/usr/bin/env bash
set -euo pipefail

# scripts/setup-local-mac.sh
# Idempotent script to prepare a macOS user (no sudo) for running this Jekyll site.
# - Uses Homebrew (assumed installed for the user)
# - Installs rbenv + ruby-build, installs Ruby, configures rbenv locally for the repo
# - Installs bundler and project gems into ./vendor/bundle
# - Safe: supports --dry-run to only print actions

DRY_RUN=0
while [[ ${1-} != "" ]]; do
  case "$1" in
    -n|--dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--dry-run]"
      echo "--dry-run  : Print actions without executing them"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

run_cmd() {
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "+ $*"
  else
    echo "+ $*"
    # Use bash -lc to execute the command string safely (preserves whitespace)
    bash -lc "$*"
  fi
}

# Determine repo root (one level up from scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Repository root: $REPO_ROOT"

echo "Starting setup-local-mac.sh (dry-run=$DRY_RUN)"

# 1) Check for Homebrew
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found in PATH. Please install Homebrew for your user first: https://brew.sh/"
  exit 1
fi

echo "Homebrew found: $(command -v brew)"

# 2) Install rbenv and ruby-build via brew if missing
if ! command -v rbenv >/dev/null 2>&1; then
  run_cmd brew update
  run_cmd brew install rbenv ruby-build
else
  echo "rbenv already installed: $(command -v rbenv)"
fi

# 3) Add rbenv init lines to ~/.zshrc if not present (idempotent)
ZSHRC_FILE="$HOME/.zshrc"
RPATH_LINE='export PATH="$HOME/.rbenv/bin:$PATH"'
REVAL_LINE='eval "$(rbenv init - zsh)"'

if ! grep -qxF "$RPATH_LINE" "$ZSHRC_FILE" 2>/dev/null; then
  # Append the PATH line to the user's ~/.zshrc
  run_cmd "printf '%s\n' '$RPATH_LINE' >> \"$ZSHRC_FILE\""
fi
# Append the rbenv init line if it's not already present
if ! grep -q "rbenv init - zsh" "$ZSHRC_FILE" 2>/dev/null; then
  run_cmd "printf '%s\n' '$REVAL_LINE' >> \"$ZSHRC_FILE\""
else
  echo "$HOME/.zshrc already contains rbenv init"
fi

# Apply rbenv to current shell (note: this affects this script's process only)
run_cmd export PATH="$HOME/.rbenv/bin:$PATH"
run_cmd eval "$(rbenv init - zsh)"

# 4) Determine Ruby version: use .ruby-version if present, else default
DEFAULT_RUBY="3.2.2"
if [ -f "$REPO_ROOT/.ruby-version" ]; then
  RUBY_VERSION="$(cat "$REPO_ROOT/.ruby-version")"
  echo "Using Ruby version from .ruby-version: $RUBY_VERSION"
else
  RUBY_VERSION="$DEFAULT_RUBY"
  echo "No .ruby-version found; using default: $RUBY_VERSION"
fi

# 5) Install Ruby via rbenv
run_cmd rbenv install -s "$RUBY_VERSION"

# 6) Set local Ruby for repo
run_cmd cd "$REPO_ROOT" && rbenv local "$RUBY_VERSION"
run_cmd rbenv rehash

# 7) Install bundler into the rbenv Ruby
run_cmd gem install bundler

# 8) Configure bundle to install into vendor/bundle and install gems
run_cmd cd "$REPO_ROOT" && bundle config set path 'vendor/bundle'
run_cmd cd "$REPO_ROOT" && bundle install --jobs=4 --retry=2

# 9) Optional: create binstub for jekyll so you can run ./bin/jekyll
if [ -d "$REPO_ROOT/bin" ]; then
  echo "./bin already exists"
else
  run_cmd mkdir -p "$REPO_ROOT/bin"
fi
run_cmd cd "$REPO_ROOT" && bundle binstubs jekyll --force --path=./bin || true

# 10) Final messages
echo ""
if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry-run complete. Re-run without --dry-run to perform the changes."
else
  echo "Setup complete. To start the site:"
  echo "  cd $REPO_ROOT"
  echo "  bundle exec jekyll serve --livereload"
fi

exit 0

