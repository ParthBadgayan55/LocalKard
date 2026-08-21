# 🤖 LocalKard Auto-Deployment Setup

Complete automation for keeping your Streamlit app always up-to-date with latest changes.

---

## ✅ Quick Setup (One-Time)

### 1. Authenticate with GitHub

```bash
cd /home/ec2-user/localkard/streamlit-demo

# Option A: Web-based (Recommended)
gh auth login --web

# Option B: Token-based
# Get token from: https://github.com/settings/tokens/new (with 'repo' scope)
echo "YOUR_TOKEN" | gh auth login --with-token

# Verify authentication
gh auth status
```

### 2. Configure Git to use GitHub CLI

```bash
gh auth setup-git
```

### 3. Test the setup

```bash
./auto-deploy.sh
```

---

## 🚀 Auto-Deploy Scripts

### `auto-deploy.sh` - Manual Deploy

Commits and pushes all changes to trigger Streamlit Cloud deployment.

**Usage:**
```bash
./auto-deploy.sh
```

**What it does:**
1. Checks for uncommitted changes
2. Stages all changes (`git add .`)
3. Commits with timestamp
4. Pushes to GitHub (`origin/main`)
5. Streamlit Cloud auto-deploys in 2-3 minutes

---

### `watch-and-deploy.sh` - Continuous Deployment

Watches for file changes and automatically deploys when files are modified.

**Usage:**
```bash
# Run in background
nohup ./watch-and-deploy.sh > deploy.log 2>&1 &

# Or run in a tmux/screen session
tmux new -s deploy
./watch-and-deploy.sh
# Press Ctrl+B then D to detach
```

**What it does:**
1. Monitors `app.py`, `requirements.txt`, config files for changes
2. Automatically runs `auto-deploy.sh` when changes detected
3. Provides debouncing (waits 2 seconds for multiple edits)
4. Logs all deployments

**Stop watching:**
```bash
# Find the process
ps aux | grep watch-and-deploy

# Kill it
kill <PID>

# Or if in tmux
tmux attach -t deploy
# Press Ctrl+C
```

---

### `wait-and-push.sh` - Helper Script

Waits for GitHub authentication to complete, then pushes changes.

**Usage:**
```bash
./wait-and-push.sh &
# Complete authentication in browser
```

---

## 📋 Typical Workflows

### Workflow 1: Manual Deployment

Make changes → Run `./auto-deploy.sh` → Wait 2-3 minutes → App updated

### Workflow 2: Continuous Deployment

**Setup once:**
```bash
# Authenticate
gh auth login --web

# Start watcher in background
nohup ./watch-and-deploy.sh > deploy.log 2>&1 &
```

**Then just edit files:**
```bash
nano app.py
# Save and exit
# Watcher automatically deploys!
```

### Workflow 3: VS Code Integration

**Add to `.vscode/tasks.json`:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Deploy to Streamlit Cloud",
      "type": "shell",
      "command": "./auto-deploy.sh",
      "options": {
        "cwd": "${workspaceFolder}/streamlit-demo"
      },
      "problemMatcher": []
    }
  ]
}
```

Then: `Ctrl+Shift+P` → "Run Task" → "Deploy to Streamlit Cloud"

---

## 🔐 Security Notes

**GitHub CLI stores credentials securely:**
- Credentials stored in system keychain
- Uses OAuth tokens, not passwords
- Tokens can be revoked at: https://github.com/settings/tokens

**For servers/CI:**
```bash
# Use a fine-grained token with only 'repo' access
export GITHUB_TOKEN="github_pat_xxx"
echo $GITHUB_TOKEN | gh auth login --with-token
```

---

## 🐛 Troubleshooting

### "You are not logged into any GitHub hosts"

**Fix:**
```bash
gh auth login --web
gh auth setup-git
```

### "Permission denied (publickey)"

**Fix:**
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/ParthBadgayan55/LocalKard.git
gh auth setup-git
```

### "Nothing to commit"

Already deployed! Check:
```bash
git status
git log --oneline -3
```

### Watcher not detecting changes

**Check if running:**
```bash
ps aux | grep watch-and-deploy
```

**Restart it:**
```bash
killall watch-and-deploy.sh
./watch-and-deploy.sh &
```

### Streamlit Cloud not updating

**Check deployment status:**
1. Go to: https://share.streamlit.io/
2. Find your app
3. Click "Manage app" → View logs
4. Look for build errors

**Common issues:**
- `requirements.txt` has invalid versions
- Python syntax errors in `app.py`
- Missing files referenced in code

---

## 📊 Monitoring Deployments

### View deployment logs
```bash
tail -f deploy.log
```

### Check recent commits
```bash
git log --oneline -10
```

### Check GitHub Actions (if configured)
```bash
gh run list
gh run view
```

### Check Streamlit Cloud status
```bash
curl -s https://localkard-demo.streamlit.app/ | grep -o "<title>.*</title>"
```

---

## ⚡ Advanced: Git Hooks

**Auto-deploy on every commit:**

Create `.git/hooks/post-commit`:
```bash
#!/bin/bash
cd /home/ec2-user/localkard/streamlit-demo
git push origin main
```

Make executable:
```bash
chmod +x .git/hooks/post-commit
```

Now every `git commit` automatically pushes!

---

## 🎯 Quick Reference

| Command | Purpose |
|---------|---------|
| `gh auth login --web` | Authenticate with GitHub |
| `gh auth status` | Check authentication |
| `./auto-deploy.sh` | Deploy now |
| `./watch-and-deploy.sh &` | Start continuous deployment |
| `git push` | Manual push (if authenticated) |
| `gh run list` | View GitHub Actions runs |

---

## 🌐 Your App URLs

- **Production:** https://localkard-demo.streamlit.app/
- **GitHub Repo:** https://github.com/ParthBadgayan55/LocalKard
- **Streamlit Dashboard:** https://share.streamlit.io/

---

## ✅ Setup Checklist

- [ ] GitHub CLI installed (`gh --version`)
- [ ] Authenticated with GitHub (`gh auth status`)
- [ ] Git configured (`gh auth setup-git`)
- [ ] Tested manual deploy (`./auto-deploy.sh`)
- [ ] Optional: Started watcher (`./watch-and-deploy.sh &`)

---

**🎉 Once set up, your Streamlit app stays automatically synced with every change!**
