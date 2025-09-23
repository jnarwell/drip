#!/usr/bin/env python3
"""
Camera calibration for FLIR A35 thermal tracking
Establishes pixel-to-mm conversion factor
"""

import numpy as np
import cv2
import time

def calibrate_camera(tracker):
    """
    Calibrate pixel-to-mm conversion using known target
    Place a heated target of known size at known position
    """
    print("\nCAMERA CALIBRATION PROCEDURE")
    print("============================")
    print("\nRequired equipment:")
    print("- Metal target of known size (10mm × 10mm recommended)")
    print("- Heat source (hot plate, soldering iron, etc)")
    print("- Ruler for positioning\n")
    
    print("Setup instructions:")
    print("1. Place target at chamber center (X=0, Y=0)")
    print("2. Heat target to >600°C")
    print("3. Ensure only target is visible in thermal image")
    print("4. Target should appear as bright spot\n")
    
    input("Press Enter when ready to start calibration...")
    
    print("\nCapturing calibration frames...")
    
    # Capture frames for averaging
    frames = []
    for i in range(60):  # 1 second of data at 60Hz
        try:
            image_result = tracker.camera.GetNextImage(1000)
            if not image_result.IsIncomplete():
                frames.append(image_result.GetNDArray())
            image_result.Release()
            
            # Progress bar
            progress = int((i + 1) / 60 * 50)
            print(f"\r[{'='*progress}{' '*(50-progress)}] {i+1}/60", end='')
        except Exception as e:
            print(f"\nError capturing frame: {e}")
            return
    
    print("\n\nProcessing calibration data...")
    
    # Average frames to reduce noise
    avg_frame = np.mean(frames, axis=0)
    
    # Convert to temperature
    temp_frame = tracker.pixel_to_temperature(avg_frame)
    
    # Find hot target
    threshold_temp = 150  # °C threshold for detection
    _, binary = cv2.threshold(
        temp_frame.astype(np.uint8),
        threshold_temp // 4,  # Scale for 8-bit
        255,
        cv2.THRESH_BINARY
    )
    
    # Find contours
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    if len(contours) == 0:
        print("\nERROR: No hot target detected!")
        print("Troubleshooting:")
        print("- Check target temperature (must be >600°C)")
        print("- Verify camera view is unobstructed")
        print("- Ensure target is in field of view")
        return
    
    # Find largest contour (should be our target)
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    
    print(f"\nTarget detected:")
    print(f"- Position: ({x + w/2:.1f}, {y + h/2:.1f}) pixels")
    print(f"- Size: {w} × {h} pixels")
    print(f"- Area: {cv2.contourArea(largest):.0f} pixels²")
    
    # Get target size from user
    print("\nEnter actual target dimensions:")
    try:
        target_width = float(input("Target width (mm): "))
        target_height = float(input("Target height (mm): "))
    except ValueError:
        print("Invalid input! Using default 10mm × 10mm")
        target_width = 10.0
        target_height = 10.0
    
    # Calculate calibration factor
    pixel_to_mm_width = target_width / w
    pixel_to_mm_height = target_height / h
    pixel_to_mm_avg = (pixel_to_mm_width + pixel_to_mm_height) / 2
    
    print(f"\nCalibration results:")
    print(f"- Width calibration: {pixel_to_mm_width:.4f} mm/pixel")
    print(f"- Height calibration: {pixel_to_mm_height:.4f} mm/pixel")
    print(f"- Average calibration: {pixel_to_mm_avg:.4f} mm/pixel")
    
    # Check for significant aspect ratio distortion
    ratio_diff = abs(pixel_to_mm_width - pixel_to_mm_height) / pixel_to_mm_avg
    if ratio_diff > 0.1:  # More than 10% difference
        print(f"\nWARNING: Aspect ratio distortion detected ({ratio_diff*100:.1f}%)")
        print("This may indicate:")
        print("- Camera not perpendicular to target")
        print("- Optical distortion")
        print("- Non-square pixels")
    
    # Save calibration
    tracker.pixel_to_mm = pixel_to_mm_avg
    
    calib_data = {
        'pixel_to_mm': pixel_to_mm_avg,
        'pixel_to_mm_width': pixel_to_mm_width,
        'pixel_to_mm_height': pixel_to_mm_height,
        'image_center': [160, 128],  # A35 resolution 320×256
        'target_size_mm': [target_width, target_height],
        'target_size_pixels': [w, h],
        'calibration_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'camera_model': 'FLIR A35',
        'resolution': [320, 256]
    }
    
    np.save('calibration/camera_calibration.npy', calib_data)
    print(f"\nCalibration saved to camera_calibration.npy")
    
    # Optional: capture calibration image
    save_image = input("\nSave calibration image? (y/n): ").lower() == 'y'
    if save_image:
        # Create visualization
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Thermal image with target box
        ax1.imshow(temp_frame, cmap='hot')
        rect = plt.Rectangle((x, y), w, h, fill=False, color='green', linewidth=2)
        ax1.add_patch(rect)
        ax1.set_title('Calibration Target Detection')
        ax1.set_xlabel('X (pixels)')
        ax1.set_ylabel('Y (pixels)')
        
        # Binary image
        ax2.imshow(binary, cmap='gray')
        ax2.set_title('Binary Threshold')
        ax2.set_xlabel('X (pixels)')
        ax2.set_ylabel('Y (pixels)')
        
        plt.tight_layout()
        plt.savefig('calibration/calibration_result.png', dpi=150)
        print("Calibration image saved to calibration_result.png")
        plt.close()
    
    print("\nCalibration complete!")
    print(f"Using calibration factor: {pixel_to_mm_avg:.4f} mm/pixel")
    
    # Test calibration with live tracking
    test_tracking = input("\nTest calibration with live tracking? (y/n): ").lower() == 'y'
    if test_tracking:
        print("\nStarting test tracking for 10 seconds...")
        print("Move heated target to verify position accuracy")
        print("Press Ctrl+C to stop early\n")
        
        test_duration = 10  # seconds
        start_time = time.time()
        
        try:
            while time.time() - start_time < test_duration:
                image_result = tracker.camera.GetNextImage(1000)
                if not image_result.IsIncomplete():
                    frame = image_result.GetNDArray()
                    detections = tracker.detect_droplets(frame)
                    
                    if len(detections) > 0:
                        det = detections[0]  # First detection
                        print(f"\rPosition: ({det['x']:+6.1f}, {det['y']:+6.1f}) mm | "
                              f"Temp: {det['temp']:4.0f}°C | "
                              f"Time: {test_duration - (time.time() - start_time):.1f}s", 
                              end='')
                    else:
                        print(f"\rNo target detected | "
                              f"Time: {test_duration - (time.time() - start_time):.1f}s", 
                              end='')
                
                image_result.Release()
                
        except KeyboardInterrupt:
            pass
        
        print("\n\nCalibration test complete!")


def verify_calibration(tracker):
    """Verify existing calibration is still accurate"""
    try:
        calib_data = np.load('calibration/camera_calibration.npy', allow_pickle=True).item()
        
        print("\nEXISTING CALIBRATION")
        print("====================")
        print(f"Calibration date: {calib_data['calibration_date']}")
        print(f"Pixel to mm: {calib_data['pixel_to_mm']:.4f}")
        print(f"Target size: {calib_data['target_size_mm'][0]} × {calib_data['target_size_mm'][1]} mm")
        print(f"Detected pixels: {calib_data['target_size_pixels'][0]} × {calib_data['target_size_pixels'][1]}")
        
        recalibrate = input("\nRecalibrate? (y/n): ").lower() == 'y'
        if recalibrate:
            calibrate_camera(tracker)
        else:
            tracker.pixel_to_mm = calib_data['pixel_to_mm']
            print(f"Using existing calibration: {tracker.pixel_to_mm:.4f} mm/pixel")
            
    except FileNotFoundError:
        print("\nNo existing calibration found.")
        calibrate_camera(tracker)