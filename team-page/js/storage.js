// Local storage handling for team data persistence

const STORAGE_KEY = 'dripTeamData';
const CONTACT_KEY = 'dripContactData';
const UI_STATE_KEY = 'dripUIState';

// Save field data
function saveField(input) {
    const role = input.dataset.role;
    const field = input.dataset.field;
    const value = input.value.trim();
    
    // Update visual state
    if (value) {
        input.classList.add('filled');
    } else {
        input.classList.remove('filled');
    }
    
    // Show saving indicator
    input.classList.add('saving');
    
    // Get existing data
    const data = getTeamData();
    
    // Initialize role if not exists
    if (!data.roles[role]) {
        data.roles[role] = {};
    }
    
    // Update field
    data.roles[role][field] = value;
    data.lastUpdated = new Date().toISOString();
    
    // Save to localStorage
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    
    // Update progress
    updateProgress();
    
    // Update last saved time
    updateLastSaved();
    
    // Remove saving indicator
    setTimeout(() => {
        input.classList.remove('saving');
    }, 500);
}

// Save contact field
function saveContact(input) {
    const field = input.dataset.contact;
    const value = input.value.trim();
    
    // Update visual state
    if (value) {
        input.classList.add('filled');
    } else {
        input.classList.remove('filled');
    }
    
    // Show saving indicator
    input.classList.add('saving');
    
    // Get existing contact data
    const data = getContactData();
    
    // Update field
    data[field] = value;
    data.lastUpdated = new Date().toISOString();
    
    // Save to localStorage
    localStorage.setItem(CONTACT_KEY, JSON.stringify(data));
    
    // Update last saved time
    updateLastSaved();
    
    // Remove saving indicator
    setTimeout(() => {
        input.classList.remove('saving');
    }, 500);
}

// Get team data from storage
function getTeamData() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
        try {
            return JSON.parse(stored);
        } catch (e) {
            console.error('Error parsing team data:', e);
        }
    }
    
    // Return default structure
    return {
        roles: {},
        lastUpdated: null
    };
}

// Get contact data from storage
function getContactData() {
    const stored = localStorage.getItem(CONTACT_KEY);
    if (stored) {
        try {
            return JSON.parse(stored);
        } catch (e) {
            console.error('Error parsing contact data:', e);
        }
    }
    
    return {};
}

// Load all data from storage
function loadTeamData() {
    // Load team roles
    const teamData = getTeamData();
    Object.keys(teamData.roles).forEach(role => {
        const roleData = teamData.roles[role];
        Object.keys(roleData).forEach(field => {
            const input = document.querySelector(`input[data-role="${role}"][data-field="${field}"]`);
            if (input) {
                input.value = roleData[field];
                if (roleData[field]) {
                    input.classList.add('filled');
                }
            }
        });
    });
    
    // Load contact data
    const contactData = getContactData();
    Object.keys(contactData).forEach(field => {
        if (field !== 'lastUpdated') {
            const input = document.querySelector(`input[data-contact="${field}"]`);
            if (input) {
                input.value = contactData[field];
                if (contactData[field]) {
                    input.classList.add('filled');
                }
            }
        }
    });
    
    // Load UI state
    loadUIState();
    
    // Update last saved time
    if (teamData.lastUpdated || contactData.lastUpdated) {
        const lastUpdate = new Date(teamData.lastUpdated || contactData.lastUpdated);
        updateLastSaved(lastUpdate);
    }
}

// Save card expansion state
function saveCardState(roleId, expanded) {
    const uiState = getUIState();
    if (!uiState.cards) {
        uiState.cards = {};
    }
    uiState.cards[roleId] = expanded;
    localStorage.setItem(UI_STATE_KEY, JSON.stringify(uiState));
}

// Save panel expansion state
function savePanelState(panelId, expanded) {
    const uiState = getUIState();
    if (!uiState.panels) {
        uiState.panels = {};
    }
    uiState.panels[panelId] = expanded;
    localStorage.setItem(UI_STATE_KEY, JSON.stringify(uiState));
}

// Get UI state
function getUIState() {
    const stored = localStorage.getItem(UI_STATE_KEY);
    if (stored) {
        try {
            return JSON.parse(stored);
        } catch (e) {
            console.error('Error parsing UI state:', e);
        }
    }
    return { cards: {}, panels: {} };
}

// Load UI state
function loadUIState() {
    const uiState = getUIState();
    
    // Restore card states
    if (uiState.cards) {
        Object.keys(uiState.cards).forEach(roleId => {
            if (uiState.cards[roleId]) {
                const card = document.querySelector(`[data-role="${roleId}"]`);
                if (card) {
                    card.classList.add('expanded');
                    const header = card.querySelector('.card-header');
                    header.setAttribute('aria-expanded', 'true');
                }
            }
        });
    }
    
    // Restore panel states
    if (uiState.panels) {
        Object.keys(uiState.panels).forEach(panelId => {
            if (uiState.panels[panelId]) {
                const panel = document.getElementById(panelId);
                if (panel) {
                    panel.classList.add('expanded');
                    const header = panel.querySelector('.panel-header');
                    header.setAttribute('aria-expanded', 'true');
                }
            }
        });
    }
}

// Update last saved display
function updateLastSaved(date) {
    const lastSavedSpan = document.getElementById('lastSaved');
    const now = date || new Date();
    const timeString = now.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    lastSavedSpan.textContent = timeString;
}

// Clear all data (for testing/reset)
function clearAllData() {
    if (confirm('Are you sure you want to clear all team data? This cannot be undone.')) {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(CONTACT_KEY);
        localStorage.removeItem(UI_STATE_KEY);
        location.reload();
    }
}

// Auto-save backup to prevent data loss
let autoSaveTimer;
function enableAutoSave() {
    // Save a backup every 5 minutes
    autoSaveTimer = setInterval(() => {
        const backup = {
            team: getTeamData(),
            contact: getContactData(),
            ui: getUIState(),
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('dripTeamBackup', JSON.stringify(backup));
    }, 5 * 60 * 1000);
}

// Restore from backup if needed
function checkForBackup() {
    const backup = localStorage.getItem('dripTeamBackup');
    if (backup && !localStorage.getItem(STORAGE_KEY)) {
        if (confirm('Previous session data found. Would you like to restore it?')) {
            try {
                const data = JSON.parse(backup);
                localStorage.setItem(STORAGE_KEY, JSON.stringify(data.team));
                localStorage.setItem(CONTACT_KEY, JSON.stringify(data.contact));
                localStorage.setItem(UI_STATE_KEY, JSON.stringify(data.ui));
                location.reload();
            } catch (e) {
                console.error('Error restoring backup:', e);
            }
        }
    }
}

// Initialize auto-save
enableAutoSave();
checkForBackup();