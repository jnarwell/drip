# Acceptance Criteria
!!! danger "PLANNING DOCUMENTATION ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

## System Level Acceptance Planning

The Acoustic Manufacturing System Level 1 will need to meet all acceptance criteria before proceeding to Level 2 development.

## Functional Requirements

### Acoustic Performance
- 📋 **Frequency Accuracy**: 40kHz ±100Hz to be verified
- [ ] **Field Uniformity**: ±5% in 80% of build volume
- 📋 **Power Delivery**: 10W per transducer target
- [ ] **Phase Control**: <1° phase error between channels
- [ ] **Stability**: <1% drift over 8 hours

### Thermal Performance
- 📋 **Temperature Range**: 700-1580°C to be demonstrated
- [ ] **Temperature Stability**: ±10°C at setpoint
- 📋 **Heating Rate**: >50°C/min target
- 📋 **Cooling Rate**: >1000°C/s to be verified
- [ ] **Thermal Uniformity**: <50°C gradient in melt zone

### Material Processing
- [ ] **Droplet Size**: 1-3mm diameter controlled
- 📋 **Position Accuracy**: ±0.3mm to be demonstrated
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
