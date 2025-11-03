import numpy as np
import matplotlib.pyplot as plt
"""
Plot the initial distribution of particles generated for the cube impact simulation.
"""

# Load particle data from the generated file
data = np.loadtxt(r'particles.txt')
positions = data[:, :3]
# Extract x, y, z coordinates
x = positions[:, 0]
y = positions[:, 1]
z = positions[:, 2]
# Create a 3D scatter plot of the particle positions
# different colors for different densities
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z, s=1, alpha=0.5, c=data[:, 6], cmap='viridis')
ax.set_title('Initial Particle Distribution for Cube Impact Simulation')
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('Density (kg/m³)')
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 10])
plt.savefig('initial_particle_distribution.png', dpi=300)
plt.show()
