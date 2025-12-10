import numpy as np
import matplotlib.pyplot as plt
import os
"""
Plot the initial distribution of particles generated for the cube impact simulation.
\n+This script reads the miluphcuda ASCII particle file format (e.g., particles.0000)
and plots particle positions. It colors by material type when available (new format)
or by density when reading the older particles.txt (legacy format). Point size is
scaled by mass.
"""

# Determine which file to read
possible_files = ['particles.0000', 'particles.txt']
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
z = data[:, 2]

# Mass is column 6 in both new and old formats
mass = data[:, 6] if data.shape[1] > 6 else np.ones_like(x)

# Decide coloring: density (prefer explicit density for legacy file; otherwise estimate)
cmap = plt.get_cmap('viridis')

def _infer_spacing(vals, min_count=10, round_dec=6):
	# Group by rounded coordinate and count occurrences; grid planes have high counts
	rounded = np.round(vals, round_dec)
	unique_vals, counts = np.unique(rounded, return_counts=True)
	grid_mask = counts >= min_count
	grid_vals = unique_vals[grid_mask]
	if grid_vals.size < 2:
		return None
	diffs = np.diff(np.sort(grid_vals))
	# Use median diff as robust spacing
	spacing = np.median(diffs)
	return float(spacing) if spacing > 0 else None

if data_file.endswith('particles.txt') and data.shape[1] > 7:
	# Legacy file with explicit density column at index 7
	colors = data[:, 7]
	color_label = 'Density'
else:
	# New format: estimate spacing from the lattice planes, prefer x then y then z
	spacing = _infer_spacing(x)
	if spacing is None:
		spacing = _infer_spacing(y)
	if spacing is None:
		spacing = _infer_spacing(z)
	if spacing is not None:
		particle_vol = spacing ** 3
		colors = mass / particle_vol
		color_label = 'Density'
	else:
		# Fallback: use mass as a proxy (monotonic with density when spacing is uniform)
		colors = mass
		color_label = 'Density (proxy)'

# Scale marker size by mass
mass_mean = np.mean(mass) if mass.size else 1.0
sizes = np.clip((mass / mass_mean) * 2.0, 0.5, 8.0)

# Create a 3D scatter plot of the particle positions
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z, s=sizes, alpha=0.6, c=colors, cmap=cmap)
ax.set_title(f'Initial Particle Distribution ({os.path.basename(data_file)})')
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label(color_label)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')

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

plt.savefig('initial_particle_distribution.png', dpi=300)
plt.show()