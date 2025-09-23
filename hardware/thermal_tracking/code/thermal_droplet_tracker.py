#!/usr/bin/env python3
"""
Real-time thermal tracking for acoustic steering control
Tracks multiple droplets with position and temperature using FLIR A35
Primary sensor for the DRIP acoustic manufacturing system
"""

import PySpin
import numpy as np
import cv2
import socket
import struct
import time
from collections import deque
from threading import Thread, Lock
from scipy.optimize import linear_sum_assignment

class ThermalDropletTracker:
    """
    Real-time thermal tracking for acoustic steering control
    Tracks multiple droplets with position and temperature
    """
    
    def __init__(self, fpga_ip="192.168.1.50", fpga_port=5000):
        # Camera parameters
        self.camera = None
        self.system = PySpin.System.GetInstance()
        
        # Tracking parameters
        self.min_temp_celsius = 600  # Minimum temp to track
        self.max_droplets = 10  # Maximum simultaneous droplets
        self.pixel_to_mm = 0.5  # Calibration factor
        
        # Kalman filter for each tracked droplet
        self.trackers = {}
        self.next_id = 0
        
        # FPGA communication
        self.fpga_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.fpga_address = (fpga_ip, fpga_port)
        
        # Performance monitoring
        self.frame_times = deque(maxlen=60)
        self.lock = Lock()
        
    def initialize_camera(self):
        """Initialize FLIR A35 with optimal settings"""
        try:
            # Get camera list
            cam_list = self.system.GetCameras()
            if cam_list.GetSize() == 0:
                raise Exception("No FLIR camera detected!")
            
            self.camera = cam_list[0]
            self.camera.Init()
            
            # Configure for maximum performance
            nodemap = self.camera.GetNodeMap()
            
            # Set pixel format to 14-bit for temperature
            pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode("PixelFormat"))
            pixel_format.SetIntValue(PySpin.PixelFormat_Mono14)
            
            # Set acquisition mode to continuous
            acquisition_mode = PySpin.CEnumerationPtr(
                nodemap.GetNode("AcquisitionMode")
            )
            acquisition_mode.SetIntValue(PySpin.AcquisitionMode_Continuous)
            
            # Set frame rate to maximum (60 Hz)
            frame_rate = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
            frame_rate.SetValue(60.0)
            
            # Enable timestamp for synchronization
            timestamp = PySpin.CBooleanPtr(nodemap.GetNode("ChunkModeActive"))
            timestamp.SetValue(True)
            
            # Configure temperature linear output mode
            # This makes pixel values directly proportional to temperature
            temp_linear = PySpin.CEnumerationPtr(
                nodemap.GetNode("TemperatureLinearMode")
            )
            temp_linear.SetIntValue(1)  # High gain mode
            
            print(f"Camera initialized: {self.camera.GetUniqueID()}")
            print(f"Resolution: 320x256 @ 60Hz")
            
        except PySpin.SpinnakerException as ex:
            print(f"Error initializing camera: {ex}")
            raise
    
    def pixel_to_temperature(self, pixel_value):
        """Convert 14-bit pixel value to temperature in Celsius"""
        # FLIR A35 linear mode: T = (pixel_value - 8192) * 0.04
        # Adjust formula based on calibration
        return (pixel_value - 8192) * 0.04
    
    def detect_droplets(self, thermal_frame):
        """
        Detect hot droplets using blob detection
        Returns list of (x, y, temperature, area) tuples
        """
        # Convert to temperature
        temp_frame = self.pixel_to_temperature(thermal_frame)
        
        # Threshold for hot objects
        _, binary = cv2.threshold(
            temp_frame.astype(np.uint8),
            self.min_temp_celsius / 4,  # Scale for 8-bit
            255,
            cv2.THRESH_BINARY
        )
        
        # Morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        detections = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:  # Minimum size filter
                # Calculate centroid
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = M["m10"] / M["m00"]
                    cy = M["m01"] / M["m00"]
                    
                    # Get temperature at centroid
                    temp = temp_frame[int(cy), int(cx)]
                    
                    # Convert to mm coordinates
                    x_mm = (cx - 160) * self.pixel_to_mm
                    y_mm = (cy - 128) * self.pixel_to_mm
                    
                    detections.append({
                        'x': x_mm,
                        'y': y_mm,
                        'temp': temp,
                        'area': area,
                        'pixel_x': cx,
                        'pixel_y': cy
                    })
        
        return detections
    
    def update_kalman_trackers(self, detections):
        """
        Update Kalman filters for each tracked droplet
        Uses Hungarian algorithm for detection-to-track association
        """
        # Predict step for all trackers
        predictions = {}
        for track_id, kf in self.trackers.items():
            predictions[track_id] = kf.predict()
        
        if len(detections) > 0 and len(self.trackers) > 0:
            # Build cost matrix for assignment
            cost_matrix = np.zeros((len(self.trackers), len(detections)))
            track_ids = list(self.trackers.keys())
            
            for i, track_id in enumerate(track_ids):
                pred = predictions[track_id]
                for j, det in enumerate(detections):
                    # Euclidean distance as cost
                    cost = np.sqrt(
                        (pred['x'] - det['x'])**2 + 
                        (pred['y'] - det['y'])**2
                    )
                    cost_matrix[i, j] = cost
            
            # Hungarian algorithm for optimal assignment
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            
            # Update matched trackers
            matched_tracks = set()
            matched_detections = set()
            
            for i, j in zip(row_ind, col_ind):
                if cost_matrix[i, j] < 10:  # Max distance threshold (mm)
                    track_id = track_ids[i]
                    self.trackers[track_id].update(detections[j])
                    matched_tracks.add(track_id)
                    matched_detections.add(j)
            
            # Create new trackers for unmatched detections
            for j, det in enumerate(detections):
                if j not in matched_detections:
                    self.trackers[self.next_id] = KalmanDropletFilter(det)
                    self.next_id += 1
            
            # Remove lost trackers
            lost_tracks = [
                tid for tid in track_ids 
                if tid not in matched_tracks
            ]
            for tid in lost_tracks:
                if self.trackers[tid].missed_frames > 5:
                    del self.trackers[tid]
                else:
                    self.trackers[tid].missed_frames += 1
        
        elif len(detections) > 0:
            # No existing trackers, create new ones
            for det in detections:
                self.trackers[self.next_id] = KalmanDropletFilter(det)
                self.next_id += 1
    
    def send_to_fpga(self, tracked_droplets):
        """
        Send droplet positions and temps to FPGA for acoustic control
        Protocol: [ID, X, Y, Z, Temp, Vx, Vy] as float32
        """
        for track_id, tracker in tracked_droplets.items():
            state = tracker.get_state()
            
            # Pack data for FPGA
            # Format: <track_id><x><y><z><temp><vx><vy>
            data = struct.pack(
                '<Iffffff',
                track_id,
                state['x'],
                state['y'],
                0.0,  # Z from acoustic model
                state['temp'],
                state['vx'],
                state['vy']
            )
            
            # Send UDP packet to FPGA
            self.fpga_socket.sendto(data, self.fpga_address)
    
    def process_frame(self, image_result):
        """Process single frame - called at 60Hz"""
        try:
            # Convert to numpy array
            frame = image_result.GetNDArray()
            
            # Detect droplets
            detections = self.detect_droplets(frame)
            
            # Update tracking
            self.update_kalman_trackers(detections)
            
            # Send to FPGA
            self.send_to_fpga(self.trackers)
            
            # Performance monitoring
            self.frame_times.append(time.time())
            
            # Return for visualization
            return {
                'frame': frame,
                'detections': detections,
                'tracks': self.trackers
            }
            
        except Exception as e:
            print(f"Frame processing error: {e}")
            return None
    
    def run_continuous(self):
        """Main tracking loop - runs at camera frame rate"""
        try:
            # Start acquisition
            self.camera.BeginAcquisition()
            print("Starting thermal tracking at 60Hz...")
            
            while True:
                # Get next frame (blocks until available)
                image_result = self.camera.GetNextImage(1000)
                
                if image_result.IsIncomplete():
                    print("Image incomplete, skipping...")
                    continue
                
                # Process frame
                result = self.process_frame(image_result)
                
                # Release frame
                image_result.Release()
                
                # Calculate and display FPS
                if len(self.frame_times) > 1:
                    fps = len(self.frame_times) / (
                        self.frame_times[-1] - self.frame_times[0]
                    )
                    print(f"\rFPS: {fps:.1f} | Tracking: {len(self.trackers)} droplets", 
                          end='')
                
        except KeyboardInterrupt:
            print("\nStopping thermal tracking...")
        finally:
            self.camera.EndAcquisition()
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.camera:
            self.camera.DeInit()
            del self.camera
        self.system.ReleaseInstance()
        self.fpga_socket.close()


class KalmanDropletFilter:
    """
    Kalman filter for tracking individual droplet
    State: [x, y, vx, vy, temp]
    """
    
    def __init__(self, initial_detection):
        # State vector: [x, y, vx, vy, temp]
        self.state = np.array([
            initial_detection['x'],
            initial_detection['y'],
            0.0,  # Initial velocity x
            0.0,  # Initial velocity y
            initial_detection['temp']
        ])
        
        # State transition matrix (constant velocity model)
        self.dt = 1/60.0  # 60Hz frame rate
        self.F = np.array([
            [1, 0, self.dt, 0, 0],
            [0, 1, 0, self.dt, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1]  # Temperature changes slowly
        ])
        
        # Measurement matrix (we measure x, y, temp)
        self.H = np.array([
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1]
        ])
        
        # Process noise covariance
        self.Q = np.eye(5) * 0.1
        self.Q[2, 2] = 0.01  # Less noise in velocity
        self.Q[3, 3] = 0.01
        
        # Measurement noise covariance
        self.R = np.eye(3)
        self.R[0, 0] = 0.5  # Position uncertainty (mm)
        self.R[1, 1] = 0.5
        self.R[2, 2] = 5.0  # Temperature uncertainty (°C)
        
        # Initial covariance
        self.P = np.eye(5) * 10
        
        self.missed_frames = 0
        self.age = 0
    
    def predict(self):
        """Predict next state"""
        self.state = self.F @ self.state
        self.P = self.F @ self.P @ self.F.T + self.Q
        return {
            'x': self.state[0],
            'y': self.state[1],
            'vx': self.state[2],
            'vy': self.state[3],
            'temp': self.state[4]
        }
    
    def update(self, detection):
        """Update with new measurement"""
        z = np.array([
            detection['x'],
            detection['y'],
            detection['temp']
        ])
        
        # Kalman gain
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update state
        y = z - self.H @ self.state
        self.state = self.state + K @ y
        
        # Update covariance
        I = np.eye(5)
        self.P = (I - K @ self.H) @ self.P
        
        self.missed_frames = 0
        self.age += 1
    
    def get_state(self):
        """Get current state estimate"""
        return {
            'x': self.state[0],
            'y': self.state[1],
            'vx': self.state[2],
            'vy': self.state[3],
            'temp': self.state[4],
            'age': self.age
        }