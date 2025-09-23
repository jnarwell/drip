#!/usr/bin/env python3
"""
Performance optimization configuration for FLIR A35 thermal tracking
These settings maximize real-time performance for 60Hz operation
"""

import os
import psutil

# Network optimization for GigE Vision
NETWORK_CONFIG = {
    'interface': 'eth1',  # Dedicated camera interface
    'mtu': 9000,          # Jumbo frames
    'rx_buffer': 134217728,  # 128MB receive buffer
    'tx_buffer': 67108864,   # 64MB transmit buffer  
    'interrupt_coalescing': False,
    'cpu_affinity': 2     # Dedicated CPU core for network IRQ
}

# Camera-specific optimizations
CAMERA_CONFIG = {
    'packet_size': 9000,      # Match MTU for jumbo frames
    'packet_delay': 0,        # Microseconds between packets (0 = max speed)
    'frame_burst': 1,         # Frames per burst
    'binning': None,          # No binning for max resolution
    'roi': None,              # Full frame (320x256)
    'pixel_format': 'Mono14', # 14-bit for temperature data
    'chunk_mode': True,       # Enable metadata chunks
    'event_notification': False,  # Polling is more deterministic
    'trigger_mode': 'Off'     # Free-running at max frame rate
}

# Processing optimizations
PROCESSING_CONFIG = {
    'use_gpu': False,         # CPU is fast enough for 320×256
    'parallel_tracks': True,   # Process multiple droplets in parallel
    'max_threads': 4,         # Thread pool size
    'numpy_threads': 2,       # NumPy internal parallelism
    'opencv_threads': 2,      # OpenCV internal parallelism
    'queue_size': 3,          # Frame buffer size (frames)
    'drop_frames': False,     # Process every frame
    'profile_enabled': False  # Disable profiling in production
}

# System-level optimizations
SYSTEM_CONFIG = {
    'process_priority': -5,    # Nice value (negative = higher priority)
    'scheduler': 'SCHED_FIFO', # Real-time scheduler
    'cpu_affinity': [3, 4],    # CPU cores for processing
    'isolate_cpus': True,      # Isolate from OS scheduler
    'memory_locked': True,     # Prevent swapping
    'huge_pages': False        # Not needed for this application
}

# Kalman filter tuning for 60Hz
KALMAN_CONFIG = {
    'dt': 1/60.0,              # Time step (60Hz)
    'process_noise': 0.1,      # Process noise covariance
    'measurement_noise': 0.5,  # Position measurement noise (mm)
    'temp_noise': 5.0,         # Temperature noise (°C)
    'velocity_noise': 0.01,    # Velocity process noise
    'max_missed_frames': 5,    # Frames before track is lost
    'min_track_age': 3         # Frames before track is stable
}

# FPGA communication settings
FPGA_CONFIG = {
    'protocol': 'UDP',         # UDP for low latency
    'packet_size': 28,         # 7 floats × 4 bytes
    'send_rate': 60,           # Hz (match camera rate)
    'socket_buffer': 65536,    # Socket buffer size
    'no_delay': True,          # Disable Nagle algorithm
    'ttl': 1                   # Time-to-live (local network only)
}


def apply_network_optimizations():
    """Apply network optimizations for GigE Vision"""
    import subprocess
    
    iface = NETWORK_CONFIG['interface']
    
    # Set MTU
    cmd = f"sudo ip link set dev {iface} mtu {NETWORK_CONFIG['mtu']}"
    subprocess.run(cmd.split(), check=True)
    
    # Increase buffers
    subprocess.run([
        "sudo", "sysctl", "-w", 
        f"net.core.rmem_max={NETWORK_CONFIG['rx_buffer']}"
    ])
    subprocess.run([
        "sudo", "sysctl", "-w",
        f"net.core.rmem_default={NETWORK_CONFIG['rx_buffer']}"
    ])
    
    # Disable interrupt coalescing
    if not NETWORK_CONFIG['interrupt_coalescing']:
        subprocess.run([
            "sudo", "ethtool", "-C", iface, "rx-usecs", "0"
        ])
    
    print(f"Network optimizations applied to {iface}")


def apply_process_optimizations():
    """Apply process-level optimizations"""
    import resource
    
    # Set process priority
    os.nice(SYSTEM_CONFIG['process_priority'])
    
    # Set CPU affinity
    p = psutil.Process()
    p.cpu_affinity(SYSTEM_CONFIG['cpu_affinity'])
    
    # Lock memory to prevent swapping
    if SYSTEM_CONFIG['memory_locked']:
        # Increase memory lock limit
        soft, hard = resource.getrlimit(resource.RLIMIT_MEMLOCK)
        resource.setrlimit(resource.RLIMIT_MEMLOCK, (hard, hard))
        
        # Note: mlockall() requires CAP_IPC_LOCK capability
        # Run with: sudo setcap cap_ipc_lock+ep python
    
    # Set thread configuration
    os.environ['OMP_NUM_THREADS'] = str(PROCESSING_CONFIG['numpy_threads'])
    os.environ['OPENBLAS_NUM_THREADS'] = str(PROCESSING_CONFIG['numpy_threads'])
    os.environ['MKL_NUM_THREADS'] = str(PROCESSING_CONFIG['numpy_threads'])
    
    print(f"Process optimizations applied (CPU: {SYSTEM_CONFIG['cpu_affinity']})")


def configure_spinnaker_optimizations(camera):
    """Apply Spinnaker SDK optimizations"""
    import PySpin
    
    nodemap = camera.GetNodeMap()
    
    # Set packet size for jumbo frames
    try:
        packet_size = PySpin.CIntegerPtr(nodemap.GetNode("GevSCPSPacketSize"))
        packet_size.SetValue(CAMERA_CONFIG['packet_size'])
    except:
        print("Warning: Could not set packet size")
    
    # Set packet delay
    try:
        packet_delay = PySpin.CIntegerPtr(nodemap.GetNode("GevSCPD"))
        packet_delay.SetValue(CAMERA_CONFIG['packet_delay'])
    except:
        print("Warning: Could not set packet delay")
    
    # Disable event notifications for polling mode
    try:
        event_node = PySpin.CEnumerationPtr(nodemap.GetNode("EventNotification"))
        off_node = event_node.GetEntryByName("Off")
        event_node.SetIntValue(off_node.GetValue())
    except:
        pass
    
    print("Camera optimizations applied")


def get_performance_stats():
    """Get current performance statistics"""
    stats = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'network_packets_recv': psutil.net_io_counters().packets_recv,
        'network_packets_dropped': psutil.net_io_counters().dropin,
    }
    
    # Check if running with real-time priority
    p = psutil.Process()
    try:
        stats['nice_value'] = p.nice()
        stats['cpu_affinity'] = p.cpu_affinity()
    except:
        pass
    
    return stats


def validate_system_requirements():
    """Check if system meets performance requirements"""
    issues = []
    
    # Check CPU cores
    if psutil.cpu_count() < 4:
        issues.append("System has <4 CPU cores, may impact performance")
    
    # Check memory
    if psutil.virtual_memory().total < 8 * 1024**3:  # 8GB
        issues.append("System has <8GB RAM, may impact performance")
    
    # Check network interface
    import subprocess
    try:
        result = subprocess.run(
            ['ip', 'link', 'show', NETWORK_CONFIG['interface']],
            capture_output=True,
            text=True
        )
        if 'mtu 9000' not in result.stdout:
            issues.append(f"Interface {NETWORK_CONFIG['interface']} not configured for jumbo frames")
    except:
        issues.append(f"Could not check network interface {NETWORK_CONFIG['interface']}")
    
    # Check Python version
    import sys
    if sys.version_info < (3, 8):
        issues.append("Python version <3.8, may have performance issues")
    
    return issues


# Presets for different scenarios
PRESETS = {
    'development': {
        'drop_frames': True,
        'visualization': True,
        'save_frames': 60,
        'profile_enabled': True
    },
    'production': {
        'drop_frames': False,
        'visualization': False,
        'save_frames': 0,
        'profile_enabled': False
    },
    'debug': {
        'drop_frames': False,
        'visualization': True,
        'save_frames': 1,
        'profile_enabled': True
    }
}


def load_preset(preset_name):
    """Load optimization preset"""
    if preset_name in PRESETS:
        preset = PRESETS[preset_name]
        for key, value in preset.items():
            if key in PROCESSING_CONFIG:
                PROCESSING_CONFIG[key] = value
        print(f"Loaded preset: {preset_name}")
    else:
        print(f"Unknown preset: {preset_name}")


if __name__ == "__main__":
    # Run system validation
    print("Validating system requirements...")
    issues = validate_system_requirements()
    
    if issues:
        print("\nWarnings:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("System meets all requirements")
    
    # Show current stats
    print("\nCurrent performance stats:")
    stats = get_performance_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")