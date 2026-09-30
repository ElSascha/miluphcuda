# Plot the rotational speed of both spheres as a function of time.
import matplotlib.pyplot as plt
from pathlib import Path

import h5py
import numpy as np


def angular_velocity(position, velocity, mass):
    """Return the rigid-body angular velocity fitted to particle motion."""
    total_mass = mass.sum()
    center_of_mass = np.sum(position * mass[:, None], axis=0) / total_mass
    center_velocity = np.sum(velocity * mass[:, None], axis=0) / total_mass
    relative_position = position - center_of_mass
    relative_velocity = velocity - center_velocity

    angular_momentum = np.sum(
        mass[:, None] * np.cross(relative_position, relative_velocity), axis=0
    )
    inertia = np.sum(
        mass[:, None, None]
        * (
            np.sum(relative_position**2, axis=1)[:, None, None] * np.eye(3)
            - relative_position[:, :, None] * relative_position[:, None, :]
        ),
        axis=0,
    )
    return np.linalg.lstsq(inertia, angular_momentum, rcond=None)[0]


def plot_rotational_speed(
    data_dir='data', output_file='rotational_speed.png', frame_stride=10
):
    particle_files = sorted(Path(data_dir).glob('balls.*.h5'))
    if not particle_files:
        raise FileNotFoundError(f'No HDF5 particle files found in {data_dir}.')
    particle_files = particle_files[::frame_stride]

    times = []
    angular_velocities = [[], []]
    mass = None
    for frame_number, particle_file in enumerate(particle_files, start=1):
        with h5py.File(particle_file, 'r') as file:
            position = file['x'][:]
            velocity = file['v'][:]
            if mass is None:
                mass = file['m'][:]
            times.append(float(file['time'][()]))

        midpoint = len(position) // 2
        particle_groups = (slice(0, midpoint), slice(midpoint, None))
        for sphere, particle_slice in enumerate(particle_groups):
            angular_velocities[sphere].append(
                angular_velocity(
                    position[particle_slice],
                    velocity[particle_slice],
                    mass[particle_slice],
                )
            )
        if frame_number % 25 == 0:
            print(f'Processed {frame_number}/{len(particle_files)} frames')

    times = np.asarray(times)
    angular_velocities = np.asarray(angular_velocities)
    order = np.argsort(times)
    times = times[order]
    angular_velocities = angular_velocities[:, order]

    fig, ax = plt.subplots(figsize=(10, 6))
    for sphere in range(2):
        speed = np.linalg.norm(angular_velocities[sphere], axis=1)
        ax.plot(times, speed, label=f'Sphere {sphere + 1}')
    ax.set_ylabel('Rotational speed |omega| (rad/s)', fontsize=18)
    ax.set_xlabel('Time (s)', fontsize=18)
    ax.set_title('Rotational Speed of Spheres')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)
    print(f'Plot saved to {output_file}')


plot_rotational_speed()
