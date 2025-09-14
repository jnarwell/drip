# Contributing Guide

## How to Contribute

We welcome contributions to the Acoustic Manufacturing System documentation! This guide explains how to contribute effectively.

## Getting Started

### Prerequisites
- Git knowledge
- Python 3.8+
- Markdown familiarity
- GitHub account

### Setup
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/drip.git
   cd drip/acoustic-sysml-v2
   ```
3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Contribution Types

### Documentation Improvements
- Fix typos or errors
- Improve clarity
- Add examples
- Update outdated information

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Test additions

### Component Updates
- Add new components
- Update specifications
- Correct costs
- Add suppliers

## Code Style Guide

### Python Code
- Follow PEP 8
- Use type hints
- Document all functions
- Write unit tests

Example:
```python
def calculate_wavelength(frequency: float, speed: float = 343) -> float:
    """
    Calculate acoustic wavelength.
    
    Args:
        frequency: Frequency in Hz
        speed: Sound speed in m/s (default: air at 20°C)
        
    Returns:
        Wavelength in meters
    """
    return speed / frequency
```

### Markdown Style
- Use ATX headers (`#`)
- Limit lines to 100 characters
- Use fenced code blocks
- Include alt text for images

## Documentation Standards

### File Naming
- Use lowercase
- Separate words with hyphens
- Be descriptive but concise
- Include file extension

Good: `thermal-analysis.md`
Bad: `ThermalAnalysis.MD`

### Content Structure
1. **Clear title**
2. **Brief overview**
3. **Detailed sections**
4. **Examples/diagrams**
5. **References**

### Writing Style
- Active voice
- Present tense
- Concise sentences
- Technical accuracy

## Testing

### Before Submitting
1. **Run tests**:
   ```bash
   python test_icd_system.py
   ```

2. **Check documentation**:
   ```bash
   python generate_mkdocs.py
   mkdocs serve
   ```

3. **Validate interfaces**:
   ```bash
   python -m models.interfaces.interface_validator
   ```

### Documentation Tests
- Links work
- Code examples run
- Images display
- Tables format correctly

## Submission Process

### Pull Request Guidelines
1. **Title**: Clear and descriptive
2. **Description**: What and why
3. **Testing**: What was tested
4. **Screenshots**: If applicable

Template:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests pass
- [ ] Documentation builds
- [ ] No warnings

## Screenshots
(if applicable)
```

### Review Process
1. Automated checks run
2. Maintainer reviews
3. Feedback addressed
4. Changes merged

## Component Registry Updates

### Adding Components
```python
new_component = Component(
    name="Component Name",
    category=ComponentCategory.ACOUSTIC,
    type=ComponentType.COTS,
    specification="Part number",
    quantity=1,
    unit_cost=100.00,
    total_cost=100.00,
    supplier="Supplier Name",
    tech_specs=TechnicalSpecs(
        power_consumption=10,
        weight=0.5,
        operating_temp=(0, 50)
    )
)
```

### Updating ICDs
1. Modify `interface_registry.py`
2. Update requirements
3. Regenerate documentation
4. Validate changes

## Common Tasks

### Update Power Budget
1. Edit component power specs
2. Run power calculator
3. Update documentation
4. Verify totals

### Add Test Procedure
1. Create procedure in `verification/procedures/`
2. Update test matrix
3. Link from verification page
4. Add to nav menu

### Fix Documentation Error
1. Find file in `docs/`
2. Make correction
3. Test locally
4. Submit PR

## Communication

### Questions
- GitHub Issues for bugs
- Discussions for questions
- Email for private matters

### Reporting Issues
Include:
- Clear title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details

### Feature Requests
- Use GitHub Issues
- Label as "enhancement"
- Describe use case
- Propose solution

## Code of Conduct

### Our Standards
- Respectful communication
- Constructive feedback
- Inclusive environment
- Professional behavior

### Unacceptable Behavior
- Harassment
- Discrimination
- Trolling
- Spam

## Recognition

Contributors are recognized in:
- Git history
- CONTRIBUTORS.md
- Release notes
- Documentation credits

## Resources

### Helpful Links
- [Markdown Guide](https://www.markdownguide.org/)
- [Python Style Guide](https://pep8.org/)
- [Git Tutorial](https://git-scm.com/tutorial)
- [MkDocs Documentation](https://www.mkdocs.org/)

### Tools
- [VS Code](https://code.visualstudio.com/) - Recommended editor
- [Python extensions](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Markdown preview](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)

Thank you for contributing to the Acoustic Manufacturing System! 🎉
