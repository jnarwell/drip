# System Dashboard

!!! warning "CONCEPTUAL PLANNING PHASE ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

<div class="dashboard-grid">

<div class="metric-card">
<span class="metric-icon">💰</span>
<div class="metric-content">
<h3>Total Cost</h3>
<p class="metric-value">$18,489</p>
<p class="metric-label">Level 1 System</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">🔧</span>
<div class="metric-content">
<h3>Components</h3>
<p class="metric-value">71</p>
<p class="metric-label">Total Parts</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">⚡</span>
<div class="metric-content">
<h3>Power Budget</h3>
<p class="metric-value">10.4kW</p>
<p class="metric-label">Net Consumption</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">🔌</span>
<div class="metric-content">
<h3>Interfaces</h3>
<p class="metric-value">5</p>
<p class="metric-label">ICDs Defined</p>
</div>
</div>

</div>

## 📊 Subsystem Breakdown

```mermaid
pie title Cost Distribution by Subsystem
    "Frame Subsystem" : 4240
    "Heated Bed Subsystem" : 1356
    "Acoustic Cylinder Subsystem" : 2540
    "Crucible Subsystem" : 3956
    "Power/Control Subsystem" : 6397
```

## 🔋 Power Distribution

| Subsystem | Consumption | Supply | Net Power |
|-----------|-------------|--------|-----------|
| Heated Bed Subsystem | 6000W | 0W | 6000W |
| Acoustic Cylinder Subsystem | 185W | 0W | 185W |
| Crucible Subsystem | 5090W | 0W | 5090W |
| Power/Control Subsystem | 1170W | 2079W | -909W |
| **TOTAL** | **12444W** | **2079W** | **10365W** |

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
|-----------|--------------|----------------|--------|
| Acoustic Array | 15 | 0 | 🔴 0% |
| Thermal System | 15 | 0 | 🔴 0% |
| Material Feed | 10 | 0 | 🔴 0% |
| Power System | 10 | 0 | 🔴 0% |
| Sensors | 10 | 0 | 🔴 0% |
| Control System | 10 | 0 | 🔴 0% |
| Chamber | 5 | 0 | 🔴 0% |
| Integration | 5 | 0 | 🔴 0% |
| Performance | 5 | 0 | 🔴 0% |
| Endurance | 10 | 0 | 🔴 0% |
| Validation | 5 | 0 | 🔴 0% |
| **TOTAL** | **100** | **0** | **🔴 0%** |

---
*Dashboard updated: 2025-09-23 10:28:13*
