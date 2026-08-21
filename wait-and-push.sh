#!/bin/bash
# Wait for GitHub authentication and then push changes

echo "⏳ Waiting for GitHub authentication to complete..."
echo "   (Complete the device authentication at https://github.com/login/device)"
echo ""

MAX_WAIT=300  # 5 minutes
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    if gh auth status 2>/dev/null; then
        echo ""
        echo "✅ GitHub authentication successful!"
        echo ""

        # Configure git to use gh
        gh auth setup-git

        # Push changes
        echo "📤 Pushing changes to GitHub..."
        cd /home/ec2-user/localkard/streamlit-demo
        git push origin main

        echo ""
        echo "✅ Successfully pushed!"
        echo "🔄 Streamlit Cloud will auto-deploy in 2-3 minutes"
        echo "🌐 App URL: https://localkard-demo.streamlit.app/"
        exit 0
    fi

    sleep 5
    ELAPSED=$((ELAPSED + 5))
    echo -n "."
done

echo ""
echo "⏱️  Timeout waiting for authentication"
echo "Please complete authentication and run: ./auto-deploy.sh"
exit 1
