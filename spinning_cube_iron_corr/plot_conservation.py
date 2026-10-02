import pandas as pd
import matplotlib.pyplot as plt
import os
import subprocess
# # 1:time 2:SPH-part-total 3:SPH-part-deactivated 4:grav.point-masses 5:total-mass 6:total-kinetic-energy 7:total-inner-energy 8:total-momentum 9:total-momentum[x] 10:total-momentum[y] 
# 11:total-momentum[z] 12:total-angular-mom 13:total-angular-mom[x] 14:total-angular-mom[y] 15:total-angular-mom[z] 16:barycenter-pos[x] 17:barycenter-pos[y] 18:barycenter-pos[z] 19:barycenter-vel[x] 20:barycenter-vel[y] 21:barycenter-vel[z]
"""
Plots the evolution of angular momentum and total energy from the
conserved_quantities.log file. The two conservation plots are shown side by
side.

|L_initial - L_step| / |L_initial| vs time is also plotted to show conservation.

"""

# Load the conserved quantities log file
log_file = 'conserved_quantities_iron_small.log'
if not os.path.exists(log_file):
    raise FileNotFoundError(f'Log file {log_file} not found.')
column_names = [
    "time", "SPH-part-total", "SPH-part-deactivated", "grav.point-masses", "total-mass",
    "total-kinetic-energy", "total-inner-energy", "total-momentum", "total-momentum[x]", "total-momentum[y]", "total-momentum[z]",
    "total-angular-mom", "total-angular-mom[x]", "total-angular-mom[y]", "total-angular-mom[z]",
    "barycenter-pos[x]", "barycenter-pos[y]", "barycenter-pos[z]",
    "barycenter-vel[x]", "barycenter-vel[y]", "barycenter-vel[z]"
]
data = pd.read_csv(log_file, sep='\s+', comment='#', names=column_names)
time = data['time']
Lx = data['total-angular-mom[x]']
Ly = data['total-angular-mom[y]']
Lz = data['total-angular-mom[z]']
L_magnitude = (Lx**2 + Ly**2 + Lz**2)**0.5
L_initial = L_magnitude.iloc[1]
L_deviation = abs(L_initial - L_magnitude) / abs(L_initial)
E_kin = data['total-kinetic-energy']
E_inner = data['total-inner-energy']
E_total = E_kin + E_inner
E_deviation = abs(E_total - E_total.iloc[1]) / abs(E_total.iloc[1])
# Create both plots side by side in one figure.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6), sharex=True)

ax1.plot(time, L_deviation, label='|L_initial - L_step| / |L_initial|')
ax1.set_ylabel('Angular Momentum Deviation', color='k', fontsize=25, labelpad=15)
ax1.tick_params(axis='x', labelsize=20, pad=5)
ax1.tick_params(axis='y', labelsize=20, pad=5)
ax1.yaxis.get_offset_text().set_fontsize(16)
ax1.set_xlabel('Time (s)', fontsize=25, labelpad=15)
ax1.set_title('Angular Momentum Conservation', fontsize=27)
ax1.legend(fontsize=16)
ax1.grid(True)

ax2.plot(time, E_deviation, label='Total Energy Deviation', color='orange')
ax2.set_ylabel('||E - E0|| / ||E0||', color='k', fontsize=25, labelpad=15)
ax2.tick_params(axis='x', labelsize=20, pad=5)
ax2.tick_params(axis='y', labelsize=20, pad=5)
ax2.yaxis.get_offset_text().set_fontsize(16)
ax2.set_xlabel('Time (s)', fontsize=25, labelpad=15)
ax2.set_title('Total Energy Conservation', fontsize=27)
ax2.legend(fontsize=16)
ax2.grid(True)

output_file = 'energy_angular_momentum_conservation.png'
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f'Plot saved to {output_file}')
plt.show()
