# Documentation Editing Guide

This documentation includes an interactive editing feature that allows authorized users to make changes directly in the browser.

## Enabling Edit Mode

### Method 1: Keyboard Shortcut
Press ++ctrl+e++ (or ++cmd+e++ on Mac) to toggle edit mode on/off.

### Method 2: Edit Button
Click the edit icon in the header toolbar to toggle edit mode.

!!! info "Edit Mode Indicator"
    When edit mode is active, you'll see:
    
    - An "EDIT MODE" badge in the top-right corner
    - Editable content highlighted on hover
    - A save button in the header showing the number of unsaved edits

## Making Edits

1. **Enable edit mode** using one of the methods above
2. **Click any text** to start editing:
   - Headers (H1-H6)
   - Paragraphs
   - List items
   - Table cells
   - Admonition content

3. **Type your changes** directly in the browser
4. **Click outside** the element to finish editing

!!! tip "Editing Tips"
    - Press ++esc++ to cancel editing the current element
    - Press ++tab++ to move to the next editable element
    - Use ++ctrl+z++ to undo changes within an element

## Saving Edits

### Export Edits
Click the save button in the header (or press ++ctrl+s++) to download your edits as a JSON file.

### Apply Edits to Source Files
To apply your edits back to the source markdown files:

```bash
# Download the edits JSON file from the browser
# Then run:
python apply_edits.py docs-edits-[timestamp].json

# For a dry run (preview changes without applying):
python apply_edits.py docs-edits-[timestamp].json --dry-run
```

!!! warning "Important Notes"
    - Edits are stored locally in your browser until exported
    - Clearing browser data will lose unsaved edits
    - Complex formatting may need manual adjustment after applying
    - Always review changes before committing to version control

## Visual Indicators

| Indicator | Meaning |
|-----------|---------|
| Blue outline on hover | Content is editable |
| Blue shadow when focused | Currently editing |
| Red asterisk (*) | Unsaved changes |
| Number badge on save button | Count of unsaved edits |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| ++ctrl+e++ | Toggle edit mode |
| ++ctrl+s++ | Save all edits |
| ++esc++ | Cancel current edit |
| ++tab++ | Next editable element |
| ++shift+tab++ | Previous editable element |

## Limitations

The editor currently supports:

- ✅ Plain text editing
- ✅ Basic formatting preservation
- ✅ Local storage of edits
- ✅ Export/import functionality

Not yet supported:

- ❌ Rich text formatting (bold, italic, etc.)
- ❌ Adding new sections
- ❌ Editing code blocks
- ❌ Editing Mermaid diagrams
- ❌ Real-time collaboration

## Troubleshooting

### Edits Not Appearing
1. Ensure edit mode is enabled
2. Check if the element is editable (hover should show blue outline)
3. Try refreshing the page

### Lost Edits
- Edits are saved in browser local storage
- Use the same browser to recover unsaved edits
- Export regularly to prevent data loss

### Apply Script Errors
- Ensure the docs directory structure hasn't changed
- Check that the JSON file is valid
- Review failed edits in the script output

## Best Practices

1. **Export frequently** to avoid losing work
2. **Review changes** before applying to source files
3. **Test locally** before pushing to production
4. **Keep backups** - the apply script creates automatic backups
5. **Coordinate with team** to avoid conflicting edits

---

*The edit feature is designed for quick content updates. For structural changes or complex formatting, edit the source markdown files directly.*