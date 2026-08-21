#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║   🚀 LocalKard - Push to GitHub                                     ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "This will push your code to GitHub so you can deploy to Streamlit Cloud."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Get Your GitHub Personal Access Token"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Open this link: https://github.com/settings/tokens/new"
echo "2. Note: LocalKard Deploy"
echo "3. Expiration: 90 days (or your choice)"
echo "4. Select scope: ✅ repo (Full control of private repositories)"
echo "5. Click 'Generate token'"
echo "6. COPY the token (you won't see it again!)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "Have you created the token? (yes/no): " READY

if [ "$READY" != "yes" ]; then
    echo ""
    echo "Please create the token first, then run this script again."
    echo "Run: ./push-to-github.sh"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: Enter Your Credentials"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "GitHub Username [localkardadmin]: " USERNAME
USERNAME=${USERNAME:-localkardadmin}

read -sp "GitHub Personal Access Token (paste here): " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo ""
    echo "❌ Token is required!"
    echo "Please run the script again with your token."
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: Pushing to GitHub..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configure remote with token
git remote set-url origin https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/localkard-demo.git

# Push to GitHub
git push -u origin main

PUSH_STATUS=$?

# Remove token from URL for security
git remote set-url origin https://github.com/${USERNAME}/localkard-demo.git

if [ $PUSH_STATUS -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                      ║"
    echo "║   ✅ SUCCESS! Code pushed to GitHub!                                ║"
    echo "║                                                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "NEXT: Deploy to Streamlit Cloud"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Go to: https://share.streamlit.io"
    echo ""
    echo "2. Sign in with GitHub (${USERNAME})"
    echo ""
    echo "3. Click 'New app'"
    echo ""
    echo "4. Configure:"
    echo "   Repository: ${USERNAME}/localkard-demo"
    echo "   Branch: main"
    echo "   Main file path: app.py"
    echo ""
    echo "5. Click 'Deploy!'"
    echo ""
    echo "6. Wait 2-3 minutes for deployment"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Your permanent URL will be something like:"
    echo "https://${USERNAME}-localkard-demo-main-xxxxx.streamlit.app"
    echo ""
    echo "🎉 Almost done! Just deploy on Streamlit Cloud now!"
    echo ""
else
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                      ║"
    echo "║   ❌ Push Failed                                                     ║"
    echo "║                                                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Possible reasons:"
    echo "1. Invalid token"
    echo "2. Repository doesn't exist on GitHub"
    echo "3. Wrong username"
    echo "4. Token doesn't have 'repo' scope"
    echo ""
    echo "Please check and try again:"
    echo "./push-to-github.sh"
    echo ""
fi

