#!/usr/bin/env python3
"""
Apply saved edits from the documentation editor back to the source markdown files.
This script reads the JSON export from the web editor and updates the original files.
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List, Tuple

class EditApplier:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.applied_edits = []
        self.failed_edits = []
        
    def load_edits(self, edits_file: str) -> Dict:
        """Load edits from JSON file."""
        with open(edits_file, 'r') as f:
            data = json.load(f)
        return data
    
    def parse_edit_id(self, edit_id: str) -> Tuple[str, str, int, str]:
        """Parse edit ID to get file path and location info."""
        parts = edit_id.split(':', 3)
        if len(parts) != 4:
            raise ValueError(f"Invalid edit ID format: {edit_id}")
        
        path, tag, index, text_snippet = parts
        return path, tag, int(index), text_snippet
    
    def find_file_from_path(self, web_path: str) -> Path:
        """Convert web path to actual file path."""
        # Remove leading/trailing slashes
        web_path = web_path.strip('/')
        
        # Handle special cases
        if web_path == '' or web_path == 'index.html':
            return self.docs_dir / 'index.md'
        
        # Remove .html extension and add .md
        if web_path.endswith('/index.html'):
            web_path = web_path[:-11]  # Remove /index.html
        elif web_path.endswith('.html'):
            web_path = web_path[:-5]  # Remove .html
        elif web_path.endswith('/'):
            web_path = web_path[:-1]  # Remove trailing slash
            
        # Convert to file path
        file_path = self.docs_dir / f"{web_path}.md"
        
        # Check if it's an index file in a directory
        if not file_path.exists():
            dir_path = self.docs_dir / web_path / "index.md"
            if dir_path.exists():
                return dir_path
                
        return file_path
    
    def apply_edit(self, edit_id: str, new_content: str) -> bool:
        """Apply a single edit to a file."""
        try:
            path, tag, index, text_snippet = self.parse_edit_id(edit_id)
            file_path = self.find_file_from_path(path)
            
            if not file_path.exists():
                print(f"Warning: File not found: {file_path}")
                self.failed_edits.append((edit_id, f"File not found: {file_path}"))
                return False
            
            # Read the file
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Convert HTML content back to Markdown
            markdown_content = self.html_to_markdown(new_content, tag)
            
            # Find and replace the content
            # This is a simplified approach - in production you'd want more robust matching
            lines = content.split('\n')
            modified = False
            
            # Try to find the line to modify based on tag type
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # Headers
                header_level = int(tag[1])
                header_prefix = '#' * header_level + ' '
                
                for i, line in enumerate(lines):
                    if line.startswith(header_prefix):
                        # Simple match - in production, you'd want better matching
                        lines[i] = header_prefix + markdown_content
                        modified = True
                        break
                        
            elif tag == 'p' or tag == 'li' or tag == 'td':
                # For paragraphs, list items, and table cells
                # This is a simplified approach
                # In production, you'd parse the markdown properly
                print(f"Info: Paragraph/list/table edit - manual review recommended for: {edit_id}")
                self.failed_edits.append((edit_id, "Complex edit - manual review needed"))
                return False
            
            if modified:
                # Write back to file
                with open(file_path, 'w') as f:
                    f.write('\n'.join(lines))
                
                self.applied_edits.append((edit_id, file_path))
                return True
            else:
                self.failed_edits.append((edit_id, "Could not locate content in file"))
                return False
                
        except Exception as e:
            print(f"Error applying edit {edit_id}: {str(e)}")
            self.failed_edits.append((edit_id, str(e)))
            return False
    
    def html_to_markdown(self, html_content: str, tag: str) -> str:
        """Convert HTML content back to Markdown."""
        # Strip HTML tags (simplified - in production use a proper HTML parser)
        content = re.sub(r'<[^>]+>', '', html_content)
        
        # Decode HTML entities
        content = content.replace('&lt;', '<')
        content = content.replace('&gt;', '>')
        content = content.replace('&amp;', '&')
        content = content.replace('&quot;', '"')
        content = content.replace('&#39;', "'")
        
        return content.strip()
    
    def apply_all_edits(self, edits_file: str) -> None:
        """Apply all edits from a file."""
        print(f"Loading edits from: {edits_file}")
        data = self.load_edits(edits_file)
        
        edits = data.get('edits', {})
        timestamp = data.get('timestamp', 'Unknown')
        
        print(f"Found {len(edits)} edits from {timestamp}")
        print("-" * 50)
        
        # Create backup directory
        backup_dir = Path(f"docs_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        backup_dir.mkdir(exist_ok=True)
        
        # Backup all files that will be modified
        modified_files = set()
        for edit_id in edits:
            try:
                path, _, _, _ = self.parse_edit_id(edit_id)
                file_path = self.find_file_from_path(path)
                if file_path.exists():
                    modified_files.add(file_path)
            except:
                pass
        
        # Create backups
        for file_path in modified_files:
            backup_path = backup_dir / file_path.relative_to(self.docs_dir)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            backup_path.write_text(file_path.read_text())
        
        print(f"Created backups in: {backup_dir}")
        print("-" * 50)
        
        # Apply edits
        for edit_id, content in edits.items():
            print(f"Applying edit: {edit_id[:50]}...")
            self.apply_edit(edit_id, content)
        
        # Summary
        print("-" * 50)
        print(f"Successfully applied: {len(self.applied_edits)} edits")
        if self.applied_edits:
            print("\nModified files:")
            for edit_id, file_path in self.applied_edits:
                print(f"  - {file_path}")
        
        if self.failed_edits:
            print(f"\nFailed to apply: {len(self.failed_edits)} edits")
            print("\nFailed edits:")
            for edit_id, reason in self.failed_edits:
                print(f"  - {edit_id[:50]}... ({reason})")
        
        print(f"\nBackups saved to: {backup_dir}")
        print("\nTo restore backups, run:")
        print(f"  cp -r {backup_dir}/* docs/")

def main():
    parser = argparse.ArgumentParser(description='Apply documentation edits from JSON export')
    parser.add_argument('edits_file', help='Path to the JSON edits file')
    parser.add_argument('--docs-dir', default='docs', help='Documentation directory (default: docs)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without applying')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.edits_file):
        print(f"Error: Edits file not found: {args.edits_file}")
        return 1
    
    applier = EditApplier(args.docs_dir)
    
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        data = applier.load_edits(args.edits_file)
        edits = data.get('edits', {})
        print(f"Would apply {len(edits)} edits:")
        for edit_id in edits:
            print(f"  - {edit_id}")
    else:
        applier.apply_all_edits(args.edits_file)
    
    return 0

if __name__ == '__main__':
    exit(main())