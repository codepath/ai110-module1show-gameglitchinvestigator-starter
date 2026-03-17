# 🍴 Git Fork & Push Cheat Sheet

## When you need to fork a repo and push your changes

### Step 1 — Fork on GitHub
1. Go to the original repo on GitHub
2. Click the **Fork** button (top-right)
3. Select your account as the owner
4. Click **Create fork**

---

### Step 2 — Point your local repo to YOUR fork
```bash
git remote set-url origin https://github.com/Isaaci11/YOUR-REPO-NAME.git
```

### Step 3 — Push to your fork
```bash
git push -u origin main
```

---

### Full workflow (add, commit, push)
```bash
git add .
git commit -m "your message here"
git remote set-url origin https://github.com/Isaaci11/YOUR-REPO-NAME.git
git push -u origin main
```

---

### Useful checks
```bash
# See where your remote is pointing
git remote -v

# See what's changed / uncommitted
git status
```

> 💡 Tip: If `git commit` says "nothing to commit, working tree clean" — 
> your changes were already committed. Just run `git push`!
