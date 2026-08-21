#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🚀 LocalKard Streamlit Demo - GitHub Setup                ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

echo ""
echo "📝 Setting up git configuration..."

# Configure git
git config user.name "${GIT_NAME:-LocalKard Demo}"
git config user.email "${GIT_EMAIL:-demo@localkard.com}"

echo "✅ Git configured"
echo ""

# Add all files
echo "📦 Staging files..."
git add .
echo "✅ Files staged"
echo ""

# Commit
echo "💾 Creating commit..."
git commit -m "LocalKard Phase 1 - Streamlit Demo

- Full interactive demo
- Shop dashboard
- WhatsApp simulation
- Product management
- Order tracking
- Documentation

Ready for deployment to Streamlit Cloud"

echo "✅ Commit created"
echo ""

# Instructions for remote
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   📤 Next: Push to GitHub                                    ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Run these commands:"
echo ""
echo "1️⃣  Create GitHub repo at: https://github.com/new"
echo "    Name: localkard-demo"
echo "    Public repository"
echo ""
echo "2️⃣  Add remote (replace YOUR_USERNAME):"
echo "    git remote add origin https://github.com/YOUR_USERNAME/localkard-demo.git"
echo ""
echo "3️⃣  Set main branch:"
echo "    git branch -M main"
echo ""
echo "4️⃣  Push to GitHub:"
echo "    git push -u origin main"
echo ""
echo "5️⃣  Deploy at: https://share.streamlit.io"
echo "    - Click 'New app'"
echo "    - Select your repository"
echo "    - Click 'Deploy!'"
echo ""
echo "🎉 Your app will be live in 2-3 minutes!"
echo ""
