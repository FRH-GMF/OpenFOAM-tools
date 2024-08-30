import numpy as np
import matplotlib.pyplot as plt


def read_velocity_data(file_path):
    # Initialize lists to store data
    time = []
    all_velocities = []
    annotations = []  # To store probe annotations

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_time = None
    current_velocities = []

    for line in lines:
        line = line.strip()

        # Omit commented lines and extract annotations
        if line.startswith('#'):
            # Extract information between parentheses
            start = line.find('(')
            end = line.find(')')
            if start != -1 and end != -1:
                annotations.append(line[start:end+1])
            continue

        if not line:
            continue

        parts = line.split()
        timestamp = float(parts[0])

        # If a new timestamp is encountered, save the current set of velocities
        if timestamp != current_time:
            if current_time is not None:
                time.append(current_time)
                all_velocities.append(current_velocities)
            current_time = timestamp
            current_velocities = []

        # Extract the velocities for all probes within this line
        # Start from index 1, step by 3 to get each probe's components
        for i in range(1, len(parts), 3):
            velocity = [float(parts[i].strip('(),')),
                        float(parts[i+1].strip('(),')),
                        float(parts[i+2].strip('(),'))]
            current_velocities.append(velocity)

    # Append the last set of velocities
    if current_time is not None:
        time.append(current_time)
        all_velocities.append(current_velocities)

    return np.array(time), np.array(all_velocities, dtype=object), annotations


def plot_velocity_components(time, all_velocities, annotations):
    # Create subplots for x, y, and z components of velocity
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    # Plot each probe's velocity data
    for probe_idx in range(len(all_velocities[0])):
        velocities_x = [all_velocities[i][probe_idx][0]
                        for i in range(len(time))]
        velocities_y = [all_velocities[i][probe_idx][1]
                        for i in range(len(time))]
        velocities_z = [all_velocities[i][probe_idx][2]
                        for i in range(len(time))]

        label = f'Probe {probe_idx + 1} {annotations[probe_idx]}'
        axs[0].plot(time, velocities_x, label=label)
        axs[1].plot(time, velocities_y)
        axs[2].plot(time, velocities_z)

    axs[0].set_ylabel('Velocity X [m/s]')
    axs[0].grid(True)

    axs[1].set_ylabel('Velocity Y [m/s]')
    axs[1].grid(True)

    axs[2].set_ylabel('Velocity Z m/s]')
    axs[2].set_xlabel('Time [s]')
    axs[2].grid(True)

    # Add title and legend
    fig.suptitle('Probe velocity measurements')
    axs[0].legend(loc='upper right', bbox_to_anchor=(1.1, 1))

    plt.tight_layout()
    plt.show()


# Usage
file_path = './postProcessing_data/probes/0.95/U'  # Path to the file
time, all_velocities, annotations = read_velocity_data(file_path)

# Print the annotations (probe information)
# for i, annotation in enumerate(annotations):
#     print(f"Probe {i+1}: {annotation}")

# Plot the velocity components for all probes
plot_velocity_components(time, all_velocities, annotations)
