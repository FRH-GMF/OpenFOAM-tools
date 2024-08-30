import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Define types of fields read from OF
fields = {"p": {"xlabel": "Time [s]", "ylabel": "Pressure [Pa]", "vector": False},
          "p_rgh": {"xlabel": "Time [s]", "ylabel": "Pressure [Pa]", "vector": False},
          "p_rgh_0": {"xlabel": "Time [s]", "ylabel": "Pressure [Pa]", "vector": False},
          "phi": {"xlabel": "Time [s]", "ylabel": "Phi [$m^3$/s]", "vector": False},
          "phi_0": {"xlabel": "Time [s]", "ylabel": "Phi [$m^3$/s]", "vector": False},
          "T": {"xlabel": "Time [s]", "ylabel": "Temperature [K]", "vector": False},
          "U": {"xlabel": "Time [s]", "ylabel": "Velocity [m/s]", "vector": True},
          "W": {"xlabel": "Time [s]", "ylabel": "Vorticity [1/s]", "vector": True}}

# Leo los archivos y lo devuelvo como vector o escalar
"""
Selecciono el path general postProcessing_data
lee todas las carpetas que hay:

Si selecciono probes:
    sale opcion de ploteo por probe comparada.
    probe:
    * hay un problema en la lectura de la probe 0 en p!
    * titulo de la imagen tiene que ser probe
    * no plotea el titulo


Si selecciono surfaceFieldValue
    sale opcion de ploteo por patch o comparada
        patch:
            me lista todos los nombres de carpetas que surfaceFieldValue
            elijo una, busca el ultimo paso temporal
            lee y plotea el contenido

        comparada:
            me lista todos los nombres de carpetas que sean iguales el nombre del patch
            busca en cada una el ultimo pso temporal
            lee el contenido y plotea el contenido comparado
"""


def list_folders_in_path(path):
    """
    FUNC: Lists all folder names in the specified path.
    INPUT: 
        - path: Directory path to search for folders.
    OUTPUT:
        - A list of folder names in the specified path.
    """
    # List all entries in the directory given by path
    all_entries = os.listdir(path)

    # Filter out entries that are directories
    folder_names = [entry for entry in all_entries if os.path.isdir(
        os.path.join(path, entry))]

    return folder_names


def postProcesses(names):
    if not names:
        return ""

    # Extract the part before the first underscore for each name
    prefixes = [name.split('_')[0] for name in names]

    # Find the common prefix
    common = list(set([x for x in prefixes if prefixes.count(x) > 1]))
    uncommon = list(set([x for x in prefixes if prefixes.count(x) == 1]))

    common = [f"{x}_" for x in common]

    # Append the two lists together
    combined = common + uncommon
    print(combined)
    return combined


def read_output(filename, vector=False):
    """ 
        FUNC:reads input file, checks if scalar or vector form, reformat data
        INPUT: path to txt file
        OUTPUT: header (probes location) and data
    """
    with open(filename) as f:
        header = []
        data_in = []
        for x in f:
            if "Probe" in x:
                header.append(x.split('#', 1)[-1].strip())

            else:
                data_in.append(x.replace('(', ' ').replace(')', ' '))
        # Me devuelve la matriz de datos
        data = np.loadtxt(data_in)

        # Lo separo distinto si es vector o escalar
        if vector:
            # Me devuelve la primera columna y un diccionario con las demas para vectores
            return data[:, 0], {header[i]: data[:, 3*i+1:3*i+4] for i in range(0, data.shape[1]//3)}
        else:
            # Me devuelve la primera columna y un diccionario con las demas para escalares
            return data[:, 0], {header[i]: data[:, i] for i in range(1, data.shape[1])}


def plot_each(data_proc, **kwargs):
    """
        FUNC: plots selected data
        INPUT: procesed data
        OUTPUT: graphs
    """
    # Grafico distinto si es vector o escalar
    if fields[field]["vector"]:
        fig, ax = plt.subplots(nrows=3, sharex=True)
        ax[0].plot(data_proc[0], data_proc[1][:, 0],
                   label=kwargs.get('label'))
        ax[1].plot(data_proc[0], data_proc[1][:, 1])
        ax[2].plot(data_proc[0], data_proc[1][:, 2])
        ax[0].legend(loc='upper right')

        fig.text(0.04, 0.5, kwargs.get('ylabel'),
                 va='center', rotation='vertical')
        ax[2].set_xlabel(kwargs.get('xlabel'))
        ax[0].set_ylabel('X')
        ax[1].set_ylabel('Y')
        ax[2].set_ylabel('Z')

    else:
        plt.plot(data_proc[0], data_proc[1], label=kwargs.get('label'))
        plt.legend(loc='upper right')
        plt.xlabel(kwargs.get('xlabel'))
        plt.ylabel(kwargs.get('ylabel'))
        plt.title("Probes")

    plt.show()

# def plot_compared(data_proc, **kwargs):
#     """
#         FUNC: plots selected data with velocity components
#         INPUT: processed data, annotations for probes
#         OUTPUT: graphs
#     """
#     if fields[field]["vector"]:
#         fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

#         for probe_idx, (probe_name, velocities) in enumerate(data_proc[1].items()):
#             label = f'{probe_name.strip()} {annotations[probe_idx]}'
#             axs[0].plot(data_proc[0], velocities[:, 0], label=label)
#             axs[1].plot(data_proc[0], velocities[:, 1])
#             axs[2].plot(data_proc[0], velocities[:, 2])

#         axs[0].set_ylabel('Velocity X [m/s]')
#         axs[0].grid(True)

#         axs[1].set_ylabel('Velocity Y [m/s]')
#         axs[1].grid(True)

#         axs[2].set_ylabel('Velocity Z [m/s]')
#         axs[2].set_xlabel('Time [s]')
#         axs[2].grid(True)

#         fig.suptitle('Probe velocity measurements')
#         axs[0].legend(loc='upper right', bbox_to_anchor=(1.1, 1))

#         plt.tight_layout()
#         plt.show()
#     else:
#         plt.plot(data_proc[0], data_proc[1])
#         plt.xlabel(kwargs.get('xlabel'))
#         plt.ylabel(kwargs.get('ylabel'))
#         plt.title(kwargs.get('title'))
#         plt.grid(True)
#         plt.show()


# filename = "./postProcessing_data/probes/0.95/U"
# filename = "./postProcessing_data/probes/0.95/U"

# field = filename.split("/")[-1]

# t, var = read_output(filename, fields[field]["vector"])
# print(header)
# print(t)
# print(var)
# Grafico todas las fields
# for key, val in var.items():
#     plot_each([t, val], **{**fields[field], "label": key,
#               'title': f"{field}-{key}", 'fileout': f"{field}-{key}.png"})
# for key, val in var.items():
#     plot_each([t, val], **{**fields[field], "label": key,
#               'fileout': f"{field}-{key}.png"})

# plot_compared([t, var.items()], **{**fields[field]})

path_general = './postProcessing_data'  # Replace with your directory path
folders = list_folders_in_path(path_general)
postProcesses(folders)

# for path in len(path_general):
#     path_specific = path_general+folders[path]

print(path_specific)


# ############################################
