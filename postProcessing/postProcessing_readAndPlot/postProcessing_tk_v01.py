import tkinter as tk
from tkinter import filedialog
import os


class FolderSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Selector")

        self.select_button = tk.Button(
            root, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)

        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select a Folder")
        if folder_path:
            self.process_folders(folder_path)

    def process_folders(self, folder_path):
        # Clear existing widgets in the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        try:
            folder_names = [item for item in os.listdir(
                folder_path) if os.path.isdir(os.path.join(folder_path, item))]

            if not folder_names:
                tk.Label(self.result_frame, text="No folders found").pack()
                return

            # Extract the part of each folder name up to the first underscore and find the common prefix
            prefix_parts = [self.extract_prefix(name) for name in folder_names]
            common_prefix = self.find_common_prefix(prefix_parts)

            # Create a button with the common prefix if it exists
            if common_prefix:
                button = tk.Button(self.result_frame, text=common_prefix, command=lambda: print(
                    f"Selected: {common_prefix}"))
                button.pack(pady=10)
            else:
                tk.Label(self.result_frame,
                         text="No common prefix found").pack()

        except Exception as e:
            tk.Label(self.result_frame, text=f"Error: {str(e)}").pack()

    def extract_prefix(self, folder_name):
        # Extract the part of the folder name up to the first underscore

        return folder_name.split('_', 1)[0]

    def find_common_prefix(self, parts):
        if not parts:
            return ""

        # Initialize common prefix to the first part
        common_prefix = parts[0]

        for part in parts[1:]:
            # Compare the current common prefix with each part
            i = 0
            while i < len(common_prefix) and i < len(part) and common_prefix[i] == part[i]:
                i += 1
            common_prefix = common_prefix[:i]

            # If common_prefix is empty, no need to continue
            if not common_prefix:
                break

        # Ensure the prefix is meaningful
        return common_prefix if len(common_prefix) > 1 else ""


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSelectorApp(root)
    root.mainloop()
