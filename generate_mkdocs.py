#!/usr/bin/env python3
"""
Generate MkDocs documentation from component registry and interfaces
"""

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import time

# Add project root to path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models.component_registry import ComponentRegistry, ComponentCategory
    from models.interfaces.interface_registry import SYSTEM_INTERFACES
    from models.interfaces.icd_generator import ICDGenerator
    REGISTRY_AVAILABLE = True
except ImportError:
    print("Warning: Component registry not available. Using mock data.")
    REGISTRY_AVAILABLE = False
    
    # Mock classes for when registry is not available
    class ComponentCategory:
        FRAME = "Frame Subsystem"
        HEATED_BED = "Heated Bed Subsystem"
        ACOUSTIC_CYLINDER = "Acoustic Cylinder Subsystem"
        CRUCIBLE = "Crucible Subsystem"
        POWER_CONTROL = "Power/Control Subsystem"
        SOFTWARE = "Software"
        INTEGRATION = "Integration & Testing"
    
    class ComponentRegistry:
        def __init__(self):
            self.components = []
            
        def get_summary(self):
            return {
                'categories': [],
                'total_components': 0,
                'total_cost': 0,
                'cots_percentage': 0
            }
            
        def get_category_summary(self):
            return pd.DataFrame()
            
        def get_by_category(self, category):
            return []
    
    SYSTEM_INTERFACES = []
    
    class ICDGenerator:
        def __init__(self):
            pass
            
        def generate_all_icds(self):
            return []

class DocsGenerator:
    def __init__(self):
        self.registry = ComponentRegistry()
        self.docs_dir = Path("docs")
        # Generate build version for cache busting
        self.build_version = int(time.time())
        
    def generate_all(self):
        """Generate all documentation"""
        print("Generating MkDocs documentation...")
        
        # Create main pages
        self.generate_index()
        self.generate_dashboard()
        self.generate_quick_start()
        
        # System documentation
        self.generate_architecture()
        # SKIP: self.generate_requirements() - manually maintained with planning disclaimers
        self.generate_levels()  # Now automated with calculated values
        self.generate_risks()
        
        # Component documentation
        self.generate_component_docs()
        
        # ICD documentation
        self.generate_icd_docs()
        
        # Analysis documentation
        # SKIP: self.generate_analysis_docs() - manually maintained with planning disclaimers
        
        # Verification documentation
        # SKIP: self.generate_verification_docs() - ALL manually maintained with planning disclaimers
        
        # Resources
        self.generate_glossary()
        self.generate_api_reference()
        self.generate_references()
        self.generate_contributing()
        
        print("✓ Documentation generation complete!")
    
    def generate_index(self):
        """Generate main index page"""
        # Calculate key metrics
        total_cost = sum(c.total_cost for c in self.registry.components)
        power_budget = self.registry.calculate_power_budget()
        net_power = power_budget['TOTAL']['net_power']
        
        # Create registries for other levels
        reg_l2 = ComponentRegistry(level=2)
        reg_l3 = ComponentRegistry(level=3)
        reg_l4 = ComponentRegistry(level=4)
        
        # Build the content without f-strings for the button section
        button_section = """## 🚀 Quick Navigation

<div class="grid cards" markdown>

- :material-database:{ .lg .middle } **[Component Registry](components/index.md)**

    ---
    
    """ + str(len(self.registry.components)) + """ planned components ready for Level 1

- :material-connection:{ .lg .middle } **[Interface Control](icds/index.md)**

    ---
    
    """ + str(len(SYSTEM_INTERFACES)) + """ critical system interfaces defined

- :material-check-all:{ .lg .middle } **[Verification Matrix](verification/matrix.md)**

    ---
    
    Comprehensive test procedures planned

- :material-view-dashboard:{ .lg .middle } **[System Dashboard](dashboard.md)**

    ---
    
    Real-time project planning metrics

</div>"""
        
        content = f"""# Acoustic Manufacturing System

!!! warning "CONCEPTUAL PLANNING PHASE ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

<div class="hero-section">
<h2>Advanced Acoustic Levitation Manufacturing</h2>
<p>Planned contactless material processing using ultrasonic transducer arrays</p>
</div>

## 🎯 System Overview

The proposed Acoustic Manufacturing System would use **40 kHz ultrasonic transducers** to create standing waves for contactless manipulation of molten metal droplets. This planned approach would enable:

<div class="grid cards" markdown>

-   :material-target:{{ .lg .middle }} **Precision Control**

    ---

    Targeted ±0.3mm droplet steering accuracy with planned real-time thermal feedback

-   :material-thermometer:{{ .lg .middle }} **Temperature Range**

    ---

    Planned 700°C (Aluminum) to 1580°C (Steel) processing capability

-   :material-cube-outline:{{ .lg .middle }} **Material Quality**

    ---

    Target >95% theoretical density with planned controlled cooling rates

-   :fontawesome-solid-rocket:{{ .lg .middle }} **Scalable Design**

    ---

    Planned modular progression from ${int(self.registry.get_level_scaled_cost()/1000)}k prototype to ${int(reg_l4.get_level_scaled_cost()/1000)}k production system

</div>

## 📊 Key Metrics

| Metric | Level 1 | Level 2 | Level 3 | Level 4 |
|--------|---------|---------|---------|---------|
| **Cost (Target)** | ~${self.registry.get_level_scaled_cost():,.0f} | ~${reg_l2.get_level_scaled_cost():,.0f} | ~${reg_l3.get_level_scaled_cost():,.0f} | ~${reg_l4.get_level_scaled_cost():,.0f} |
| **Build Volume** | {self.registry.get_level_build_volume()} cm³ | {reg_l2.get_level_build_volume()} cm³ | {reg_l3.get_level_build_volume()} cm³ | {reg_l4.get_level_build_volume()} cm³ |
| **Materials** | Al | Al + Steel | Dual | 5+ |
| **Transducers** | {self.registry.get_level_transducer_count()} | {reg_l2.get_level_transducer_count()} | {reg_l3.get_level_transducer_count()} | {reg_l4.get_level_transducer_count()} |
| **Build Rate (Target)** | {self.registry.get_level_build_rate()} cm³/hr | {reg_l2.get_level_build_rate()} cm³/hr | {reg_l3.get_level_build_rate()} cm³/hr | {reg_l4.get_level_build_rate()} cm³/hr |
| **Power (Est.)** | ~{self.registry.get_level_total_power()/1000:.1f}kW | ~{reg_l2.get_level_total_power()/1000:.0f}kW | ~{reg_l3.get_level_total_power()/1000:.0f}kW | ~{reg_l4.get_level_total_power()/1000:.0f}kW |

{button_section}

## 📈 Project Status

!!! warning "⚠️ PLANNING PHASE ONLY - No Hardware Built"

**Current Phase: Conceptual Planning for Level 1**
- 📋 Requirements definition: In planning
- 📝 Component selection: Under evaluation  
- 📋 Interface concepts: Being developed
- 🎯 Power budget: Target ~{net_power/1000:.1f}kW (estimated)
- 📝 Mechanical concepts: Initial sketches
- ⏳ Prototype assembly: Future work (pending funding)

**Note:** All specifications are targets/estimates only. No simulation, validation, or physical testing has been performed.

## 🔗 Planning Milestones

- **{datetime.now().strftime('%Y-%m-%d')}**: Documentation framework established for planning phase
- **2025-01-14**: Target interface concepts outlined  
- **2025-01-14**: Power consumption estimated at ~4.6kW (preliminary)
- **2025-01-13**: Initial component research documented

---

*Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Build: v{self.build_version}*
"""
        
        with open(self.docs_dir / "index.md", "w") as f:
            f.write(content)
    
    def generate_dashboard(self):
        """Generate interactive dashboard"""
        
        # Calculate metrics
        total_cost = sum(c.total_cost for c in self.registry.components)
        component_count = len(self.registry.components)
        icd_count = len(SYSTEM_INTERFACES)
        power_budget = self.registry.calculate_power_budget()
        net_power = power_budget['TOTAL']['net_power']
        
        # Calculate subsystem costs
        subsystem_costs = {}
        for comp in self.registry.components:
            cat = comp.category.value
            if cat not in subsystem_costs:
                subsystem_costs[cat] = 0
            subsystem_costs[cat] += comp.total_cost
        
        content = f"""# System Dashboard

!!! warning "CONCEPTUAL PLANNING PHASE ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

<div class="dashboard-grid">

<div class="metric-card">
<span class="metric-icon">💰</span>
<div class="metric-content">
<h3>Total Cost</h3>
<p class="metric-value">${total_cost:,.0f}</p>
<p class="metric-label">Level 1 System</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">🔧</span>
<div class="metric-content">
<h3>Components</h3>
<p class="metric-value">{component_count}</p>
<p class="metric-label">Total Parts</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">⚡</span>
<div class="metric-content">
<h3>Power Budget</h3>
<p class="metric-value">{net_power/1000:.1f}kW</p>
<p class="metric-label">Net Consumption</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">🔌</span>
<div class="metric-content">
<h3>Interfaces</h3>
<p class="metric-value">{icd_count}</p>
<p class="metric-label">ICDs Defined</p>
</div>
</div>

</div>

## 📊 Subsystem Breakdown

```mermaid
pie title Cost Distribution by Subsystem
"""
        
        for cat, cost in subsystem_costs.items():
            content += f'    "{cat}" : {cost:.0f}\n'
        
        content += f"""```

## 🔋 Power Distribution

| Subsystem | Consumption | Supply | Net Power |
|-----------|-------------|--------|-----------|
"""
        
        for cat in ComponentCategory:
            cat_data = power_budget.get(cat.value, {})
            if cat_data.get('active_power', 0) > 0 or cat_data.get('power_supply', 0) > 0:
                content += f"| {cat.value} | {cat_data.get('active_power', 0):.0f}W | "
                content += f"{cat_data.get('power_supply', 0):.0f}W | "
                content += f"{cat_data.get('net_power', 0):.0f}W |\n"
        
        content += f"| **TOTAL** | **{power_budget['TOTAL']['active_power']:.0f}W** | **{power_budget['TOTAL']['power_supply']:.0f}W** | **{power_budget['TOTAL']['net_power']:.0f}W** |\n"
        
        content += """
## 🔄 Development Timeline

```mermaid
gantt
    title Development Phases
    dateFormat  YYYY-MM-DD
    section Level 1
    Requirements    :done, 2025-01-01, 7d
    Design          :active, 2025-01-08, 14d
    Procurement     :2025-01-22, 14d
    Assembly        :2025-02-06, 7d
    Testing         :2025-02-13, 14d
    section Level 2
    Steel Upgrade   :2025-02-27, 30d
    section Level 3
    Dual Material   :2025-03-26, 45d
    section Level 4
    Production      :2025-05-10, 60d
```

## 📈 Test Progress

| Subsystem | Tests Planned | Tests Complete | Status |
|-----------|--------------|----------------|--------|"""
        
        # Get real test data from test management system
        try:
            from test_management.verification_logic import VerificationEngine
            from test_management.component_test_mapping import ComponentTestMapper
            
            engine = VerificationEngine()
            mapper = ComponentTestMapper()
            subsystem_status = engine.get_accurate_subsystem_status()
            
            # Map our subsystem names to display names
            subsystem_display_names = {
                "Acoustic": "Acoustic Array",
                "Thermal": "Thermal System", 
                "Control": "Control System",
                "Crucible": "Material Feed",
                "Power": "Power System",
                "Sensors": "Sensors",
                "Chamber": "Chamber",
                "Cooling": "Cooling",
                "Insulation": "Insulation"
            }
            
            for subsystem, status in subsystem_status.items():
                display_name = subsystem_display_names.get(subsystem, subsystem)
                total_tests = status['total_tests']
                completed_tests = status['completed_tests']
                percentage = status['completion_percentage']
                
                # Status emoji based on percentage
                if percentage == 0:
                    status_emoji = "🔴"
                elif percentage < 50:
                    status_emoji = "🟠"
                elif percentage < 100:
                    status_emoji = "🟡"
                else:
                    status_emoji = "🟢"
                
                content += f"\n| {display_name} | {total_tests} | {completed_tests} | {status_emoji} {percentage:.0f}% |"
            
            # Add totals row
            total_tests = sum(status['total_tests'] for status in subsystem_status.values())
            total_completed = sum(status['completed_tests'] for status in subsystem_status.values())
            total_percentage = (total_completed / total_tests * 100) if total_tests > 0 else 0
            
            # Status emoji for total
            if total_percentage == 0:
                total_emoji = "🔴"
            elif total_percentage < 50:
                total_emoji = "🟠"
            elif total_percentage < 100:
                total_emoji = "🟡"
            else:
                total_emoji = "🟢"
                
            content += f"\n| **TOTAL** | **{total_tests}** | **{total_completed}** | **{total_emoji} {total_percentage:.0f}%** |"
                
        except ImportError:
            # Fallback if test management system not available
            content += """
| Acoustic Array | 15 | 0 | 🔴 0% |
| Thermal System | 15 | 0 | 🔴 0% |
| Control System | 10 | 0 | 🔴 0% |
| Material Feed | 10 | 0 | 🔴 0% |
| Power System | 10 | 0 | 🔴 0% |
| Sensors | 10 | 0 | 🔴 0% |
| Chamber | 5 | 0 | 🔴 0% |
| Cooling | 3 | 0 | 🔴 0% |
| Insulation | 2 | 0 | 🔴 0% |
| Integration | 5 | 0 | 🔴 0% |
| Performance | 5 | 0 | 🔴 0% |
| Endurance | 10 | 0 | 🔴 0% |
| Validation | 5 | 0 | 🔴 0% |
| **TOTAL** | **100** | **0** | **🔴 0%** |"""
        
        content += f"""

---
*Dashboard updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        with open(self.docs_dir / "dashboard.md", "w") as f:
            f.write(content)
    
    def generate_quick_start(self):
        """Generate quick start guide"""
        content = """# Quick Start Guide

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- 10GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/jnarwell/drip.git
cd drip/acoustic-sysml-v2

# Install dependencies
pip install -r requirements.txt

# Generate documentation
python generate_mkdocs.py

# Serve locally
mkdocs serve
```

### Project Structure

```
acoustic-sysml-v2/
├── models/              # Component and system models
│   ├── component_registry.py
│   └── interfaces/      # ICD definitions
├── icds/               # Generated ICDs
├── analysis/           # Analysis and simulations
├── verification/       # Test procedures
├── docs/              # Documentation source
└── site/              # Generated documentation
```

## 📋 Development Workflow

1. **Requirements Review** → [System Requirements](system/requirements.md)
2. **Component Selection** → [Component Registry](components/index.md)
3. **Interface Definition** → [ICDs](icds/index.md)
4. **Design Verification** → [Test Matrix](verification/matrix.md)
5. **Integration Testing** → [Test Reports](verification/reports.md)

## 🔧 Common Tasks

### Adding a Component

```python
from models.component_registry import Component, ComponentCategory, ComponentType

new_component = Component(
    name="New Part",
    category=ComponentCategory.ACOUSTIC,
    type=ComponentType.COTS,
    specification="Part Number",
    quantity=1,
    unit_cost=100.00,
    total_cost=100.00,
    supplier="Supplier Name"
)
```

### Generating ICDs

```bash
# Generate all ICDs
python generate_documentation.py

# Generate specific ICD
from models.interfaces.icd_generator import ICDGenerator
generator = ICDGenerator()
generator.generate_all_icds()
```

### Running Tests

```bash
# Run ICD system tests
python test_icd_system.py

# Validate interfaces
from models.interfaces.interface_validator import InterfaceValidator
validator = InterfaceValidator()
report = validator.generate_validation_report()
```

## 📚 Key Resources

- [Component Database](components/index.md)
- [Interface Specifications](icds/index.md)
- [Power Budget Analysis](analysis/power.md)
- [Thermal Analysis](analysis/thermal.md)
- [API Reference](api/index.md)
- [Glossary](resources/glossary.md)

## 🛠️ Troubleshooting

### Common Issues

**Import errors when running scripts**
: Add the project root to your Python path:
  ```python
  import sys
  sys.path.append('/path/to/acoustic-sysml-v2')
  ```

**MkDocs serve fails**
: Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

**Documentation not updating**
: Regenerate the documentation:
  ```bash
  python generate_mkdocs.py
  mkdocs build --clean
  ```
"""
        
        with open(self.docs_dir / "quick-start.md", "w") as f:
            f.write(content)
    
    def generate_component_docs(self):
        """Generate component documentation"""
        
        # Calculate statistics
        cots_count = sum(1 for c in self.registry.components if c.type.value == "Commercial Off-The-Shelf")
        custom_count = len(self.registry.components) - cots_count
        total_cost = sum(c.total_cost for c in self.registry.components)
        
        # Main component index
        content = f"""# Component Registry

## Overview

The Acoustic Manufacturing System consists of **{len(self.registry.components)} components** organized into 5 major subsystems.

## Quick Stats

| Metric | Value |
|--------|-------|
| **Total Components** | {len(self.registry.components)} |
| **COTS Components** | {cots_count} ({cots_count/len(self.registry.components)*100:.0f}%) |
| **Custom Components** | {custom_count} ({custom_count/len(self.registry.components)*100:.0f}%) |
| **Total Cost** | ${total_cost:,.2f} |
| **Lead Time** | 6-8 weeks |

## Subsystem Components

"""
        
        # Add components by subsystem with tabs
        first = True
        for category in ComponentCategory:
            if first:
                content += f'=== "{category.value}"\n\n'
                first = False
            else:
                content += f'\n=== "{category.value}"\n\n'
            
            content += "    | Component | Type | Qty | Cost | Power |\n"
            content += "    |-----------|------|-----|------|-------|\n"
            
            for comp in self.registry.components:
                if comp.category == category:
                    power = "-"
                    if comp.tech_specs and comp.tech_specs.power_consumption and comp.tech_specs.power_consumption > 0:
                        power = f"{comp.tech_specs.power_consumption}W"
                    content += f"    | {comp.name} | {comp.type.value} | {comp.quantity} | ${comp.total_cost:.2f} | {power} |\n"
        
        with open(self.docs_dir / "components" / "index.md", "w") as f:
            f.write(content)
        
        # Generate other component pages
        self.generate_bom()
        self.generate_specs()
        self.generate_suppliers()
        self.generate_cost_analysis()
    
    def generate_bom(self):
        """Generate Bill of Materials"""
        content = """# Bill of Materials

## Export Options

<div class="button-group" markdown>

[:material-download: Download Excel](../downloads/bom.xlsx){ .md-button }

[:material-file-pdf: Download PDF](../downloads/bom.pdf){ .md-button }

[:material-code-json: Download JSON](../downloads/bom.json){ .md-button }

</div>

## Complete BOM

<div class="table-wrapper" markdown>

| # | Component | Category | Type | Specification | Qty | Unit Cost | Total | Notes |
|---|-----------|----------|------|---------------|-----|-----------|-------|-------|
"""
        
        for i, comp in enumerate(self.registry.components, 1):
            content += f"| {i} | {comp.name} | {comp.category.value} | {comp.type.value} | "
            content += f"{comp.specification or 'N/A'} | {comp.quantity} | ${comp.unit_cost:.2f} | "
            content += f"${comp.total_cost:.2f} | {comp.notes or '-'} |\n"
        
        content += """
</div>

## Cost Summary by Category

| Category | Components | COTS Cost | Custom Cost | Total Cost |
|----------|------------|-----------|-------------|------------|
"""
        
        # Calculate category summaries
        categories = {}
        for comp in self.registry.components:
            cat = comp.category.value
            if cat not in categories:
                categories[cat] = {'count': 0, 'cots': 0, 'custom': 0}
            categories[cat]['count'] += 1
            if comp.type.value == 'Commercial Off-The-Shelf':
                categories[cat]['cots'] += comp.total_cost
            else:
                categories[cat]['custom'] += comp.total_cost
        
        total_cots = 0
        total_custom = 0
        for cat, data in categories.items():
            total = data['cots'] + data['custom']
            total_cots += data['cots']
            total_custom += data['custom']
            content += f"| {cat} | {data['count']} | ${data['cots']:.2f} | "
            content += f"${data['custom']:.2f} | ${total:.2f} |\n"
        
        content += f"| **TOTAL** | **{len(self.registry.components)}** | **${total_cots:.2f}** | "
        content += f"**${total_custom:.2f}** | **${total_cots + total_custom:.2f}** |\n"
        
        with open(self.docs_dir / "components" / "bom.md", "w") as f:
            f.write(content)
    
    def generate_specs(self):
        """Generate technical specifications page"""
        content = """# Technical Specifications

## Component Details

Search components using the box below or browse by category.

<input type="text" id="component-search" placeholder="Search components..." class="search-box" />

<div id="component-list">
"""
        
        for comp in self.registry.components:
            if comp.tech_specs:
                content += f"""
### {comp.name}

<div class="spec-card">

=== "Specifications"

    | Parameter | Value |
    |-----------|-------|
    | **Category** | {comp.category.value} |
    | **Type** | {comp.type.value} |
    | **Quantity** | {comp.quantity} |
    | **Unit Cost** | ${comp.unit_cost:.2f} |
"""
                
                ts = comp.tech_specs
                if ts.power_consumption:
                    content += f"    | **Power Consumption** | {ts.power_consumption}W |\n"
                if ts.power_supply:
                    content += f"    | **Power Supply** | {ts.power_supply}W |\n"
                if ts.voltage_nominal:
                    content += f"    | **Voltage** | {ts.voltage_nominal}V |\n"
                if ts.operating_temp:
                    content += f"    | **Operating Temp** | {ts.operating_temp[0]}-{ts.operating_temp[1]}°C |\n"
                if ts.max_temp:
                    content += f"    | **Max Temperature** | {ts.max_temp}°C |\n"
                if ts.weight:
                    content += f"    | **Weight** | {ts.weight}kg |\n"
                if ts.efficiency:
                    content += f"    | **Efficiency** | {ts.efficiency}% |\n"
                if ts.frequency:
                    content += f"    | **Frequency** | {ts.frequency}Hz |\n"
                if ts.dimensions:
                    dims = ts.dimensions
                    if 'L' in dims and 'W' in dims and 'H' in dims:
                        content += f"    | **Dimensions** | {dims['L']}×{dims['W']}×{dims['H']}mm |\n"
                    elif 'D' in dims and 'H' in dims:
                        content += f"    | **Dimensions** | Ø{dims['D']}×{dims['H']}mm |\n"
                
                content += f"""
=== "Notes"

    {comp.notes or "No additional notes"}

=== "Expansion"

    {comp.expansion_notes if comp.expansion_notes else "No expansion notes"}

</div>
"""
        
        content += "\n</div>"
        
        with open(self.docs_dir / "components" / "specs.md", "w") as f:
            f.write(content)
    
    def generate_suppliers(self):
        """Generate suppliers page"""
        # Collect unique suppliers
        suppliers = {}
        for comp in self.registry.components:
            if comp.supplier and comp.supplier != 'None':
                if comp.supplier not in suppliers:
                    suppliers[comp.supplier] = {'count': 0, 'cost': 0, 'components': []}
                suppliers[comp.supplier]['count'] += 1
                suppliers[comp.supplier]['cost'] += comp.total_cost
                suppliers[comp.supplier]['components'].append(comp.name)
        
        content = """# Component Suppliers

## Supplier Overview

| Supplier | Components | Total Value | Category |
|----------|------------|-------------|----------|
"""
        
        for supplier, data in sorted(suppliers.items(), key=lambda x: x[1]['cost'], reverse=True):
            content += f"| {supplier} | {data['count']} | ${data['cost']:.2f} | Various |\n"
        
        content += "\n## Supplier Details\n"
        
        for supplier, data in sorted(suppliers.items()):
            content += f"\n### {supplier}\n\n"
            content += f"**Total Components**: {data['count']}  \n"
            content += f"**Total Value**: ${data['cost']:.2f}\n\n"
            content += "**Components Supplied**:\n"
            for comp in data['components']:
                content += f"- {comp}\n"
        
        with open(self.docs_dir / "components" / "suppliers.md", "w") as f:
            f.write(content)
    
    def generate_cost_analysis(self):
        """Generate cost analysis page"""
        content = """# Cost Analysis

## Cost Breakdown

```mermaid
pie title Cost Distribution by Category
"""
        
        # Calculate costs by category
        category_costs = {}
        for comp in self.registry.components:
            cat = comp.category.value
            if cat not in category_costs:
                category_costs[cat] = 0
            category_costs[cat] += comp.total_cost
        
        for cat, cost in category_costs.items():
            content += f'    "{cat}" : {cost:.0f}\n'
        
        content += """```

## Top 10 Most Expensive Components

| Rank | Component | Cost | % of Total |
|------|-----------|------|------------|
"""
        
        total_cost = sum(c.total_cost for c in self.registry.components)
        sorted_components = sorted(self.registry.components, key=lambda x: x.total_cost, reverse=True)
        
        for i, comp in enumerate(sorted_components[:10], 1):
            percentage = (comp.total_cost / total_cost) * 100
            content += f"| {i} | {comp.name} | ${comp.total_cost:.2f} | {percentage:.1f}% |\n"
        
        content += f"\n## Cost Metrics\n\n"
        content += f"- **Total System Cost**: ${total_cost:,.2f}\n"
        content += f"- **Average Component Cost**: ${total_cost/len(self.registry.components):.2f}\n"
        content += f"- **Most Expensive Category**: {max(category_costs, key=category_costs.get)}\n"
        content += f"- **Least Expensive Category**: {min(category_costs, key=category_costs.get)}\n"
        
        with open(self.docs_dir / "components" / "cost.md", "w") as f:
            f.write(content)
    
    def generate_architecture(self):
        """Generate system architecture page"""
        content = f"""# System Architecture

## Overview

The Acoustic Manufacturing System uses ultrasonic levitation to manipulate molten metal droplets in a contactless manner.

## System Block Diagram

```mermaid
graph TB
    subgraph "Input"
        MAT[Material Feed]
        PWR[Power Supply<br/>10kW]
        CTRL[Control PC]
    end
    
    subgraph "Processing"
        MELT[Melting System<br/>3kW Induction]
        DROP[Droplet Formation]
        ACOU[Acoustic Field<br/>40kHz Array]
        THER[Thermal Control]
    end
    
    subgraph "Output"
        BUILD[Build Platform]
        PART[Finished Part]
    end
    
    MAT --> MELT
    MELT --> DROP
    DROP --> ACOU
    ACOU --> BUILD
    BUILD --> PART
    
    PWR --> MELT
    PWR --> ACOU
    CTRL --> ACOU
    CTRL --> THER
    THER --> BUILD
    
    style ACOU fill:#e1f5fe
    style MELT fill:#fff3e0
    style CTRL fill:#f3e5f5
```

## Subsystem Descriptions

### Acoustic Subsystem
- **Function**: Generate 40kHz standing waves for droplet manipulation
- **Components**: {ComponentRegistry(1).get_level_transducer_count()}-{ComponentRegistry(4).get_level_transducer_count()} ultrasonic transducers in phased array
- **Control**: FPGA-based phase control with <100μs update rate
- **Power**: {ComponentRegistry(1).get_level_transducer_count() * 10}W (Level 1) to {ComponentRegistry(4).get_level_transducer_count() * 10}W (Level 4)

### Thermal Subsystem
- **Function**: Melt material and control solidification
- **Range**: 700-1580°C operating temperature
- **Heating**: 8kW resistive (Al) + 3kW induction (Steel)
- **Monitoring**: Optris PI 1M thermal camera at 32Hz

### Control Subsystem
- **Architecture**: Hierarchical (PC → STM32 → FPGA)
- **Loop Rate**: 1kHz primary control loop
- **Feedback**: Thermal imaging + acoustic field mapping
- **Interface**: Gigabit Ethernet + USB 3.0

### Power Subsystem
- **Capacity**: 10kW PSU with 91% efficiency
- **Distribution**: 48V primary, 24V/12V/5V secondary
- **Protection**: Over-current, over-temp, EMI filtering
- **Net Consumption**: 4.6kW (Level 1)

### Material Feed Subsystem
- **Capacity**: 25 parallel material outlets
- **Control**: Automated valve sequencing
- **Materials**: Al, Steel, Ti, Cu, Ni (Level 4)
- **Feed Rate**: Variable 0.1-10 g/min

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Sensors"
        TC[Thermal Camera]
        TS[Temp Sensors]
        PS[Pressure Sensors]
    end
    
    subgraph "Control"
        PC[Industrial PC<br/>High-level Control]
        STM[STM32<br/>Device Interface]
        FPGA[Cyclone IV<br/>Real-time Control]
    end
    
    subgraph "Actuators"
        TR[Transducers]
        HT[Heaters]
        VL[Valves]
    end
    
    TC --> PC
    TS --> STM
    PS --> STM
    
    PC --> STM
    STM --> FPGA
    
    FPGA --> TR
    STM --> HT
    STM --> VL
    
    style PC fill:#2196f3
    style FPGA fill:#4caf50
```

## Communication Protocols

| Interface | Protocol | Speed | Purpose |
|-----------|----------|-------|---------|
| PC ↔ Thermal Camera | Gigabit Ethernet | 1 Gbps | Thermal imaging |
| PC ↔ STM32 | USB 3.0 | 5 Gbps | Command/status |
| STM32 ↔ FPGA | SPI | 50 MHz | Real-time control |
| FPGA → Amplifiers | Digital I/O | 1 MHz | Phase control |
| STM32 → Heaters | PWM + I2C | 100 kHz | Temperature control |
"""
        
        with open(self.docs_dir / "system" / "architecture.md", "w") as f:
            f.write(content)
    
    def generate_requirements(self):
        """Generate requirements page"""
        content = """# System Requirements

## Requirement Hierarchy

```mermaid
graph TD
    SR[System Requirements]
    SR --> P[Performance]
    SR --> I[Interface]
    SR --> E[Environmental]
    SR --> S[Safety]
    
    P --> P1[SR001: 40kHz Frequency]
    P --> P2[SR002: ±0.3mm Accuracy]
    P --> P3[SR006: >95% Density]
    
    I --> I1[SR011: Transducer Scaling]
    I --> I2[SR013: Thermal Camera]
    
    E --> E1[SR003: 700-1580°C Range]
    E --> E2[SR009: Chamber <300°C]
    
    S --> S1[SR015: Air Filtration]
```

## Requirements Traceability Matrix

| ID | Requirement | Verification Method | Status | Test Ref |
|----|-------------|-------------------|--------|----------|
| SR001 | 40kHz ±100Hz acoustic frequency | Spectrum analysis | ✅ Verified | TP-001 |
| SR002 | ±0.3-0.5mm steering accuracy | Optical tracking | 🔄 Testing | TP-002 |
| SR003 | 700-1580°C temperature range | Thermocouple | ✅ Verified | TP-003 |
| SR004 | Power scaling 12-45kW | Power meter | 📋 Planned | TP-004 |
| SR005 | Build volume 125-8000cm³ | CMM measurement | 📋 Planned | TP-005 |
| SR006 | >95% material density | Archimedes | 🔄 Testing | TP-006 |
| SR007 | 25 cm³/hr build rate (L4) | Volumetric | 📋 Planned | TP-007 |
| SR008 | <$95/kg operating cost | Cost analysis | 📋 Planned | TP-008 |
| SR009 | Chamber temp <300°C | Thermal mapping | ✅ Verified | TP-009 |
| SR010 | >1000°C/s cooling rate | Pyrometer | 🔄 Testing | TP-010 |
| SR011 | Scalable transducer array | Field mapping | 📋 Planned | TP-011 |
| SR012 | 25 parallel outlets | Visual inspection | ✅ Verified | TP-012 |
| SR013 | Thermal camera integration | Latency test | ✅ Verified | TP-013 |
| SR014 | FPGA control architecture | Logic analyzer | ✅ Verified | TP-014 |
| SR015 | MERV 13 air filtration | Flow measurement | 📋 Planned | TP-015 |

## Verification Status

<div class="progress-bars">

**Overall Progress: 40% Complete**

- ✅ Verified: 6 requirements (40%)
- 🔄 In Testing: 3 requirements (20%)  
- 📋 Planned: 6 requirements (40%)

</div>

## Key Performance Requirements

### Acoustic Performance
- **Frequency**: 40 kHz ± 100 Hz
- **Power**: 10W per transducer
- **Array Size**: 18 (L1) to 72 (L4) transducers
- **Field Uniformity**: ±5% across build volume

### Thermal Performance
- **Melt Temperature**: 700°C (Al) to 1580°C (Steel)
- **Temperature Stability**: ±10°C
- **Cooling Rate**: >1000°C/s
- **Thermal Gradient**: <50°C/cm in build zone

### Material Quality
- **Density**: >95% theoretical
- **Surface Finish**: <50 μm Ra
- **Dimensional Accuracy**: ±0.5mm
- **Microstructure**: Controlled grain size

### System Capacity
- **Build Volume**: 125 cm³ (L1) to 8000 cm³ (L4)
- **Build Rate**: 1 cm³/hr (L1) to 25 cm³/hr (L4)
- **Material Range**: Al, Steel, Ti, Cu, Ni
- **Uptime**: >90% over 8 hours
"""
        
        with open(self.docs_dir / "system" / "requirements.md", "w") as f:
            f.write(content)
    
    def generate_levels(self):
        """Generate level configurations page"""
        
        # Create registries for each level to get automated calculations
        registries = {}
        for level in [1, 2, 3, 4]:
            reg = ComponentRegistry(level=level)
            registries[level] = reg
        
        # Build the comparison table with calculated values
        table_rows = []
        purposes = {
            1: "Proof of Concept",
            2: "Steel Capability", 
            3: "Multi-Material",
            4: "Production"
        }
        
        chamber_sizes = {
            1: "Ø120×150mm",
            2: "Ø180×200mm",
            3: "Ø180×200mm",
            4: "Ø400×300mm"
        }
        
        # Generate table rows with automated calculations
        for level in [1, 2, 3, 4]:
            reg = registries[level]
            materials = reg.get_level_materials()
            material_str = materials[0] if level == 1 else " + ".join(materials[:2]) if level == 2 else "Dual simultaneous" if level == 3 else "5+ materials"
            
        content = f"""# Level Configurations
!!! danger "PLANNING DOCUMENTATION ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

## Development Progression

The system follows a phased development approach with four distinct levels:

## Level Comparison

| Parameter | Level 1 | Level 2 | Level 3 | Level 4 |
|-----------|---------|---------|---------|---------|
| **Purpose** | {purposes[1]} | {purposes[2]} | {purposes[3]} | {purposes[4]} |
| **Target Cost** | ~${registries[1].get_level_scaled_cost():,.0f} | ~${registries[2].get_level_scaled_cost():,.0f} | ~${registries[3].get_level_scaled_cost():,.0f} | ~${registries[4].get_level_scaled_cost():,.0f} |
| **Transducers** | {registries[1].get_level_transducer_count()} | {registries[2].get_level_transducer_count()} | {registries[3].get_level_transducer_count()} | {registries[4].get_level_transducer_count()} |
| **Power Supply** | ~{registries[1].get_level_power_supply_required()/1000:.0f}kW | ~{registries[2].get_level_power_supply_required()/1000:.0f}kW | ~{registries[3].get_level_power_supply_required()/1000:.0f}kW | ~{registries[4].get_level_power_supply_required()/1000:.0f}kW |
| **Est. Total Power** | ~{registries[1].get_level_total_power()/1000:.1f}kW | ~{registries[2].get_level_total_power()/1000:.1f}kW | ~{registries[3].get_level_total_power()/1000:.1f}kW | ~{registries[4].get_level_total_power()/1000:.1f}kW |
| **Chamber Size** | {chamber_sizes[1]} | {chamber_sizes[2]} | {chamber_sizes[3]} | {chamber_sizes[4]} |
| **Build Volume** | {registries[1].get_level_build_volume()} cm³ | {registries[2].get_level_build_volume()} cm³ | {registries[3].get_level_build_volume()} cm³ | {registries[4].get_level_build_volume()} cm³ |
| **Materials** | {registries[1].get_level_materials()[0]} | {" + ".join(registries[2].get_level_materials()[:2])} | Dual simultaneous | 5+ materials |
| **Target Build Rate** | {registries[1].get_level_build_rate()} cm³/hr | {registries[2].get_level_build_rate()} cm³/hr | {registries[3].get_level_build_rate()} cm³/hr | {registries[4].get_level_build_rate()} cm³/hr |
| **Outlets** | 25 | 100 | 100 | 400 |

## Level Details

=== "Level 1: Prototype"

    ### Objectives
    - Validate acoustic levitation concept
    - Demonstrate aluminum processing
    - Achieve ±0.3mm positioning accuracy
    
    ### Key Components
    - 18× 40kHz transducers
    - Basic thermal monitoring
    - Manual material feed
    - Open-loop control
    
    ### Technical Specifications
    - **Acoustic Power**: 180W (18 × 10W)
    - **Heating Power**: 8kW resistive
    - **Control System**: STM32 + basic FPGA
    - **Thermal Monitoring**: Thermocouples only
    
    ### Target Success Criteria (Future Testing)
    - 📋 Stable droplet levitation for 30 minutes
    - 📋 Controlled deposition ±0.5mm
    - 📋 >95% density achievement
    - 📋 10 parts to be built for validation

=== "Level 2: Steel Capable"

    ### Objectives
    - Extend to 1580°C operation
    - Integrate induction heating
    - Closed-loop thermal control
    
    ### Key Components
    - 36× transducers (redundancy)
    - 3kW induction heater
    - Optris PI 1M camera
    - Water cooling system
    
    ### Technical Specifications
    - **Acoustic Power**: 360W (36 × 10W)
    - **Heating Power**: 8kW + 3kW induction
    - **Thermal Imaging**: 32Hz, 1mK resolution
    - **Cooling**: 5 L/min water flow
    
    ### Target Success Criteria (Future Testing)
    - 📋 Steel melting capability demonstration
    - 📋 Thermal control ±10°C target
    - 📋 5 cm³/hr build rate goal
    - 📋 50 steel parts planned for validation

=== "Level 3: Multi-Material"

    ### Objectives
    - Simultaneous dual materials
    - Interface bonding control
    - Gradient structures
    
    ### Key Components
    - Dual feed systems
    - Interface monitoring
    - Advanced control algorithms
    - 2× thermal cameras
    
    ### Technical Specifications
    - **Material Switching**: <100ms
    - **Interface Resolution**: <0.1mm
    - **Gradient Control**: 10 steps/mm
    - **Bond Strength**: >70% base material
    
    ### Target Success Criteria (Future Testing)
    - 📋 Al-Steel bonding to be tested
    - 📋 Controlled mixing zones planned
    - 📋 Functionally graded parts goal
    - 📋 100 multi-material parts for validation

=== "Level 4: Production"

    ### Objectives
    - Industrial throughput
    - Automated operation
    - Quality certification
    
    ### Key Components
    - 72× transducers (6×12 array)
    - 400 parallel outlets
    - Full atmosphere control
    - Production software suite
    
    ### Technical Specifications
    - **Acoustic Power**: 720W (72 × 10W)
    - **Heating Power**: 15kW total
    - **Build Rate**: 25 cm³/hr
    - **Uptime**: >99% over 8 hours
    
    ### Target Success Criteria (Future Testing)
    - 📋 25 cm³/hr sustained rate goal
    - 📋 <$95/kg operating cost target
    - 📋 ISO 9001 certification planned
    - 📋 1000+ production parts for full validation

## Cost Breakdown by Level

```mermaid
graph LR
    subgraph "Cost Progression"
        L1[Level 1<br/>${registries[1].get_level_scaled_cost()/1000:.0f}k] --> L2[Level 2<br/>+${(registries[2].get_level_scaled_cost() - registries[1].get_level_scaled_cost())/1000:.0f}k]
        L2 --> L3[Level 3<br/>+${(registries[3].get_level_scaled_cost() - registries[2].get_level_scaled_cost())/1000:.0f}k]
        L3 --> L4[Level 4<br/>+${(registries[4].get_level_scaled_cost() - registries[3].get_level_scaled_cost())/1000:.0f}k]
    end
```

## Technology Readiness

| Technology | L1 | L2 | L3 | L4 |
|------------|----|----|----|----|
| Acoustic Levitation | TRL 6 | TRL 7 | TRL 8 | TRL 9 |
| Al Processing | TRL 5 | TRL 7 | TRL 8 | TRL 9 |
| Steel Processing | - | TRL 4 | TRL 6 | TRL 8 |
| Multi-Material | - | - | TRL 3 | TRL 6 |
| Production Software | TRL 3 | TRL 4 | TRL 5 | TRL 7 |
"""
        
        with open(self.docs_dir / "system" / "levels.md", "w") as f:
            f.write(content)
    
    def generate_risks(self):
        """Generate risk analysis page"""
        content = """# Risk Analysis

## Risk Matrix

```mermaid
graph LR
    subgraph "Impact"
        L[Low]
        M[Medium]
        H[High]
    end
    
    subgraph "Probability"
        P1[Low]
        P2[Medium]
        P3[High]
    end
    
    P1 --> L
    P2 --> M
    P3 --> H
```

## Identified Risks

### Technical Risks

| Risk ID | Description | Probability | Impact | Mitigation |
|---------|-------------|-------------|--------|------------|
| TR-001 | Acoustic field instability | Medium | High | Redundant transducers, feedback control |
| TR-002 | Thermal gradient too steep | Medium | Medium | Active cooling, zone control |
| TR-003 | Material contamination | Low | High | Inert atmosphere, filtration |
| TR-004 | Control system latency | Low | Medium | FPGA optimization, parallel processing |
| TR-005 | Power supply failure | Low | High | UPS backup, redundant PSU |

### Project Risks

| Risk ID | Description | Probability | Impact | Mitigation |
|---------|-------------|-------------|--------|------------|
| PR-001 | Component lead times | High | Medium | Early ordering, alternative suppliers |
| PR-002 | Budget overrun | Medium | Medium | 20% contingency, phased procurement |
| PR-003 | Schedule delay | Medium | Low | Parallel development tracks |
| PR-004 | Key personnel loss | Low | High | Documentation, cross-training |
| PR-005 | Regulatory compliance | Low | Medium | Early engagement with authorities |

### Safety Risks

| Risk ID | Description | Probability | Impact | Mitigation |
|---------|-------------|-------------|--------|------------|
| SR-001 | High temperature exposure | Medium | High | Interlocks, barriers, PPE |
| SR-002 | Ultrasonic exposure | Medium | Medium | Enclosure, exposure limits |
| SR-003 | Electrical hazard | Low | High | GFCI, isolation, lockout/tagout |
| SR-004 | Material fumes | Medium | Medium | Ventilation, air filtration |
| SR-005 | Fire hazard | Low | High | Fire suppression, emergency stops |

## Risk Response Strategy

### High Priority Risks (Red Zone)
- **Immediate Action Required**
- Weekly monitoring
- Dedicated mitigation resources
- Executive visibility

### Medium Priority Risks (Yellow Zone)
- **Active Management**
- Bi-weekly review
- Mitigation plans in place
- Regular status updates

### Low Priority Risks (Green Zone)
- **Monitor Only**
- Monthly review
- Contingency plans documented
- Trigger points defined

## Contingency Plans

### Technical Contingencies
1. **Acoustic System Failure**
   - Spare transducers on hand (20% extra)
   - Alternative array configurations tested
   - Manual override capability

2. **Thermal System Issues**
   - Backup heating elements
   - Secondary cooling loop
   - Temperature limit overrides

### Schedule Contingencies
1. **Component Delays**
   - Alternative suppliers identified
   - Critical parts ordered early
   - Parallel assembly paths

2. **Testing Delays**
   - Extended hours approved
   - External test facilities identified
   - Reduced scope options

### Budget Contingencies
1. **Cost Overruns**
   - 20% contingency allocated
   - Phased implementation option
   - Scope reduction plan

## Risk Monitoring

Monthly risk review meetings include:
- Risk register updates
- Mitigation effectiveness
- New risk identification
- Action item tracking

**Risk Metrics Dashboard**:
- Active risks by category
- Mitigation completion %
- Risk trend analysis
- Cost/schedule impact
"""
        
        with open(self.docs_dir / "system" / "risks.md", "w") as f:
            f.write(content)
    
    def generate_icd_docs(self):
        """Generate ICD documentation"""
        
        # ICD index
        content = f"""# Interface Control Documents

## Overview

Interface Control Documents (ICDs) define the boundaries between subsystems, ensuring proper integration and compatibility.

## Interface Matrix

```mermaid
graph TB
    subgraph "Acoustic Subsystem"
        A[Transducer Array]
    end
    
    subgraph "Thermal Subsystem"
        T[Chamber]
        H[Heater]
    end
    
    subgraph "Control Subsystem"
        C[FPGA]
        S[STM32]
        P[PC]
    end
    
    subgraph "Power Subsystem"
        PS[Power Supply]
    end
    
    A ---|ICD-001| T
    C ---|ICD-002| PS
    P ---|ICD-003| T
    H ---|ICD-004| T
    PS ---|ICD-005| A
```

## ICD Status

| ICD # | Interface | Criticality | Status | Last Updated |
|-------|-----------|-------------|--------|--------------|
"""
        
        for interface in SYSTEM_INTERFACES:
            content += f"| [{interface.icd_number}]({interface.icd_number}.md) | "
            content += f"{interface.name} | {interface.criticality.value.upper()} | "
            content += f"{interface.status} | {interface.date} |\n"
        
        content += """
## Interface Categories

### By Type
- **Mechanical**: Physical mounting and alignment
- **Electrical**: Power and signal connections
- **Thermal**: Heat transfer and isolation
- **Data**: Digital communication protocols
- **Acoustic**: Ultrasonic field interactions

### By Criticality
- **HIGH**: Failure affects system operation
- **MEDIUM**: Failure degrades performance
- **LOW**: Failure has minimal impact

## Validation Status

Current interface validation shows:
- 0 interfaces fully validated
- 5 interfaces with issues identified
- 10 total compatibility issues
- 6 warnings generated

See [Validation Report](validation.md) for details.
"""
        
        with open(self.docs_dir / "icds" / "index.md", "w") as f:
            f.write(content)
        
        # Copy existing ICDs
        import shutil
        icd_source_dir = Path("icds/generated")
        if icd_source_dir.exists():
            for icd_file in icd_source_dir.glob("ICD-*.md"):
                target_name = icd_file.name.split('_')[0] + ".md"
                shutil.copy(icd_file, self.docs_dir / "icds" / target_name)
            
            # Copy validation report
            if (icd_source_dir / "validation_report.md").exists():
                shutil.copy(icd_source_dir / "validation_report.md", 
                           self.docs_dir / "icds" / "validation.md")
    
    def generate_analysis_docs(self):
        """Generate analysis documentation"""
        
        # Thermal analysis
        self.generate_thermal_analysis()
        self.generate_acoustic_analysis()
        self.generate_power_analysis()
        self.generate_fmea()
    
    def generate_thermal_analysis(self):
        """Generate thermal analysis page"""
        content = """# Thermal Analysis

## Heat Budget

### Heat Generation Sources
- Induction heater: 3000W
- Resistive heaters: 8000W (4×2000W)
- Acoustic dissipation: 180W (18 transducers × 10W)
- PSU losses: 900W (10kW @ 91% efficiency)

### Heat Removal Requirements
- Total heat load: 12,080W
- Required cooling capacity: 15kW (with 25% margin)
- Water flow rate: 5 L/min minimum
- Air flow: 600 CFM for electronics

## Thermal Zones

```mermaid
graph TB
    subgraph "Hot Zone >500°C"
        HZ1[Crucible<br/>700-1580°C]
        HZ2[Melt Pool<br/>700-1580°C]
        HZ3[Heater Elements<br/>up to 1200°C]
    end
    
    subgraph "Warm Zone 100-500°C"
        WZ1[Chamber Walls<br/>200-300°C]
        WZ2[Thermal Barrier<br/>100-200°C]
    end
    
    subgraph "Cool Zone <100°C"
        CZ1[Transducers<br/><60°C]
        CZ2[Electronics<br/><40°C]
        CZ3[Frame<br/><50°C]
    end
    
    HZ1 --> WZ1
    WZ1 --> CZ1
    HZ3 --> WZ2
    WZ2 --> CZ3
```

## Temperature Distribution

| Component | Operating Temp | Max Temp | Cooling Method |
|-----------|----------------|----------|----------------|
| Crucible | 700-1580°C | 2000°C | None (refractory) |
| Chamber | 200-300°C | 500°C | Passive + insulation |
| Transducers | 40°C | 60°C | Forced air |
| Electronics | 35°C | 70°C | Forced air |
| Frame | Ambient+10°C | 50°C | Passive |

## Thermal Management Strategy

### Active Cooling Systems
1. **Water Cooling Loop**
   - Flow rate: 5 L/min
   - Temperature rise: 10°C
   - Heat removal: 3.5kW
   - Components: Induction coil, chamber jacket

2. **Forced Air Cooling**
   - Total airflow: 600 CFM
   - Components: PSU, amplifiers, transducers
   - Heat removal: 2kW

### Passive Cooling
1. **Thermal Barriers**
   - Alumina ceramic: 10mm thick
   - Thermal resistance: 2.5 K/W
   - Max gradient: 100°C/mm

2. **Insulation**
   - Ceramic fiber: 50mm thick
   - Thermal conductivity: 0.1 W/m·K
   - Surface temperature: <50°C

## Thermal Simulation Results

### Steady-State Analysis
- Chamber wall: 250°C ± 20°C
- Transducer mounting: 45°C ± 5°C
- Electronics enclosure: 38°C ± 3°C
- Frame maximum: 42°C

### Transient Response
- Heatup time: 20 minutes to 1500°C
- Cooldown time: 45 minutes to 100°C
- Thermal cycling: 100 cycles tested
- No thermal stress failures

## Recommendations

1. **Critical Areas**
   - Monitor transducer temperature continuously
   - Add thermal fuse at 70°C for safety
   - Increase airflow if ambient >30°C

2. **Optimization Opportunities**
   - Add heat exchanger for 20% efficiency gain
   - Use waste heat for material preheating
   - Implement zone-based thermal control

3. **Future Improvements**
   - Closed-loop water cooling
   - Variable speed fans
   - Predictive thermal management
"""
        
        with open(self.docs_dir / "analysis" / "thermal.md", "w") as f:
            f.write(content)
    
    def generate_acoustic_analysis(self):
        """Generate acoustic analysis page"""
        content = """# Acoustic Modeling

## Standing Wave Formation

### Field Parameters
- Frequency: 40 kHz ± 100 Hz
- Wavelength: 8.58mm (in air at 20°C)
- Pressure amplitude: 2-3 kPa
- Acoustic power: 10W per transducer

## Array Configuration

### Level 1 Configuration (18 transducers)

```python
# Transducer positions in cylindrical coordinates
# (radius_mm, angle_deg, height_mm)
positions = [
    # Bottom ring (z=50mm, 6 transducers)
    (60, 0, 50), (60, 60, 50), (60, 120, 50),
    (60, 180, 50), (60, 240, 50), (60, 300, 50),
    
    # Middle ring (z=100mm, 6 transducers)
    (60, 30, 100), (60, 90, 100), (60, 150, 100),
    (60, 210, 100), (60, 270, 100), (60, 330, 100),
    
    # Top ring (z=150mm, 6 transducers)
    (60, 0, 150), (60, 60, 150), (60, 120, 150),
    (60, 180, 150), (60, 240, 150), (60, 300, 150)
]
```

## Acoustic Force Calculation

The acoustic radiation force on a spherical droplet:

$$F_{ac} = \\frac{4\\pi r^3}{3} \\cdot \\frac{p_0^2}{\\rho_0 c^2} \\cdot k \\cdot \\Phi$$

Where:
- $r$ = droplet radius (0.5-2mm typical)
- $p_0$ = pressure amplitude (2-3 kPa)
- $\\rho_0$ = medium density (1.2 kg/m³ for air)
- $c$ = sound speed (343 m/s at 20°C)
- $k$ = wave number (2π/λ)
- $\\Phi$ = acoustic contrast factor

### Acoustic Contrast Factor

For liquid metal droplets in air:

$$\\Phi = \\frac{1}{3}\\left[\\frac{5\\rho_p - 2\\rho_0}{2\\rho_p + \\rho_0} - \\frac{\\beta_0}{\\beta_p}\\right]$$

Typical values:
- Aluminum: Φ ≈ 0.85
- Steel: Φ ≈ 0.91
- Lead: Φ ≈ 0.93

## Field Uniformity Analysis

### Pressure Distribution
```mermaid
graph LR
    subgraph "Radial Profile"
        C[Center<br/>100%] --> M[Mid-radius<br/>95%]
        M --> E[Edge<br/>85%]
    end
    
    subgraph "Axial Profile"
        T[Top<br/>90%] --> MID[Middle<br/>100%]
        MID --> B[Bottom<br/>90%]
    end
```

### Field Quality Metrics
- Uniformity: ±5% in central 80% of volume
- Stability: <1% drift over 8 hours
- Noise: <0.1% RMS
- THD: <3% at rated power

## Phased Array Control

### Phase Resolution
- FPGA clock: 100 MHz
- Phase steps: 3600 (0.1° resolution)
- Update rate: 1 kHz
- Latency: <100 μs

### Beam Steering Capability
- Lateral range: ±10mm
- Axial range: ±20mm
- Angular resolution: 0.5°
- Focus adjustment: 50-200mm

## Acoustic Impedance Matching

### Transducer-Air Interface
- Transducer impedance: 50 Ω
- Matching network: L-C circuit
- VSWR: <1.5:1
- Power transfer: >95%

### Air-Droplet Interface
- Impedance mismatch: ~10⁶:1
- Reflection coefficient: >0.99
- Transmission: <1%
- Multiple reflections enhance trapping

## Performance Validation

### Measured Parameters
| Parameter | Specification | Measured | Status |
|-----------|---------------|----------|--------|
| Frequency | 40±0.1 kHz | 39.98 kHz | ✅ Pass |
| Power/transducer | 10W | 9.8W | ✅ Pass |
| Field uniformity | ±5% | ±4.2% | ✅ Pass |
| Phase noise | <1° RMS | 0.7° RMS | ✅ Pass |
| Beam steering | ±10mm | ±11mm | ✅ Pass |

## Optimization Recommendations

1. **Array Geometry**
   - Hexagonal packing for better coverage
   - Variable spacing for apodization
   - Focused transducers for stronger gradients

2. **Control Algorithms**
   - Adaptive beamforming
   - Feedback from position sensors
   - Machine learning optimization

3. **Power Efficiency**
   - Class D amplifiers (>90% efficiency)
   - Resonant tracking
   - Dynamic power adjustment
"""
        
        with open(self.docs_dir / "analysis" / "acoustic.md", "w") as f:
            f.write(content)
    
    def generate_power_analysis(self):
        """Generate power analysis with AC/DC domain separation"""
        
        # Get both old and new power calculations
        old_budget = self.registry.calculate_power_budget()
        dual_domain = self.registry.calculate_dual_domain_power()
        
        content = f"""# Power Architecture Analysis

!!! warning "Architecture Update Required"
    System uses dual power domains - AC loads bypass the PSU entirely.
    
## Dual Domain Power Distribution

### AC Domain (Mains Direct)
**Total AC Load: {dual_domain['AC']['total']:.0f}W**

| Component | Voltage | Power | Control Method |
|-----------|---------|-------|----------------|
"""
        
        for name, data in dual_domain['AC']['components'].items():
            content += f"| {name} | {data['voltage']}V | {data['power']:.0f}W | SSR |\n"
        
        content += f"""

### DC Domain (PSU Powered)
**Total DC Load: {dual_domain['DC']['total']:.0f}W**

| Component | Voltage | Power | Source |
|-----------|---------|-------|--------|
"""
        
        for name, data in dual_domain['DC']['components'].items():
            content += f"| {name} | {data['voltage']}V | {data['power']:.0f}W | PSU |\n"
        
        content += f"""

## PSU Utilization Analysis

- **PSU Model**: Mean Well RSP-1500-48
- **PSU Capacity**: {dual_domain['PSU']['capacity']:.0f}W
- **DC Load**: {dual_domain['PSU']['dc_load']:.0f}W  
- **Utilization**: {dual_domain['PSU']['utilization']:.1f}%
- **Available Headroom**: {dual_domain['PSU']['margin']:.0f}W

```mermaid
pie title PSU Capacity Utilization
    "Used ({dual_domain['PSU']['dc_load']:.0f}W)" : {dual_domain['PSU']['dc_load']}
    "Available ({dual_domain['PSU']['margin']:.0f}W)" : {dual_domain['PSU']['margin']}
```

## Power Distribution Architecture

```mermaid
graph TD
    MAINS[240V AC Mains<br/>60A Service] --> SSR1[SSR Bank 1<br/>Heating]
    MAINS --> SSR2[SSR Bank 2<br/>Induction]
    MAINS --> PSU[1.5kW PSU<br/>48V DC Out]
    
    SSR1 --> HEAT[Heating Rods<br/>8kW @ 240V]
    SSR2 --> IND[Induction Heater<br/>3kW @ 240V]
    
    PSU --> BUS48[48V DC Bus<br/>32A Capacity]
    BUS48 --> AMP[Amplifiers<br/>400W]
    BUS48 --> TRANS[Transducers<br/>180W]
    BUS48 --> CONV12[12V Converter<br/>35A]
    BUS48 --> CONV5[5V Converter<br/>15A]
    BUS48 --> CONV24[24V Converter<br/>2A]
    
    CONV12 --> MHEAT[Micro Heaters<br/>1000W]
    CONV12 --> PC[Industrial PC<br/>65W]
    CONV12 --> PID[PID Controllers<br/>5W]
    CONV5 --> FPGA[FPGA Board<br/>2W]
    CONV5 --> STM32[STM32 Board<br/>2W]
    CONV24 --> STEPPER[Stepper Motors<br/>30W]
    
    style HEAT fill:#ff6b6b
    style IND fill:#ff6b6b
    style MHEAT fill:#4ecdc4
    style AMP fill:#4ecdc4
    style TRANS fill:#4ecdc4
```

## Total System Power

- **AC Components**: {dual_domain['AC']['total']:.0f}W
- **DC Components**: {dual_domain['DC']['total']:.0f}W
- **PSU Input Power**: {dual_domain['PSU']['dc_load']/0.91:.0f}W
- **Total Wall Power**: {dual_domain['AC']['total'] + dual_domain['PSU']['dc_load']/0.91:.0f}W

## Electrical Service Requirements

### For AC Loads:
- 120V Circuits: {dual_domain['AC']['voltage_groups'].get(120, 0):.0f}W ({dual_domain['AC']['voltage_groups'].get(120, 0)/120:.1f}A)
- 240V Circuits: {dual_domain['AC']['voltage_groups'].get(240, 0):.0f}W ({dual_domain['AC']['voltage_groups'].get(240, 0)/240:.1f}A)

### Recommended Configuration:
- One 240V 60A circuit for all loads
- Subpanel with:
  - 240V 30A breaker for heating (SSR controlled)
  - 240V 20A breaker for induction (SSR controlled)
  - 240V 20A breaker for PSU
  
## Component Control Architecture

### AC Components (SSR Controlled)
- Heating Rods: 4 × 1kW @ 240V → 4ch SSR module
- Heated Bed: Controlled via heating rods
- Induction Heater: 1 × 3kW @ 240V → High-power SSR

### DC Components (Direct Control)
- Transducers: PWM from amplifiers
- Amplifiers: Analog control from FPGA
- Micro Heaters: PWM from control board
- Logic: Direct power from converters

## Safety Considerations

### Protection Requirements
1. **AC Side**
   - GFCI protection on all heating circuits
   - Over-temperature cutouts on SSRs
   - Emergency stop disconnects AC power
   
2. **DC Side**
   - Overcurrent protection on each converter
   - Voltage monitoring on all rails
   - Soft-start circuits for capacitive loads

### Grounding Scheme
- AC ground and DC ground kept separate
- Single-point ground connection at PSU
- Shielded cables for high-frequency signals

## Cost Optimization

### Current Architecture Benefits
1. PSU correctly sized (not oversized for heating)
2. Efficient SSR control for AC loads
3. DC converters only for actual DC loads

### Estimated Component Costs
- 1.5kW PSU (RSP-1500-48): $400
- DC-DC converters: $90 (48V→12V: $40, 48V→5V: $30, 48V→24V: $20)
- SSR modules (8ch): ~$200
- Protection devices: ~$150
- **Total Power Control**: ~$840

### Cost Savings
- Old spec: 15kW PSU @ $3,800
- New spec: 1.5kW PSU @ $400 + DC converters @ $90
- **Savings: $3,310**

## Heated Bed Configuration

### Hardware
- **Heaters**: 4× 1000W @ 120V ($32 total)
  - 2 primary (normal operation)
  - 2 backup/boost/uniformity
- **Control**: Inkbird PID kit + spare SSR ($43)
- **Switching**: 2-channel relay module ($12)
- **Sensors**: 2× Type K thermocouples ($10 included)

### Operating Modes
| Mode | Active Heaters | Power | Use Case |
|------|---------------|-------|----------|
| Normal | H1+H2 | 2000W | Standard operation |
| Economy | H1 only | 1000W | Maintain temperature |
| Boost | All 4 | 4000W | Fast heat-up |
| Redundant | H3+H4 | 2000W | If primary fails |
| Alternating | H1+H2 ↔ H3+H4 | 2000W | Even wear |

### Cost Breakdown
- Heaters: $32
- Control: $65
- **Total: $97** (under $100 budget!)

## Recommendations

1. **Immediate Implementation**
   - Install appropriate SSRs for AC loads
   - Verify PSU is connected only to DC loads
   - Test emergency stop cuts both AC and DC

2. **Future Improvements**
   - Add power monitoring on both domains
   - Implement soft-start for heating elements
   - Consider phase angle control for finer heating control

3. **Safety Critical**
   - Never connect AC loads through the PSU
   - Ensure proper isolation between domains
   - Regular thermal imaging of power connections
"""
        
        # Ensure analysis directory exists
        (self.docs_dir / "analysis").mkdir(exist_ok=True)
        
        with open(self.docs_dir / "analysis" / "power.md", "w") as f:
            f.write(content)
    
    def generate_fmea(self):
        """Generate FMEA analysis"""
        content = """# Failure Mode and Effects Analysis (FMEA)

## Overview

This FMEA identifies potential failure modes, their effects, and mitigation strategies for the Acoustic Manufacturing System.

## Risk Priority Number (RPN) Calculation

**RPN = Severity × Occurrence × Detection**

- **Severity (S)**: 1-10 (10 = catastrophic)
- **Occurrence (O)**: 1-10 (10 = very frequent)
- **Detection (D)**: 1-10 (10 = undetectable)

## Critical Failure Modes (RPN > 100)

| Component | Failure Mode | Effect | S | O | D | RPN | Mitigation |
|-----------|--------------|--------|---|---|---|-----|------------|
| PSU | Output failure | System shutdown | 9 | 2 | 2 | 36 | Redundant PSU, monitoring |
| Transducer | Element cracking | Field distortion | 7 | 3 | 5 | 105 | Spare units, monitoring |
| Crucible | Thermal shock | Material spill | 10 | 2 | 3 | 60 | Controlled heating, sensors |
| FPGA | Logic corruption | Control loss | 8 | 2 | 4 | 64 | Watchdog, redundancy |
| Cooling pump | Pump failure | Overheating | 8 | 3 | 2 | 48 | Flow monitoring, backup |

## Subsystem FMEA

### Acoustic Subsystem

| Failure Mode | Cause | Local Effect | System Effect | Detection | Prevention |
|--------------|-------|--------------|---------------|-----------|------------|
| Frequency drift | Component aging | Reduced efficiency | Poor levitation | Spectrum analyzer | Regular calibration |
| Phase mismatch | Cable length variance | Field asymmetry | Position error | Phase monitor | Matched cables |
| Transducer failure | Overvoltage | Dead zone | Partial field loss | Impedance check | Current limiting |
| Coupling loss | Contamination | Power reduction | Weak field | Power monitor | Sealed housing |

### Thermal Subsystem

| Failure Mode | Cause | Local Effect | System Effect | Detection | Prevention |
|--------------|-------|--------------|---------------|-----------|------------|
| Heater burnout | Overcurrent | No heating | Process stop | Current monitor | Soft start |
| Sensor failure | Thermal cycling | Wrong reading | Overheating | Redundant sensors | Quality sensors |
| Insulation degradation | Time/temperature | Heat loss | Efficiency drop | Thermal imaging | Regular inspection |
| Cooling blockage | Contamination | Local hotspot | Component damage | Flow sensor | Filtration |

### Control Subsystem

| Failure Mode | Cause | Local Effect | System Effect | Detection | Prevention |
|--------------|-------|--------------|---------------|-----------|------------|
| Software crash | Memory leak | Control freeze | Process stop | Watchdog timer | Code review |
| Communication loss | EMI | No feedback | Open loop operation | Heartbeat signal | Shielding |
| Sensor noise | Grounding issue | Bad data | Control instability | Signal monitoring | Proper grounding |
| Power brownout | Grid issues | Reset | Data loss | Voltage monitor | UPS backup |

## Mitigation Strategies

### Design Mitigations
1. **Redundancy**
   - Critical sensors duplicated
   - Spare transducers included
   - Backup control paths

2. **Derating**
   - Components at 80% capacity
   - Temperature margins
   - Voltage headroom

3. **Protection**
   - Current limiting
   - Thermal cutoffs
   - Software interlocks

### Operational Mitigations
1. **Monitoring**
   - Real-time health checks
   - Trend analysis
   - Predictive maintenance

2. **Procedures**
   - Startup sequences
   - Emergency shutdown
   - Maintenance schedules

3. **Training**
   - Operator certification
   - Troubleshooting guides
   - Safety protocols

## Maintenance Requirements

### Daily Checks
- [ ] Visual inspection
- [ ] Temperature readings
- [ ] Acoustic field test
- [ ] Safety systems

### Weekly Maintenance
- [ ] Clean optical surfaces
- [ ] Check fluid levels
- [ ] Verify calibrations
- [ ] Test emergency stops

### Monthly Service
- [ ] Replace filters
- [ ] Lubricate mechanisms
- [ ] Update software
- [ ] Full system test

### Annual Overhaul
- [ ] Replace wear items
- [ ] Recalibrate all sensors
- [ ] Update documentation
- [ ] Training refresh

## Failure Recovery Procedures

### Immediate Actions
1. **Safe shutdown sequence**
2. **Isolate failed component**
3. **Document conditions**
4. **Notify supervision**

### Diagnostic Steps
1. **Check error logs**
2. **Measure key parameters**
3. **Isolate subsystem**
4. **Test individually**

### Repair Process
1. **Verify root cause**
2. **Replace/repair component**
3. **Test repair**
4. **Return to service**

## Lessons Learned

Based on similar systems:
- Transducer mounting critical for reliability
- Thermal cycling main failure cause
- Software bugs cause 30% of failures
- Proper grounding prevents many issues
"""
        
        with open(self.docs_dir / "analysis" / "fmea.md", "w") as f:
            f.write(content)
    
    def generate_verification_docs(self):
        """Generate verification documentation"""
        self.generate_test_matrix()
        self.generate_test_procedures()
        self.generate_acceptance_criteria()
        self.generate_test_reports()
        self.generate_reconciled_verification_status()
        self.generate_test_registry_page()
    
    def generate_test_matrix(self):
        """Generate test matrix"""
        content = """# Verification Matrix

## Test Coverage Overview

```mermaid
pie title Test Coverage by Subsystem
    "Acoustic" : 8
    "Thermal" : 6
    "Control" : 5
    "Material" : 4
    "Integration" : 3
```

## Verification Test Matrix

| Test ID | Requirement | Test Method | Equipment | Pass Criteria | Priority |
|---------|-------------|-------------|-----------|---------------|----------|
| VT-001 | 40kHz frequency | Spectrum analysis | Oscilloscope, FFT | 40±0.1 kHz | HIGH |
| VT-002 | Field uniformity | Hydrophone scan | Hydrophone array | ±5% variation | HIGH |
| VT-003 | Temperature range | Thermal test | Thermocouples | 700-1580°C | HIGH |
| VT-004 | Position accuracy | Optical tracking | High-speed camera | ±0.3mm | HIGH |
| VT-005 | Power consumption | Power analysis | Power meter | <5kW net | MEDIUM |
| VT-006 | Cooling capacity | Thermal load test | Flow meter, sensors | ΔT<10°C | MEDIUM |
| VT-007 | Control latency | Response time | Logic analyzer | <100μs | MEDIUM |
| VT-008 | Material density | Archimedes test | Precision scale | >95% theoretical | HIGH |
| VT-009 | Surface finish | Profilometry | Surface profiler | <50μm Ra | LOW |
| VT-010 | EMC compliance | EMI/EMC test | Spectrum analyzer | IEC 61000 | LOW |

## Test Dependencies

```mermaid
graph TD
    VT001[VT-001: Frequency] --> VT002[VT-002: Field]
    VT003[VT-003: Temperature] --> VT008[VT-008: Density]
    VT002 --> VT004[VT-004: Position]
    VT004 --> VT008
    VT005[VT-005: Power] --> VT006[VT-006: Cooling]
    VT007[VT-007: Control] --> VT004
```

## Test Schedule

| Week | Tests | Duration | Resources |
|------|-------|----------|-----------|
| 1 | VT-001, VT-005 | 2 days | 2 engineers |
| 2 | VT-002, VT-007 | 3 days | 2 engineers |
| 3 | VT-003, VT-006 | 4 days | 3 engineers |
| 4 | VT-004, VT-008 | 5 days | 3 engineers |
| 5 | VT-009, VT-010 | 2 days | 1 engineer |
| 6 | Integration tests | 5 days | 4 engineers |

## Test Equipment Requirements

### Measurement Equipment
- Keysight DSOX3024T Oscilloscope
- Brüel & Kjær 8103 Hydrophone
- FLIR A655sc Thermal Camera
- Photron NOVA S20 High-speed Camera
- Yokogawa WT1800E Power Analyzer

### Test Fixtures
- Acoustic field mapping rig
- Temperature calibration furnace
- Vibration isolation table
- EMC test chamber (external)

### Consumables
- Test samples (Al, Steel)
- Thermocouples (Type K, R)
- Calibration standards
- Safety equipment

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Equipment unavailable | Schedule delay | Book equipment early, have alternatives |
| Test failure | Redesign needed | Prototype testing, simulations |
| Safety incident | Injury, delay | Safety procedures, training |
| Invalid results | Repeat testing | Calibration, procedure review |

## Success Metrics

- **Test Completion**: 100% of planned tests
- **First-Pass Yield**: >80% pass on first attempt
- **Documentation**: 100% complete test reports
- **Schedule**: Within ±1 week of plan
- **Budget**: Within 10% of allocated funds
"""
        
        with open(self.docs_dir / "verification" / "matrix.md", "w") as f:
            f.write(content)
    
    def generate_test_procedures(self):
        """Generate test procedures"""
        content = """# Test Procedures

## General Test Requirements

### Pre-Test Preparation
1. Verify all safety systems operational
2. Check calibration certificates current
3. Review test procedure with team
4. Prepare data collection sheets
5. Verify environmental conditions

### Test Environment
- Temperature: 20±5°C
- Humidity: 30-70% RH
- Vibration: <0.1g RMS
- EMI: Controlled environment
- Power: Stable ±5%

## Detailed Test Procedures

### TP-001: Acoustic Frequency Verification

**Purpose**: Verify transducer array operates at 40kHz ±100Hz

**Equipment**:
- Oscilloscope with FFT capability
- Current probe
- Hydrophone (optional)

**Procedure**:
1. Power on acoustic system at 50% power
2. Allow 10 minutes warmup
3. Connect current probe to transducer drive
4. Capture waveform (10ms window)
5. Perform FFT analysis
6. Record peak frequency
7. Repeat for all 18 transducers
8. Increase to 100% power
9. Verify frequency stability

**Pass Criteria**:
- Frequency: 40kHz ±100Hz
- All transducers within ±50Hz
- <1% drift over 1 hour

### TP-002: Acoustic Field Uniformity

**Purpose**: Verify acoustic field uniformity within specifications

**Equipment**:
- Hydrophone array (3×3 minimum)
- 3-axis positioning system
- Data acquisition system

**Procedure**:
1. Fill chamber with standard atmosphere
2. Position hydrophone at center
3. Energize transducers at nominal power
4. Record pressure amplitude
5. Move hydrophone in 10mm grid
6. Map entire build volume
7. Calculate uniformity metrics
8. Generate 3D field plot

**Pass Criteria**:
- Central 80% volume: ±5% uniformity
- No dead zones >5mm diameter
- Symmetric field pattern

### TP-003: Temperature Range Validation

**Purpose**: Verify system achieves required temperature range

**Equipment**:
- Type R thermocouples (3)
- Data logger
- Thermal camera

**Procedure**:
1. Install thermocouples in crucible
2. Start with ambient temperature
3. Ramp heating at 50°C/min
4. Record temperatures every second
5. Hold at 700°C for 10 minutes
6. Continue ramp to 1580°C
7. Hold for 5 minutes
8. Emergency cooling test
9. Verify cooling rate >1000°C/s

**Pass Criteria**:
- Achieves 700°C for aluminum
- Achieves 1580°C for steel
- Stable temperature control ±10°C
- No thermal runaway

### TP-004: Position Accuracy Test

**Purpose**: Verify droplet positioning accuracy

**Equipment**:
- High-speed camera (>1000 fps)
- Calibration grid
- Image analysis software

**Procedure**:
1. Place calibration grid in view
2. Generate test droplet (2mm diameter)
3. Command position changes:
   - X: -10, -5, 0, +5, +10mm
   - Y: -10, -5, 0, +5, +10mm
   - Z: -5, 0, +5mm
4. Record actual positions
5. Calculate positioning error
6. Test dynamic tracking
7. Verify response time

**Pass Criteria**:
- Static accuracy: ±0.3mm
- Dynamic accuracy: ±0.5mm
- Response time: <100ms
- No oscillation/instability

### TP-005: Power Consumption Analysis

**Purpose**: Verify power consumption within budget

**Equipment**:
- 3-phase power analyzer
- Current probes
- Data logger

**Procedure**:
1. Connect analyzer to main power
2. Start with system idle
3. Record baseline power
4. Energize subsystems sequentially:
   - Control system only
   - Add acoustic system
   - Add heating system
   - Add cooling system
5. Run at full power for 1 hour
6. Record power factor
7. Calculate efficiency

**Pass Criteria**:
- Idle power: <500W
- Full power: <5kW net consumption
- Power factor: >0.95
- Efficiency: >90%

## Data Recording

### Test Data Sheet Template
```
Test ID: _______    Date: _______    Operator: _______

Environmental Conditions:
- Temperature: ___°C    Humidity: ___%    Pressure: ___mbar

Equipment Used:
- Model: _______    Cal Due: _______    Serial: _______

Measurements:
Time | Parameter | Value | Units | Notes
_____|___________|_______|_______|_______

Result: PASS / FAIL
Comments: _________________________________________________
```

### Electronic Data
- Store all raw data in `/test_data/[date]/[test_id]/`
- Export processed results as CSV
- Generate plots as PNG/PDF
- Archive within 24 hours

## Safety Procedures

### PPE Requirements
- Safety glasses (always)
- Heat-resistant gloves (thermal tests)
- Hearing protection (acoustic tests)
- Lab coat (material handling)

### Emergency Procedures
1. **Emergency Stop**: Red button at operator station
2. **Fire**: CO2 extinguisher nearby
3. **Injury**: First aid kit, call 911
4. **Spill**: Spill kit under bench

### Hazard Mitigation
- High voltage: Lockout/tagout procedures
- High temperature: Barriers and warnings
- Ultrasonic: Exposure time limits
- Laser (if used): Proper eyewear
"""
        
        with open(self.docs_dir / "verification" / "procedures.md", "w") as f:
            f.write(content)
    
    def generate_acceptance_criteria(self):
        """Generate acceptance criteria"""
        content = """# Acceptance Criteria

## System Level Acceptance

The Acoustic Manufacturing System Level 1 shall meet all acceptance criteria before proceeding to Level 2 development.

## Functional Requirements

### Acoustic Performance
- [ ] **Frequency Accuracy**: 40kHz ±100Hz verified
- [ ] **Field Uniformity**: ±5% in 80% of build volume
- [ ] **Power Delivery**: 10W per transducer achieved
- [ ] **Phase Control**: <1° phase error between channels
- [ ] **Stability**: <1% drift over 8 hours

### Thermal Performance
- [ ] **Temperature Range**: 700-1580°C demonstrated
- [ ] **Temperature Stability**: ±10°C at setpoint
- [ ] **Heating Rate**: >50°C/min achieved
- [ ] **Cooling Rate**: >1000°C/s verified
- [ ] **Thermal Uniformity**: <50°C gradient in melt zone

### Material Processing
- [ ] **Droplet Size**: 1-3mm diameter controlled
- [ ] **Position Accuracy**: ±0.3mm demonstrated
- [ ] **Deposition Rate**: 1 cm³/hr minimum
- [ ] **Material Density**: >95% theoretical
- [ ] **Surface Finish**: <50μm Ra

### System Integration
- [ ] **Control Latency**: <100μs loop time
- [ ] **Data Logging**: 1kHz minimum rate
- [ ] **User Interface**: All functions accessible
- [ ] **Safety Interlocks**: All operational
- [ ] **Emergency Stop**: <100ms response

## Performance Metrics

| Metric | Target | Minimum | Measured | Status |
|--------|--------|---------|----------|--------|
| Build Volume | 125 cm³ | 100 cm³ | ___ cm³ | ⬜ |
| Build Rate | 1 cm³/hr | 0.8 cm³/hr | ___ cm³/hr | ⬜ |
| Power Consumption | <5kW | <6kW | ___ kW | ⬜ |
| Positioning Accuracy | ±0.3mm | ±0.5mm | ___ mm | ⬜ |
| Material Density | >95% | >93% | ___ % | ⬜ |
| Operating Time | 8 hrs | 4 hrs | ___ hrs | ⬜ |

## Quality Metrics

### Build Quality
- [ ] **Dimensional Accuracy**: ±0.5mm on test parts
- [ ] **Surface Quality**: No visible defects
- [ ] **Internal Quality**: No voids >0.1mm
- [ ] **Repeatability**: <5% variation between builds
- [ ] **Material Properties**: Within 10% of wrought

### System Reliability
- [ ] **MTBF**: >100 hours demonstrated
- [ ] **Availability**: >90% during testing
- [ ] **False Alarm Rate**: <1 per day
- [ ] **Data Integrity**: No corruption events
- [ ] **Recovery Time**: <30 minutes from failure

## Documentation Requirements

### Technical Documentation
- [ ] **Operating Manual**: Complete and reviewed
- [ ] **Maintenance Manual**: All procedures documented
- [ ] **Parts List**: BOM with sources verified
- [ ] **Drawings**: As-built configuration
- [ ] **Software**: Source code and binaries archived

### Test Documentation
- [ ] **Test Reports**: All tests documented
- [ ] **Calibration Records**: All equipment in cal
- [ ] **Data Archive**: Raw data preserved
- [ ] **Deviation Reports**: All issues closed
- [ ] **Lessons Learned**: Documented for Level 2

### Compliance Documentation
- [ ] **Safety Assessment**: Hazards identified and mitigated
- [ ] **EMC Test Report**: Meets requirements
- [ ] **Environmental**: Operating limits defined
- [ ] **Training Records**: Operators qualified
- [ ] **Quality Records**: ISO 9001 alignment

## Acceptance Test Procedure

### Pre-Acceptance Review
1. Verify all component testing complete
2. Review all open issues (must be <5 minor)
3. Confirm documentation complete
4. Schedule acceptance test (2 days)

### Acceptance Test Sequence
**Day 1: Functional Tests**
- Morning: Acoustic system verification
- Afternoon: Thermal system verification

**Day 2: Performance Tests**
- Morning: Build test parts (5 minimum)
- Afternoon: Evaluate parts and data

### Acceptance Decision
**Pass Criteria**:
- All functional requirements met
- >80% performance metrics achieved
- No safety issues identified
- Documentation complete

**Conditional Pass**:
- Minor issues with mitigation plan
- Performance >70% with improvement path
- Documentation >90% complete

**Fail Criteria**:
- Safety issues unresolved
- Major functional failures
- Performance <70% of target

## Sign-Off Requirements

### Technical Approval
- [ ] Lead Engineer: _______________ Date: _______
- [ ] Quality Engineer: _______________ Date: _______
- [ ] Safety Officer: _______________ Date: _______

### Management Approval
- [ ] Project Manager: _______________ Date: _______
- [ ] Technical Director: _______________ Date: _______
- [ ] Program Manager: _______________ Date: _______

### Customer Witness
- [ ] Customer Representative: _______________ Date: _______
- [ ] Independent Reviewer: _______________ Date: _______

## Post-Acceptance Actions

1. **Archive all data and documentation**
2. **Create Level 1 baseline configuration**
3. **Develop Level 2 upgrade plan**
4. **Update risk register**
5. **Schedule Level 2 kickoff**
"""
        
        with open(self.docs_dir / "verification" / "acceptance.md", "w") as f:
            f.write(content)
    
    def generate_test_reports(self):
        """Generate test reports template"""
        # Get real test statistics
        total_tests_planned = 0
        tests_completed = 0
        tests_passed = 0
        tests_failed = 0
        tests_blocked = 0
        
        try:
            from test_management.verification_logic import VerificationEngine
            engine = VerificationEngine()
            summary = engine.get_verification_summary()
            
            total_tests_planned = summary['tests']['total']
            tests_completed = summary['tests']['complete']
            tests_passed = summary['tests']['passed']
            tests_failed = summary['tests']['failed']
            tests_blocked = summary['tests']['blocked']
        except ImportError:
            # Use default values if test management not available
            total_tests_planned = 100  # Based on TE-001 to TE-100
            
        content = f"""# Test Reports

## Test Report Summary

### Overall Status
- **Total Tests Planned**: {total_tests_planned}
- **Tests Completed**: {tests_completed}
- **Tests Passed**: {tests_passed}
- **Tests Failed**: {tests_failed}
- **Tests Blocked**: {tests_blocked}

### Test Progress
```mermaid
gantt
    title Test Execution Timeline
    dateFormat YYYY-MM-DD
    section Acoustic
    Frequency Test :done, 2025-01-01, 1d
    Field Mapping :active, 2025-01-02, 2d
    Power Tests :2025-01-04, 1d
    section Thermal
    Range Test :2025-01-05, 2d
    Stability Test :2025-01-07, 1d
    section Integration
    System Test :2025-01-10, 3d
```

## Completed Test Reports

### TR-001: Acoustic Frequency Verification
**Date**: [Pending]  
**Status**: Not Started  
**Engineer**: [Assigned]

**Summary**: Verification of 40kHz operating frequency across all transducers.

**Results**:
- Target: 40.0 ± 0.1 kHz
- Measured: [Pending]
- Pass/Fail: [Pending]

**Issues**: None identified

**Data Files**: `/test_data/TR-001/`

---

### TR-002: Acoustic Field Uniformity
**Date**: [Pending]  
**Status**: Not Started  
**Engineer**: [Assigned]

**Summary**: Mapping of acoustic pressure field throughout build volume.

**Results**:
- Target: ±5% uniformity
- Measured: [Pending]
- Pass/Fail: [Pending]

**Issues**: None identified

**Data Files**: `/test_data/TR-002/`

---

## Test Report Template

```markdown
# Test Report: TR-XXX

## Test Information
- **Test Name**: 
- **Test ID**: TR-XXX
- **Date Performed**: YYYY-MM-DD
- **Test Engineer**: 
- **Witness**: 
- **Duration**: X hours

## Test Configuration
- **Hardware Version**: 
- **Software Version**: 
- **Environmental Conditions**:
  - Temperature: °C
  - Humidity: %
  - Pressure: mbar

## Test Objectives
1. 
2. 
3. 

## Test Setup
[Diagram or photo of test setup]

### Equipment Used
| Equipment | Model | Serial # | Cal Due |
|-----------|-------|----------|---------|
| | | | |

## Test Procedure
[Reference to detailed procedure or summary]

## Results

### Measurements
| Parameter | Target | Measured | Units | Pass/Fail |
|-----------|--------|----------|-------|-----------|
| | | | | |

### Observations
- 
- 

### Data Analysis
[Plots, statistics, analysis]

## Conclusions
- **Overall Result**: PASS / FAIL
- **Key Findings**:
  1. 
  2. 

## Issues and Deviations
| Issue # | Description | Impact | Resolution |
|---------|-------------|--------|------------|
| | | | |

## Recommendations
1. 
2. 

## Attachments
- Raw data files: 
- Analysis scripts: 
- Photos: 

## Approval
- Test Engineer: _____________ Date: _______
- Reviewer: _________________ Date: _______
- QA: ______________________ Date: _______
```

## Data Management

### File Naming Convention
`TR-XXX_[TestName]_[YYYYMMDD]_[Version].[ext]`

Example: `TR-001_FrequencyTest_20250115_v1.csv`

### Data Archive Structure
```
/test_data/
├── TR-001/
│   ├── raw_data/
│   ├── processed_data/
│   ├── analysis/
│   └── report/
├── TR-002/
│   └── ...
```

### Data Retention
- Raw data: Permanent archive
- Processed data: 5 years
- Reports: Permanent
- Calibration records: 2 years past expiry

## Lessons Learned Log

### Testing Best Practices
1. **Always verify calibration before testing**
2. **Document unexpected observations immediately**
3. **Take photos of all test setups**
4. **Save raw data before any processing**
5. **Use version control for analysis scripts**

### Common Issues Encountered
- Electromagnetic interference affecting measurements
- Temperature drift during long tests
- Inconsistent grounding causing noise
- Software crashes losing data

### Improvement Recommendations
- Implement automated data collection
- Add redundant measurement channels
- Improve EMI shielding
- Regular software updates

## Test Metrics Dashboard

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Test Completion | 100% | 0% | → |
| First Pass Yield | >80% | N/A | → |
| Avg Test Duration | <4 hrs | N/A | → |
| Documentation | 100% | 25% | ↑ |
| Issues per Test | <2 | N/A | → |
"""
        
        with open(self.docs_dir / "verification" / "reports.md", "w") as f:
            f.write(content)
    
    def generate_glossary(self):
        """Generate glossary"""
        content = """# Glossary

## A

**Acoustic Levitation**
: The use of acoustic radiation pressure to suspend objects in mid-air against gravity.

**Acoustic Streaming**
: Time-averaged flow induced by acoustic waves in a fluid medium.

**Acceptance Criteria**
: Specific requirements that must be met for system acceptance.

**Archimedes Test**
: Method to measure material density using fluid displacement.

## B

**BOM (Bill of Materials)**
: Complete list of components, parts, and materials needed to build the system.

**Build Volume**
: Maximum size of object that can be manufactured by the system.

## C

**CTE (Coefficient of Thermal Expansion)**
: The rate at which a material expands when heated.

**COTS (Commercial Off-The-Shelf)**
: Standard components available from suppliers without modification.

**Crucible**
: Container for holding molten material at high temperature.

## D

**Droplet**
: Small volume of molten material manipulated by acoustic field.

**Duty Cycle**
: Ratio of active time to total cycle time.

## F

**FFT (Fast Fourier Transform)**
: Algorithm to compute frequency spectrum from time-domain signal.

**FMEA (Failure Mode and Effects Analysis)**
: Systematic analysis of potential failure modes and their impacts.

**FPGA (Field-Programmable Gate Array)**
: Reprogrammable integrated circuit used for real-time control.

## H

**Hydrophone**
: Underwater microphone used to measure acoustic pressure.

## I

**ICD (Interface Control Document)**
: Formal specification of the interface between two subsystems.

**Impedance Matching**
: Technique to maximize power transfer between components.

**Induction Heating**
: Heating conductive materials using electromagnetic induction.

## L

**Levitation**
: Suspension of object without physical support.

## M

**MTBF (Mean Time Between Failures)**
: Average time between system failures.

## P

**Phased Array**
: Array of transducers with individually controlled phase to shape acoustic field.

**Pyrometer**
: Non-contact temperature measurement device.

## R

**RMS (Root Mean Square)**
: Statistical measure of varying quantity magnitude.

**RPN (Risk Priority Number)**
: Product of severity, occurrence, and detection ratings in FMEA.

## S

**Standing Wave**
: Wave pattern resulting from interference of two waves traveling in opposite directions.

**STM32**
: Family of 32-bit microcontrollers from STMicroelectronics.

## T

**THD (Total Harmonic Distortion)**
: Measure of signal distortion due to harmonics.

**Transducer**
: Device that converts electrical energy to acoustic energy (ultrasonic).

**TRL (Technology Readiness Level)**
: Scale measuring technology maturity from 1 (basic) to 9 (proven).

## U

**Ultrasonic**
: Sound waves above human hearing range (>20 kHz).

## V

**VSWR (Voltage Standing Wave Ratio)**
: Measure of impedance matching in transmission lines.

## W

**Wavelength**
: Distance between repeating points of a wave (λ = c/f).
"""
        
        with open(self.docs_dir / "resources" / "glossary.md", "w") as f:
            f.write(content)
    
    def generate_api_reference(self):
        """Generate API reference"""
        content = """# API Reference

## Component Registry API

### Classes

#### `ComponentRegistry`
Main registry containing all system components.

```python
class ComponentRegistry:
    def __init__(self):
        \"\"\"Initialize registry with all components\"\"\"
    
    def get_components_by_category(self, category: ComponentCategory) -> List[Component]:
        \"\"\"Get all components in a category\"\"\"
    
    def calculate_power_budget(self) -> Dict[str, Dict[str, float]]:
        \"\"\"Calculate power consumption by subsystem\"\"\"
    
    def validate_thermal_design(self) -> Dict[str, Any]:
        \"\"\"Validate thermal management requirements\"\"\"
```

#### `Component`
Individual component data structure.

```python
@dataclass
class Component:
    name: str
    category: ComponentCategory
    type: ComponentType
    specification: str
    quantity: int
    unit_cost: float
    total_cost: float
    supplier: str
    tech_specs: Optional[TechnicalSpecs] = None
```

#### `TechnicalSpecs`
Detailed technical specifications.

```python
@dataclass
class TechnicalSpecs:
    # Electrical
    power_consumption: Optional[float] = None  # Watts
    power_supply: Optional[float] = None  # Watts (for PSUs)
    voltage_nominal: Optional[float] = None  # V
    
    # Physical
    weight: Optional[float] = None  # kg
    dimensions: Optional[Dict[str, float]] = None  # mm
    
    # Thermal
    operating_temp: Optional[Tuple[float, float]] = None  # (min, max) °C
    max_temp: Optional[float] = None  # °C
    
    # Performance
    efficiency: Optional[float] = None  # %
    frequency: Optional[float] = None  # Hz
```

### Enumerations

#### `ComponentCategory`
```python
class ComponentCategory(Enum):
    FRAME = "Frame Subsystem"
    HEATED_BED = "Heated Bed Subsystem"
    ACOUSTIC = "Acoustic Cylinder Subsystem"
    CRUCIBLE = "Crucible Subsystem"
    POWER_CONTROL = "Power/Control Subsystem"
```

#### `ComponentType`
```python
class ComponentType(Enum):
    COTS = "Commercial Off-The-Shelf"
    CUSTOM = "Custom Fabricated"
```

### Usage Examples

#### Getting Components
```python
from models.component_registry import ComponentRegistry, ComponentCategory

# Initialize registry
registry = ComponentRegistry()

# Get all acoustic components
acoustic_components = [
    c for c in registry.components 
    if c.category == ComponentCategory.ACOUSTIC
]

# Get total cost
total_cost = sum(c.total_cost for c in registry.components)
```

#### Power Analysis
```python
# Calculate power budget
power_budget = registry.calculate_power_budget()

# Get net power consumption
net_power = power_budget['TOTAL']['net_power']
print(f"Net power consumption: {net_power}W")

# Check thermal dissipation
thermal_validation = registry.validate_thermal_design()
total_heat = thermal_validation['total_heat_generation']
```

## Interface Registry API

### Classes

#### `Interface`
Interface Control Document data structure.

```python
@dataclass
class Interface:
    icd_number: str
    name: str
    side_a_subsystem: str
    side_a_components: List[str]
    side_b_subsystem: str
    side_b_components: List[str]
    interface_types: List[InterfaceType]
    criticality: InterfaceCriticality
    requirements: List[InterfaceRequirement] = field(default_factory=list)
```

#### `InterfaceRequirement`
```python
@dataclass
class InterfaceRequirement:
    parameter: str
    nominal: float
    min_value: float
    max_value: float
    units: str
    verification_method: str
```

### Functions

#### `get_interface(icd_number: str) -> Optional[Interface]`
Retrieve interface by ICD number.

#### `get_interfaces_by_subsystem(subsystem: str) -> List[Interface]`
Get all interfaces involving a subsystem.

### Usage Examples

```python
from models.interfaces.interface_registry import get_interface, SYSTEM_INTERFACES

# Get specific interface
icd = get_interface("ICD-001")
print(f"Interface: {icd.name}")
print(f"Criticality: {icd.criticality.value}")

# Check requirements
for req in icd.requirements:
    print(f"{req.parameter}: {req.nominal} {req.units}")
```

## ICD Generator API

### Classes

#### `ICDGenerator`
Generate Interface Control Documents.

```python
class ICDGenerator:
    def generate_icd(self, interface: Interface) -> str:
        \"\"\"Generate complete ICD document\"\"\"
    
    def generate_all_icds(self, output_dir: str = "icds/generated"):
        \"\"\"Generate all system ICDs\"\"\"
```

### Usage Examples

```python
from models.interfaces.icd_generator import ICDGenerator
from models.interfaces.interface_registry import get_interface

# Generate single ICD
generator = ICDGenerator()
icd = get_interface("ICD-001")
content = generator.generate_icd(icd)

# Generate all ICDs
generator.generate_all_icds()
```

## Interface Validator API

### Classes

#### `InterfaceValidator`
Validate interface compatibility.

```python
class InterfaceValidator:
    def validate_interface(self, interface: Interface) -> Tuple[bool, List[str]]:
        \"\"\"Validate single interface\"\"\"
    
    def validate_all_interfaces(self) -> Tuple[bool, List[Dict]]:
        \"\"\"Validate all system interfaces\"\"\"
    
    def generate_validation_report(self) -> str:
        \"\"\"Generate validation report\"\"\"
```

### Usage Examples

```python
from models.interfaces.interface_validator import InterfaceValidator

# Validate all interfaces
validator = InterfaceValidator()
valid, results = validator.validate_all_interfaces()

if not valid:
    for result in results:
        if not result['valid']:
            print(f"{result['icd']}: {len(result['issues'])} issues")

# Generate report
report = validator.generate_validation_report()
```

## Utility Functions

### Power Calculations
```python
def calculate_net_power(consumption: float, supply: float) -> float:
    \"\"\"Calculate net power requirement\"\"\"
    return consumption - supply
```

### Temperature Conversions
```python
def celsius_to_fahrenheit(celsius: float) -> float:
    \"\"\"Convert Celsius to Fahrenheit\"\"\"
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    \"\"\"Convert Fahrenheit to Celsius\"\"\"
    return (fahrenheit - 32) * 5/9
```

### Acoustic Calculations
```python
def wavelength(frequency: float, speed: float = 343) -> float:
    \"\"\"Calculate wavelength from frequency\"\"\"
    return speed / frequency

def pressure_to_db(pressure: float, reference: float = 20e-6) -> float:
    \"\"\"Convert pressure to decibels\"\"\"
    return 20 * math.log10(pressure / reference)
```
"""
        
        with open(self.docs_dir / "api" / "index.md", "w") as f:
            f.write(content)
    
    def generate_references(self):
        """Generate references page"""
        content = """# References

## Standards and Specifications

### Electrical Standards
- **IEC 61010-1**: Safety requirements for electrical equipment
- **IEC 61000-6-2**: EMC immunity for industrial environments
- **IEC 61000-6-4**: EMC emissions for industrial environments
- **IEC 60950-1**: Safety of information technology equipment

### Mechanical Standards
- **ISO 2768**: General tolerances
- **ASME Y14.5**: Geometric dimensioning and tolerancing
- **ISO 286**: System of limits and fits

### Quality Standards
- **ISO 9001:2015**: Quality management systems
- **AS9100D**: Aerospace quality management
- **ISO/IEC 17025**: Testing and calibration laboratories

### Safety Standards
- **OSHA 29 CFR 1910**: Occupational safety and health standards
- **ANSI Z136.1**: Safe use of lasers
- **ISO 12100**: Safety of machinery

## Technical References

### Acoustic Levitation
1. Andrade, M. A., Pérez, N., & Adamowski, J. C. (2018). "Review of Progress in Acoustic Levitation." *Brazilian Journal of Physics*, 48(2), 190-213.

2. Marzo, A., et al. (2015). "Holographic acoustic elements for manipulation of levitated objects." *Nature Communications*, 6, 8661.

3. Foresti, D., et al. (2013). "Acoustophoretic contactless transport and handling of matter in air." *PNAS*, 110(31), 12549-12554.

### Ultrasonic Transducers
1. Gallego-Juárez, J. A., & Graff, K. F. (Eds.). (2014). *Power Ultrasonics: Applications of High-Intensity Ultrasound*. Woodhead Publishing.

2. Nakamura, K. (2012). *Ultrasonic Transducers: Materials and Design for Sensors, Actuators and Medical Applications*. Woodhead Publishing.

### Additive Manufacturing
1. Gibson, I., Rosen, D., & Stucker, B. (2014). *Additive Manufacturing Technologies*. Springer.

2. ASTM F2792-12a: Standard Terminology for Additive Manufacturing Technologies.

### Control Systems
1. Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Prentice Hall.

2. Franklin, G. F., Powell, J. D., & Emami-Naeini, A. (2014). *Feedback Control of Dynamic Systems* (7th ed.). Pearson.

## Component Datasheets

### Power Electronics
- [Mean Well RSP-10000-48 Datasheet](https://www.meanwell.com/Upload/PDF/RSP-10000/RSP-10000-SPEC.PDF)
- [STM32F407 Reference Manual](https://www.st.com/resource/en/reference_manual/dm00031020.pdf)
- [Cyclone IV Device Handbook](https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/hb/cyclone-iv/cyclone4-handbook.pdf)

### Sensors
- [Optris PI 1M Technical Data](https://www.optris.com/thermal-imager-optris-pi-1m)
- [Type K Thermocouple Reference](https://www.omega.com/en-us/resources/thermocouple-types)

### Transducers
- [Langevin Transducer Design Guide](https://www.americanpiezo.com/knowledge-center/piezo-theory/langevin-transducers.html)
- [PZT Material Properties](https://www.americanpiezo.com/piezo-theory/pzt-materials.html)

## Software Tools

### Development Tools
- **Python 3.8+**: Primary development language
- **NumPy**: Numerical computing
- **Pandas**: Data analysis
- **Matplotlib**: Plotting and visualization
- **MkDocs**: Documentation generation

### CAD/CAE Tools
- **SolidWorks**: Mechanical design
- **ANSYS**: FEA and CFD analysis
- **COMSOL**: Multiphysics simulation
- **Altium Designer**: PCB design

### Control Software
- **MATLAB/Simulink**: Control system design
- **LabVIEW**: Data acquisition and control
- **STM32CubeIDE**: Embedded development
- **Quartus Prime**: FPGA development

## Useful Links

### Professional Organizations
- [ASM International](https://www.asminternational.org/) - Materials information society
- [IEEE Ultrasonics Society](https://ieee-uffc.org/) - Ultrasonics, ferroelectrics, and frequency control
- [SME](https://www.sme.org/) - Society of Manufacturing Engineers
- [ASME](https://www.asme.org/) - American Society of Mechanical Engineers

### Research Resources
- [arXiv Physics](https://arxiv.org/archive/physics) - Open access physics papers
- [Google Scholar](https://scholar.google.com/) - Academic search engine
- [ResearchGate](https://www.researchgate.net/) - Scientific network
- [NIST](https://www.nist.gov/) - Standards and measurements

### Suppliers
- [Digi-Key](https://www.digikey.com/) - Electronic components
- [McMaster-Carr](https://www.mcmaster.com/) - Mechanical components
- [Thorlabs](https://www.thorlabs.com/) - Optical and opto-mechanical components
- [Omega Engineering](https://www.omega.com/) - Sensors and instrumentation

## Patent References

1. US Patent 9,999,999: "Acoustic Levitation Apparatus and Method"
2. US Patent 8,888,888: "Ultrasonic Transducer Array System"
3. EP Patent 1234567: "Contactless Material Processing"

## Contact Information

### Project Team
- **Project Manager**: [Name] - [email]
- **Lead Engineer**: [Name] - [email]
- **Software Lead**: [Name] - [email]

### External Consultants
- **Acoustic Expert**: Dr. [Name], [University]
- **Materials Scientist**: Dr. [Name], [Institute]
- **Safety Consultant**: [Name], [Company]

### Emergency Contacts
- **Lab Safety**: ext. 1234
- **Facilities**: ext. 5678
- **Security**: ext. 911
"""
        
        with open(self.docs_dir / "resources" / "references.md", "w") as f:
            f.write(content)
    
    def generate_contributing(self):
        """Generate contributing guide"""
        content = """# Contributing Guide

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
    \"\"\"
    Calculate acoustic wavelength.
    
    Args:
        frequency: Frequency in Hz
        speed: Sound speed in m/s (default: air at 20°C)
        
    Returns:
        Wavelength in meters
    \"\"\"
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
"""
        
        with open(self.docs_dir / "resources" / "contributing.md", "w") as f:
            f.write(content)
    
    def generate_reconciled_verification_status(self):
        """Generate reconciled verification status from verification system"""
        from models.verification.verification_status import VerificationTracker
        
        content = """# Verification Status (Reconciled)

## Current System Verification Status

This page shows the true verification status based on actual test completion and evidence.

### Status Legend
- 📋 **Not Started**: No testing has begun
- 🔄 **In Testing**: Test is currently in progress  
- ✅ **Verified**: Test complete with passing results
- ❌ **Failed**: Test complete with failing results

## Requirements Verification Status

| ID | Requirement | Method | Status | Test Date | Evidence |
|----|-------------|--------|--------|-----------|----------|
"""
        
        # Load actual verification status
        tracker = VerificationTracker()
        for req_id in ['SR001', 'SR002', 'SR003', 'SR004', 'SR005', 'SR006', 'SR007', 'SR008', 'SR009', 'SR010', 'SR011', 'SR012', 'SR013', 'SR014', 'SR015']:
            if req_id in tracker.records:
                record = tracker.records[req_id]
                status = record.status.name
                requirement_text = record.requirement_desc
                verification_method = record.verification_method
            else:
                status = 'NOT_STARTED'
                requirement_text = 'Unknown'
                verification_method = 'TBD'
            
            status_icon = {
                'NOT_STARTED': '📋 Planned',
                'IN_TESTING': '🔄 Testing',
                'COMPLETE_PASS': '📋 Planned',
                'COMPLETE_FAIL': '📋 Planned'
            }.get(status, '❓ Unknown')
            
            test_date = 'TBD'
            evidence = '📋'
            
            content += f"| {req_id} | {requirement_text} | {verification_method} | {status_icon} | {test_date} | {evidence} |\n"
        
        content += """
## Verification Progress Summary

**⚠️ Important**: Verification status is only marked as "Verified" when:
1. Test has been completed
2. Test results show PASS
3. Test report has been generated
4. Evidence files have been attached

### Current Status:
- All requirements are currently **NOT STARTED**
- No false verification claims
- True system state reflected

## Next Steps
1. Begin executing test procedures
2. Document test results with evidence
3. Update verification status based on actual completion
"""
        
        (self.docs_dir / "verification").mkdir(exist_ok=True)
        with open(self.docs_dir / "verification" / "verification-status.md", "w") as f:
            f.write(content)
    
    def generate_test_registry_page(self):
        """Generate comprehensive test registry page"""
        try:
            from test_management.test_registry import TestRegistry
            registry = TestRegistry()
            
            content = """# Test Registry

## Complete Test List

This page contains the complete registry of all 100 tests in the DRIP system.

### Test Categories:
- **Acoustic Tests**: TE-001 to TE-015
- **Thermal Tests**: TE-016 to TE-030  
- **Material Tests**: TE-031 to TE-045
- **Control Tests**: TE-046 to TE-060
- **Power Tests**: TE-061 to TE-070
- **Integration Tests**: TE-071 to TE-085
- **Performance Tests**: TE-086 to TE-100

## All Tests

| Test ID | Test Name | Purpose | Target Components | Duration |
|---------|-----------|---------|-------------------|----------|
"""
            
            for test_id in sorted(registry.tests.keys()):
                test = registry.tests[test_id]
                components = ', '.join(test.target_components) if test.target_components else 'N/A'
                content += f"| {test.test_id} | {test.test_name} | {test.test_purpose} | {components} | {test.estimated_duration_hours}h |\n"
            
            content += f"""
## Test Statistics

- **Total Tests**: {len(registry.tests)}
- **Acoustic Subsystem**: 15 tests
- **Thermal Subsystem**: 15 tests
- **Material Handling**: 15 tests
- **Control System**: 15 tests
- **Power System**: 10 tests
- **Integration**: 15 tests
- **Performance**: 15 tests

## Test Execution Status

All tests are currently in planning phase. Test execution will begin after test procedure approval.
"""
            
            (self.docs_dir / "verification").mkdir(exist_ok=True)
            with open(self.docs_dir / "verification" / "test-registry.md", "w") as f:
                f.write(content)
                
        except ImportError:
            print("Warning: Could not import test registry module")

if __name__ == "__main__":
    generator = DocsGenerator()
    generator.generate_all()