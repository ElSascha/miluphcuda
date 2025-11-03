import numpy as numpy

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
cube_size = 5.0  # Size of the cube (length of one side) in meters
num_particles_per_axis = 50  # Number of particles along each axis
cube_particle_spacing = cube_size / num_particles_per_axis  # Spacing between particles
projectile_radius = 0.5  # Radius of the projectile in meters
projectile_initial_position = numpy.array([0.0, 0.0, 15.0])  # Initial position of the projectile
projectile_velocity = numpy.array([0.0, 0.0, -20.0])  # Velocity of the projectile in m/s
density_solid = 7860.0  # Density of solid material in kg/m^3 (Iron)
density_porous = 2500.0 # Density of porous material in kg/m^ (Basalt with porosity)
porous_shell_thickness = 0.2  # Thickness of the porous shell in meters
output_file = 'particles.txt'  # Output file name
# Generate particle positions
particles = []
for i in range(num_particles_per_axis):
    for j in range(num_particles_per_axis):
        for k in range(num_particles_per_axis):
            position = numpy.array([
                -cube_size / 2 + i * cube_particle_spacing,
                -cube_size / 2 + j * cube_particle_spacing,
                -cube_size / 2 + k * cube_particle_spacing
            ])
            # Determine if the particle is in the porous shell or solid core
            distance_from_center = numpy.linalg.norm(position)
            if distance_from_center >= (cube_size / 2 - porous_shell_thickness):
                density = density_porous  # Porous material
            else:
                density = density_solid  # Solid material
            velocity = numpy.array([0.0, 0.0, 0.0])  # Initial velocity of cube particles
            particles.append((position, velocity, density))
# Add projectile particles
num_projectile_particles = 10000  # Number of particles in the projectile
for n in range(num_projectile_particles):
    # Randomly distribute particles within the sphere
    while True:
        random_position = numpy.random.uniform(-projectile_radius, projectile_radius, 3)
        if numpy.linalg.norm(random_position) <= projectile_radius:
            break
    position = projectile_initial_position + random_position
    velocity = projectile_velocity  # Initial velocity of projectile particles
    density = density_solid  # Solid material for projectile
    particles.append((position, velocity, density))
# Save particles to file
with open(output_file, 'w') as f:
    for position, velocity, density in particles:
        f.write(f"{position[0]} {position[1]} {position[2]} {velocity[0]} {velocity[1]} {velocity[2]} {density}\n") 
print(f"Generated {len(particles)} particles and saved to '{output_file}'.")
