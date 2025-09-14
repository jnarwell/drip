// Custom JavaScript for Acoustic Manufacturing System docs

// Component search functionality
document.addEventListener('DOMContentLoaded', function() {
    // Component search box
    const searchBox = document.getElementById('component-search');
    const componentList = document.getElementById('component-list');
    
    if (searchBox && componentList) {
        const components = componentList.querySelectorAll('h3');
        
        searchBox.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            
            components.forEach(component => {
                const parent = component.parentElement;
                const text = component.textContent.toLowerCase();
                
                if (text.includes(searchTerm)) {
                    parent.classList.remove('hidden');
                } else {
                    parent.classList.add('hidden');
                }
            });
        });
    }
    
    // Add copy buttons to code blocks
    document.querySelectorAll('pre > code').forEach(function(codeBlock) {
        const button = document.createElement('button');
        button.className = 'md-clipboard md-icon';
        button.title = 'Copy to clipboard';
        button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"></path></svg>';
        
        button.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"></path></svg>';
                setTimeout(function() {
                    button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"></path></svg>';
                }, 2000);
            });
        });
        
        const pre = codeBlock.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading animation to mermaid diagrams
    document.querySelectorAll('.mermaid').forEach(diagram => {
        const loader = document.createElement('div');
        loader.className = 'mermaid-loader';
        loader.textContent = 'Loading diagram...';
        diagram.appendChild(loader);
    });
    
    // Enhanced table sorting (requires tablesort.js)
    if (typeof Tablesort !== 'undefined') {
        document.querySelectorAll('table').forEach(table => {
            new Tablesort(table);
        });
    }
});

// Dashboard auto-refresh (if on dashboard page)
if (window.location.pathname.includes('dashboard')) {
    // Refresh dashboard data every 5 minutes
    setInterval(function() {
        const lastUpdated = document.querySelector('*:contains("Dashboard updated:")');
        if (lastUpdated) {
            const now = new Date();
            lastUpdated.textContent = `Dashboard updated: ${now.toISOString()}`;
        }
    }, 300000);
}

// Print optimization
window.addEventListener('beforeprint', function() {
    // Expand all collapsed sections
    document.querySelectorAll('details').forEach(details => {
        details.setAttribute('open', '');
    });
    
    // Show all tabbed content
    document.querySelectorAll('.tabbed-set input').forEach(input => {
        if (input.checked) {
            input.parentElement.style.display = 'block';
        }
    });
});

// Component count animation
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    let current = start;
    
    const timer = setInterval(function() {
        current += increment;
        element.textContent = current;
        if (current === end) {
            clearInterval(timer);
        }
    }, stepTime);
}

// Animate metric values on dashboard
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('dashboard')) {
        document.querySelectorAll('.metric-value').forEach(element => {
            const value = parseInt(element.textContent.replace(/[^0-9]/g, ''));
            if (!isNaN(value)) {
                animateValue(element, 0, value, 1000);
            }
        });
    }
});