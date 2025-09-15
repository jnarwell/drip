#!/usr/bin/env python3
"""
Integrate draw.io diagrams into MkDocs documentation
"""

import os
import shutil
from pathlib import Path

class DiagramIntegrator:
    def __init__(self):
        self.docs_dir = Path("docs")
        self.assets_dir = self.docs_dir / "assets"
        self.diagrams_dir = self.assets_dir / "diagrams"
        
    def setup_diagram_directories(self):
        """Create necessary directories for diagrams"""
        os.makedirs(self.diagrams_dir, exist_ok=True)
        os.makedirs(self.assets_dir / "images", exist_ok=True)
        print(f"✓ Created diagram directories")
    
    def process_drawio_files(self):
        """Process draw.io files for integration"""
        
        # Copy the HTML file for interactive viewing
        source_html = "drip_printing.drawio (2).html"
        if os.path.exists(source_html):
            shutil.copy(source_html, self.diagrams_dir / "system_architecture.html")
            print(f"✓ Copied interactive HTML diagram")
        
        # Instructions for exporting static versions
        self.create_export_instructions()
    
    def create_export_instructions(self):
        """Create instructions for exporting draw.io diagrams"""
        
        instructions = """# Draw.io Export Instructions

## To export your diagram as PNG:
1. Open your diagram in draw.io
2. File → Export as → PNG
3. Settings:
   - Border: 10
   - DPI: 300 (for high quality)
   - Transparent background: Optional
4. Save as: `system_architecture.png`
5. Place in: `docs/assets/images/`

## To export as SVG (recommended for scalability):
1. File → Export as → SVG
2. Settings:
   - Include a copy of my diagram: Yes
   - Links: Open in new window
3. Save as: `system_architecture.svg`
4. Place in: `docs/assets/images/`

## To export for interactive embedding:
1. File → Export as → HTML
2. Settings:
   - All Pages: Yes
   - Lightbox: Yes
   - Layers: Yes
3. Save as: `system_architecture_interactive.html`
4. Place in: `docs/assets/diagrams/`
"""
        
        with open(self.diagrams_dir / "EXPORT_INSTRUCTIONS.md", "w") as f:
            f.write(instructions)
        
        print("✓ Created export instructions")

if __name__ == "__main__":
    integrator = DiagramIntegrator()
    integrator.setup_diagram_directories()
    integrator.process_drawio_files()