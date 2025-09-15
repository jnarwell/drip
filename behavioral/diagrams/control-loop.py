"""Generate control loop timing diagram"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create timing diagram showing <3ms total loop time
fig, ax = plt.subplots(figsize=(12, 6))

# Component lanes
components = ['Thermal Camera', 'STM32', 'FPGA', 'Transducers', 'Droplet']
y_positions = {comp: i for i, comp in enumerate(components)}

# Timing events (in microseconds)
events = [
    ('Thermal Camera', 0, 1000, 'Capture', '#FF6B6B'),
    ('STM32', 1100, 500, 'Extract', '#4ECDC4'),
    ('STM32', 1600, 400, 'Compute', '#45B7D1'),
    ('FPGA', 2050, 20, 'Transfer', '#96CEB4'),
    ('FPGA', 2080, 10, 'Distribute', '#DDA0DD'),
    ('Transducers', 2100, 1, 'Drive', '#FFD93D'),
    ('Droplet', 2300, 200, 'Response', '#6C5CE7')
]

# Draw timing blocks
for comp, start, duration, label, color in events:
    y = y_positions[comp]
    rect = patches.Rectangle((start, y-0.3), duration, 0.6, 
                            linewidth=1, edgecolor='black', 
                            facecolor=color, alpha=0.7)
    ax.add_patch(rect)
    
    # Add label if duration is wide enough
    if duration > 50:
        ax.text(start + duration/2, y, label, 
                ha='center', va='center', fontsize=10, weight='bold')

# Add arrows showing data flow
arrow_props = dict(arrowstyle='->', lw=2, color='gray')
ax.annotate('', xy=(1100, 0.7), xytext=(1000, 0.3), arrowprops=arrow_props)
ax.annotate('', xy=(2050, 1.7), xytext=(2000, 1.3), arrowprops=arrow_props)
ax.annotate('', xy=(2100, 2.7), xytext=(2090, 2.3), arrowprops=arrow_props)
ax.annotate('', xy=(2300, 3.7), xytext=(2101, 3.3), arrowprops=arrow_props)

# Formatting
ax.set_xlim(0, 3000)
ax.set_ylim(-0.5, len(components)-0.5)
ax.set_xlabel('Time (μs)', fontsize=12, weight='bold')
ax.set_yticks(range(len(components)))
ax.set_yticklabels(components, fontsize=11)
ax.set_title('DRIP Control Loop Timing (<3ms Total)', fontsize=14, weight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Add total time annotation
ax.axvline(x=2500, color='red', linestyle='--', alpha=0.5)
ax.text(2500, 4.2, 'Total: 2.5ms', ha='center', fontsize=12, 
        weight='bold', color='red')

# Add requirement line
ax.axvline(x=3000, color='green', linestyle='--', alpha=0.5)
ax.text(3000, 4.2, 'SR014: 3ms', ha='center', fontsize=12, 
        weight='bold', color='green')

plt.tight_layout()
plt.savefig('/Users/jmarwell/Desktop/Projects/drip/acoustic-sysml-v2/docs/behavioral/diagrams/control-loop-timing.png', dpi=150, bbox_inches='tight')
plt.close()

# Create a second diagram showing parallel processing
fig2, ax2 = plt.subplots(figsize=(10, 8))

# Define parallel processes
processes = {
    'Main Control': [
        (0, 1000, 'Thermal Capture'),
        (1000, 900, 'Processing'),
        (1900, 100, 'FPGA Update'),
        (2000, 500, 'Wait Next Cycle')
    ],
    'Droplet Tracking': [
        (0, 200, 'Position Update'),
        (200, 300, 'Trajectory Calc'),
        (500, 200, 'Collision Check'),
        (700, 1800, 'Continuous Monitoring')
    ],
    'Thermal Control': [
        (0, 100, 'Read Sensors'),
        (100, 200, 'PID Compute'),
        (300, 100, 'Heater Adjust'),
        (400, 2100, 'Temperature Regulation')
    ],
    'Safety Monitor': [
        (0, 50, 'E-Stop Check'),
        (500, 50, 'E-Stop Check'),
        (1000, 50, 'E-Stop Check'),
        (1500, 50, 'E-Stop Check'),
        (2000, 50, 'E-Stop Check')
    ]
}

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD93D']

for i, (process, events) in enumerate(processes.items()):
    y_base = i
    color = colors[i % len(colors)]
    
    # Draw process label
    ax2.text(-200, y_base, process, ha='right', va='center', 
             fontsize=11, weight='bold')
    
    # Draw events
    for start, duration, label in events:
        rect = patches.Rectangle((start, y_base-0.3), duration, 0.6,
                                linewidth=1, edgecolor='black',
                                facecolor=color, alpha=0.7)
        ax2.add_patch(rect)
        
        if duration > 100:
            ax2.text(start + duration/2, y_base, label,
                    ha='center', va='center', fontsize=9)

# Add synchronization lines
for t in [0, 1000, 2000]:
    ax2.axvline(x=t, color='gray', linestyle=':', alpha=0.5)
    ax2.text(t, -0.7, f'{t/1000:.0f}ms', ha='center', fontsize=10)

ax2.set_xlim(-300, 2500)
ax2.set_ylim(-1, len(processes))
ax2.set_xlabel('Time (μs)', fontsize=12, weight='bold')
ax2.set_title('Parallel Process Execution in DRIP System', 
              fontsize=14, weight='bold')
ax2.grid(True, alpha=0.3, axis='x')
ax2.set_yticks([])

plt.tight_layout()
plt.savefig('/Users/jmarwell/Desktop/Projects/drip/acoustic-sysml-v2/docs/behavioral/diagrams/parallel-processes.png', dpi=150, bbox_inches='tight')
plt.close()

print("Control loop timing diagrams generated successfully!")
print("- control-loop-timing.png")
print("- parallel-processes.png")