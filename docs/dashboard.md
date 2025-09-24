# System Dashboard

!!! warning "CONCEPTUAL PLANNING PHASE ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

<div class="dashboard-grid">

<div class="metric-card">
<span class="metric-icon">💰</span>
<div class="metric-content">
<h3>Total Cost</h3>
<p class="metric-value">$19,139</p>
<p class="metric-label">Level 1 System</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">🔧</span>
<div class="metric-content">
<h3>Components</h3>
<p class="metric-value">72</p>
<p class="metric-label">Total Parts</p>
</div>
</div>

<div class="metric-card">
<span class="metric-icon">⚡</span>
<div class="metric-content">
<h3>Power Budget</h3>
<p class="metric-value">6.1kW</p>
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
    "Crucible Subsystem" : 4206
    "Power/Control Subsystem" : 6797
```

## 🔋 Power Distribution

| Subsystem | Consumption | Supply | Net Power |
|-----------|-------------|--------|-----------|
| Heated Bed Subsystem | 6000W | 0W | 6000W |
| Acoustic Cylinder Subsystem | 185W | 0W | 185W |
| Crucible Subsystem | 5110W | 0W | 5110W |
| Power/Control Subsystem | 1500W | 6687W | -5187W |
| **TOTAL** | **12794W** | **6687W** | **6107W** |

## 🔄 Development Phases

```mermaid
gantt
    title Development Phases (Conceptual Sequence)
    dateFormat X
    axisFormat %s
    section Level 1
    Requirements    :done, req, 0, 1w
    Design          :active, des, after req, 2w
    Procurement     :proc, after des, 2w
    Assembly        :assm, after proc, 1w
    Testing         :test, after assm, 2w
    section Level 2
    Steel Upgrade   :steel, after test, 4w
    section Level 3
    Dual Material   :dual, after steel, 6w
    section Level 4
    Production      :prod, after dual, 8w
```

**Timeline: TBD pending project funding and approval**

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
*Dashboard generated from component registry*
