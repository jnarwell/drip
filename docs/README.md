# Acoustic Manufacturing System Documentation

This directory contains the source files for the MkDocs documentation site.

## Quick Start

1. **Setup**: Run `./setup_docs.sh` to install dependencies and generate docs
2. **Test**: Run `./serve_docs.sh` to view documentation locally
3. **Deploy**: Run `./deploy_docs.sh` to deploy to GitHub Pages

## Structure

```
docs/
├── index.md            # Home page
├── dashboard.md        # Interactive dashboard
├── quick-start.md      # Getting started guide
├── components/         # Component documentation
├── icds/              # Interface Control Documents
├── system/            # System architecture and requirements
├── analysis/          # Analysis reports
├── verification/      # Test procedures and reports
└── resources/         # Additional resources
```

## Key Features

- **Auto-generated content** from component registry
- **Interactive dashboard** with system metrics
- **Searchable component database**
- **Mobile-responsive design**
- **Dark/light theme toggle**
- **Automatic deployment** via GitHub Actions

## Maintenance

- Run `python generate_mkdocs.py` to regenerate documentation
- Documentation is automatically deployed on push to main branch
- Custom styling in `stylesheets/extra.css`
- Interactive features in `javascripts/extra.js`