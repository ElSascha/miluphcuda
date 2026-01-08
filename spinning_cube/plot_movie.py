import numpy as np
import h5py
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')

"""
Plot particle distributions from simulation output files as a movie in 3d.
This script reads miluphcuda HDF5 output files (e.g., particles.0000.h5, particles.0001.h5, ...)
and generates a series of plots showing the particle positions at each timestep. The plots are saved as PNG files
in a directory named 'movie_frames', which can be combined into a movie using external tools like ffmpeg.
"""

def _infer_spacing(coords):
    """Infer particle spacing from a 1D array of coordinates."""
    unique_coords = np.unique(coords)
    if len(unique_coords) < 2:
        return None
    diffs = np.diff(np.sort(unique_coords))
    # Filter out near-zero differences
    diffs = diffs[diffs > 1e-9]
    if len(diffs) == 0:
        return None
    # Use a histogram to find the most common spacing
    hist, bins = np.histogram(diffs, bins=100)
    return bins[np.argmax(hist)]

# Create output directory for frames
script_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(script_dir, 'movie_frames_density')
os.makedirs(output_dir, exist_ok=True)
# Find all HDF5 particle files
particle_files = sorted([f for f in os.listdir(script_dir) if f.startswith('particles.') and f.endswith('.h5')])

# Determine axis limits from the first frame to use for all frames
if particle_files:
    with h5py.File(os.path.join(script_dir, particle_files[0]), 'r') as f:
        pos = f['x'][:]
    if pos.ndim == 1:
        pos = pos.reshape(1, -1)
    
    # Find the bounding box of the data
    min_coords = np.min(pos, axis=0)
    max_coords = np.max(pos, axis=0)
    
    # Calculate the center and the largest span
    center = (max_coords + min_coords) / 2
    max_span = np.max(max_coords - min_coords)
    
    # Set limits to create a cubic bounding box
    half_span = max_span / 2 * 1.1  # Add 10% buffer
    lim_min = center - half_span
    lim_max = center + half_span
else:
    # Fallback limits
    lim_min = np.array([-1, -1, -1])
    lim_max = np.array([1, 1, 1])

# Loop over each particle file and generate a plot
for frame_idx, particle_file in enumerate(particle_files):
    with h5py.File(os.path.join(script_dir, particle_file), 'r') as f:
        pos = f['x'][:]
        rho = f['rho'][:]
    if pos.ndim == 1:
        pos = pos.reshape(1, -1)
    x = pos[:, 0]
    y = pos[:, 1]
    z = pos[:, 2]

    colors = rho
    color_label = 'Density (kg/m^3)'

    fig = plt.figure(figsize=(8, 8)) # Use a square figure for better aspect ratio
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c=colors, cmap='viridis', s=50)
    ax.set_title(f'Particle Density at Frame {frame_idx}')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_xlim(lim_min[0], lim_max[0])
    ax.set_ylim(lim_min[1], lim_max[1])
    ax.set_zlim(lim_min[2], lim_max[2])
    ax.set_aspect('equal', adjustable='box')
    plt.colorbar(sc, label=color_label, shrink=0.6)
    plt.tight_layout()
    frame_filename = os.path.join(output_dir, f'frame_{frame_idx:04d}.png')
    plt.savefig(frame_filename, dpi=300)
    plt.close(fig)
print(f'Generated {len(particle_files)} frames in directory: {output_dir}')
