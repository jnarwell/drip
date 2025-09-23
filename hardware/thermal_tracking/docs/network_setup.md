# FLIR A35 Network Configuration Guide

## Overview

The FLIR A35 uses GigE Vision protocol which requires specific network configuration for optimal 60Hz performance. This guide covers dedicated network setup for reliable real-time thermal tracking.

## Hardware Requirements

- **Gigabit Ethernet NIC** (dedicated for camera)
- **Cat 6 or better cable** (< 100m length)
- **PoE+ injector or switch** (802.3at, 25.5W) *optional*

## Network Architecture

```
FLIR A35 (192.168.1.1) ─── GigE ──→ Dedicated NIC (192.168.1.100) → PC
                                           │
                                           └── Isolated subnet for camera
                                           
Main Network (eth0) ────────────────→ PC → Regular network/internet

FPGA (192.168.1.50) ────────────────→ Same GigE subnet for low latency
```

## Ubuntu Network Configuration

### 1. Identify Network Interface

```bash
# List network interfaces
ip link show

# Should see something like:
# 1: lo: <LOOPBACK,UP,LOWER_UP>
# 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>  # Main network
# 3: eth1: <BROADCAST,MULTICAST>              # Camera interface
```

### 2. Configure Dedicated Interface

Create netplan configuration:

```bash
sudo nano /etc/netplan/02-camera-network.yaml
```

Add this configuration:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth1:  # Replace with your interface name
      addresses:
        - 192.168.1.100/24
      mtu: 9000  # Enable jumbo frames
      dhcp4: no
      dhcp6: no
      optional: true
      link-local: []
```

Apply configuration:

```bash
sudo netplan apply
```

### 3. Enable Jumbo Frames

```bash
# Verify MTU is set
ip link show eth1 | grep mtu
# Should show: mtu 9000

# If not set, manually configure:
sudo ip link set dev eth1 mtu 9000
```

### 4. Optimize Network Performance

```bash
# Increase receive buffer size
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.rmem_default=134217728

# Disable interrupt coalescing for low latency
sudo ethtool -C eth1 rx-usecs 0

# Set CPU affinity for network interrupts
# Find interrupt number
grep eth1 /proc/interrupts
# Set affinity to CPU 2 (adjust as needed)
sudo echo 4 > /proc/irq/[IRQ_NUMBER]/smp_affinity

# Make settings persistent
echo "net.core.rmem_max=134217728" | sudo tee -a /etc/sysctl.conf
echo "net.core.rmem_default=134217728" | sudo tee -a /etc/sysctl.conf
```

### 5. Firewall Configuration

```bash
# Allow GigE Vision traffic
sudo ufw allow in on eth1 from 192.168.1.0/24
sudo ufw allow out on eth1 to 192.168.1.0/24

# Allow specific ports if needed
sudo ufw allow 3956/udp  # GigE Vision control
sudo ufw allow 5000/udp  # FPGA data port
```

## Camera Network Setup

### 1. Factory Reset (if needed)

If camera has unknown IP:
```bash
# Use FLIR IP Config tool or arping to find camera
sudo arping -I eth1 192.168.1.0/24

# Or reset via button:
# Hold reset button while powering on
# Release after 5 seconds
# Camera defaults to 192.168.1.1
```

### 2. Configure Camera IP (if needed)

```python
import PySpin

system = PySpin.System.GetInstance()
cam_list = system.GetCameras()

if cam_list.GetSize() > 0:
    cam = cam_list[0]
    cam.Init()
    
    # Access transport layer
    nodemap_tl = cam.GetTLDeviceNodeMap()
    
    # Set persistent IP
    ip_node = PySpin.CIntegerPtr(nodemap_tl.GetNode("GevPersistentIPAddress"))
    ip_node.SetValue(0xC0A80101)  # 192.168.1.1
    
    subnet_node = PySpin.CIntegerPtr(nodemap_tl.GetNode("GevPersistentSubnetMask"))
    subnet_node.SetValue(0xFFFFFF00)  # 255.255.255.0
    
    # Enable persistent IP
    persist_node = PySpin.CBooleanPtr(nodemap_tl.GetNode("GevCurrentIPConfigurationPersistentIP"))
    persist_node.SetValue(True)
    
    cam.DeInit()
```

### 3. Verify Camera Connection

```bash
# Ping camera
ping -c 4 192.168.1.1

# Check GigE Vision discovery
# Install aravis tools
sudo apt install aravis-tools

# Discover GigE cameras
arv-tool-0.8

# Should show:
# FLIR-[SERIAL] (192.168.1.1)
```

## Performance Testing

### 1. Network Throughput Test

```python
# test_bandwidth.py
import PySpin
import time

system = PySpin.System.GetInstance()
cam_list = system.GetCameras()
cam = cam_list[0]
cam.Init()

# Configure for max bandwidth test
nodemap = cam.GetNodeMap()
pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode("PixelFormat"))
pixel_format.SetIntValue(PySpin.PixelFormat_Mono14)

# Set packet size to jumbo
packet_size = PySpin.CIntegerPtr(nodemap.GetNode("GevSCPSPacketSize"))
packet_size.SetValue(9000)

# Measure frame rate
cam.BeginAcquisition()
start_time = time.time()
frame_count = 0

while frame_count < 600:  # 10 seconds at 60fps
    image = cam.GetNextImage(1000)
    if not image.IsIncomplete():
        frame_count += 1
    image.Release()

elapsed = time.time() - start_time
fps = frame_count / elapsed

print(f"Achieved: {fps:.1f} FPS")
print(f"Bandwidth: {fps * 320 * 256 * 2 / 1e6:.1f} MB/s")

cam.EndAcquisition()
cam.DeInit()
```

### 2. Latency Test

```bash
# Install tcpdump
sudo apt install tcpdump

# Capture packets to analyze latency
sudo tcpdump -i eth1 -w capture.pcap host 192.168.1.1

# In another terminal, run your thermal tracking
# Then analyze with Wireshark
```

## Troubleshooting

### Camera Not Found

1. Check cable and connections
2. Verify network interface is up:
   ```bash
   sudo ip link set eth1 up
   ```
3. Check firewall isn't blocking
4. Try factory reset

### Low Frame Rate

1. Enable jumbo frames (MTU 9000)
2. Check CPU governor:
   ```bash
   sudo cpupower frequency-set -g performance
   ```
3. Increase packet delay:
   ```python
   delay_node = PySpin.CIntegerPtr(nodemap.GetNode("GevSCPD"))
   delay_node.SetValue(1000)  # microseconds
   ```

### Packet Loss

1. Check cable quality (Cat 6 or better)
2. Reduce cable length (<100m)
3. Check for electromagnetic interference
4. Increase receive buffers

### High CPU Usage

1. Ensure interrupt coalescing is disabled
2. Set CPU affinity for interrupts
3. Use dedicated CPU core for processing
4. Disable unnecessary services

## Production Configuration

### systemd Service

Create `/etc/systemd/system/camera-network.service`:

```ini
[Unit]
Description=FLIR A35 Network Configuration
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/setup-camera-network.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Create `/usr/local/bin/setup-camera-network.sh`:

```bash
#!/bin/bash
# Set up camera network optimizations

# Set MTU
ip link set dev eth1 mtu 9000

# Increase buffers
sysctl -w net.core.rmem_max=134217728
sysctl -w net.core.rmem_default=134217728

# Disable interrupt coalescing
ethtool -C eth1 rx-usecs 0

# Set CPU affinity (adjust IRQ number)
echo 4 > /proc/irq/24/smp_affinity

echo "Camera network configured"
```

Make executable and enable:
```bash
sudo chmod +x /usr/local/bin/setup-camera-network.sh
sudo systemctl enable camera-network.service
sudo systemctl start camera-network.service
```

## Network Checklist

- [ ] Dedicated gigabit NIC installed
- [ ] Cat 6 cable connected
- [ ] Static IP configured (192.168.1.100/24)
- [ ] Jumbo frames enabled (MTU 9000)
- [ ] Receive buffers increased
- [ ] Interrupt coalescing disabled
- [ ] CPU affinity configured
- [ ] Firewall rules added
- [ ] Camera pingable at 192.168.1.1
- [ ] 60 FPS achieved in testing
- [ ] systemd service configured