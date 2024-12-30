import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import zipfile

# Funzione per elencare i contenuti di un file zip con le dimensioni
def list_zip_contents(zip_file_path, listbox):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zipf:
            # Ottiene la lista dei contenuti del file zip
            zip_contents = zipf.infolist()
            # Pulisce la listbox
            listbox.delete(0, tk.END)
            # Aggiunge i contenuti alla listbox con le dimensioni
            for item in zip_contents:
                # Converte la dimensione da byte a MB
                file_size_mb = item.file_size / (1024 * 1024)
                # Formatta il nome del file con la sua dimensione in MB, arrotondando a 2 decimali
                listbox.insert(tk.END, f"{item.filename} - {file_size_mb:.2f} MB")
    except zipfile.BadZipFile:
        messagebox.showerror("Error", "The selected file is not a valid ZIP file.")

# Funzione per selezionare un file zip e visualizzarne i contenuti
def select_and_list_contents():
    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    if zip_file_path:
        list_zip_contents(zip_file_path, listbox)

# Creare la finestra principale
root = tk.Tk()
root.title("ZIP Contents Viewer")

# Aggiungere una lista per mostrare i contenuti del file zip
listbox = Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Aggiungere un pulsante per selezionare un file zip e visualizzarne i contenuti
select_button = tk.Button(root, text="Select ZIP File", command=select_and_list_contents)
select_button.pack(fill=tk.X, padx=5, pady=5)

# Avviare il loop principale dell'interfaccia grafica
root.mainloop()