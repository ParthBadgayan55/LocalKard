# 🚀 LocalKard Auto-Deploy - Quick Start

Your Streamlit app is now set up for **automatic deployment**! Every change you make will automatically go live.

---

## ✅ What's Set Up

- ✅ GitHub CLI authenticated (ParthBadgayan55)
- ✅ Git configured for automatic pushes
- ✅ Dependencies fixed (streamlit>=1.50.0, pandas>=2.1.0)
- ✅ Python 3.9 specified for Streamlit Cloud
- ✅ Automation scripts ready to use

---

## 🎯 How to Deploy Changes

### Option 1: Auto-Deploy Script (Recommended)

**Just run:**
```bash
cd /home/ec2-user/localkard/streamlit-demo
./auto-deploy.sh
```

**What it does:**
- Stages all changes
- Commits with timestamp
- Pushes to GitHub
- Triggers Streamlit Cloud deployment

### Option 2: Continuous Deployment (Set & Forget)

**Start the watcher once:**
```bash
cd /home/ec2-user/localkard/streamlit-demo
nohup ./watch-and-deploy.sh > deploy.log 2>&1 &
```

**Then just edit files:**
```bash
nano app.py
# Save and exit - automatically deploys!
```

**Stop watcher:**
```bash
pkill -f watch-and-deploy.sh
```

### Option 3: Manual Git Commands

```bash
cd /home/ec2-user/localkard/streamlit-demo
git add .
git commit -m "Your message"
git push
```

---

## 📱 Your Live App

**URL:** https://localkard-demo.streamlit.app/

**Deployment time:** 2-3 minutes after push

**Check deployment status:**
1. Go to: https://share.streamlit.io/
2. Sign in with GitHub
3. Find "LocalKard" app
4. View logs if needed

---

## 🔥 Quick Examples

### Update app title
```bash
cd /home/ec2-user/localkard/streamlit-demo
nano app.py
# Change page_title = "LocalKard Phase 1 Demo" to whatever you want
./auto-deploy.sh
# Wait 2-3 minutes → Live!
```

### Add new Python package
```bash
cd /home/ec2-user/localkard/streamlit-demo
echo "plotly>=5.0.0" >> requirements.txt
./auto-deploy.sh
```

### Update theme colors
```bash
nano .streamlit/config.toml
# Change primaryColor = "#2563eb" to your brand color
./auto-deploy.sh
```

---

## 🐛 Troubleshooting

### "Authentication failed"
```bash
gh auth status  # Check if still logged in
gh auth login --web  # Re-authenticate if needed
```

### "No changes to deploy"
Everything is already pushed! Check:
```bash
git status
git log --oneline -3
```

### Streamlit app not updating
- Wait full 3 minutes
- Check https://share.streamlit.io/ for build errors
- View logs in Streamlit Cloud dashboard
- Common issues:
  - Syntax errors in app.py
  - Invalid package versions in requirements.txt
  - Missing files

### View recent deployments
```bash
cd /home/ec2-user/localkard/streamlit-demo
git log --oneline -10
```

---

## 📊 Monitor Your App

### Check if app is live
```bash
curl -I https://localkard-demo.streamlit.app/ | head -5
```

### View deployment logs (if using watcher)
```bash
tail -f /home/ec2-user/localkard/streamlit-demo/deploy.log
```

### Check GitHub pushes
```bash
cd /home/ec2-user/localkard/streamlit-demo
git log --graph --oneline --all -10
```

---

## 💡 Pro Tips

1. **Use the auto-deploy script** - It's the easiest way
2. **Run watcher in tmux/screen** for persistent background deployment
3. **Test locally first** with `streamlit run app.py` before deploying
4. **Keep an eye on Streamlit Cloud** dashboard for build status
5. **Use descriptive commit messages** when using manual git commands

---

## 🎉 You're All Set!

**Your workflow is now:**
1. Edit `app.py` or other files
2. Run `./auto-deploy.sh`
3. Wait 2-3 minutes
4. Changes are live at https://localkard-demo.streamlit.app/

**No more manual uploads, no more complex deployments - just code and deploy!**

---

**Repository:** https://github.com/ParthBadgayan55/LocalKard
**Live App:** https://localkard-demo.streamlit.app/
**Streamlit Dashboard:** https://share.streamlit.io/

🚀 **Happy coding!**
