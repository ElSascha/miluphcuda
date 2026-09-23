import numpy as np
import matplotlib.pyplot as plt
import os

# Determine which file to read
possible_files = ['data/cube.0000']
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

# Load density data on place 8 starting from 1
density = data[:, 7] if data.shape[1] > 7 else None

# Extract x, y, z coordinates (first three columns)
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]

# Decide coloring: density (prefer explicit density for legacy file; otherwise estimate)
cmap = plt.get_cmap('viridis')
if density is not None:
    colors = density
else:
    colors = np.linalg.norm(data[:, 3:6], axis=1)
color_label = 'Density (Kg/m³)'

# Create a 3D scatter plot of the particle positions
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z, c=colors, cmap=cmap, s=40)
ax.set_title(f'Initial Particle Distribution', fontsize=22)
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label(color_label, fontsize=16, labelpad=15)
cbar.ax.tick_params(labelsize=14)
ax.set_xlabel('X (m)', fontsize=16, labelpad=15)
ax.set_ylabel('Y (m)', fontsize=16, labelpad=15)
ax.set_zlabel('Z (m)', fontsize=16, labelpad=15)
ax.tick_params(axis='x', labelsize=14, pad=5)
ax.tick_params(axis='y', labelsize=14, pad=5)
ax.tick_params(axis='z', labelsize=14, pad=5)


# Enforce equal scale on all three axes
xmin, xmax = float(x.min()), float(x.max())
ymin, ymax = float(y.min()), float(y.max())
zmin, zmax = float(z.min()), float(z.max())

xc, yc, zc = (xmin + xmax) / 2.0, (ymin + ymax) / 2.0, (zmin + zmax) / 2.0
rx, ry, rz = (xmax - xmin), (ymax - ymin), (zmax - zmin)
max_range = max(rx, ry, rz, 1e-12)

# Add ~5% padding
half = 0.5 * max_range * 1.05
ax.set_xlim([xc - half, xc + half])
ax.set_ylim([yc - half, yc + half])
ax.set_zlim([zc - half, zc + half])

# If available (mpl>=3.3), set equal box aspect
setattr(ax, 'set_box_aspect', getattr(ax, 'set_box_aspect', None))
if callable(getattr(ax, 'set_box_aspect', None)):
	ax.set_box_aspect((1, 1, 1))

plt.savefig('Basalt_initial_cube_dist_velocity_shepard.png', dpi=300)
plt.show()