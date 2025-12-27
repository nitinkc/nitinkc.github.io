#!/bin/bash

# Algolia Indexing Script
# Usage: ./algolia-index.sh YOUR_ADMIN_API_KEY

if [ -z "$1" ]; then
    echo "Error: Admin API Key is required"
    echo "Usage: ./algolia-index.sh YOUR_ADMIN_API_KEY"
    echo ""
    echo "Get your Admin API Key from:"
    echo "https://www.algolia.com/account/api-keys/all"
    exit 1
fi

echo "🔍 Indexing site to Algolia..."
echo "Application ID: PH0MFL12HG"
echo "Index Name: nitinkc_github_io"
echo ""

# Set the API key and run the indexing
ALGOLIA_API_KEY="$1" bundle exec jekyll algolia

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Indexing complete!"
    echo "Your search is now powered by Algolia"
else
    echo ""
    echo "❌ Indexing failed"
    echo "Please check your Admin API Key and try again"
    exit 1
fi
