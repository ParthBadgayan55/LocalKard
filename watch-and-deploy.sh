#!/bin/bash
# Watch for file changes and auto-deploy to Streamlit Cloud
# Run this in the background to enable continuous deployment

echo "👀 LocalKard Auto-Deploy Watcher"
echo "================================"
echo ""
echo "Watching for changes in: /home/ec2-user/localkard/streamlit-demo"
echo "Press Ctrl+C to stop"
echo ""

cd /home/ec2-user/localkard/streamlit-demo

# Install inotify-tools if not available
if ! command -v inotifywait &> /dev/null; then
    echo "Installing file watcher..."
    sudo yum install -y inotify-tools 2>&1 | tail -5
fi

# Function to deploy
deploy() {
    echo ""
    echo "🔄 Changes detected! Deploying..."
    ./auto-deploy.sh
    echo ""
    echo "👀 Watching for more changes..."
}

# Watch for file changes
while inotifywait -e modify,create,delete,move -r . --exclude '\.git|node_modules|__pycache__|\.pyc' 2>/dev/null; do
    # Debounce: wait 2 seconds for more changes
    sleep 2

    # Check if there are uncommitted changes
    if [[ -n $(git status --porcelain) ]]; then
        deploy
    fi
done
