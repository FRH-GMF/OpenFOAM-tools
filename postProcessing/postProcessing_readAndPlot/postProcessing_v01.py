import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox


class FileSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("File Selector")
        self.selected_files = []

        # Button to select a folder
        self.select_folder_button = tk.Button(
            root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        # Frame to hold the checkboxes
        self.files_frame = tk.Frame(root)
        self.files_frame.pack(pady=10)

    def select_folder(self):
        # Clear the previous checkboxes
        for widget in self.files_frame.winfo_children():
            widget.destroy()

        folder_path = filedialog.askdirectory()
        if folder_path:
            files = os.listdir(folder_path)
            self.file_vars = []
            for file in files:
                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(
                    self.files_frame, text=file, variable=var)
                checkbox.pack(anchor="w")
                self.file_vars.append((var, os.path.join(folder_path, file)))

    def get_selected_files(self):
        return [file for var, file in self.file_vars if var.get()]


class ProbePlotter:
    def read_data(self, filename):
        """Lee los datos de un archivo y los retorna."""
        time = []
        pressures = []
        annotations = []

        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()

                # Omitir líneas comentadas y líneas vacías
                if line.startswith('#'):
                    # Extraer información entre paréntesis
                    start = line.find('(')
                    end = line.find(')')
                    if start != -1 and end != -1:
                        annotations.append(line[start:end+1])
                    continue
                if not line:
                    continue

                print(annotations)

                # Dividir la línea en valores
                values = line.split()

                # Convertir valores a floats
                values = [float(val) for val in values]

                # La primera columna es tiempo, el resto son presiones
                time.append(values[0])
                pressures.append(values[1:])

        return time, pressures, annotations

    def plot_files(self, files):
        excluded_files = {}
        for file in files:
            if os.path.basename(file) not in excluded_files:
                time, pressures, annotations = self.read_data(file)
                plt.figure()
                for i in range(len(pressures[0])):
                    # Agregar la primera anotación junto al label de Probes 1
                    if i < len(annotations):
                        plt.plot(time, [p[i] for p in pressures],
                                 label=f'Probe {i} {annotations[i]}')
                    else:
                        plt.plot(time, [p[i]
                                 for p in pressures], label=f'Probe {i}')

                plt.title(f'Data from {os.path.basename(file)}')
                plt.xlabel('Time [s]')
                plt.ylabel('Pressure [Pa]')
                plt.legend(fontsize=7.5)
                # Mostrar gráficos de manera no bloqueante
                plt.show(block=False)

        plt.show()  # Mantener todas las ventanas abiertas


if __name__ == "__main__":
    root = tk.Tk()

    # Create instances of the classes
    file_selector = FileSelector(root)
    probe_plotter = ProbePlotter()

    # Button to plot selected files
    plot_button = tk.Button(root, text="Plot Selected Files",
                            command=lambda: probe_plotter.plot_files(file_selector.get_selected_files()))
    plot_button.pack(pady=10)

    root.mainloop()
