#create particle distribution files for testing
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import h5py

# Create a cubic grid of particles saved in a particles.0000 text file that rotates around the z axis
# input file format for file <particles.XXXX>:
#1:x[0] 2:x[1] 3:x[2] 4:v[0] 5:v[1] 6:v[2] 7:mass 8:density 9:energy 10:smoothing length 11:material type 12:S/sigma[0][0] 13:S/sigma[0][1] 14:S/sigma[0][2] 15:S/sigma[1][0] 16:S/sigma[1][1] 17:S/sigma[1][2] 18:S/sigma[2][0] 19:S/sigma[2][1] 20:S/sigma[2][2] 21:alpha_jutzi 22:pressure 

def create_cube_distribution(n_particles_per_side, size, filename, rho_solid, alpha_jutzi, omega):
    # Create a cubic grid of cell-centered particles.
    # For p-alpha porosity (PALPHA_POROSITY), rho in the particle file is the *bulk* density.
    # Consistent initial conditions require rho_bulk = rho_solid / alpha_jutzi.
    spacing = size / n_particles_per_side
    coords = (np.arange(n_particles_per_side) + 0.5) * spacing
    x, y, z = np.meshgrid(coords, coords, coords, indexing='ij')
    
    # Flatten and stack positions
    positions = np.column_stack([x.ravel(), y.ravel(), z.ravel()])
    
    # Create velocities for rotation around z axis
    n_particles = n_particles_per_side ** 3
    velocities = np.zeros((n_particles, 3))

    # Rotate about the cube center
    center_x = coords.mean()
    center_y = coords.mean()
    dx = positions[:, 0] - center_x
    dy = positions[:, 1] - center_y
    velocities[:, 0] = -omega * dy  # vx = -ω y
    velocities[:, 1] = omega * dx   # vy =  ω x
    velocities[:, 2] = 0.0
    
    # Verify zero net momentum
    print(f"Net momentum: vx={velocities[:,0].mean():.2e}, vy={velocities[:,1].mean():.2e}")
    
    # Create density and pressure columns
    rho_bulk = rho_solid / alpha_jutzi
    mass = (rho_bulk * spacing**3)
    density = rho_bulk
    energy = 0.0
    material_type = 0
    smoothing_length = spacing * 1.2  # typical choice for initial smoothing length
    S_sigma = np.zeros((n_particles, 9))  # 3x3 stress tensor flattened
    pressure = 0.0
    # Combine all data into one array
    data = np.column_stack([
        positions,
        velocities,
        np.full(n_particles, mass),
        np.full(n_particles, density),
        np.full(n_particles, energy),
        np.full(n_particles, smoothing_length),
        np.full(n_particles, material_type),
        S_sigma,
        np.full(n_particles, alpha_jutzi),
        np.full(n_particles, pressure)
    ])
    # save to txt file
    np.savetxt(filename, data, fmt='%.6e')
    print(f"Created cube distribution with {n_particles} particles in '{filename}'")


if __name__ == "__main__":
    # rho_solid should match till_rho_0 in material.cfg for Tillotson.
    create_cube_distribution(15, 1.0, r'particles.0000', rho_solid=2700.0, alpha_jutzi=1.25, omega=1.0)
    
