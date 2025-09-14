#!/bin/bash
# deploy_docs.sh - Deploy documentation to GitHub Pages

echo "🚀 Deploying Acoustic Manufacturing System Documentation"
echo "======================================================"

# Change to script directory
cd "$(dirname "$0")"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository!"
    echo "Please initialize git and set up your GitHub remote first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Generate documentation
echo "📝 Generating documentation..."
python generate_mkdocs.py

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo "✅ Documentation generated successfully!"
else
    echo "❌ Documentation generation failed!"
    exit 1
fi

# Build the documentation
echo "🔨 Building static site..."
mkdocs build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Site built successfully!"
else
    echo "❌ Site build failed!"
    exit 1
fi

# Deploy to GitHub Pages
echo "📤 Deploying to GitHub Pages..."
echo "======================================================"

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📌 Current branch: $CURRENT_BRANCH"

# Confirm deployment
read -p "Deploy to GitHub Pages? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdocs gh-deploy --force
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Deployment successful!"
        echo "======================================================"
        echo "🌐 Your documentation is now live at:"
        echo "   https://jmarwell.github.io/drip/"
        echo ""
        echo "Note: It may take a few minutes for changes to appear."
    else
        echo "❌ Deployment failed!"
        exit 1
    fi
else
    echo "❌ Deployment cancelled."
fi

# Deactivate virtual environment
deactivate