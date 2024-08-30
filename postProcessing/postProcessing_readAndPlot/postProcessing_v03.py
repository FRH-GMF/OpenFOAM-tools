import os
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm
from functions import *

# Define types of fields read from OF
fields = {"p": {"xlabel": "Time [s]", "ylabel": "Pressure [Pa]", "vector": False},
          "p_rgh": {"xlabel": "Time [s]", "ylabel": "Pressure [Pa]", "vector": False},
          "p_rgh_0": {"xlabel": "Time [s]", "ylabel": "Pressure [Pa]", "vector": False},
          "phi": {"xlabel": "Time [s]", "ylabel": "Phi [$m^3$/s]", "vector": False},
          "phi_0": {"xlabel": "Time [s]", "ylabel": "Phi [$m^3$/s]", "vector": False},
          "T": {"xlabel": "Time [s]", "ylabel": "Temperature [K]", "vector": False},
          "U": {"xlabel": "Time [s]", "ylabel": "Velocity [m/s]", "vector": True},
          "W": {"xlabel": "Time [s]", "ylabel": "Vorticity [1/s]", "vector": True}}


if __name__ == "__main__":

    path = "postProcessing_data/surfaceFieldValue_*_phi/*/*"
    # path = "postProcessing_data/probes/*/*"

    path = "../../../utn/23_hydraulicDamper_HD/02_hd_CASES/hd_h_uv/hd_h_uv_results/hd_h_uv_v08_results/postProcessing"

    print(path)
    last_time = str(0.95)
    if "probes" in path:
        # Grafico los probes
        for filepath in tqdm(glob(path), desc="Probes: "):
            if filepath.split('/')[-2] != last_time:
                continue
            # Archivo de salida
            fileout = f"figs/fig_{'_'.join(filepath.split('/')[1:])}.png"
            # Variable procesada
            variable = filepath.split('/')[-1]
            # Leo los datos
            t, V = read_output(filename=filepath,
                               vector=fields[variable]["vector"])
            # Los grafico
            plot_each(t, V, single=False, variable=variable,
                      fileout=fileout, **fields[variable])
    else:
        # Grafico los surface comparando
        V = {}
        for filepath in tqdm(glob(path), desc="Surface: "):
            if filepath.split('/')[-2] != last_time:
                continue
            # Variable procesada
            variable = filepath.split('/')[-3].split("_")[-1]
            patch = filepath.split('/')[-3].split("_")[-2]
            # Leo los datos
            t, _V = read_output(filename=filepath,
                                vector=fields[variable]["vector"])
            V[patch] = _V[patch]

        # Archivo de salida
        fileout = '_'.join(filepath.split('/')[2:])
        fileout = f"figs/fig_{filepath.split('/')[0]}_{fileout}.png".replace(
            ".dat", "")
        # Los grafico
        plot_each(t, V, single=False, variable=variable,
                  fileout=fileout, **fields[variable])
