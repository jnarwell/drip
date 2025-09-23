# FLIR A35 Thermal Tracking System

## Overview

This is the **PRIMARY SENSOR** for the DRIP acoustic steering system. The FLIR A35 thermal camera provides real-time position (X,Y) and temperature data for falling molten metal droplets at 60Hz, enabling closed-loop acoustic field steering. Without this sensor, controlled droplet steering is not possible.

**Key Features:**
- 60Hz real-time droplet tracking
- Sub-millimeter position accuracy
- Multi-droplet tracking with Kalman filtering
- Direct FPGA integration via UDP
- Temperature measurement up to 1600°C
- GigE Vision interface for deterministic timing

## System Components

### Hardware
- **Camera**: FLIR A35 (320×256 @ 60Hz)
- **Interface**: Gigabit Ethernet (GigE Vision)
- **Power**: PoE+ or 12-24V DC
- **Cost**: $3,995

### Software Architecture
```
FLIR A35 → GigE → Thermal Tracker → UDP → FPGA
   ↓                    ↓                    ↓
Thermal     Blob Detection +      Acoustic Control
Images      Kalman Filtering         (X,Y,T data)
```

## Quick Start

### 1. Hardware Setup
```bash
# Connect camera to dedicated network interface
# Configure network (see docs/network_setup.md)
sudo ip addr add 192.168.1.100/24 dev eth1
sudo ip link set dev eth1 mtu 9000
```

### 2. Install Dependencies
```bash
# Install Spinnaker SDK (download from FLIR website)
cd ~/Downloads/spinnaker-*
sudo sh install_spinnaker.sh

# Install Python packages
pip install PySpin numpy opencv-python scipy matplotlib
```

### 3. Run Thermal Tracking
```bash
# Basic operation
./main_thermal_tracking.py

# With visualization
./main_thermal_tracking.py --visualize

# Run calibration first time
./main_thermal_tracking.py --calibrate
```

## Directory Structure

```
thermal_tracking/
├── README.md                    # This file
├── INSTALL.md                   # Detailed installation guide
├── main_thermal_tracking.py     # Main executable
├── code/
│   ├── thermal_droplet_tracker.py   # Core tracking algorithm
│   ├── thermal_visualizer.py        # Real-time visualization
│   └── fpga_thermal_interface.h     # FPGA integration header
├── calibration/
│   └── camera_calibration.py        # Pixel-to-mm calibration
├── config/
│   └── performance_config.py        # Performance optimization
└── docs/
    └── network_setup.md             # Network configuration guide
```

## Performance Specifications

| Parameter | Value |
|-----------|-------|
| Frame Rate | 60 Hz (16.67ms) |
| Resolution | 320×256 pixels |
| Position Accuracy | <1mm |
| Temperature Range | -40°C to 1600°C |
| Latency | <20ms total |
| Tracking Capacity | 10 simultaneous droplets |
| Network Bandwidth | ~10 MB/s |
| CPU Usage | <50% (single core) |

## Calibration

The system requires calibration to convert pixels to millimeters:

```bash
# Run calibration procedure
./main_thermal_tracking.py --calibrate

# Place 10×10mm heated target at center
# Follow on-screen instructions
# Calibration saved to calibration/camera_calibration.npy
```

## Integration with DRIP System

### FPGA Communication Protocol
The tracker sends UDP packets at 60Hz containing:
```c
typedef struct {
    uint32_t track_id;      // Unique droplet ID
    float x_mm;             // X position in mm
    float y_mm;             // Y position in mm  
    float z_mm;             // Z from acoustic model
    float temperature_c;    // Temperature in °C
    float velocity_x;       // X velocity in mm/s
    float velocity_y;       // Y velocity in mm/s
} DropletData;  // 28 bytes per droplet
```

### Control Loop Integration
```
Camera (60Hz) → Tracking (60Hz) → FPGA (60Hz) → Transducers (40kHz)
     16.7ms          <1ms            <1ms         25μs updates
```

## Troubleshooting

### Camera Not Found
- Check network cable and power
- Verify IP configuration: `ping 192.168.1.1`
- Check with discovery: `arv-tool-0.8`

### Low Frame Rate
- Enable jumbo frames: `sudo ip link set eth1 mtu 9000`
- Check CPU governor: `sudo cpupower frequency-set -g performance`
- Disable visualization: Remove `--visualize` flag

### Poor Tracking
- Recalibrate camera
- Check for obstructions or reflections
- Verify minimum temperature threshold
- Clean camera lens

### Network Issues
- Use dedicated NIC (not shared)
- Disable interrupt coalescing
- Increase receive buffers
- See `docs/network_setup.md`

## Command Line Options

```bash
./main_thermal_tracking.py --help

Options:
  --fpga-ip IP          FPGA IP address (default: 192.168.1.50)
  --fpga-port PORT      FPGA UDP port (default: 5000)
  --visualize           Enable real-time visualization
  --calibrate           Run calibration procedure
  --save-frames N       Save every Nth frame (0=disabled)
  --min-temp TEMP       Minimum temperature to track (°C)
```

## System Requirements

### Minimum
- Ubuntu 20.04 LTS
- 4 CPU cores
- 8GB RAM
- Gigabit Ethernet

### Recommended
- Ubuntu 22.04 LTS
- 8+ CPU cores
- 16GB RAM
- Dedicated GigE NIC
- SSD for frame logging

## Maintenance

### Daily
- Verify 60Hz operation
- Check tracking accuracy
- Monitor temperatures

### Weekly
- Clean camera lens
- Verify calibration
- Review error logs

### Monthly
- Full recalibration
- Update software
- Performance profiling

## Key Differences from Optris

| Feature | FLIR A35 | Optris Xi 400 |
|---------|----------|---------------|
| Purpose | Droplet tracking | Temperature only |
| Frame Rate | 60Hz optimized | 80Hz available |
| Integration | Direct FPGA path | General purpose |
| Cost | $3,995 | $4,000 |
| Software | Custom tracking | Generic SDK |

## Support Resources

### FLIR
- SDK Documentation: [Spinnaker SDK](https://www.flir.com/products/spinnaker-sdk/)
- Support: https://www.flir.com/support/
- Part Number: 436-0015-00

### DRIP Project
- GitHub Issues: Report bugs here
- Discord: #thermal-tracking channel
- Wiki: Additional documentation

## Critical Notes

1. **This enables acoustic steering** - Without position feedback, no trajectory control
2. **60Hz is mandatory** - Lower rates cause poor steering accuracy
3. **Calibration is critical** - Wrong scaling breaks position control
4. **Network must be dedicated** - Shared networks cause frame drops
5. **This is a real-time system** - Delays cascade to control instability

---

**Remember: This camera is what makes droplet control possible. Treat it as the critical sensor it is.**