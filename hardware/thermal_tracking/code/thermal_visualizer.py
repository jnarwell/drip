#!/usr/bin/env python3
"""
Real-time visualization of thermal tracking
Shows thermal image and droplet positions/velocities
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation

class ThermalVisualizer:
    """Real-time visualization of thermal tracking"""
    
    def __init__(self, tracker):
        self.tracker = tracker
        
        # Set up matplotlib for real-time display
        plt.ion()
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Thermal image display
        self.thermal_img = self.ax1.imshow(
            np.zeros((256, 320)),
            cmap='hot',
            vmin=0,
            vmax=1600
        )
        self.ax1.set_title("Thermal View")
        self.ax1.set_xlabel("X (pixels)")
        self.ax1.set_ylabel("Y (pixels)")
        
        # Position plot
        self.ax2.set_xlim(-50, 50)
        self.ax2.set_ylim(-50, 50)
        self.ax2.set_aspect('equal')
        self.ax2.set_title("Droplet Positions (mm)")
        self.ax2.set_xlabel("X (mm)")
        self.ax2.set_ylabel("Y (mm)")
        self.ax2.grid(True)
        
        self.position_plots = {}
    
    def update_display(self, result):
        """Update visualization with latest tracking data"""
        if result is None:
            return
        
        # Update thermal image
        temp_frame = self.tracker.pixel_to_temperature(result['frame'])
        self.thermal_img.set_data(temp_frame)
        
        # Clear previous patches
        for patch in self.ax1.patches[:]:
            patch.remove()
        
        # Draw detection boxes on thermal image
        for det in result['detections']:
            circle = Circle(
                (det['pixel_x'], det['pixel_y']),
                radius=5,
                fill=False,
                color='green',
                linewidth=2
            )
            self.ax1.add_patch(circle)
        
        # Update position plot
        self.ax2.clear()
        self.ax2.set_xlim(-50, 50)
        self.ax2.set_ylim(-50, 50)
        self.ax2.set_aspect('equal')
        self.ax2.grid(True)
        
        for track_id, tracker in result['tracks'].items():
            state = tracker.get_state()
            
            # Plot position
            self.ax2.plot(state['x'], state['y'], 'ro', markersize=10)
            
            # Add velocity vector
            self.ax2.arrow(
                state['x'], state['y'],
                state['vx'] * 10, state['vy'] * 10,
                head_width=2,
                head_length=1,
                fc='blue',
                ec='blue'
            )
            
            # Add text label
            self.ax2.text(
                state['x'] + 2, state['y'] + 2,
                f"ID:{track_id}\nT:{state['temp']:.0f}°C",
                fontsize=8
            )
        
        self.ax2.set_title(f"Tracking {len(result['tracks'])} droplets")
        
        plt.pause(0.001)

    def save_frame(self, result, filename):
        """Save current visualization to file"""
        if result is None:
            return
            
        # Create composite image
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Thermal image
        temp_frame = self.tracker.pixel_to_temperature(result['frame'])
        im1 = ax1.imshow(temp_frame, cmap='hot', vmin=0, vmax=1600)
        ax1.set_title("Thermal View")
        plt.colorbar(im1, ax=ax1, label='Temperature (°C)')
        
        # Add detection circles
        for det in result['detections']:
            circle = Circle(
                (det['pixel_x'], det['pixel_y']),
                radius=5,
                fill=False,
                color='green',
                linewidth=2
            )
            ax1.add_patch(circle)
        
        # Position plot
        ax2.set_xlim(-50, 50)
        ax2.set_ylim(-50, 50)
        ax2.set_aspect('equal')
        ax2.grid(True)
        ax2.set_title("Droplet Positions (mm)")
        ax2.set_xlabel("X (mm)")
        ax2.set_ylabel("Y (mm)")
        
        for track_id, tracker in result['tracks'].items():
            state = tracker.get_state()
            ax2.plot(state['x'], state['y'], 'ro', markersize=10)
            ax2.arrow(
                state['x'], state['y'],
                state['vx'] * 10, state['vy'] * 10,
                head_width=2,
                head_length=1,
                fc='blue',
                ec='blue'
            )
            ax2.text(
                state['x'] + 2, state['y'] + 2,
                f"ID:{track_id}",
                fontsize=8
            )
        
        # Temperature histogram
        ax3.hist(temp_frame.flatten(), bins=50, range=(0, 1600))
        ax3.set_xlabel("Temperature (°C)")
        ax3.set_ylabel("Pixel Count")
        ax3.set_title("Temperature Distribution")
        
        # Tracking statistics
        ax4.axis('off')
        stats_text = f"Frame Statistics:\n\n"
        stats_text += f"Detections: {len(result['detections'])}\n"
        stats_text += f"Active Tracks: {len(result['tracks'])}\n"
        stats_text += f"Frame Rate: {len(self.tracker.frame_times):.1f} Hz\n\n"
        
        if len(result['tracks']) > 0:
            stats_text += "Tracked Droplets:\n"
            for track_id, tracker in result['tracks'].items():
                state = tracker.get_state()
                stats_text += f"\nID {track_id}:\n"
                stats_text += f"  Position: ({state['x']:.1f}, {state['y']:.1f}) mm\n"
                stats_text += f"  Velocity: ({state['vx']:.1f}, {state['vy']:.1f}) mm/s\n"
                stats_text += f"  Temperature: {state['temp']:.0f}°C\n"
                stats_text += f"  Age: {state['age']} frames\n"
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, 
                 verticalalignment='top', fontfamily='monospace')
        ax4.set_title("Tracking Statistics")
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close(fig)