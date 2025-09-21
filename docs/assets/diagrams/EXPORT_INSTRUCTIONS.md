# Export Instructions for Draw.io Diagrams

This document explains how to export diagrams from Draw.io to static image formats.

## Current System Architecture Diagram

The interactive system architecture diagram is embedded in the documentation at:
- **Location**: [System Architecture](../../system/architecture.md)
- **File**: `docs/assets/diagrams/system_architecture.html`

## Exporting from the Embedded Viewer

### Quick Export (PNG)
1. Open the [System Architecture](../../system/architecture.md) page
2. In the embedded diagram viewer, look for the toolbar at the top
3. Click the three dots menu (⋮) or export icon
4. Select "Export as" → "PNG"
5. Choose settings and download

### Opening in Draw.io Editor
1. In the embedded viewer, click the pencil icon (Edit)
2. This opens the diagram in the Draw.io editor
3. Make any necessary edits
4. Export using File menu options

## Export Settings by Format

### PNG Export (Recommended for Documentation)
1. File → Export as → PNG
2. Settings:
   - **Zoom**: 200% (for high resolution)
   - **Width**: 2400px
   - **Border**: 10px
   - **Background**: White
   - **DPI**: 300 (if available)
3. Save as: `system_architecture.png`
4. Place in: `docs/assets/images/`

### SVG Export (Recommended for Scalability)
1. File → Export as → SVG
2. Settings:
   - **Include a copy of my diagram**: Yes
   - **Links**: Open in new window
   - **Embed Images**: Yes
   - **Embed Fonts**: Yes
3. Save as: `system_architecture.svg`
4. Place in: `docs/assets/images/`

### PDF Export (For Printing)
1. File → Export as → PDF
2. Settings:
   - **Page Size**: A3 Landscape
   - **Fit to Page**: Yes
   - **Include Grid**: No
3. Save as: `system_architecture.pdf`
4. Place in: `docs/assets/`

## Updating the Interactive Diagram

When you need to update the embedded interactive diagram:

1. Make changes in Draw.io
2. File → Export as → HTML
3. Settings:
   - **Lightbox**: Yes
   - **Layers**: Yes
   - **Pages**: Current page only
   - **Border**: 0
4. Copy the entire HTML output
5. Replace contents of `docs/assets/diagrams/system_architecture.html`
6. Test the embedding in the documentation
7. Commit both the HTML and a PNG backup

## File Naming Convention

Use descriptive names for different versions:
- `system_architecture.html` - Interactive main diagram
- `system_architecture_full.png` - Full diagram export
- `system_architecture_subsystems.png` - Subsystems only view
- `system_architecture_interfaces.png` - Interface connections focus
- `system_architecture_simplified.svg` - Simplified version for presentations

## Version Control Best Practices

1. Always commit both interactive (HTML) and static (PNG) versions
2. Use descriptive commit messages:
   ```
   docs: Update system architecture diagram
   - Added emergency shutdown connections
   - Updated component colors for clarity
   - Fixed ICD-010 interface routing
   ```
3. Tag major diagram versions in git for reference
