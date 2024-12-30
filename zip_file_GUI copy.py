import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os

class FileCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Compressor")

        # Initialize GUI components
        self.create_widgets()

    def create_widgets(self):
        # Select Files Button
        self.select_files_button = tk.Button(self.root, text="Select Files", command=self.select_files, font=("Helvetica", 16))
        self.select_files_button.pack(fill=tk.X, padx=5, pady=5)

        # Select Folders Button
        self.select_folders_button = tk.Button(self.root, text="Select Folders", command=self.select_folders, font=("Helvetica", 16))
        self.select_folders_button.pack(fill=tk.X, padx=5, pady=5)

         # Select output folder Button
        self.select_output_folders_button = tk.Button(self.root, text="Select output Folder", command=self.select_output_folder, font=("Helvetica", 16))
        self.select_output_folders_button.pack(fill=tk.X, padx=5, pady=5)

        # Output Path Entry
        self.output_path_label = tk.Label(self.root, text="Output name:", font=("Helvetica", 16))
        self.output_path_label.pack(fill=tk.X, padx=5, pady=5)
        self.output_path_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.output_path_entry.pack(fill=tk.X, padx=5, pady=5)

        # Compress Button
        self.compress_button = tk.Button(self.root, text="Compress", command=self.compress_files, font=("Helvetica", 16))
        self.compress_button.pack(fill=tk.X, padx=5, pady=5)

        # Reset Button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_gui, font=("Helvetica", 16))
        self.reset_button.pack(fill=tk.X, padx=5, pady=5)

        # File Listbox
        self.file_list = tk.Listbox(self.root)
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(padx=5, pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames()
        for file in files:
            self.file_list.insert(tk.END, file)

    def select_folders(self):
        folder = filedialog.askdirectory()
        self.file_list.insert(tk.END, folder)
        
    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, folder)

    def compress_files(self):
        lista_files = self.file_list.get(0, tk.END)
        if not lista_files:
            messagebox.showerror("Error", "No files or folders selected!")
            return
        output_folder = self.output_folder
        output_name = self.output_path_entry.get()
        output_path = os.path.join(output_folder, output_name)
        if not output_path:
            messagebox.showerror("Error", "No output path selected!")
            return

        self.compress_to_zip(lista_files, output_path, self.progress_bar)
        messagebox.showinfo("Success", "Files compressed successfully!")
        
    def get_dir_size(self, path='.'):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.get_dir_size(entry.path)
        return total

    def compress_to_zip(self, lista_files, output_path, progress_bar):
        total_size = sum(os.path.getsize(f) if os.path.isfile(f) else self.get_dir_size(f) for f in lista_files)
        compressed_size = 0

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for sources in lista_files:
                if os.path.isfile(sources):
                    zipf.write(os.path.join(sources), os.path.basename(sources))
                    compressed_size += os.path.getsize(sources)
                    progress_bar['value'] = (compressed_size / total_size) * 100
                    self.root.update_idletasks()
                elif os.path.isdir(sources):
                    for root_dir, dirs, files in os.walk(sources):
                        for file in files:
                            file_path = os.path.join(root_dir, file)
                            if '.DS_Store' not in file_path and '__MACOSX' not in file_path and not file_path.startswith('._'):
                                archive_path = f"{os.path.basename(sources)}/{os.path.relpath(file_path, sources)}"
                                zipf.write(file_path, archive_path)
                                compressed_size += os.path.getsize(file_path)
                                progress_bar['value'] = (compressed_size / total_size) * 100
                                self.root.update_idletasks()

    def reset_gui(self):
        self.file_list.delete(0, tk.END)
        self.output_folder = None
        self.output_path_entry.delete(0, tk.END)
        self.progress_bar['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCompressorApp(root)
    root.mainloop()
