"""
Test Registry - Defines all 100 tests for DRIP system verification
"""
from .data_models import TestDefinition, VerificationType

class TestRegistry:
    def __init__(self):
        self.tests = {}
        self._initialize_acoustic_tests()
        self._initialize_thermal_tests()
        self._initialize_crucible_tests()
        self._initialize_power_tests()
        self._initialize_sensor_tests()
        self._initialize_control_tests()
        self._initialize_chamber_tests()
        self._initialize_integration_tests()
        self._initialize_performance_tests()
        self._initialize_endurance_tests()
        self._initialize_validation_tests()
    
    def _initialize_acoustic_tests(self):
        """TE-001 to TE-015: Acoustic Subsystem Tests"""
        
        # Transducer Tests
        self.tests['TE-001'] = TestDefinition(
            test_id='TE-001',
            test_name='Individual Transducer Frequency Characterization',
            test_purpose='Verify each transducer operates at 40kHz ±100Hz per SR001',
            target_components=['40kHz Transducers'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=3.0,
            required_equipment=['Network Analyzer', 'Temperature Chamber', 'Test Fixture TF-001'],
            acceptance_criteria='All transducers within 40kHz ±100Hz at 23°C'
        )
        
        self.tests['TE-002'] = TestDefinition(
            test_id='TE-002',
            test_name='Transducer Power Rating Verification',
            test_purpose='Confirm 10W continuous power capability',
            target_components=['40kHz Transducers'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-001'],
            estimated_duration_hours=4.0,
            required_equipment=['Power Meter', 'Thermal Camera', 'Load Bank'],
            acceptance_criteria='10W continuous for 4 hours, temp <60°C'
        )
        
        self.tests['TE-003'] = TestDefinition(
            test_id='TE-003',
            test_name='Transducer Impedance Matching',
            test_purpose='Verify 50Ω impedance at operating frequency',
            target_components=['40kHz Transducers'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=2.0,
            required_equipment=['Impedance Analyzer', 'Calibration Kit'],
            acceptance_criteria='Impedance 50Ω ±5% at 40kHz'
        )
        
        self.tests['TE-004'] = TestDefinition(
            test_id='TE-004',
            test_name='Transducer Efficiency Measurement',
            test_purpose='Confirm >80% electroacoustic efficiency',
            target_components=['40kHz Transducers'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-001', 'TE-003'],
            estimated_duration_hours=3.0,
            required_equipment=['Calorimeter', 'Power Analyzer', 'Acoustic Meter'],
            acceptance_criteria='Efficiency >80% at rated power'
        )
        
        # Array Tests
        self.tests['TE-005'] = TestDefinition(
            test_id='TE-005',
            test_name='Array Phase Coherence',
            test_purpose='Verify phase matching across transducer array',
            target_components=['40kHz Transducers', 'Transducer Array Layer'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-001'],
            estimated_duration_hours=4.0,
            required_equipment=['Multi-channel Oscilloscope', 'Phase Meter Array'],
            acceptance_criteria='Phase variance <5° across array'
        )
        
        self.tests['TE-006'] = TestDefinition(
            test_id='TE-006',
            test_name='Acoustic Field Mapping',
            test_purpose='Characterize 3D acoustic pressure field',
            target_components=['40kHz Transducers', 'Transducer Array Layer', 'Acoustic Cylinder'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-005'],
            enables_tests=['TE-056'],
            estimated_duration_hours=8.0,
            required_equipment=['3D Positioning System', 'Hydrophone', 'Data Acquisition'],
            acceptance_criteria='Field uniformity ±10% in work volume'
        )
        
        # Amplifier Tests
        self.tests['TE-007'] = TestDefinition(
            test_id='TE-007',
            test_name='Amplifier Channel Verification',
            test_purpose='Test all 6 channels for power and frequency response',
            target_components=['6-Channel Amplifiers'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=3.0,
            required_equipment=['Oscilloscope', 'Dummy Loads', 'Spectrum Analyzer'],
            acceptance_criteria='500W/channel, THD <1%, 35-45kHz response'
        )
        
        self.tests['TE-008'] = TestDefinition(
            test_id='TE-008',
            test_name='Amplifier-Transducer Integration',
            test_purpose='Verify proper impedance matching and power transfer',
            target_components=['6-Channel Amplifiers', '40kHz Transducers'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-003', 'TE-007'],
            estimated_duration_hours=4.0,
            required_equipment=['Network Analyzer', 'Power Meter', 'Thermal Camera'],
            acceptance_criteria='Power transfer >95%, no thermal runaway'
        )
        
        self.tests['TE-009'] = TestDefinition(
            test_id='TE-009',
            test_name='Amplifier Protection Circuits',
            test_purpose='Test overcurrent, overvoltage, and thermal protection',
            target_components=['6-Channel Amplifiers'],
            verification_type=VerificationType.SAFETY,
            prerequisite_tests=['TE-007'],
            estimated_duration_hours=2.0,
            required_equipment=['Electronic Load', 'High Voltage Supply', 'Heat Gun'],
            acceptance_criteria='All protections trigger within spec'
        )
        
        # Cylinder Tests
        self.tests['TE-010'] = TestDefinition(
            test_id='TE-010',
            test_name='Acoustic Cylinder Resonance',
            test_purpose='Verify no resonances near 40kHz operating frequency',
            target_components=['Acoustic Cylinder'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=3.0,
            required_equipment=['Vibration Analyzer', 'Impact Hammer', 'Accelerometers'],
            acceptance_criteria='No resonances 35-45kHz, damping >5%'
        )
        
        self.tests['TE-011'] = TestDefinition(
            test_id='TE-011',
            test_name='Cylinder Thermal Isolation',
            test_purpose='Test thermal barrier effectiveness',
            target_components=['Acoustic Cylinder', 'Thermal Isolation Tube'],
            verification_type=VerificationType.PERFORMANCE,
            estimated_duration_hours=6.0,
            required_equipment=['Thermal Chamber', 'Thermocouples', 'Data Logger'],
            acceptance_criteria='Transducer side <60°C with chamber at 300°C'
        )
        
        # Phase Array Tests
        self.tests['TE-012'] = TestDefinition(
            test_id='TE-012',
            test_name='Phase Array Controller Verification',
            test_purpose='Test FPGA phase control resolution and accuracy',
            target_components=['Phase Array Controller'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=4.0,
            required_equipment=['Logic Analyzer', 'High-Speed Oscilloscope'],
            acceptance_criteria='Phase resolution <0.1°, update rate >10kHz'
        )
        
        self.tests['TE-013'] = TestDefinition(
            test_id='TE-013',
            test_name='Acoustic Beam Steering',
            test_purpose='Verify ±0.3mm positioning accuracy per SR002',
            target_components=['Phase Array Controller', '40kHz Transducers', 'Control System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-005', 'TE-012'],
            enables_tests=['TE-057'],
            estimated_duration_hours=6.0,
            required_equipment=['High-Speed Camera', 'Test Particles', 'Position Encoder'],
            acceptance_criteria='Position accuracy ±0.3mm in 50mm³ volume'
        )
        
        self.tests['TE-014'] = TestDefinition(
            test_id='TE-014',
            test_name='Control Loop Timing',
            test_purpose='Verify <3ms control cycle time per SR014',
            target_components=['Phase Array Controller', 'Control System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-012'],
            estimated_duration_hours=3.0,
            required_equipment=['Real-Time Analyzer', 'Signal Generator'],
            acceptance_criteria='Loop closure <3ms, jitter <0.1ms'
        )
        
        self.tests['TE-015'] = TestDefinition(
            test_id='TE-015',
            test_name='Acoustic Subsystem EMI/EMC',
            test_purpose='Verify electromagnetic compatibility',
            target_components=['40kHz Transducers', '6-Channel Amplifiers', 'Phase Array Controller'],
            verification_type=VerificationType.ENVIRONMENTAL,
            estimated_duration_hours=8.0,
            required_equipment=['EMI Test Chamber', 'Spectrum Analyzer', 'Field Probes'],
            acceptance_criteria='Meets IEC 61000-4 standards'
        )
    
    def _initialize_thermal_tests(self):
        """TE-016 to TE-030: Thermal Subsystem Tests"""
        
        # Thermal Camera Tests
        self.tests['TE-016'] = TestDefinition(
            test_id='TE-016',
            test_name='Thermal Camera Calibration',
            test_purpose='Verify temperature measurement accuracy',
            target_components=['Thermal Cameras'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=4.0,
            required_equipment=['Blackbody Calibrator', 'Reference Thermocouples'],
            acceptance_criteria='±2°C accuracy 500-1600°C range'
        )
        
        self.tests['TE-017'] = TestDefinition(
            test_id='TE-017',
            test_name='Thermal Camera Frame Rate',
            test_purpose='Confirm 1000fps capability per SR013',
            target_components=['Thermal Cameras'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-016'],
            estimated_duration_hours=2.0,
            required_equipment=['High-Speed Trigger', 'Rotating Heat Source'],
            acceptance_criteria='1000fps sustained, <1% frame drop'
        )
        
        self.tests['TE-018'] = TestDefinition(
            test_id='TE-018',
            test_name='Camera-Control Integration',
            test_purpose='Verify real-time data transfer to control system',
            target_components=['Thermal Cameras', 'Control System'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-017'],
            enables_tests=['TE-058'],
            estimated_duration_hours=3.0,
            required_equipment=['Network Analyzer', 'Data Logger'],
            acceptance_criteria='<1ms latency, no data loss'
        )
        
        # Temperature Sensor Tests
        self.tests['TE-019'] = TestDefinition(
            test_id='TE-019',
            test_name='Thermocouple Array Calibration',
            test_purpose='Calibrate all Type K thermocouples',
            target_components=['Thermocouples Type K'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=6.0,
            required_equipment=['Calibration Furnace', 'Reference Standards'],
            acceptance_criteria='±1.5°C or 0.4% accuracy'
        )
        
        self.tests['TE-020'] = TestDefinition(
            test_id='TE-020',
            test_name='RTD Sensor Verification',
            test_purpose='Test PT100 RTD accuracy and response',
            target_components=['RTD PT100 Sensors'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=4.0,
            required_equipment=['Precision Calibrator', 'Ice Bath', 'Oil Bath'],
            acceptance_criteria='±0.3°C accuracy, <5s response time'
        )
        
        # Heated Bed Tests
        self.tests['TE-021'] = TestDefinition(
            test_id='TE-021',
            test_name='Heated Bed Temperature Uniformity',
            test_purpose='Verify ±5°C uniformity across build surface',
            target_components=['Heated Build Platform', 'Temperature Controllers'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-019'],
            estimated_duration_hours=6.0,
            required_equipment=['Thermal Camera', 'Thermocouple Grid'],
            acceptance_criteria='±5°C uniformity at 200°C setpoint'
        )
        
        self.tests['TE-022'] = TestDefinition(
            test_id='TE-022',
            test_name='Bed Heating Rate',
            test_purpose='Measure time to reach operating temperature',
            target_components=['Heated Build Platform', 'Silicon Heating Plates'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-021'],
            estimated_duration_hours=3.0,
            required_equipment=['Data Logger', 'Power Meter'],
            acceptance_criteria='<10 min to 200°C, <2kW power'
        )
        
        # Cooling System Tests
        self.tests['TE-023'] = TestDefinition(
            test_id='TE-023',
            test_name='Water Cooling Capacity',
            test_purpose='Verify cooling system heat removal capability',
            target_components=['Water Pumps', 'Radiator Fans', 'Water Cooling Blocks'],
            verification_type=VerificationType.PERFORMANCE,
            estimated_duration_hours=4.0,
            required_equipment=['Flow Meter', 'Thermocouples', 'Heat Load Bank'],
            acceptance_criteria='>10kW heat removal at 30°C ambient'
        )
        
        self.tests['TE-024'] = TestDefinition(
            test_id='TE-024',
            test_name='Cooling System Flow Rate',
            test_purpose='Verify required flow rates to all components',
            target_components=['Water Pumps', 'Flow Regulators'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=2.0,
            required_equipment=['Flow Meters', 'Pressure Gauges'],
            acceptance_criteria='2-5 L/min per circuit, <2 bar pressure'
        )
        
        self.tests['TE-025'] = TestDefinition(
            test_id='TE-025',
            test_name='Cooling System Leak Test',
            test_purpose='Verify all connections are leak-free',
            target_components=['Water Cooling Blocks', 'Fittings 1/2 NPT to 3/8 Barb'],
            verification_type=VerificationType.SAFETY,
            prerequisite_tests=['TE-024'],
            estimated_duration_hours=3.0,
            required_equipment=['Pressure Test Kit', 'Leak Detection Fluid'],
            acceptance_criteria='No leaks at 3 bar for 24 hours'
        )
        
        # Insulation Tests
        self.tests['TE-026'] = TestDefinition(
            test_id='TE-026',
            test_name='Ceramic Insulation Performance',
            test_purpose='Test thermal barrier effectiveness',
            target_components=['Ceramic Fiber Blanket', 'Ceramic Insulation Plates'],
            verification_type=VerificationType.PERFORMANCE,
            estimated_duration_hours=8.0,
            required_equipment=['Thermal Chamber', 'Heat Flux Sensors'],
            acceptance_criteria='<50W/m² heat flux at 1000°C delta'
        )
        
        self.tests['TE-027'] = TestDefinition(
            test_id='TE-027',
            test_name='Insulation Mechanical Integrity',
            test_purpose='Verify insulation withstands thermal cycling',
            target_components=['Ceramic Fiber Blanket', 'Ceramic Insulation Plates'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-026'],
            estimated_duration_hours=24.0,
            required_equipment=['Thermal Cycling Chamber', 'Visual Inspection Tools'],
            acceptance_criteria='No cracking/degradation after 100 cycles'
        )
        
        # Temperature Control Tests
        self.tests['TE-028'] = TestDefinition(
            test_id='TE-028',
            test_name='PID Controller Tuning',
            test_purpose='Optimize temperature control parameters',
            target_components=['Temperature Controllers'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-019', 'TE-020'],
            estimated_duration_hours=6.0,
            required_equipment=['Process Simulator', 'Data Logger'],
            acceptance_criteria='<2% overshoot, <1°C steady-state error'
        )
        
        self.tests['TE-029'] = TestDefinition(
            test_id='TE-029',
            test_name='Multi-Zone Control Coordination',
            test_purpose='Test interaction between temperature zones',
            target_components=['Temperature Controllers', 'Heated Build Platform', 'Thermal Cameras'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-028'],
            estimated_duration_hours=4.0,
            required_equipment=['Multi-channel Recorder', 'Thermal Loads'],
            acceptance_criteria='Independent zone control ±3°C'
        )
        
        self.tests['TE-030'] = TestDefinition(
            test_id='TE-030',
            test_name='Thermal Subsystem Response Time',
            test_purpose='Measure control loop response to disturbances',
            target_components=['Temperature Controllers', 'Thermal Cameras', 'Control System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-018', 'TE-029'],
            estimated_duration_hours=3.0,
            required_equipment=['Signal Generator', 'Fast Recorder'],
            acceptance_criteria='<200ms to detect and respond'
        )
    
    def _initialize_crucible_tests(self):
        """TE-031 to TE-040: Crucible & Droplet Generation Tests"""
        
        self.tests['TE-031'] = TestDefinition(
            test_id='TE-031',
            test_name='Crucible Temperature Range',
            test_purpose='Verify 700-1580°C operation per SR003',
            target_components=['Graphite Crucibles', 'Induction Heater Module'],
            verification_type=VerificationType.PERFORMANCE,
            estimated_duration_hours=8.0,
            required_equipment=['Optical Pyrometer', 'Induction Power Supply'],
            acceptance_criteria='Stable operation 700-1580°C ±10°C'
        )
        
        self.tests['TE-032'] = TestDefinition(
            test_id='TE-032',
            test_name='Crucible Heating Rate',
            test_purpose='Measure time to reach melting temperature',
            target_components=['Induction Heater Module', 'Induction Coils'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-031'],
            estimated_duration_hours=4.0,
            required_equipment=['Power Analyzer', 'Temperature Logger'],
            acceptance_criteria='<15 min to 1580°C, <25kW power'
        )
        
        self.tests['TE-033'] = TestDefinition(
            test_id='TE-033',
            test_name='Droplet Generation Consistency',
            test_purpose='Verify repeatable droplet size and timing',
            target_components=['Piezo Droplet Dispensers', 'Graphite Crucibles'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-031'],
            enables_tests=['TE-059'],
            estimated_duration_hours=6.0,
            required_equipment=['High-Speed Camera', 'Image Analysis Software'],
            acceptance_criteria='±5% size variation, ±1ms timing'
        )
        
        self.tests['TE-034'] = TestDefinition(
            test_id='TE-034',
            test_name='Piezo Dispenser Frequency Response',
            test_purpose='Characterize dispenser actuation dynamics',
            target_components=['Piezo Droplet Dispensers', 'Piezo Drivers'],
            verification_type=VerificationType.PERFORMANCE,
            estimated_duration_hours=3.0,
            required_equipment=['Function Generator', 'Laser Vibrometer'],
            acceptance_criteria='10-1000Hz operation, <0.1ms response'
        )
        
        self.tests['TE-035'] = TestDefinition(
            test_id='TE-035',
            test_name='Material Feed System',
            test_purpose='Test wire feeder operation and control',
            target_components=['Material Wire Feeders', 'Linear Actuators'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=4.0,
            required_equipment=['Force Gauge', 'Position Encoder'],
            acceptance_criteria='0.1-10mm/s feed rate, ±0.01mm position'
        )
        
        self.tests['TE-036'] = TestDefinition(
            test_id='TE-036',
            test_name='Crucible-Induction Coupling',
            test_purpose='Verify efficient power transfer',
            target_components=['Graphite Crucibles', 'Induction Coils'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-031'],
            estimated_duration_hours=3.0,
            required_equipment=['Power Meter', 'Thermal Camera'],
            acceptance_criteria='>85% coupling efficiency'
        )
        
        self.tests['TE-037'] = TestDefinition(
            test_id='TE-037',
            test_name='Multi-Material Capability',
            test_purpose='Test switching between Al and Steel',
            target_components=['Graphite Crucibles', 'Material Wire Feeders'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-033', 'TE-035'],
            estimated_duration_hours=6.0,
            required_equipment=['Material Samples', 'Chemical Analysis Kit'],
            acceptance_criteria='<5 min changeover, <0.1% contamination'
        )
        
        self.tests['TE-038'] = TestDefinition(
            test_id='TE-038',
            test_name='Crucible Thermal Shock',
            test_purpose='Verify crucible survives rapid temperature changes',
            target_components=['Graphite Crucibles'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-031'],
            estimated_duration_hours=12.0,
            required_equipment=['Thermal Shock Chamber', 'Crack Detection Kit'],
            acceptance_criteria='No cracks after 50 cycles to 1580°C'
        )
        
        self.tests['TE-039'] = TestDefinition(
            test_id='TE-039',
            test_name='Induction Field Containment',
            test_purpose='Verify magnetic field safety limits',
            target_components=['Induction Heater Module', 'Magnetic Shielding'],
            verification_type=VerificationType.SAFETY,
            estimated_duration_hours=3.0,
            required_equipment=['Gauss Meter', 'Field Mapping System'],
            acceptance_criteria='<1mT at 30cm distance'
        )
        
        self.tests['TE-040'] = TestDefinition(
            test_id='TE-040',
            test_name='Droplet Temperature Measurement',
            test_purpose='Validate pyrometer readings of droplets',
            target_components=['Pyrometers', 'Graphite Crucibles'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-033'],
            estimated_duration_hours=4.0,
            required_equipment=['Reference Pyrometer', 'Thermocouple Probe'],
            acceptance_criteria='±20°C accuracy on 2mm droplets'
        )
    
    def _initialize_power_tests(self):
        """TE-041 to TE-050: Power & Electrical Tests"""
        
        self.tests['TE-041'] = TestDefinition(
            test_id='TE-041',
            test_name='Main Power Supply Load Test',
            test_purpose='Verify 10kW continuous output capability',
            target_components=['Mean Well RSP-10000-48'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=4.0,
            required_equipment=['Electronic Load Bank', 'Power Analyzer'],
            acceptance_criteria='10kW at 48V, <2% ripple, >94% efficiency'
        )
        
        self.tests['TE-042'] = TestDefinition(
            test_id='TE-042',
            test_name='Power Supply Protection Features',
            test_purpose='Test OVP, OCP, OTP protection circuits',
            target_components=['Mean Well RSP-10000-48'],
            verification_type=VerificationType.SAFETY,
            prerequisite_tests=['TE-041'],
            estimated_duration_hours=3.0,
            required_equipment=['Variable Load', 'Oscilloscope', 'Heat Gun'],
            acceptance_criteria='All protections trigger within spec'
        )
        
        self.tests['TE-043'] = TestDefinition(
            test_id='TE-043',
            test_name='DC-DC Converter Verification',
            test_purpose='Test all voltage conversion stages',
            target_components=['DC-DC Converters 48V to 24V', 'DC-DC Converters 48V to 12V'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=3.0,
            required_equipment=['Electronic Loads', 'Multimeters'],
            acceptance_criteria='Output regulation ±2%, >90% efficiency'
        )
        
        self.tests['TE-044'] = TestDefinition(
            test_id='TE-044',
            test_name='UPS Battery Backup Test',
            test_purpose='Verify control system backup power',
            target_components=['UPS Battery Backup 3kVA'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=4.0,
            required_equipment=['AC Load Bank', 'Power Monitor'],
            acceptance_criteria='>15 min runtime at 1kW load'
        )
        
        self.tests['TE-045'] = TestDefinition(
            test_id='TE-045',
            test_name='Power Distribution Verification',
            test_purpose='Test all circuit breakers and distribution',
            target_components=['Circuit Breakers 3-phase 100A', 'Fuses 250V 10A'],
            verification_type=VerificationType.SAFETY,
            estimated_duration_hours=6.0,
            required_equipment=['Current Injection Set', 'Insulation Tester'],
            acceptance_criteria='Trip curves within spec, >1MΩ insulation'
        )
        
        self.tests['TE-046'] = TestDefinition(
            test_id='TE-046',
            test_name='Emergency Stop Circuit',
            test_purpose='Verify E-stop cuts all hazardous power',
            target_components=['Emergency Stop System', 'Circuit Breakers 3-phase 100A'],
            verification_type=VerificationType.SAFETY,
            estimated_duration_hours=2.0,
            required_equipment=['Circuit Tester', 'Response Timer'],
            acceptance_criteria='<100ms power cutoff, fail-safe operation'
        )
        
        self.tests['TE-047'] = TestDefinition(
            test_id='TE-047',
            test_name='Ground Fault Protection',
            test_purpose='Test GFCI and ground monitoring',
            target_components=['Circuit Breakers 3-phase 100A', 'Emergency Stop System'],
            verification_type=VerificationType.SAFETY,
            prerequisite_tests=['TE-045'],
            estimated_duration_hours=3.0,
            required_equipment=['Ground Fault Tester', 'Megohmmeter'],
            acceptance_criteria='GFCI trips at 30mA, <0.1Ω ground'
        )
        
        self.tests['TE-048'] = TestDefinition(
            test_id='TE-048',
            test_name='Power Quality Analysis',
            test_purpose='Measure harmonics and power factor',
            target_components=['Mean Well RSP-10000-48', 'Induction Heater Module'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-041'],
            estimated_duration_hours=4.0,
            required_equipment=['Power Quality Analyzer', 'Current Probes'],
            acceptance_criteria='THD <5%, PF >0.95'
        )
        
        self.tests['TE-049'] = TestDefinition(
            test_id='TE-049',
            test_name='Inrush Current Measurement',
            test_purpose='Verify soft-start and inrush limiting',
            target_components=['Mean Well RSP-10000-48', 'Induction Heater Module'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=2.0,
            required_equipment=['Current Probe', 'Storage Oscilloscope'],
            acceptance_criteria='Inrush <50A peak, <10ms duration'
        )
        
        self.tests['TE-050'] = TestDefinition(
            test_id='TE-050',
            test_name='Cable and Connector Test',
            test_purpose='Verify all power cables rated for load',
            target_components=['Power Cables AWG 2', 'Anderson Connectors 175A'],
            verification_type=VerificationType.SAFETY,
            estimated_duration_hours=4.0,
            required_equipment=['Micro-ohmmeter', 'Thermal Camera', 'Current Source'],
            acceptance_criteria='<40°C rise at rated current'
        )
    
    def _initialize_sensor_tests(self):
        """TE-051 to TE-060: Sensor & Measurement Tests"""
        
        self.tests['TE-051'] = TestDefinition(
            test_id='TE-051',
            test_name='Load Cell Calibration',
            test_purpose='Calibrate force measurement system',
            target_components=['Load Cells 50kg'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=3.0,
            required_equipment=['Calibration Weights', 'Dead Weight Tester'],
            acceptance_criteria='±0.1% accuracy, <0.02% hysteresis'
        )
        
        self.tests['TE-052'] = TestDefinition(
            test_id='TE-052',
            test_name='Accelerometer Characterization',
            test_purpose='Verify vibration measurement capability',
            target_components=['Accelerometers 3-axis'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=3.0,
            required_equipment=['Vibration Calibrator', 'Spectrum Analyzer'],
            acceptance_criteria='1-10kHz response, ±5% accuracy'
        )
        
        self.tests['TE-053'] = TestDefinition(
            test_id='TE-053',
            test_name='Humidity Sensor Verification',
            test_purpose='Test environmental monitoring accuracy',
            target_components=['Humidity Sensors'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=2.0,
            required_equipment=['Humidity Chamber', 'Reference Hygrometer'],
            acceptance_criteria='±3% RH accuracy, 10-90% range'
        )
        
        self.tests['TE-054'] = TestDefinition(
            test_id='TE-054',
            test_name='Gas Flow Sensor Calibration',
            test_purpose='Calibrate shield gas flow measurement',
            target_components=['Gas Flow Sensors'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=3.0,
            required_equipment=['Flow Calibrator', 'Reference Flow Meter'],
            acceptance_criteria='±2% accuracy, 0.1-10 L/min range'
        )
        
        self.tests['TE-055'] = TestDefinition(
            test_id='TE-055',
            test_name='Sensor Data Acquisition',
            test_purpose='Verify all sensors integrate with DAQ',
            target_components=['Control System', 'All Sensors'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-051', 'TE-052', 'TE-053', 'TE-054'],
            estimated_duration_hours=4.0,
            required_equipment=['Signal Generator', 'Protocol Analyzer'],
            acceptance_criteria='All channels functional, <10ms latency'
        )
        
        self.tests['TE-056'] = TestDefinition(
            test_id='TE-056',
            test_name='Acoustic Levitation Force Measurement',
            test_purpose='Calibrate force vs position relationship',
            target_components=['Load Cells 50kg', '40kHz Transducers', 'Phase Array Controller'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-006', 'TE-051'],
            estimated_duration_hours=6.0,
            required_equipment=['Precision Positioner', 'Force Gauge'],
            acceptance_criteria='Force model ±10% accuracy'
        )
        
        self.tests['TE-057'] = TestDefinition(
            test_id='TE-057',
            test_name='Position Sensing Accuracy',
            test_purpose='Verify droplet position measurement',
            target_components=['Thermal Cameras', 'Control System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-013', 'TE-018'],
            estimated_duration_hours=4.0,
            required_equipment=['Calibration Target', 'Linear Stage'],
            acceptance_criteria='±0.1mm accuracy in 3D space'
        )
        
        self.tests['TE-058'] = TestDefinition(
            test_id='TE-058',
            test_name='Thermal Gradient Measurement',
            test_purpose='Map temperature fields in chamber',
            target_components=['Thermal Cameras', 'Thermocouples Type K'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-018', 'TE-019'],
            estimated_duration_hours=8.0,
            required_equipment=['Heat Source Array', '3D Positioning System'],
            acceptance_criteria='±5°C agreement camera vs thermocouple'
        )
        
        self.tests['TE-059'] = TestDefinition(
            test_id='TE-059',
            test_name='Droplet Size Measurement',
            test_purpose='Calibrate optical droplet sizing',
            target_components=['Thermal Cameras', 'Piezo Droplet Dispensers'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-033'],
            estimated_duration_hours=4.0,
            required_equipment=['Calibration Spheres', 'Microscope'],
            acceptance_criteria='±0.05mm size accuracy'
        )
        
        self.tests['TE-060'] = TestDefinition(
            test_id='TE-060',
            test_name='Sensor Noise Characterization',
            test_purpose='Measure noise floor of all sensors',
            target_components=['All Sensors', 'Control System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-055'],
            estimated_duration_hours=6.0,
            required_equipment=['Shielded Chamber', 'Spectrum Analyzer'],
            acceptance_criteria='SNR >40dB for all channels'
        )
    
    def _initialize_control_tests(self):
        """TE-061 to TE-070: Control System Tests"""
        
        self.tests['TE-061'] = TestDefinition(
            test_id='TE-061',
            test_name='STM32 Controller Functionality',
            test_purpose='Verify main controller operation',
            target_components=['STM32F7 Controllers'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=4.0,
            required_equipment=['JTAG Debugger', 'Logic Analyzer'],
            acceptance_criteria='All peripherals functional, RTOS stable'
        )
        
        self.tests['TE-062'] = TestDefinition(
            test_id='TE-062',
            test_name='Raspberry Pi Vision Processing',
            test_purpose='Test image processing performance',
            target_components=['Raspberry Pi 4 8GB'],
            verification_type=VerificationType.PERFORMANCE,
            estimated_duration_hours=3.0,
            required_equipment=['Test Image Set', 'Performance Monitor'],
            acceptance_criteria='30fps processing at 640x480'
        )
        
        self.tests['TE-063'] = TestDefinition(
            test_id='TE-063',
            test_name='FPGA Configuration',
            test_purpose='Verify FPGA loads and operates correctly',
            target_components=['Phase Array Controller'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-012'],
            estimated_duration_hours=3.0,
            required_equipment=['JTAG Programmer', 'Test Vectors'],
            acceptance_criteria='Configuration success, timing met'
        )
        
        self.tests['TE-064'] = TestDefinition(
            test_id='TE-064',
            test_name='Control Network Communication',
            test_purpose='Test all communication interfaces',
            target_components=['Control System', 'Ethernet Switches'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=4.0,
            required_equipment=['Network Analyzer', 'Protocol Tester'],
            acceptance_criteria='<1ms latency, no packet loss'
        )
        
        self.tests['TE-065'] = TestDefinition(
            test_id='TE-065',
            test_name='Real-Time Performance',
            test_purpose='Verify control loop timing requirements',
            target_components=['Control System', 'STM32F7 Controllers'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-061', 'TE-064'],
            estimated_duration_hours=6.0,
            required_equipment=['Real-Time Analyzer', 'Timing Generator'],
            acceptance_criteria='Deterministic <3ms loop, <100μs jitter'
        )
        
        self.tests['TE-066'] = TestDefinition(
            test_id='TE-066',
            test_name='Control Algorithm Validation',
            test_purpose='Test predictive control algorithms',
            target_components=['Control System'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-065'],
            enables_tests=['TE-077'],
            estimated_duration_hours=8.0,
            required_equipment=['Simulation Environment', 'Test Scenarios'],
            acceptance_criteria='±0.3mm accuracy in all test cases'
        )
        
        self.tests['TE-067'] = TestDefinition(
            test_id='TE-067',
            test_name='HMI Interface Testing',
            test_purpose='Verify operator interface functionality',
            target_components=['HMI Touch Screen 15 inch', 'Control System'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=4.0,
            required_equipment=['Touch Tester', 'UI Test Scripts'],
            acceptance_criteria='All functions accessible, <200ms response'
        )
        
        self.tests['TE-068'] = TestDefinition(
            test_id='TE-068',
            test_name='Data Logging Verification',
            test_purpose='Test data recording and retrieval',
            target_components=['Control System', 'SSD 1TB Industrial'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=3.0,
            required_equipment=['Data Generator', 'Analysis Tools'],
            acceptance_criteria='No data loss, 1kHz logging rate'
        )
        
        self.tests['TE-069'] = TestDefinition(
            test_id='TE-069',
            test_name='Fault Detection and Recovery',
            test_purpose='Test error handling and recovery',
            target_components=['Control System', 'Emergency Stop System'],
            verification_type=VerificationType.SAFETY,
            prerequisite_tests=['TE-046'],
            estimated_duration_hours=6.0,
            required_equipment=['Fault Injection Tools', 'System Monitor'],
            acceptance_criteria='All faults detected, safe shutdown'
        )
        
        self.tests['TE-070'] = TestDefinition(
            test_id='TE-070',
            test_name='Software Update Process',
            test_purpose='Verify OTA update capability',
            target_components=['Control System', 'STM32F7 Controllers', 'Raspberry Pi 4 8GB'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=3.0,
            required_equipment=['Update Server', 'Version Control'],
            acceptance_criteria='Updates without data loss, rollback works'
        )
    
    def _initialize_chamber_tests(self):
        """TE-071 to TE-075: Chamber & Environmental Tests"""
        
        self.tests['TE-071'] = TestDefinition(
            test_id='TE-071',
            test_name='Chamber Leak Test',
            test_purpose='Verify chamber seal integrity',
            target_components=['Aluminum Chamber Walls', 'Chamber Door Seals'],
            verification_type=VerificationType.FUNCTIONAL,
            estimated_duration_hours=4.0,
            required_equipment=['Leak Detector', 'Pressure Gauge'],
            acceptance_criteria='<0.1 L/min at 100Pa differential'
        )
        
        self.tests['TE-072'] = TestDefinition(
            test_id='TE-072',
            test_name='HEPA Filter Performance',
            test_purpose='Verify MERV 13 filtration per SR015',
            target_components=['HEPA Filters MERV 13'],
            verification_type=VerificationType.PERFORMANCE,
            estimated_duration_hours=3.0,
            required_equipment=['Particle Counter', 'Aerosol Generator'],
            acceptance_criteria='>99.97% at 0.3μm particles'
        )
        
        self.tests['TE-073'] = TestDefinition(
            test_id='TE-073',
            test_name='Exhaust System Flow',
            test_purpose='Verify proper ventilation flow rates',
            target_components=['Exhaust Blowers', 'Dampers Motorized'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-072'],
            estimated_duration_hours=3.0,
            required_equipment=['Anemometer', 'Smoke Generator'],
            acceptance_criteria='10 air changes/hour, uniform flow'
        )
        
        self.tests['TE-074'] = TestDefinition(
            test_id='TE-074',
            test_name='Chamber Temperature Limits',
            test_purpose='Verify chamber walls <300°C per SR009',
            target_components=['Aluminum Chamber Walls', 'Ceramic Fiber Blanket'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-026'],
            estimated_duration_hours=6.0,
            required_equipment=['Thermocouple Array', 'Heat Source'],
            acceptance_criteria='All surfaces <300°C during operation'
        )
        
        self.tests['TE-075'] = TestDefinition(
            test_id='TE-075',
            test_name='Shield Gas Distribution',
            test_purpose='Verify uniform inert gas coverage',
            target_components=['Gas Manifolds', 'Gas Flow Sensors'],
            verification_type=VerificationType.FUNCTIONAL,
            prerequisite_tests=['TE-054'],
            estimated_duration_hours=4.0,
            required_equipment=['O2 Analyzer', 'Smoke Visualization'],
            acceptance_criteria='<1% O2 in work zone'
        )
    
    def _initialize_integration_tests(self):
        """TE-076 to TE-080: System Integration Tests"""
        
        self.tests['TE-076'] = TestDefinition(
            test_id='TE-076',
            test_name='Acoustic-Thermal Integration',
            test_purpose='Test interaction between subsystems',
            target_components=['40kHz Transducers', 'Thermal Cameras', 'Control System'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-013', 'TE-030'],
            estimated_duration_hours=8.0,
            required_equipment=['Integration Test Rig', 'Data Logger'],
            acceptance_criteria='No thermal drift in acoustic performance'
        )
        
        self.tests['TE-077'] = TestDefinition(
            test_id='TE-077',
            test_name='Full Control Loop Test',
            test_purpose='End-to-end control system verification',
            target_components=['Control System', 'All Subsystems'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-066'],
            enables_tests=['TE-081'],
            estimated_duration_hours=12.0,
            required_equipment=['Complete System', 'Test Materials'],
            acceptance_criteria='Stable droplet control for 1 hour'
        )
        
        self.tests['TE-078'] = TestDefinition(
            test_id='TE-078',
            test_name='Multi-Droplet Coordination',
            test_purpose='Test parallel droplet control',
            target_components=['Control System', 'Phase Array Controller'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-077'],
            estimated_duration_hours=6.0,
            required_equipment=['Multiple Dispensers', 'Tracking System'],
            acceptance_criteria='5 droplets controlled simultaneously'
        )
        
        self.tests['TE-079'] = TestDefinition(
            test_id='TE-079',
            test_name='Power System Integration',
            test_purpose='Test all power consumers together',
            target_components=['Mean Well RSP-10000-48', 'All Power Consumers'],
            verification_type=VerificationType.INTEGRATION,
            prerequisite_tests=['TE-048'],
            estimated_duration_hours=8.0,
            required_equipment=['Power Monitor', 'Thermal Camera'],
            acceptance_criteria='<10kW total, no overheating'
        )
        
        self.tests['TE-080'] = TestDefinition(
            test_id='TE-080',
            test_name='Safety Interlock Verification',
            test_purpose='Test all safety systems integration',
            target_components=['Emergency Stop System', 'All Safety Sensors'],
            verification_type=VerificationType.SAFETY,
            prerequisite_tests=['TE-046', 'TE-069'],
            estimated_duration_hours=6.0,
            required_equipment=['Interlock Tester', 'Fault Scenarios'],
            acceptance_criteria='All interlocks prevent unsafe operation'
        )
    
    def _initialize_performance_tests(self):
        """TE-081 to TE-085: System Performance Tests"""
        
        self.tests['TE-081'] = TestDefinition(
            test_id='TE-081',
            test_name='Droplet Placement Accuracy',
            test_purpose='Measure overall system accuracy',
            target_components=['Complete System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-077'],
            estimated_duration_hours=8.0,
            required_equipment=['Coordinate Measuring Machine', 'Test Patterns'],
            acceptance_criteria='±0.3mm over 200x200x200mm per SR002'
        )
        
        self.tests['TE-082'] = TestDefinition(
            test_id='TE-082',
            test_name='Build Speed Measurement',
            test_purpose='Quantify deposition rate',
            target_components=['Complete System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-081'],
            estimated_duration_hours=12.0,
            required_equipment=['Scale', 'Timer', 'Test Geometry'],
            acceptance_criteria='>10g/min deposition rate'
        )
        
        self.tests['TE-083'] = TestDefinition(
            test_id='TE-083',
            test_name='Cooling Rate Verification',
            test_purpose='Confirm >1000°C/s cooling per SR010',
            target_components=['Complete System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-040', 'TE-081'],
            estimated_duration_hours=6.0,
            required_equipment=['High-Speed Pyrometer', 'Data Logger'],
            acceptance_criteria='>1000°C/s measured on droplets'
        )
        
        self.tests['TE-084'] = TestDefinition(
            test_id='TE-084',
            test_name='Material Quality Assessment',
            test_purpose='Verify deposited material properties',
            target_components=['Complete System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-082'],
            estimated_duration_hours=16.0,
            required_equipment=['Microscope', 'Hardness Tester', 'Tensile Tester'],
            acceptance_criteria='Density >98%, grain size <50μm'
        )
        
        self.tests['TE-085'] = TestDefinition(
            test_id='TE-085',
            test_name='Process Repeatability',
            test_purpose='Measure consistency across builds',
            target_components=['Complete System'],
            verification_type=VerificationType.PERFORMANCE,
            prerequisite_tests=['TE-084'],
            estimated_duration_hours=40.0,
            required_equipment=['Metrology Tools', 'Statistical Software'],
            acceptance_criteria='Cpk >1.33 for critical dimensions'
        )
    
    def _initialize_endurance_tests(self):
        """TE-086 to TE-095: Endurance & Reliability Tests"""
        
        self.tests['TE-086'] = TestDefinition(
            test_id='TE-086',
            test_name='Power Supply Endurance',
            test_purpose='Long-term stability test',
            target_components=['Mean Well RSP-10000-48'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-041'],
            estimated_duration_hours=168.0,  # 1 week
            required_equipment=['Data Logger', 'Load Bank'],
            acceptance_criteria='<1% drift over 168 hours'
        )
        
        self.tests['TE-087'] = TestDefinition(
            test_id='TE-087',
            test_name='Transducer Lifetime',
            test_purpose='Verify 10,000 hour operation',
            target_components=['40kHz Transducers'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-004'],
            estimated_duration_hours=1000.0,  # Accelerated test
            required_equipment=['Life Test Rig', 'Monitoring System'],
            acceptance_criteria='<10% performance degradation'
        )
        
        self.tests['TE-088'] = TestDefinition(
            test_id='TE-088',
            test_name='Crucible Durability',
            test_purpose='Test crucible lifetime',
            target_components=['Graphite Crucibles'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-038'],
            estimated_duration_hours=200.0,
            required_equipment=['Automated Test Rig', 'Inspection Tools'],
            acceptance_criteria='>500 thermal cycles'
        )
        
        self.tests['TE-089'] = TestDefinition(
            test_id='TE-089',
            test_name='Cooling System Endurance',
            test_purpose='Verify long-term cooling reliability',
            target_components=['Water Pumps', 'Radiator Fans'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-023'],
            estimated_duration_hours=500.0,
            required_equipment=['Flow Monitors', 'Temperature Logger'],
            acceptance_criteria='No degradation over 500 hours'
        )
        
        self.tests['TE-090'] = TestDefinition(
            test_id='TE-090',
            test_name='Control System Stability',
            test_purpose='Long-term software stability',
            target_components=['Control System'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-070'],
            estimated_duration_hours=720.0,  # 30 days
            required_equipment=['Monitoring Software', 'Stress Test Suite'],
            acceptance_criteria='No crashes or memory leaks'
        )
        
        self.tests['TE-091'] = TestDefinition(
            test_id='TE-091',
            test_name='Piezo Dispenser Lifetime',
            test_purpose='Verify dispenser reliability',
            target_components=['Piezo Droplet Dispensers'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-034'],
            estimated_duration_hours=200.0,
            required_equipment=['Cycle Counter', 'Performance Monitor'],
            acceptance_criteria='>10 million actuations'
        )
        
        self.tests['TE-092'] = TestDefinition(
            test_id='TE-092',
            test_name='Filter Life Testing',
            test_purpose='Determine filter replacement interval',
            target_components=['HEPA Filters MERV 13'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-072'],
            estimated_duration_hours=1000.0,
            required_equipment=['Particle Counter', 'Pressure Monitor'],
            acceptance_criteria='>2000 hours before replacement'
        )
        
        self.tests['TE-093'] = TestDefinition(
            test_id='TE-093',
            test_name='Thermal Camera Stability',
            test_purpose='Long-term calibration stability',
            target_components=['Thermal Cameras'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-016'],
            estimated_duration_hours=720.0,
            required_equipment=['Blackbody Reference', 'Drift Monitor'],
            acceptance_criteria='<1°C drift over 720 hours'
        )
        
        self.tests['TE-094'] = TestDefinition(
            test_id='TE-094',
            test_name='Mechanical Wear Testing',
            test_purpose='Assess moving parts durability',
            target_components=['Linear Actuators', 'Dampers Motorized'],
            verification_type=VerificationType.ENDURANCE,
            estimated_duration_hours=500.0,
            required_equipment=['Cycle Counter', 'Wear Gauge'],
            acceptance_criteria='<0.1mm wear after 100k cycles'
        )
        
        self.tests['TE-095'] = TestDefinition(
            test_id='TE-095',
            test_name='Full System Endurance',
            test_purpose='Continuous operation test',
            target_components=['Complete System'],
            verification_type=VerificationType.ENDURANCE,
            prerequisite_tests=['TE-085'],
            estimated_duration_hours=168.0,  # 1 week
            required_equipment=['Full Monitoring Suite', 'Test Parts'],
            acceptance_criteria='168 hours without intervention'
        )
    
    def _initialize_validation_tests(self):
        """TE-096 to TE-100: Final Validation Tests"""
        
        self.tests['TE-096'] = TestDefinition(
            test_id='TE-096',
            test_name='Reference Part Production',
            test_purpose='Build qualification parts',
            target_components=['Complete System'],
            verification_type=VerificationType.ACCEPTANCE,
            prerequisite_tests=['TE-095'],
            estimated_duration_hours=24.0,
            required_equipment=['Reference CAD Models', 'Inspection Tools'],
            acceptance_criteria='Parts meet all specifications'
        )
        
        self.tests['TE-097'] = TestDefinition(
            test_id='TE-097',
            test_name='Multi-Material Validation',
            test_purpose='Verify material switching capability',
            target_components=['Complete System'],
            verification_type=VerificationType.ACCEPTANCE,
            prerequisite_tests=['TE-096'],
            estimated_duration_hours=12.0,
            required_equipment=['Al and Steel Wire', 'Chemical Analysis'],
            acceptance_criteria='Clean material transitions'
        )
        
        self.tests['TE-098'] = TestDefinition(
            test_id='TE-098',
            test_name='Operator Training Validation',
            test_purpose='Verify system usability',
            target_components=['Complete System', 'HMI Touch Screen 15 inch'],
            verification_type=VerificationType.ACCEPTANCE,
            prerequisite_tests=['TE-067'],
            estimated_duration_hours=16.0,
            required_equipment=['Training Materials', 'Test Operators'],
            acceptance_criteria='Operators build parts successfully'
        )
        
        self.tests['TE-099'] = TestDefinition(
            test_id='TE-099',
            test_name='Documentation Verification',
            test_purpose='Ensure all documentation complete',
            target_components=['Complete System'],
            verification_type=VerificationType.ACCEPTANCE,
            estimated_duration_hours=8.0,
            required_equipment=['Document Checklist', 'Review Team'],
            acceptance_criteria='All required documents present'
        )
        
        self.tests['TE-100'] = TestDefinition(
            test_id='TE-100',
            test_name='Final System Acceptance',
            test_purpose='Customer acceptance test',
            target_components=['Complete System'],
            verification_type=VerificationType.ACCEPTANCE,
            prerequisite_tests=['TE-096', 'TE-097', 'TE-098', 'TE-099'],
            estimated_duration_hours=40.0,
            required_equipment=['Acceptance Test Plan', 'Customer Parts'],
            acceptance_criteria='All requirements verified'
        )
    
    def get_test(self, test_id):
        """Get a specific test definition"""
        return self.tests.get(test_id)
    
    def get_tests_for_component(self, component_name):
        """Get all tests that verify a specific component"""
        component_tests = []
        for test in self.tests.values():
            if component_name in test.target_components:
                component_tests.append(test)
        return component_tests
    
    def get_tests_by_type(self, verification_type):
        """Get all tests of a specific verification type"""
        return [test for test in self.tests.values() 
                if test.verification_type == verification_type]
    
    def get_prerequisite_chain(self, test_id):
        """Get all prerequisite tests recursively"""
        chain = []
        test = self.get_test(test_id)
        if test:
            for prereq_id in test.prerequisite_tests:
                chain.extend(self.get_prerequisite_chain(prereq_id))
                chain.append(prereq_id)
        return list(dict.fromkeys(chain))  # Remove duplicates while preserving order
    
    def export_test_registry(self):
        """Export test registry to JSON"""
        registry_data = {}
        for test_id, test in self.tests.items():
            registry_data[test_id] = test.to_dict()
        return registry_data