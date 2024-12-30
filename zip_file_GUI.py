import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os

def compress_to_zip(lista_files, output_path, progress_bar):
    # Calcolare la dimensione totale dei file
    total_size = sum(os.path.getsize(f) for f in lista_files if os.path.isfile(f))
    compressed_size = 0

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for sources in lista_files:
            if os.path.isfile(sources):
                zipf.write(os.path.join(sources), os.path.basename(sources))
                compressed_size += os.path.getsize(sources)
                progress_bar['value'] = (compressed_size / total_size) * 100
                root.update_idletasks()
            elif os.path.isdir(sources):
                for root_dir, dirs, files in os.walk(sources):
                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        if '.DS_Store' not in file_path and '__MACOSX' not in file_path and not file_path.startswith('._'):
                            archive_path = f"{os.path.basename(sources)}/{os.path.relpath(file_path, sources)}"
                            zipf.write(file_path, archive_path)
                            compressed_size += os.path.getsize(file_path)
                            progress_bar['value'] = (compressed_size / total_size) * 100
                            root.update_idletasks()
            else:
                print("no file or directory")

def select_files():
    files = filedialog.askopenfilenames()
    file_list.delete(0, tk.END)  # Clear the list
    for file in files:
        file_list.insert(tk.END, file)  # Add file to the list
    return list(files)

def select_files_folders():
    selections = []
    # Permetti all'utente di selezionare più file
    files = filedialog.askopenfilenames(title="Select files")
    selections.extend(files)
    # Permetti all'utente di selezionare più cartelle
    while True:
        folder = filedialog.askdirectory(title="Select folder (Cancel to finish)")
        if folder:
            selections.append(folder)
        else:
            break
        
    file_list.delete(0, tk.END)  # Pulisce la lista
    for item in selections:
        file_list.insert(tk.END, item)  # Aggiunge l'elemento alla lista
    
    return selections

def compress_files():
    lista_files = select_files_folders()
    if not lista_files:
        messagebox.showerror("Error", "No files selected!")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".zip",
                                               filetypes=[("ZIP files", "*.zip")])
    if not output_path:
        messagebox.showerror("Error", "No output path selected!")
        return

    compress_to_zip(lista_files, output_path, progress_bar)
    messagebox.showinfo("Success", "Files compressed successfully!")

# Creare la finestra principale
root = tk.Tk()
root.title("File Compressor")

# Aggiungere un pulsante per selezionare i file e avviare la compressione
compress_button = tk.Button(root, text="Select Files and Compress", command=compress_files, font=("Helvetica", 16))
compress_button.pack(fill=tk.X, padx=5, pady=5)  # Make the button larger and fill the width

# Aggiungere una lista per mostrare i file selezionati
file_list = tk.Listbox(root)
file_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Make the listbox fill the available space

# Aggiungere una barra di progresso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(padx=5, pady=5)

# Avviare il loop principale dell'interfaccia grafica
root.mainloop()
