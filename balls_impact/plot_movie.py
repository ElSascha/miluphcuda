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
data_dir = os.path.join(script_dir, 'data')
output_dir = os.path.join(script_dir, 'movie_frames')
os.makedirs(output_dir, exist_ok=True)
# Find all HDF5 particle files
particle_files = sorted([f for f in os.listdir(data_dir) if f.startswith('balls.') and f.endswith('.h5')])

# Determine axis limits from the first frame to use for all frames to KEEP ZOOM CONSTANT
fixed_half_span = None

if particle_files:
    with h5py.File(os.path.join(data_dir, particle_files[0]), 'r') as f:
        pos = f['x'][:]
    if pos.ndim == 1:
        pos = pos.reshape(1, -1)
    
    # Find the bounding box of the data
    min_coords = np.min(pos, axis=0)
    max_coords = np.max(pos, axis=0)
    
    # Calculate the largest span
    max_span = np.max(max_coords - min_coords)
    if max_span == 0: max_span = 1.0
    
    # Set fixed span based on first frame (constant zoom level)
    fixed_half_span = max_span / 2 * 1.5  # Add 50% buffer to keep them in view longer
else:
    fixed_half_span = 1.0

# Loop over each particle file and generate a plot
for frame_idx, particle_file in enumerate(particle_files):
    with h5py.File(os.path.join(data_dir, particle_file), 'r') as f:
        pos = f['x'][:]
        rho = f['rho'][:]
        vel = f['v'][:]
    if pos.ndim == 1:
        pos = pos.reshape(1, -1)

    # Calculate dynamic center to track the system
    min_coords = np.min(pos, axis=0)
    max_coords = np.max(pos, axis=0)
    center = (max_coords + min_coords) / 2
    
    # Use FIXED span to prevent balls from looking smaller (constant zoom)
    lim_min = center - fixed_half_span
    lim_max = center + fixed_half_span

    x = pos[:, 0]
    y = pos[:, 1]
    z = pos[:, 2]

    time_step_size = 0.001 # assuming constant time step size; adjust as needed

    colors = np.linalg.norm(vel, axis=1)
    color_label = 'Velocity magnitude (m/s)'

    fig = plt.figure(figsize=(8, 8)) # Use a square figure for better aspect ratio
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c=colors, cmap='viridis', s=40)
    ax.set_title(f'Particle velocity at t = {frame_idx * time_step_size:.3f} s', fontsize=20)
    ax.set_xlabel('X (m)', fontsize=18, labelpad=15)
    ax.set_ylabel('Y (m)', fontsize=18, labelpad=15)
    ax.set_zlabel('Z (m)', fontsize=18, labelpad=15)
    ax.tick_params(axis='both', which='major', labelsize=16, pad=5)
    # make dynamic limits based on location of the particles
    ax.set_xlim(-3 , 3)
    ax.set_ylim(-3 , 3)
    ax.set_zlim(-3 , 3)
    ax.set_box_aspect([1,1,1])  # Set aspect ratio to be equal
    cbar = plt.colorbar(sc, shrink=0.6, pad=0.15)
    cbar.set_label(color_label, fontsize=18, labelpad=10)
    cbar.ax.tick_params(labelsize=16)
    plt.tight_layout()
    frame_filename = os.path.join(output_dir, f'frame_{frame_idx:04d}.png')
    plt.savefig(frame_filename, dpi=300)
    plt.close(fig)
print(f'Generated {len(particle_files)} frames in directory: {output_dir}')
