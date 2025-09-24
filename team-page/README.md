# DRIP Team Structure Page

A professional team organization webpage for the DRIP (Drop Resonance Induction Printing) acoustic manufacturing system project at Stanford.

## Features

- **Interactive Role Cards**: Click to expand/collapse detailed information for each team role
- **Auto-save**: All entered data is automatically saved to browser local storage
- **Progress Tracking**: Visual progress bar shows team completion status
- **Search Functionality**: Filter roles by keywords
- **Export Options**: Export team data as text, JSON, or PDF
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Print-friendly**: Optimized print stylesheet for documentation
- **Keyboard Navigation**: Full keyboard accessibility support

## Usage

1. **Open the page**: Open `index.html` in a web browser
2. **Fill positions**: Click on input fields to add team member information
3. **Expand cards**: Click role headers to see detailed responsibilities
4. **Search**: Use the search bar to filter roles by keywords
5. **Export data**: Click Export button to save team data
6. **Print**: Click Print button for a clean printed version

## Keyboard Shortcuts

- `Escape`: Close all expanded cards
- `Ctrl/Cmd + E`: Export team data
- `Ctrl/Cmd + S`: Copy team summary to clipboard
- `Enter/Space`: Toggle card expansion when focused

## File Structure

```
team-page/
├── index.html          # Main HTML page
├── css/
│   ├── main.css       # Core styles
│   ├── responsive.css # Mobile/tablet styles
│   └── print.css      # Print-specific styles
├── js/
│   ├── team.js        # Core functionality
│   ├── storage.js     # Local storage handling
│   └── export.js      # Export functionality
└── assets/            # Images and icons (to be added)
```

## Team Roles

1. **Mechanical/Systems Lead**: System architecture, CAD, testing
2. **Thermal/Materials Engineer**: Thermal design, materials, crucible
3. **Power/Electronics Engineer**: Power systems, PCBs, safety
4. **Acoustics/Control Engineer**: Acoustic modeling, FPGA, software
5. **UX/Industrial Designer**: Industrial design, UI/UX, documentation

## Technologies Used

- Vanilla JavaScript (no frameworks required)
- CSS Grid and Flexbox for layout
- Local Storage API for data persistence
- Print CSS for documentation
- Semantic HTML for accessibility

## Browser Support

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support

## Deployment

Simply host the files on any web server or open locally. No build process required.

For GitHub Pages:
1. Push to repository
2. Enable GitHub Pages in settings
3. Access at: `https://[username].github.io/[repo-name]/team-page/`

## Data Privacy

All team member data is stored locally in the browser. No data is sent to any server.