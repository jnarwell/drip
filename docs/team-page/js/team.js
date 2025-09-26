// Core team management functionality

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadTeamData();
    updateProgress();
    initializeEventListeners();
});

// Event listener initialization
function initializeEventListeners() {
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllCards();
        }
    });
    
    // Add focus trap for accessibility
    const cards = document.querySelectorAll('.role-card');
    cards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const roleId = this.dataset.role;
                toggleCard(roleId);
            }
        });
    });
}

// Toggle card expansion
function toggleCard(roleId) {
    const card = document.querySelector(`[data-role="${roleId}"]`);
    const isExpanded = card.classList.contains('expanded');
    
    // Close all other cards
    document.querySelectorAll('.role-card').forEach(c => {
        if (c !== card) {
            c.classList.remove('expanded');
        }
    });
    
    // Toggle current card
    card.classList.toggle('expanded');
    
    // Announce state change for screen readers
    const header = card.querySelector('.card-header');
    header.setAttribute('aria-expanded', !isExpanded);
    
    // Smooth scroll to card if expanding
    if (!isExpanded) {
        setTimeout(() => {
            card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }
    
    // Save state
    saveCardState(roleId, !isExpanded);
}

// Toggle info panel
function togglePanel(panelId) {
    const panel = document.getElementById(panelId);
    const isExpanded = panel.classList.contains('expanded');
    
    panel.classList.toggle('expanded');
    
    // Announce state change
    const header = panel.querySelector('.panel-header');
    header.setAttribute('aria-expanded', !isExpanded);
    
    // Save panel state
    savePanelState(panelId, !isExpanded);
}

// Close all cards
function closeAllCards() {
    document.querySelectorAll('.role-card').forEach(card => {
        card.classList.remove('expanded');
        const header = card.querySelector('.card-header');
        header.setAttribute('aria-expanded', 'false');
    });
}

// Filter roles based on search input
function filterRoles(searchTerm) {
    const term = searchTerm.toLowerCase();
    const cards = document.querySelectorAll('.role-card');
    let visibleCount = 0;
    
    cards.forEach(card => {
        const content = card.textContent.toLowerCase();
        if (content.includes(term) || term === '') {
            card.style.display = 'block';
            visibleCount++;
            // Highlight matching text
            if (term !== '') {
                highlightText(card, term);
            } else {
                removeHighlights(card);
            }
        } else {
            card.style.display = 'none';
        }
    });
    
    // Update results count
    updateSearchResults(visibleCount, searchTerm);
}

// Highlight matching text
function highlightText(element, term) {
    // This is a simplified version - in production, use a more robust solution
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
        if (node.parentElement.tagName !== 'SCRIPT' && 
            node.parentElement.tagName !== 'STYLE' &&
            !node.parentElement.classList.contains('highlight')) {
            textNodes.push(node);
        }
    }
    
    textNodes.forEach(textNode => {
        const text = textNode.textContent;
        const regex = new RegExp(`(${term})`, 'gi');
        if (regex.test(text)) {
            const span = document.createElement('span');
            span.innerHTML = text.replace(regex, '<mark class="highlight">$1</mark>');
            textNode.parentElement.replaceChild(span, textNode);
        }
    });
}

// Remove highlights
function removeHighlights(element) {
    const highlights = element.querySelectorAll('.highlight');
    highlights.forEach(highlight => {
        const parent = highlight.parentElement;
        parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
        parent.normalize();
    });
}

// Update search results display
function updateSearchResults(count, term) {
    // Could add a results counter if desired
    if (term && count === 0) {
        showNoResults();
    } else {
        hideNoResults();
    }
}

// Show no results message
function showNoResults() {
    let noResults = document.getElementById('noResults');
    if (!noResults) {
        noResults = document.createElement('div');
        noResults.id = 'noResults';
        noResults.className = 'no-results';
        noResults.textContent = 'No matching roles found. Try a different search term.';
        document.querySelector('.role-cards').appendChild(noResults);
    }
}

// Hide no results message
function hideNoResults() {
    const noResults = document.getElementById('noResults');
    if (noResults) {
        noResults.remove();
    }
}

// Update progress bar
function updateProgress() {
    const inputs = document.querySelectorAll('.status-field input[data-field="name"]');
    let filledCount = 0;
    
    inputs.forEach(input => {
        if (input.value.trim()) {
            filledCount++;
        }
    });
    
    const percentage = (filledCount / inputs.length) * 100;
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('filledPositions');
    
    progressFill.style.width = percentage + '%';
    progressText.textContent = filledCount;
    
    // Add celebration animation if all positions filled
    if (filledCount === inputs.length && filledCount > 0) {
        progressFill.style.backgroundColor = 'var(--success-color)';
        celebrateCompletion();
    }
}

// Celebrate when all positions are filled
function celebrateCompletion() {
    // Simple celebration effect
    const progressSection = document.querySelector('.progress-section');
    progressSection.classList.add('celebrate');
    
    setTimeout(() => {
        progressSection.classList.remove('celebrate');
    }, 2000);
}

// Add celebration animation to CSS
const style = document.createElement('style');
style.textContent = `
    .celebrate {
        animation: celebrate 2s ease;
    }
    
    @keyframes celebrate {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .no-results {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        font-style: italic;
    }
`;
document.head.appendChild(style);