// Export functionality for team data

// Export team data in various formats
function exportTeamData() {
    const format = prompt('Export format: "pdf", "text", or "json"?', 'text');
    
    if (!format) return;
    
    switch(format.toLowerCase()) {
        case 'pdf':
            exportAsPDF();
            break;
        case 'json':
            exportAsJSON();
            break;
        case 'text':
        default:
            exportAsText();
            break;
    }
}

// Export as formatted text
function exportAsText() {
    const teamData = getTeamData();
    const contactData = getContactData();
    const date = new Date().toLocaleDateString();
    
    let output = `DRIP TEAM STRUCTURE - EXPORTED ${date}\n`;
    output += '═'.repeat(50) + '\n\n';
    
    // Add filled positions
    output += 'TEAM MEMBERS\n';
    output += '─'.repeat(30) + '\n\n';
    
    const roles = [
        { id: 'mech-lead', name: 'Mechanical/Systems Lead' },
        { id: 'thermal-lead', name: 'Thermal/Materials Engineer' },
        { id: 'power-lead', name: 'Power/Electronics Engineer' },
        { id: 'acoustics-lead', name: 'Acoustics/Control Engineer' },
        { id: 'cs-math-lead', name: 'Computer Science/Mathematics Engineer' }
    ];
    
    let filledCount = 0;
    roles.forEach(role => {
        const data = teamData.roles[role.id];
        if (data && data.name) {
            filledCount++;
            output += `${role.name}\n`;
            output += `  Name:  ${data.name}\n`;
            output += `  Email: ${data.email || 'Not provided'}\n`;
            output += `  Phone: ${data.phone || 'Not provided'}\n\n`;
        }
    });
    
    // Add unfilled positions
    output += '\nOPEN POSITIONS\n';
    output += '─'.repeat(30) + '\n\n';
    
    roles.forEach(role => {
        const data = teamData.roles[role.id];
        if (!data || !data.name) {
            output += `• ${role.name}\n`;
        }
    });
    
    // Add contact information
    output += '\n\nCONTACT INFORMATION\n';
    output += '─'.repeat(30) + '\n\n';
    
    if (contactData['lead-name']) {
        output += 'Project Lead\n';
        output += `  Name:   ${contactData['lead-name']}\n`;
        output += `  Email:  ${contactData['lead-email'] || 'Not provided'}\n`;
        output += `  Phone:  ${contactData['lead-phone'] || 'Not provided'}\n`;
        output += `  Office: ${contactData['lead-office'] || 'Not provided'}\n\n`;
    }
    
    output += 'Faculty Advisors\n';
    output += `  Acoustics:      ${contactData['advisor-acoustics'] || 'TBD'}\n`;
    output += `  Thermal:        ${contactData['advisor-thermal'] || 'TBD'}\n`;
    output += `  Manufacturing:  ${contactData['advisor-manufacturing'] || 'TBD'}\n\n`;
    
    output += 'Lab Coordinators\n';
    output += `  PRL Contact: ${contactData['lab-prl'] || 'TBD'}\n`;
    output += `  EE Shop:     ${contactData['lab-ee'] || 'TBD'}\n`;
    output += `  ME Testing:  ${contactData['lab-me'] || 'TBD'}\n\n`;
    
    // Add summary
    output += '\n' + '═'.repeat(50) + '\n';
    output += `Summary: ${filledCount} of 5 positions filled\n`;
    
    // Download file
    downloadFile('DRIP_Team_Structure.txt', output, 'text/plain');
}

// Export as JSON
function exportAsJSON() {
    const exportData = {
        exportDate: new Date().toISOString(),
        teamData: getTeamData(),
        contactData: getContactData(),
        metadata: {
            version: '1.0',
            system: 'DRIP Team Structure',
            totalPositions: 5
        }
    };
    
    const json = JSON.stringify(exportData, null, 2);
    downloadFile('DRIP_Team_Data.json', json, 'application/json');
}

// Export as PDF (simplified version using print)
function exportAsPDF() {
    // Store current state
    const currentPrintState = document.body.classList.contains('print-mode');
    
    // Add print mode class for better formatting
    document.body.classList.add('print-mode');
    
    // Expand all cards and panels for printing
    document.querySelectorAll('.role-card').forEach(card => {
        card.classList.add('expanded');
    });
    document.querySelectorAll('.info-panel').forEach(panel => {
        panel.classList.add('expanded');
    });
    
    // Trigger print dialog
    setTimeout(() => {
        window.print();
        
        // Restore previous state after print
        setTimeout(() => {
            if (!currentPrintState) {
                document.body.classList.remove('print-mode');
            }
            // Restore expansion states from saved UI state
            loadUIState();
        }, 100);
    }, 100);
}

// Download file helper
function downloadFile(filename, content, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    
    // Clean up
    setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }, 100);
}

// Generate team summary for quick sharing
function generateSummary() {
    const teamData = getTeamData();
    const filledPositions = [];
    const openPositions = [];
    
    const roles = [
        { id: 'mech-lead', name: 'Mechanical/Systems Lead' },
        { id: 'thermal-lead', name: 'Thermal/Materials Engineer' },
        { id: 'power-lead', name: 'Power/Electronics Engineer' },
        { id: 'acoustics-lead', name: 'Acoustics/Control Engineer' },
        { id: 'cs-math-lead', name: 'Computer Science/Mathematics Engineer' }
    ];
    
    roles.forEach(role => {
        const data = teamData.roles[role.id];
        if (data && data.name) {
            filledPositions.push(`${role.name}: ${data.name}`);
        } else {
            openPositions.push(role.name);
        }
    });
    
    let summary = `DRIP Team Status (${filledPositions.length}/5 filled)\n\n`;
    
    if (filledPositions.length > 0) {
        summary += 'Current Team:\n';
        filledPositions.forEach(pos => {
            summary += `✓ ${pos}\n`;
        });
    }
    
    if (openPositions.length > 0) {
        summary += '\nOpen Positions:\n';
        openPositions.forEach(pos => {
            summary += `• ${pos}\n`;
        });
    }
    
    return summary;
}

// Copy summary to clipboard
function copySummaryToClipboard() {
    const summary = generateSummary();
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(summary).then(() => {
            showNotification('Team summary copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy:', err);
            fallbackCopyToClipboard(summary);
        });
    } else {
        fallbackCopyToClipboard(summary);
    }
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showNotification('Team summary copied to clipboard!');
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showNotification('Failed to copy summary', 'error');
    }
    
    document.body.removeChild(textArea);
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'var(--success-color)' : 'var(--warning-color)'};
        color: white;
        border-radius: 4px;
        box-shadow: var(--shadow-md);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add animation styles
const exportStyles = document.createElement('style');
exportStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .print-mode .search-section,
    .print-mode .header-actions {
        display: none !important;
    }
`;
document.head.appendChild(exportStyles);

// Add keyboard shortcut for export
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + E for export
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        exportTeamData();
    }
    
    // Ctrl/Cmd + S for summary copy
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        copySummaryToClipboard();
    }
});