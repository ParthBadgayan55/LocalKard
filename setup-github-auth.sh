#!/bin/bash
# GitHub Authentication Setup Script
# This will set up automatic authentication for GitHub pushes

echo "🔐 Setting up GitHub authentication for LocalKard..."

# Check if already authenticated
if gh auth status 2>/dev/null; then
    echo "✅ Already authenticated with GitHub CLI"
    gh auth setup-git
    echo "✅ Git configured to use GitHub CLI"
else
    echo ""
    echo "🚀 GitHub Authentication Required"
    echo "=================================="
    echo ""
    echo "Option 1: Authenticate via GitHub CLI (Recommended)"
    echo "Run: gh auth login"
    echo ""
    echo "Option 2: Use Personal Access Token"
    echo "1. Go to: https://github.com/settings/tokens/new"
    echo "2. Generate token with 'repo' scope"
    echo "3. Run: export GITHUB_TOKEN=your_token_here"
    echo "4. Run: echo \$GITHUB_TOKEN | gh auth login --with-token"
    echo ""

    # Try web-based auth
    echo "Attempting web-based authentication..."
    gh auth login --web
fi

# Configure git to use gh
gh auth setup-git

echo ""
echo "✅ Setup complete!"
echo "Now you can push with: git push"
