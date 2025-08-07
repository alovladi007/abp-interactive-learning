#!/bin/bash

# ABP Interactive Learning - GitHub Pages Deployment Script
# This script helps you deploy your website to GitHub Pages

echo "🚀 ABP Interactive Learning - GitHub Pages Deployment"
echo "=================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required."
    exit 1
fi

# Repository name
REPO_NAME="abp-interactive-learning"

echo ""
echo "📋 Deployment Summary:"
echo "Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "Live Site: https://$GITHUB_USERNAME.github.io/$REPO_NAME"
echo ""

# Confirm deployment
read -p "Do you want to proceed with deployment? (y/N): " CONFIRM

if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled."
    exit 0
fi

echo ""
echo "🔧 Setting up Git repository..."

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
git add .
echo "✅ Files added to staging"

# Commit files
git commit -m "Deploy ABP Interactive Learning Platform to GitHub Pages"
echo "✅ Files committed"

# Add remote origin
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "✅ Remote origin added"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Your website has been deployed!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "2. Click 'Settings' tab"
    echo "3. Scroll to 'Pages' section"
    echo "4. Under 'Source', select 'Deploy from a branch'"
    echo "5. Choose 'main' branch and '/ (root)' folder"
    echo "6. Click 'Save'"
    echo ""
    echo "🌐 Your site will be live at:"
    echo "https://$GITHUB_USERNAME.github.io/$REPO_NAME"
    echo ""
    echo "⏱️  It may take a few minutes for the site to become available."
else
    echo ""
    echo "❌ Deployment failed. Please check:"
    echo "1. Make sure the repository exists on GitHub"
    echo "2. Check your internet connection"
    echo "3. Verify your GitHub credentials"
    echo ""
    echo "💡 Manual steps:"
    echo "1. Create repository at: https://github.com/new"
    echo "2. Name it: $REPO_NAME"
    echo "3. Make it public"
    echo "4. Don't initialize with README"
    echo "5. Run this script again"
fi
