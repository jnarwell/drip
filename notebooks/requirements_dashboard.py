import pandas as pd
import matplotlib.pyplot as plt

# Create requirements tracking DataFrame
data = {
    'Level': [1, 2, 3, 4],
    'Cost': [14320, 44470, 78620, 163970],
    'Power': [12000, 25000, 30000, 45000],
    'Volume': [125, 1000, 1000, 8000],
    'Transducers': [18, 36, 36, 72],
    'Outlets': [25, 100, 100, 400]
}

df = pd.DataFrame(data)

# Generate visualizations
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Cost progression
axes[0, 0].bar(df['Level'], df['Cost'])
axes[0, 0].set_title('Cost by Level')
axes[0, 0].set_ylabel('Cost ($)')

# Power scaling
axes[0, 1].plot(df['Level'], df['Power'], 'o-')
axes[0, 1].set_title('Power Requirements')
axes[0, 1].set_ylabel('Power (W)')

# Volume scaling
axes[1, 0].bar(df['Level'], df['Volume'])
axes[1, 0].set_title('Build Volume')
axes[1, 0].set_ylabel('Volume (cm³)')

# Component scaling
axes[1, 1].plot(df['Level'], df['Transducers'], 'o-', label='Transducers')
axes[1, 1].plot(df['Level'], df['Outlets'], 's-', label='Outlets')
axes[1, 1].set_title('Component Scaling')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('reports/requirements_dashboard.png')
plt.show()

print("Dashboard saved to reports/requirements_dashboard.png")