import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import shutil
import platform

class MinecraftMapInstaller(tk.Tk):
    """
    A simple Tkinter application to install Minecraft maps from zip files.
    Now with automatic scanning for Minecraft installations.
    """
    def __init__(self):
        super().__init__()
        self.title("Minecraft Map Installer")
        self.geometry("550x400")
        self.configure(bg="#f0f0f0")

        # --- UI Elements ---
        self.main_label = tk.Label(self, text="Drag and drop your Minecraft map .zip file here", 
                               bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
        self.main_label.pack(pady=20, padx=20)

        self.path_entry = tk.Entry(self, width=70, font=("Helvetica", 10))
        self.path_entry.pack(pady=5, padx=20)
        
        # Make the entry widget a drop target
        self.path_entry.drop_target_register('DND_FILES')
        self.path_entry.dnd_bind('<<Drop>>', self.drop_inside_entry)

        self.install_button = tk.Button(self, text="Add the Map", command=self.install_map,
                                        bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                                        relief="flat", padx=10, pady=5)
        self.install_button.pack(pady=20)
        
        # --- Minecraft Path Section ---
        self.path_frame = tk.LabelFrame(self, text="Minecraft Installation Path", bg="#f0f0f0", padx=10, pady=10)
        self.path_frame.pack(pady=10, padx=20, fill="x")

        self.saves_path_label = tk.Label(self.path_frame, text="Scanning for saves folder...", 
                                         bg="#f0f0f0", fg="#555", wraplength=480)
        self.saves_path_label.pack(side="left", fill="x", expand=True)

        self.browse_button = tk.Button(self.path_frame, text="Browse...", command=self.browse_for_saves_folder,
                                       bg="#2196F3", fg="white", relief="flat")
        self.browse_button.pack(side="right")
        self.switch_language(self.current_language) 
        
        self.file_path = None
        self.saves_path = None
        self.after(100, self.find_and_set_saves_path) # Defer scanning to allow UI to draw
        
    def drop_inside_entry(self, event):
        """ Handles the drag and drop event. """
        filepath = event.data.strip()
        if filepath.startswith('{') and filepath.endswith('}'):
             filepath = filepath[1:-1] # Remove braces on some systems

        if filepath.endswith('.zip'):
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filepath)
            self.file_path = filepath
        else:
            messagebox.showerror("Error", "Please drop a .zip file.")

    def find_and_set_saves_path(self):
        """ Scans for the saves path and updates the UI. """
        path = self.get_minecraft_saves_path()
        if path and os.path.isdir(path):
            self.saves_path = path
            self.saves_path_label.config(text=f"Found: {self.saves_path}")
        else:
            self.saves_path_label.config(text="Could not find Minecraft saves folder automatically. Please use 'Browse' to select it.")

    def browse_for_saves_folder(self):
        """ Opens a dialog to manually select the saves folder. """
        path = filedialog.askdirectory(title="Select Minecraft 'saves' folder")
        if path:
            if os.path.basename(path) != 'saves':
                 messagebox.showwarning("Warning", "The selected folder is not named 'saves'. Please ensure it is the correct directory.")
            self.saves_path = path
            self.saves_path_label.config(text=f"Selected: {self.saves_path}")

    def get_minecraft_saves_path(self):
        """
        Determines the path to the Minecraft saves folder by scanning common locations.
        """
        system = platform.system()
        # Default paths
        if system == "Windows":
            default_path = os.path.join(os.environ.get('APPDATA', ''), '.minecraft', 'saves')
        elif system == "Darwin": # macOS
            default_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'minecraft', 'saves')
        elif system == "Linux":
            default_path = os.path.join(os.path.expanduser('~'), '.minecraft', 'saves')
        else:
            return None
        
        # Check if default path exists first
        if os.path.isdir(default_path):
            return default_path

        # If not, perform a broader scan (example for Windows)
        if system == "Windows":
            for drive in ['C:', 'D:', 'E:', 'F:']:
                if os.path.exists(drive):
                    for root, dirs, files in os.walk(os.path.join(drive, os.sep, 'Users')):
                        if '.minecraft' in dirs:
                            mc_path = os.path.join(root, '.minecraft', 'saves')
                            if os.path.isdir(mc_path):
                                return mc_path
        return None # Return None if nothing is found

    def install_map(self):
        """ The main logic for unzipping and installing the map. """
        self.file_path = self.path_entry.get()
        if not self.file_path:
            messagebox.showerror("Error", "Please select a .zip file first.")
            return

        if not self.saves_path or not os.path.isdir(self.saves_path):
            messagebox.showerror("Error", "Minecraft saves directory is not set. Please select it using the 'Browse' button.")
            return

        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                # Find the actual map folder inside the zip.
                top_level_items = list(set([item.split('/')[0] for item in zip_ref.namelist() if '/' in item]))
                if not top_level_items: # If no directories, it's likely a flat zip
                    top_level_items = [""] 
                
                map_folder_name = None
                potential_map_folder = ""
                for item in top_level_items:
                    try:
                        path_to_check = f"{item}/level.dat" if item else "level.dat"
                        zip_ref.getinfo(path_to_check)
                        potential_map_folder = item
                        break
                    except KeyError:
                        continue
                
                if potential_map_folder == "": # Map files are at the root of the zip
                    map_folder_name = os.path.splitext(os.path.basename(self.file_path))[0]
                    extract_path = os.path.join(self.saves_path, map_folder_name)
                    if os.path.isdir(extract_path):
                        if not messagebox.askyesno("Warning", f"A map named '{map_folder_name}' already exists. Overwrite?"): return
                        shutil.rmtree(extract_path)
                    os.makedirs(extract_path, exist_ok=True)
                    zip_ref.extractall(extract_path)
                
                else: # Map is in a subfolder
                    map_folder_name = potential_map_folder
                    extract_path = os.path.join(self.saves_path, map_folder_name)
                    if os.path.isdir(extract_path):
                        if not messagebox.askyesno("Warning", f"A map named '{map_folder_name}' already exists. Overwrite?"): return
                        shutil.rmtree(extract_path)

                    temp_extract_dir = os.path.join(self.saves_path, "temp_map_install_123")
                    if os.path.exists(temp_extract_dir): shutil.rmtree(temp_extract_dir)
                    os.makedirs(temp_extract_dir)
                    zip_ref.extractall(temp_extract_dir)

                    source_map_folder = os.path.join(temp_extract_dir, map_folder_name)
                    shutil.move(source_map_folder, self.saves_path)
                    shutil.rmtree(temp_extract_dir)

                messagebox.showinfo("Success", f"Map '{map_folder_name}' installed successfully!")

        except zipfile.BadZipFile:
            messagebox.showerror("Error", "The selected file is not a valid .zip file.")
        except Exception as e:
            messagebox.showerror("An Error Occurred", str(e))

if __name__ == "__main__":
    app = MinecraftMapInstaller()
    app.mainloop()
