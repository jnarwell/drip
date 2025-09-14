#!/bin/bash
# serve_docs.sh - Local documentation testing server

echo "🔨 Building Acoustic Manufacturing System Documentation..."
echo "=================================================="

# Change to script directory
cd "$(dirname "$0")"

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

# Serve documentation
echo ""
echo "🚀 Starting documentation server..."
echo "=================================================="
echo "📌 Documentation will be available at: http://localhost:8000"
echo "📌 Press Ctrl+C to stop the server"
echo ""

mkdocs serve --dev-addr=0.0.0.0:8000

# Deactivate virtual environment on exit
deactivate