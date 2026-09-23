import numpy as np
import matplotlib.pyplot as plt
import os

# Determine which file to read
possible_files = ['data/balls.0000']
data_file = None
for fn in possible_files:
	if os.path.exists(fn):
		data_file = fn
		break

if data_file is None:
	raise FileNotFoundError('No particle file found. Expected one of: ' + ', '.join(possible_files))

# Load particle data from the selected file
data = np.loadtxt(data_file)
if data.ndim == 1:
	data = data.reshape(1, -1)

# Extract x, y, z coordinates (first three columns)
x = data[:, 0]
y = data[:, 1]

# Decide coloring: density (prefer explicit density for legacy file; otherwise estimate)
cmap = plt.get_cmap('viridis')
colors = np.linalg.norm(data[:, 3:6], axis=1)
color_label = 'Velocity magnitude (m/s)'

# create 2d scatter plot of the particle positions
fig, ax = plt.subplots(figsize=(8, 8))
scatter = ax.scatter(x, y, c=colors, cmap=cmap, s=40)
ax.set_title(f'Initial Particle Distribution', fontsize=22)
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label(color_label, fontsize=16, labelpad=15)
cbar.ax.tick_params(labelsize=14)
ax.set_xlabel('X (m)', fontsize=16, labelpad=15)
ax.set_ylabel('Y (m)', fontsize=16, labelpad=12)
ax.tick_params(axis='x', labelsize=14, pad=5)
ax.tick_params(axis='y', labelsize=14, pad=5)
ax.grid(True)
# Enforce equal scale on both axes
xmin, xmax = float(x.min()), float(x.max())
ymin, ymax = float(y.min()), float(y.max())
xc, yc = (xmin + xmax) / 2.0, (ymin + ymax) / 2.0
rx, ry = (xmax - xmin), (ymax - ymin)
max_range = max(rx, ry, 1e-12)
# Add ~5% padding
half = 0.5 * max_range * 1.05
ax.set_xlim([xc - half, xc + half])
ax.set_ylim([yc - half, yc + half])
plt.savefig('Basalt_2d_initial_balls_dist_velocity.png', dpi=300)
plt.show()