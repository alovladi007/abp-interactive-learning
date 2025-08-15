# 📋 Detailed Manual Deployment Guide for GitHub Pages

## Prerequisites
- GitHub account (free at https://github.com)
- Git installed on your computer
- Terminal/Command Prompt access

## Step 1: Create GitHub Repository

### 1.1 Go to GitHub
- Open your web browser
- Navigate to https://github.com
- Sign in to your account

### 1.2 Create New Repository
- Click the green "New" button (or go to https://github.com/new)
- Repository name: `abp-interactive-learning`
- Description: "ABP Interactive Learning Platform - AI-powered educational platform"
- Make sure it's set to **Public** (required for free GitHub Pages)
- **DO NOT** check "Add a README file"
- **DO NOT** check "Add .gitignore"
- **DO NOT** check "Choose a license"
- Click "Create repository"

### 1.3 Copy Repository URL
After creation, you'll see a page with setup instructions. Copy the repository URL:
`https://github.com/YOUR_USERNAME/abp-interactive-learning.git`

## Step 2: Prepare Your Local Files

### 2.1 Open Terminal/Command Prompt
- **Mac**: Press Cmd+Space, type "Terminal", press Enter
- **Windows**: Press Win+R, type "cmd", press Enter
- **Linux**: Press Ctrl+Alt+T

### 2.2 Navigate to Project Directory
```bash
cd Desktop/abp-interactive-learning
```

### 2.3 Verify Files Are Present
```bash
ls -la
```
You should see all these files:
- index.html
- tutoring-videos.html
- premium-tutoring-videos.html
- dashboard.html
- academic-setup.html
- certifications.html
- home.html
- styles.css
- dashboard.css
- dashboard.js
- script.js
- README.md
- .gitignore

## Step 3: Initialize Git Repository

### 3.1 Initialize Git
```bash
git init
```
This creates a new Git repository in your folder.

### 3.2 Configure Git (First Time Only)
If you haven't used Git before, configure your identity:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3.3 Add All Files
```bash
git add .
```
This stages all files for commit.

### 3.4 Create Initial Commit
```bash
git commit -m "Initial commit: ABP Interactive Learning Platform"
```

### 3.5 Set Main Branch
```bash
git branch -M main
```

## Step 4: Connect to GitHub

### 4.1 Add Remote Origin
Replace `YOUR_USERNAME` with your actual GitHub username:
```bash
git remote add origin https://github.com/YOUR_USERNAME/abp-interactive-learning.git
```

### 4.2 Push to GitHub
```bash
git push -u origin main
```

**Note**: You may be prompted for your GitHub credentials:
- Username: Your GitHub username
- Password: Your GitHub personal access token (not your account password)

### 4.3 Create Personal Access Token (If Needed)
If you don't have a personal access token:
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "ABP Learning Deployment"
4. Select expiration (recommend 90 days)
5. Check "repo" scope
6. Click "Generate token"
7. Copy the token and use it as your password

## Step 5: Enable GitHub Pages

### 5.1 Go to Repository Settings
- Navigate to your repository: `https://github.com/YOUR_USERNAME/abp-interactive-learning`
- Click the "Settings" tab (far right in the repository menu)

### 5.2 Find Pages Section
- Scroll down to "Pages" in the left sidebar
- Click on "Pages"

### 5.3 Configure Pages
- Under "Source", select "Deploy from a branch"
- Under "Branch", select "main"
- Under "Folder", select "/ (root)"
- Click "Save"

### 5.4 Wait for Deployment
- GitHub will show a message: "Your site is ready to be published"
- Wait 5-10 minutes for the site to build and deploy
- Refresh the page to see the live URL

## Step 6: Access Your Live Site

Your website will be available at:
`https://YOUR_USERNAME.github.io/abp-interactive-learning`

## Step 7: Verify Everything Works

### 7.1 Test Main Pages
- ✅ Landing page loads
- ✅ Navigation menu works
- ✅ Tutoring Videos page loads
- ✅ Premium Access button works
- ✅ Premium videos page loads
- ✅ All styling appears correctly

### 7.2 Test Premium Access
- Go to Tutoring Videos page
- Click "View All Premium Videos (400+)" button
- Verify it takes you to premium-tutoring-videos.html

## Troubleshooting

### Problem: "Repository not found" error
**Solution**: 
- Check repository name is exactly `abp-interactive-learning`
- Verify your username is correct in the URL
- Make sure repository is public

### Problem: Git push fails with authentication error
**Solution**:
- Use personal access token instead of password
- Check username is correct
- Verify token has "repo" permissions

### Problem: Site shows 404 error
**Solution**:
- Wait 10-15 minutes after enabling Pages
- Check Pages settings are correct (main branch, / root)
- Verify index.html exists in repository

### Problem: Premium button doesn't work
**Solution**:
- Check premium-tutoring-videos.html exists in repository
- Verify file names are exactly correct (case-sensitive)
- Clear browser cache and try again

### Problem: Styling looks broken
**Solution**:
- Check styles.css and dashboard.css are uploaded
- Verify Font Awesome CDN link is working
- Check browser console for errors (F12)

## Making Updates

To update your site after initial deployment:

1. **Make changes to your local files**
2. **Add and commit changes:**
   ```bash
   git add .
   git commit -m "Update: description of changes"
   ```
3. **Push to GitHub:**
   ```bash
   git push origin main
   ```
4. **Wait 2-5 minutes** for changes to appear on live site

## Security Notes

- Never commit sensitive information (passwords, API keys)
- Use .gitignore to exclude sensitive files
- Personal access tokens should be kept secure
- Repository must be public for free GitHub Pages

## Support

If you encounter issues:
1. Check GitHub's status page: https://www.githubstatus.com/
2. Review GitHub Pages documentation: https://docs.github.com/en/pages
3. Check repository settings are correct
4. Verify all files uploaded successfully

---

**Your site will be live at: `https://YOUR_USERNAME.github.io/abp-interactive-learning`**
