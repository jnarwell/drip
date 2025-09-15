#!/bin/bash
# Script to help export draw.io diagrams

echo "Draw.io Diagram Export Helper"
echo "============================="
echo ""
echo "This script will guide you through exporting your diagrams"
echo ""

# Check for draw.io files in Downloads
HTML_FILE="$HOME/Downloads/drip_printing.drawio (2).html"
PNG_FILE="$HOME/Downloads/drip_printing.drawio (4).png"

if [ -f "$HTML_FILE" ]; then
    echo "✓ Found draw.io HTML file"
    mkdir -p docs/assets/diagrams
    cp "$HTML_FILE" "docs/assets/diagrams/system_architecture.html"
    echo "✓ Copied HTML to docs/assets/diagrams/"
else
    echo "✗ Draw.io HTML file not found"
fi

if [ -f "$PNG_FILE" ]; then
    echo "✓ Found draw.io PNG file"
    mkdir -p docs/assets/images
    cp "$PNG_FILE" "docs/assets/images/system_architecture.png"
    echo "✓ Copied PNG to docs/assets/images/"
else
    echo "✗ Draw.io PNG file not found"
fi

echo ""
echo "Manual Export Steps Required:"
echo "-----------------------------"
echo "1. Open your diagram in draw.io (https://app.diagrams.net)"
echo "2. File → Open → Select your .drawio file"
echo ""
echo "3. Export as PNG (for static display):"
echo "   - File → Export as → PNG"
echo "   - Settings: 300 DPI, Border: 10px"
echo "   - Save to: docs/assets/images/system_architecture.png"
echo ""
echo "4. Export subsystem views:"
echo "   - Select specific subsystem in diagram"
echo "   - File → Export as → PNG"
echo "   - Save with descriptive names:"
echo "     * frame_subsystem.png"
echo "     * acoustic_subsystem.png"
echo "     * thermal_subsystem.png"
echo "     * control_hierarchy.png"
echo ""
echo "5. Optional: Export as SVG for scalability"
echo "   - File → Export as → SVG"
echo "   - Save to: docs/assets/images/system_architecture.svg"