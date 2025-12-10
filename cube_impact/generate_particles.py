import numpy as np

"""
Generate initial particle positions for cube impact simulation.
This script creates a cubic lattice of particles within a defined volume, using a specified number of particles along each axis.
The cube has an outer shell of particles of a porous material and an inner core of solid material. 
Furthermore a projectile (sphere) hits the cube with a defined velocity.
The cube has the dimensions 10m x 10m x 10m and is centered at the origin.
The projectile has a radius of 1m and is initially positioned at (0, 0, 15) with a velocity of (0, 0, -20)m/s.
The generated particle data is saved to a text file named 'particles.txt'.
"""

# Parameters
cube_size = 10.0  # Size of the cube (length of one side) in meters
num_particles_per_axis = 20  # Number of particles along each axis
cube_particle_spacing = cube_size / num_particles_per_axis  # Spacing between particles

#For the projektile we put the particles in a grid and cut out a sphere
projectile_radius = 2.0 # Radius of the projectile in meters
num_projectile_particles_per_axis = int(np.ceil(projectile_radius / cube_particle_spacing))  # Number of particles along each axis for the projectile in rectangle grid

projectile_initial_position = np.array([0.0, 0.0, 8.0])  # Initial position of the projectile
projectile_velocity = np.array([0.0, 0.0, -200.0])  # Velocity of the projectile in m/s
density_solid = 7.68e3  # Density of solid material in kg/m^3 (Iron)
density_porous = 2.86e3  # Density of porous material in kg/m^3 (Basalt with porosity)
mass_solid = density_solid * cube_particle_spacing**3  # Mass of solid particle
mass_projectile = density_solid * cube_particle_spacing**3  # Mass of projectile particle
mass_porous = density_porous * cube_particle_spacing**3  # Mass of porous particle
porous_shell_thickness = 3.0  # Thickness of the porous shell in meters
# Output file name: use the miluphcuda ASCII input convention (basename.XXXX)
output_file = 'particles.0000'
# material type indices (must match entries in material.cfg)
material_solid = 0
material_porous = 1
# default per-particle fields

default_stress = [0.0] * 9  # S00, S01, S02, S10, S11, S12, S20, S21, S22
# Generate particle positions
particles = []
for i in range(num_particles_per_axis):
    for j in range(num_particles_per_axis):
        for k in range(num_particles_per_axis):
            position = np.array([
                -cube_size / 2 + i * cube_particle_spacing,
                -cube_size / 2 + j * cube_particle_spacing,
                -cube_size / 2 + k * cube_particle_spacing
            ])
            # Determine if the particle is in the porous shell or solid core
            distance_from_center = np.linalg.norm(position)
            if distance_from_center >= (cube_size / 2 - porous_shell_thickness):
                density = density_porous  # Porous material
                material_type = material_porous
                mass = mass_porous
            else:
                density = density_solid  # Solid material
                material_type = material_solid
                mass = mass_solid
            velocity = np.array([0.0, 0.0, 0.0])  # Initial velocity of cube particles
            particles.append((position, velocity, mass, material_type))
# put projectile particles in a grid and cut out a sphere
for i in range(-num_projectile_particles_per_axis, num_projectile_particles_per_axis + 1):
    for j in range(-num_projectile_particles_per_axis, num_projectile_particles_per_axis + 1):
        for k in range(-num_projectile_particles_per_axis, num_projectile_particles_per_axis + 1):
            position = np.array([
                i * cube_particle_spacing,
                j * cube_particle_spacing,
                k * cube_particle_spacing
            ])
            if np.linalg.norm(position) <= projectile_radius:
                world_position = projectile_initial_position + position
                velocity = projectile_velocity
                mass = mass_projectile
                material_type = material_solid
                particles.append((world_position, velocity, mass, material_type))




# Save particles to file
with open(output_file, 'w') as f:
    for position, velocity, mass, material_type in particles:
        # Columns required by miluphcuda (3D solid):
        # x y z vx vy vz mass energy material_type DIM-root S00 S01 S02 S10 S11 S12 S20 S21 S22
        parts = [
            f"{position[0]:.6e}", f"{position[1]:.6e}", f"{position[2]:.6e}",
            f"{velocity[0]:.6e}", f"{velocity[1]:.6e}", f"{velocity[2]:.6e}",
            f"{mass:.6e}",
            str(material_type),
        ] + [f"{s:.6e}" for s in default_stress]
        # no flaw thresholds appended because default_num_flaws == 0
        f.write(" ".join(parts) + "\n")

print(f"Generated {len(particles)} particles and saved to '{output_file}'.")
