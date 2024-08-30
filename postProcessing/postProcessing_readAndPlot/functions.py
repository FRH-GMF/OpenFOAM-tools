import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

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
            if ("Probe" in x) or ("Region" in x):
                header.append(x.split('#', 1)[-1].strip().replace("Region type : patch ", ""))
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
            return data[:, 0], {header[i-1]: data[:, i] for i in range(1, data.shape[1])}
        

def plot_each(t, V, single, variable, fileout, **kwargs):
    """
        FUNC: plots selected data
        INPUT: procesed data
        OUTPUT: graphs
    """
    if "probe" in fileout: 
        kind = "Probes"
    else:
        kind = "Surface"

    # Grafico distinto si es vector o escalar
    if kwargs.get('vector') == True:
        fig, ax = plt.subplots(nrows=3, sharex=True)
        for key, value in V.items(): 
            ax[0].plot(t, value[:, 0], label=key)
            ax[1].plot(t, value[:, 1])
            ax[2].plot(t, value[:, 2])
        ax[0].legend(loc='upper right')

        fig.supylabel(kwargs.get('ylabel'))
        ax[2].set_xlabel(kwargs.get('xlabel'))
        ax[0].set_ylabel('X')
        ax[1].set_ylabel('Y')
        ax[2].set_ylabel('Z')
        fig.suptitle(f"{kind} - {variable}")
    else:
        for key, value in V.items(): plt.plot(t, value, label=key)
        plt.legend(loc='upper right')
        plt.xlabel(kwargs.get('xlabel'))
        plt.ylabel(kwargs.get('ylabel'))
        plt.title(f"{kind} - {variable}")
    
    plt.tight_layout()
    plt.savefig(fileout, dpi=300)
    plt.savefig(fileout.replace("png", "pdf"), bbox_inches='tight')
    plt.close()