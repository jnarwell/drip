#!/usr/bin/env python3
"""
Main thermal tracking program for DRIP acoustic levitation system
Provides real-time droplet position and temperature tracking at 60Hz
"""

import sys
import signal
import argparse
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

from thermal_droplet_tracker import ThermalDropletTracker
from thermal_visualizer import ThermalVisualizer

def signal_handler(sig, frame):
    """Clean shutdown on Ctrl+C"""
    print('\nShutting down thermal tracking...')
    if 'tracker' in globals():
        tracker.cleanup()
    sys.exit(0)

def load_calibration():
    """Load saved calibration data"""
    import numpy as np
    try:
        calib_data = np.load('calibration/camera_calibration.npy', allow_pickle=True).item()
        print(f"Loaded calibration: 1 pixel = {calib_data['pixel_to_mm']:.3f} mm")
        return calib_data['pixel_to_mm']
    except:
        print("No calibration found, using default (0.5 mm/pixel)")
        return 0.5

def main():
    parser = argparse.ArgumentParser(
        description="FLIR A35 Thermal Tracking for DRIP System"
    )
    parser.add_argument(
        '--fpga-ip', 
        default='192.168.1.50',
        help='FPGA IP address for droplet data'
    )
    parser.add_argument(
        '--fpga-port',
        type=int,
        default=5000,
        help='FPGA UDP port'
    )
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Enable real-time visualization'
    )
    parser.add_argument(
        '--calibrate',
        action='store_true',
        help='Run calibration procedure'
    )
    parser.add_argument(
        '--save-frames',
        type=int,
        default=0,
        help='Save visualization every N frames (0=disabled)'
    )
    parser.add_argument(
        '--min-temp',
        type=float,
        default=600,
        help='Minimum temperature to track (°C)'
    )
    
    args = parser.parse_args()
    
    # Create directories if needed
    os.makedirs('calibration', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Initialize tracker
    global tracker
    tracker = ThermalDropletTracker(
        fpga_ip=args.fpga_ip,
        fpga_port=args.fpga_port
    )
    
    tracker.min_temp_celsius = args.min_temp
    
    try:
        # Initialize camera
        print("Initializing FLIR A35 thermal camera...")
        tracker.initialize_camera()
        
        # Load or run calibration
        if args.calibrate:
            print("\n" + "="*50)
            print("CAMERA CALIBRATION PROCEDURE")
            print("="*50)
            from calibration.camera_calibration import calibrate_camera
            calibrate_camera(tracker)
        else:
            tracker.pixel_to_mm = load_calibration()
        
        # Set up visualization if requested
        visualizer = None
        if args.visualize:
            print("Starting visualization...")
            visualizer = ThermalVisualizer(tracker)
        
        # Register signal handler for clean shutdown
        signal.signal(signal.SIGINT, signal_handler)
        
        # Print startup info
        print("\n" + "="*50)
        print("THERMAL DROPLET TRACKING ACTIVE")
        print("="*50)
        print(f"FPGA Target: {args.fpga_ip}:{args.fpga_port}")
        print(f"Min Temperature: {args.min_temp}°C")
        print(f"Calibration: {tracker.pixel_to_mm:.3f} mm/pixel")
        print(f"Visualization: {'Enabled' if args.visualize else 'Disabled'}")
        print("\nPress Ctrl+C to stop")
        print("="*50 + "\n")
        
        # Main tracking loop
        tracker.camera.BeginAcquisition()
        frame_count = 0
        
        while True:
            # Get next frame
            image_result = tracker.camera.GetNextImage(1000)
            
            if image_result.IsIncomplete():
                print("Image incomplete, skipping...")
                continue
            
            # Process frame
            result = tracker.process_frame(image_result)
            frame_count += 1
            
            # Update visualization
            if visualizer and result:
                visualizer.update_display(result)
                
                # Save frames if requested
                if args.save_frames > 0 and frame_count % args.save_frames == 0:
                    filename = f"logs/thermal_frame_{frame_count:06d}.png"
                    visualizer.save_frame(result, filename)
            
            # Release frame
            image_result.Release()
            
            # Display performance
            if len(tracker.frame_times) > 1:
                fps = len(tracker.frame_times) / (
                    tracker.frame_times[-1] - tracker.frame_times[0]
                )
                status = f"FPS: {fps:.1f} | Tracking: {len(tracker.trackers)} droplets"
                
                if not args.visualize:
                    print(f"\r{status}", end='')
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nCleaning up...")
        tracker.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()