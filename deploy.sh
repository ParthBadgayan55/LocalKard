#!/bin/bash

echo "🚀 LocalKard Streamlit Deployment Helper"
echo ""
echo "This script will help you push to GitHub."
echo ""
echo "You need a GitHub Personal Access Token."
echo "Get one here: https://github.com/settings/tokens/new"
echo ""
echo "Required scope: repo"
echo ""

read -p "Enter your GitHub username [localkardadmin]: " USERNAME
USERNAME=${USERNAME:-localkardadmin}

read -sp "Enter your GitHub Personal Access Token: " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo "❌ Token is required"
    exit 1
fi

# Push using token
git remote set-url origin https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/localkard-demo.git
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Next steps:"
    echo "1. Go to: https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select: ${USERNAME}/localkard-demo"
    echo "5. Click 'Deploy!'"
    echo ""
    echo "Your app will be live in 2-3 minutes!"
else
    echo ""
    echo "❌ Push failed. Check your token and try again."
fi

# Remove token from remote URL for security
git remote set-url origin https://github.com/${USERNAME}/localkard-demo.git
