#!/bin/bash
# Auto-deploy script for LocalKard Streamlit app
# Automatically commits and pushes changes to trigger Streamlit Cloud deployment

set -e

echo "🚀 LocalKard Auto-Deploy to Streamlit Cloud"
echo "==========================================="
echo ""

cd "$(dirname "$0")"

# Check for changes
if [[ -z $(git status --porcelain) ]]; then
    echo "✅ No changes to deploy"
    exit 0
fi

# Show changes
echo "📝 Changes detected:"
git status --short
echo ""

# Add all changes
git add .

# Generate commit message with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="Auto-deploy: Update LocalKard demo - $TIMESTAMP"

# Commit
git commit -m "$COMMIT_MSG" || {
    echo "⚠️  Nothing to commit (already committed)"
}

# Check if gh is authenticated
if gh auth status 2>/dev/null; then
    echo "✅ GitHub authenticated"
    gh auth setup-git 2>/dev/null || true
    git push origin main
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🔄 Streamlit Cloud will auto-deploy in 2-3 minutes"
    echo "🌐 App URL: https://localkard-demo.streamlit.app/"
else
    echo ""
    echo "⚠️  GitHub authentication required!"
    echo ""
    echo "Run: gh auth login --web"
    echo "Then run this script again: ./auto-deploy.sh"
    exit 1
fi
