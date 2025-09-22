# System Dashboard

<div class="dashboard-grid">

<div class="metric-card">
<span class="metric-icon">💰</span>
<div class="metric-content">
<h3>Total Cost</h3>
<p class="metric-value">$13,988</p>
<p class="metric-label">Level 1 System</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">🔧</span>
<div class="metric-content">
<h3>Components</h3>
<p class="metric-value">51</p>
<p class="metric-label">Total Parts</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">⚡</span>
<div class="metric-content">
<h3>Power Budget</h3>
<p class="metric-value">4.6kW</p>
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
    "Frame Subsystem" : 3040
    "Heated Bed Subsystem" : 1424
    "Acoustic Cylinder Subsystem" : 2540
    "Crucible Subsystem" : 3634
    "Power/Control Subsystem" : 3350
```

## 🔋 Power Distribution

| Subsystem | Consumption | Supply | Net Power |
|-----------|-------------|--------|-----------|
| Heated Bed Subsystem | 8000W | 0W | 8000W |
| Acoustic Cylinder Subsystem | 185W | 0W | 185W |
| Crucible Subsystem | 5068W | 0W | 5068W |
| Power/Control Subsystem | 1342W | 10000W | -8658W |

| **TOTAL** | **14596W** | **10000W** | **4596W** |

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
| Acoustic Array | 8 | 6 | 🟡 75% |
| Thermal System | 6 | 4 | 🟡 67% |
| Control System | 5 | 5 | 🟢 100% |
| Material Feed | 4 | 2 | 🟠 50% |
| Integration | 3 | 0 | 🔴 0% |

---
*Dashboard updated: 2025-09-21 19:34:01*
