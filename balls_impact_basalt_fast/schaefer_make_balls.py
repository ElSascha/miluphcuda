import numpy as np

# =========================
# Setup
# =========================
radius = 1.0
dx = 0.1
density = 2.86e3
collision_velocity = 1000.0

m = density * dx**3

offset_dx = int(radius / dx) * dx
offset_dy = int(0.5 * radius / dx) * dx

# =========================
# Reference sphere WITHOUT extreme points
# =========================
steps = int(np.ceil(radius / dx))
coords = np.arange(-steps, steps + 1) * dx

xg, yg, zg = np.meshgrid(coords, coords, coords, indexing="ij")

# shrink radius slightly to kill isolated surface particles
alpha = 0.75        # between 0.5 and 1.0 works well
r_eff = radius - alpha * dx

mask = (xg**2 + yg**2 + zg**2) <= r_eff**2

xref = np.column_stack((xg[mask], yg[mask], zg[mask]))
npart = len(xref)

# =========================
# Two identical balls
# =========================
x1 = xref.copy()
x1[:, 0] -= offset_dx
x1[:, 1] -= offset_dy

x2 = xref.copy()
x2[:, 0] += offset_dx
x2[:, 1] += offset_dy

v1 = np.zeros_like(x1) 
v2 = np.zeros_like(x2)

v1[:, 0] = +collision_velocity / 2.0
v2[:, 0] = -collision_velocity / 2.0

# =========================
# Properties
# =========================
mass = np.full(npart, m)
rho = np.full(npart, density)
material = np.ones(npart, dtype=int) * 0 # material type 0
stress = np.zeros((npart, 9))
sml = np.full(npart, dx * 3.8) # Wendland c4 kernel support radius is 1.866 * dx for 3D, so this ensures that each particle has neighbors to interact with
energy = np.zeros(npart)

p1 = np.c_[x1, v1, mass, rho, energy, sml, material, stress]
p2 = np.c_[x2, v2, mass, rho, energy, sml, material, stress]

particles = np.vstack((p1, p2))
np.savetxt("data/balls.0000", particles)