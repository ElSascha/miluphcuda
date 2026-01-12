import numpy as np
import matplotlib.pyplot as plt

# setup in SI units
# two balls colliding with speed 1 m/s with an offset
radius = 1.0
dx = 0.1
offset_dx = radius+1.1*dx
offset_dy = radius/1.1
collision_velocity = 3.0
density = 1e3
m = density * dx**3

# smoothing length (SPH) as 1.2x particle spacing
h = 1.8 * dx

x = np.arange(-radius*1.5, radius*1.5, dx)

xg, yg, zg = np.meshgrid(x, x, x)


xb1 = xg[np.where(xg**2 + yg**2 + zg**2 <= radius**2)]
yb1 = yg[np.where(xg**2 + yg**2 + zg**2 <= radius**2)]
zb1 = zg[np.where(xg**2 + yg**2 + zg**2 <= radius**2)]
vxb1 = np.ones_like(xb1) * collision_velocity/2.
vxb2 = np.ones_like(xb1) * -collision_velocity/2.
vyb1 = np.zeros_like(yb1)
vyb2 = np.zeros_like(yb1)
vzb1 = np.zeros_like(zb1)
vzb2 = np.zeros_like(zb1)
mb1 = np.ones_like(xb1) * m
mb2 = np.ones_like(xb1) * m
rhob1 = np.ones_like(xb1) * density
rhob2 = np.ones_like(xb1) * density
material_typeb1 = np.ones_like(xb1, dtype=int) * 0
material_typeb2 = np.ones_like(xb1, dtype=int) * 0
Sb1 = np.zeros((len(xb1), 9))
Sb2 = np.zeros((len(xb1), 9))

xb2 = xb1 + offset_dx
yb2 = yb1 + offset_dy
zb2 = zb1
xb1 = xb1 - offset_dx
yb1 = yb1 - offset_dy

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.scatter(xb1, yb1, zb1, color='b', s=1)
# ax.scatter(xb2, yb2, zb2, color='r', s=1)
# ax.set_box_aspect([1,1,1])
# plt.show()
np.savetxt('particles_ball1.ini', np.c_[xb1, yb1, zb1, vxb1, vyb1, vzb1, mb1, rhob1, material_typeb1, Sb1.reshape(len(Sb1),9)])
np.savetxt('particles_ball2.ini', np.c_[xb2, yb2, zb2, vxb2, vyb2, vzb2, mb2, rhob2, material_typeb2, Sb2.reshape(len(Sb2),9)])