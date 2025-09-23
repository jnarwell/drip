# FLIR A35 Thermal Tracking Installation Guide

## System Requirements

### Hardware
- FLIR A35 thermal camera (Part #436-0015-00)
- Dedicated gigabit Ethernet card
- PoE+ switch or 12-24V power supply
- Cat 6 Ethernet cable
- PC with Ubuntu 20.04+ (or compatible Linux)

### Software
- Python 3.8+
- FLIR Spinnaker SDK
- Git

## Step-by-Step Installation

### 1. Hardware Setup

#### Mount Camera
```
1. Position camera above levitation chamber
   - Clear view of entire work area
   - Perpendicular to levitation plane
   - Distance: 300-500mm typical
   
2. Secure mounting
   - Use vibration-dampened mount
   - Ensure no movement during operation
   - Cable strain relief
```

#### Connect Camera
```
1. Connect GigE cable to dedicated NIC
2. Connect power:
   - Option A: PoE+ switch
   - Option B: 12-24V DC power jack
3. Verify LED indicators:
   - Power LED: Solid green
   - Link LED: Blinking green
```

### 2. Network Configuration

Follow the detailed steps in [docs/network_setup.md](docs/network_setup.md)

Quick setup:
```bash
# Configure dedicated network interface
sudo nano /etc/netplan/02-camera-network.yaml

# Add configuration (replace eth1 with your interface):
network:
  version: 2
  renderer: networkd
  ethernets:
    eth1:
      addresses: [192.168.1.100/24]
      mtu: 9000

# Apply
sudo netplan apply

# Verify camera is reachable
ping 192.168.1.1
```

### 3. Install Spinnaker SDK

#### Download SDK
```bash
# Register at https://www.flir.com/products/spinnaker-sdk/
# Download Linux SDK (Ubuntu 20.04 version)
cd ~/Downloads
tar -xzf spinnaker-*.tar.gz
cd spinnaker-*-amd64/
```

#### Install Dependencies
```bash
# Install required packages
sudo apt-get install libusb-1.0-0 libpcre3 libpcre3-dev

# Install Spinnaker
sudo sh install_spinnaker.sh

# Answer prompts:
# - Add user to flirimaging group: yes
# - Install USB drivers: yes (even for GigE)
# - Set USB buffer size: yes
```

#### Verify Installation
```bash
# Logout and login for group changes
# Then test:
spinview

# Should open GUI and show camera
```

### 4. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv ~/venv/thermal_tracking
source ~/venv/thermal_tracking/bin/activate

# Install packages
pip install --upgrade pip
pip install numpy opencv-python matplotlib scipy
pip install PySpin  # From Spinnaker installation

# Test PySpin
python -c "import PySpin; print(PySpin.__version__)"
```

### 5. Install Thermal Tracking Software

```bash
# Clone repository
cd ~/Projects
git clone https://github.com/your-org/drip-acoustic-sysml.git
cd drip-acoustic-sysml/hardware/thermal_tracking

# Make main script executable
chmod +x main_thermal_tracking.py
```

### 6. Initial Camera Test

```bash
# Activate virtual environment
source ~/venv/thermal_tracking/bin/activate

# Run basic test
python3 -c "
import PySpin
system = PySpin.System.GetInstance()
cam_list = system.GetCameras()
print(f'Found {cam_list.GetSize()} camera(s)')
if cam_list.GetSize() > 0:
    cam = cam_list[0]
    cam.Init()
    print(f'Camera Model: {cam.GetUniqueID()}')
    cam.DeInit()
"
```

### 7. Calibration

```bash
# Run calibration procedure
./main_thermal_tracking.py --calibrate

# Follow on-screen instructions:
# 1. Place 10x10mm heated target at center
# 2. Heat to >600°C
# 3. Press Enter to capture
# 4. Verify calibration results
```

### 8. System Integration

#### Configure FPGA Communication
```bash
# Edit configuration if needed
nano config/system_config.json

{
  "fpga_ip": "192.168.1.50",
  "fpga_port": 5000,
  "camera_ip": "192.168.1.1",
  "min_temp_celsius": 600,
  "max_droplets": 10
}
```

#### Test Full System
```bash
# Run with visualization
./main_thermal_tracking.py --visualize

# Run in production mode (no visualization)
./main_thermal_tracking.py
```

### 9. Create systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/thermal-tracking.service

[Unit]
Description=FLIR A35 Thermal Droplet Tracking
After=network.target camera-network.service

[Service]
Type=simple
User=drip
WorkingDirectory=/home/drip/Projects/drip-acoustic-sysml/hardware/thermal_tracking
Environment="PATH=/home/drip/venv/thermal_tracking/bin"
ExecStart=/home/drip/venv/thermal_tracking/bin/python main_thermal_tracking.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable thermal-tracking.service
sudo systemctl start thermal-tracking.service

# Check status
sudo systemctl status thermal-tracking.service
```

## Verification Tests

### 1. Frame Rate Test
```bash
./main_thermal_tracking.py --save-frames 60

# Should maintain 60 FPS
# Check logs/ directory for saved frames
```

### 2. Tracking Accuracy Test
```bash
# Use heated target on XY stage
# Move in known pattern
# Verify position accuracy <1mm
```

### 3. Latency Test
```bash
# Monitor with tcpdump
sudo tcpdump -i eth1 -ttt host 192.168.1.1

# Should see consistent 16.67ms intervals (60Hz)
```

### 4. Multi-Droplet Test
```bash
# Heat multiple targets
# Verify all tracked simultaneously
# Check ID persistence
```

## Troubleshooting

### Camera Not Found
```bash
# Check network
ip addr show  # Verify interface configured
ping 192.168.1.1  # Verify camera reachable

# Check with arping
sudo arping -I eth1 192.168.1.1

# Reset camera to factory defaults if needed
```

### Low Frame Rate
```bash
# Check MTU
ip link show eth1 | grep mtu  # Should be 9000

# Check CPU
htop  # Monitor during operation

# Reduce visualization overhead
./main_thermal_tracking.py  # No --visualize flag
```

### Import Errors
```bash
# Verify virtual environment activated
which python  # Should show venv path

# Reinstall PySpin
pip uninstall PySpin
pip install PySpin
```

### Permission Errors
```bash
# Add user to flirimaging group
sudo usermod -a -G flirimaging $USER

# Logout and login again
```

## Performance Optimization

See [config/performance_config.py](config/performance_config.py) for advanced tuning:
- CPU affinity settings
- Network buffer optimization
- Real-time scheduling
- Memory locking

## Maintenance

### Daily
- Verify 60Hz operation
- Check camera lens for debris
- Monitor CPU/memory usage

### Weekly
- Clean lens with appropriate cloth
- Verify calibration with test target
- Check mounting stability

### Monthly
- Full calibration procedure
- Update software
- Review tracking logs

## Support

### FLIR Support
- Technical: https://www.flir.com/support-center/
- SDK Issues: Spinnaker forums

### DRIP System Support
- GitHub Issues: [your-repo]/issues
- Discord: #thermal-tracking channel

## Next Steps

1. Complete network optimization (network_setup.md)
2. Run calibration procedure
3. Integrate with FPGA control system
4. Set up monitoring and alerts
5. Train operators on troubleshooting