#!/bin/bash

# EUREKA Landing Page Copy Script
# This script copies all necessary files to build the landing page elsewhere

echo "🚀 EUREKA Landing Page Copy Script"
echo "===================================="
echo ""

# Check if destination is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide a destination folder"
    echo ""
    echo "Usage: ./copy-landing-page.sh /path/to/destination"
    echo "Example: ./copy-landing-page.sh ~/my-new-project"
    exit 1
fi

DEST="$1"

echo "📂 Destination: $DEST"
echo ""

# Create destination folder
echo "📁 Creating folder structure..."
mkdir -p "$DEST"
mkdir -p "$DEST/images"

# Copy core files
echo "📄 Copying HTML file..."
cp index.html "$DEST/"

echo "🎨 Copying CSS file..."
cp styles.css "$DEST/"

echo "⚡ Copying JavaScript file..."
cp script.js "$DEST/"

echo "🖼️  Copying images..."
cp images/slide1.webp "$DEST/images/" 2>/dev/null || echo "   ⚠️  slide1.webp not found"
cp images/slide2.png "$DEST/images/" 2>/dev/null || echo "   ⚠️  slide2.png not found"
cp images/slide3.png "$DEST/images/" 2>/dev/null || echo "   ⚠️  slide3.png not found"

echo "📚 Copying instructions..."
cp LANDING_PAGE_BUILD_INSTRUCTIONS.md "$DEST/" 2>/dev/null || echo "   ⚠️  Instructions file not found"

echo ""
echo "✅ Done! Files copied to: $DEST"
echo ""
echo "📋 File structure:"
tree "$DEST" 2>/dev/null || ls -R "$DEST"

echo ""
echo "🎯 Next steps:"
echo "   1. cd $DEST"
echo "   2. python3 -m http.server 8000"
echo "   3. Open http://localhost:8000"
echo ""
echo "📖 Read LANDING_PAGE_BUILD_INSTRUCTIONS.md for detailed setup"
echo ""
