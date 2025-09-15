// Editor functionality for Acoustic Manufacturing System docs
// Enables inline editing of documentation content

document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const EDIT_MODE_KEY = 'docs-edit-mode';
    const EDITS_STORAGE_KEY = 'docs-edits';
    const API_ENDPOINT = '/api/save-edits'; // You'll need to set up this endpoint
    
    // State
    let editMode = localStorage.getItem(EDIT_MODE_KEY) === 'true';
    let unsavedEdits = JSON.parse(localStorage.getItem(EDITS_STORAGE_KEY) || '{}');
    
    // Add edit mode toggle button
    function addEditToggle() {
        const header = document.querySelector('.md-header__inner');
        if (!header) return;
        
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'edit-mode-toggle md-header__button md-icon';
        toggleBtn.innerHTML = editMode ? 
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5,3C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19H5V5H12V3H5M17.78,4C17.61,4 17.43,4.07 17.3,4.2L16.08,5.41L18.58,7.91L19.8,6.7C20.06,6.44 20.06,6 19.8,5.75L18.25,4.2C18.12,4.07 17.95,4 17.78,4M15.37,6.12L8,13.5V16H10.5L17.87,8.62L15.37,6.12Z"/></svg>' :
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"/></svg>';
        toggleBtn.title = editMode ? 'Exit Edit Mode' : 'Enter Edit Mode';
        toggleBtn.onclick = toggleEditMode;
        
        header.appendChild(toggleBtn);
        
        // Add save button if in edit mode
        if (editMode) {
            const saveBtn = document.createElement('button');
            saveBtn.className = 'save-edits-btn md-header__button md-icon';
            saveBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15,9H5V5H15M12,19A3,3 0 0,1 9,16A3,3 0 0,1 12,13A3,3 0 0,1 15,16A3,3 0 0,1 12,19M17,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V7L17,3Z"/></svg>';
            saveBtn.title = 'Save All Edits';
            saveBtn.onclick = saveAllEdits;
            header.appendChild(saveBtn);
        }
    }
    
    // Toggle edit mode
    function toggleEditMode() {
        editMode = !editMode;
        localStorage.setItem(EDIT_MODE_KEY, editMode);
        location.reload(); // Reload to apply changes
    }
    
    // Make content editable
    function makeEditable() {
        if (!editMode) return;
        
        // Select all editable content areas
        const editableSelectors = [
            '.md-content h1',
            '.md-content h2',
            '.md-content h3',
            '.md-content h4',
            '.md-content h5',
            '.md-content h6',
            '.md-content p',
            '.md-content li',
            '.md-content td',
            '.md-content .admonition-title',
            '.md-content .admonition p'
        ];
        
        editableSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(element => {
                // Skip if already processed or contains code
                if (element.getAttribute('contenteditable') || 
                    element.querySelector('code') || 
                    element.closest('.mermaid')) {
                    return;
                }
                
                // Make editable
                element.setAttribute('contenteditable', 'true');
                element.classList.add('editable-content');
                
                // Generate unique ID for tracking edits
                const id = generateElementId(element);
                element.setAttribute('data-edit-id', id);
                
                // Load saved edit if exists
                if (unsavedEdits[id]) {
                    element.innerHTML = unsavedEdits[id];
                    element.classList.add('has-unsaved-edit');
                }
                
                // Add event listeners
                element.addEventListener('input', handleEdit);
                element.addEventListener('focus', handleFocus);
                element.addEventListener('blur', handleBlur);
                element.addEventListener('paste', handlePaste);
            });
        });
        
        // Add edit mode indicator
        document.body.classList.add('edit-mode-active');
    }
    
    // Generate unique ID for element
    function generateElementId(element) {
        const page = window.location.pathname;
        const tagName = element.tagName.toLowerCase();
        const text = element.textContent.substring(0, 20).replace(/\s+/g, '-');
        const index = Array.from(element.parentNode.children).indexOf(element);
        return `${page}:${tagName}:${index}:${text}`;
    }
    
    // Handle content edit
    function handleEdit(event) {
        const element = event.target;
        const id = element.getAttribute('data-edit-id');
        const content = element.innerHTML;
        
        // Save to local storage
        unsavedEdits[id] = content;
        localStorage.setItem(EDITS_STORAGE_KEY, JSON.stringify(unsavedEdits));
        
        // Mark as edited
        element.classList.add('has-unsaved-edit');
        
        // Update save indicator
        updateSaveIndicator();
    }
    
    // Handle focus
    function handleFocus(event) {
        event.target.classList.add('editing');
    }
    
    // Handle blur
    function handleBlur(event) {
        event.target.classList.remove('editing');
    }
    
    // Handle paste - strip formatting
    function handlePaste(event) {
        event.preventDefault();
        const text = event.clipboardData.getData('text/plain');
        document.execCommand('insertText', false, text);
    }
    
    // Update save indicator
    function updateSaveIndicator() {
        const count = Object.keys(unsavedEdits).length;
        const saveBtn = document.querySelector('.save-edits-btn');
        if (saveBtn) {
            saveBtn.setAttribute('data-edit-count', count);
            saveBtn.title = `Save ${count} edit${count !== 1 ? 's' : ''}`;
        }
    }
    
    // Save all edits
    async function saveAllEdits() {
        if (Object.keys(unsavedEdits).length === 0) {
            showNotification('No edits to save', 'info');
            return;
        }
        
        // Show saving indicator
        const saveBtn = document.querySelector('.save-edits-btn');
        saveBtn.classList.add('saving');
        
        try {
            // In a real implementation, this would save to a backend
            // For now, we'll export as a JSON file
            const editsData = {
                timestamp: new Date().toISOString(),
                edits: unsavedEdits
            };
            
            // Create download link
            const blob = new Blob([JSON.stringify(editsData, null, 2)], 
                                 {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `docs-edits-${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            // Clear saved edits
            unsavedEdits = {};
            localStorage.removeItem(EDITS_STORAGE_KEY);
            
            // Update UI
            document.querySelectorAll('.has-unsaved-edit').forEach(el => {
                el.classList.remove('has-unsaved-edit');
            });
            
            showNotification('Edits exported successfully!', 'success');
        } catch (error) {
            showNotification('Failed to save edits', 'error');
            console.error('Save error:', error);
        } finally {
            saveBtn.classList.remove('saving');
            updateSaveIndicator();
        }
    }
    
    // Show notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `edit-notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Add keyboard shortcuts
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(event) {
            // Ctrl/Cmd + E to toggle edit mode
            if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
                event.preventDefault();
                toggleEditMode();
            }
            
            // Ctrl/Cmd + S to save in edit mode
            if (editMode && (event.ctrlKey || event.metaKey) && event.key === 's') {
                event.preventDefault();
                saveAllEdits();
            }
        });
    }
    
    // Initialize
    addEditToggle();
    makeEditable();
    addKeyboardShortcuts();
    updateSaveIndicator();
    
    // Show edit mode notification
    if (editMode) {
        setTimeout(() => {
            showNotification('Edit mode is active. Click any text to edit.', 'info');
        }, 500);
    }
});

// Export functionality for integration
window.DocsEditor = {
    toggleEditMode: function() {
        const event = new Event('toggle-edit-mode');
        document.dispatchEvent(event);
    },
    saveEdits: function() {
        const event = new Event('save-edits');
        document.dispatchEvent(event);
    },
    getEdits: function() {
        return JSON.parse(localStorage.getItem('docs-edits') || '{}');
    }
};