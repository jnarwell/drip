#!/bin/bash
# setup_docs.sh - Complete documentation setup

echo "🚀 Setting up Acoustic Manufacturing System Documentation"
echo "======================================================="

# Change to script directory
cd "$(dirname "$0")"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Generate documentation
echo "📝 Generating documentation..."
python generate_mkdocs.py

# Build documentation
echo "🔨 Building documentation..."
mkdocs build

# Success message
echo ""
echo "✅ Documentation setup complete!"
echo "======================================================="
echo ""
echo "📚 Next steps:"
echo "1. Test locally:    ./serve_docs.sh"
echo "2. Deploy to web:   ./deploy_docs.sh"
echo "3. View site:       http://localhost:8000 (local)"
echo "                    https://jmarwell.github.io/drip/ (deployed)"
echo ""
echo "📌 GitHub Actions will automatically deploy on push to main branch"

# Deactivate virtual environment
deactivate