from PIL import Image, ImageTk
from rembg import remove
import os
import tkinter as tk
from tkinter import filedialog, messagebox


class RimuoviSfondoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rimuovi Sfondo")

        self.immagine = None
        self.immagine_senza_sfondo = None

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.button_scegli = tk.Button(self.frame, text="Scegli Immagine", command=self.scegli_immagine)
        self.button_scegli.pack(fill=tk.X, pady=5)

        self.button_rimuovi = tk.Button(self.frame, text="Remove BG", command=self.rimuovi_sfondo_e_mostra)
        self.button_rimuovi.pack(fill=tk.X, pady=5)

        self.button_salva = tk.Button(self.frame, text="Save", command=self.salva_immagine)
        self.button_salva.pack(fill=tk.X, pady=5)

        self.label_img = tk.Label(root)
        self.label_img.pack(padx=10, pady=10)

    def rimuovi_sfondo(self, immagine: Image) -> Image:
        """
        Rimuove lo sfondo da un'immagine utilizzando la libreria rembg.
        """
        immagine_senza_sfondo = remove(immagine)
    
        return immagine_senza_sfondo
    
    def carica_immagine(self, immagine_path: str) -> Image:
        """
        Carica un'immagine da un percorso specifico e verifica che sia in un formato supportato (PNG o JPG).

        :param immagine_path: Percorso dell'immagine di input.
        :return: Oggetto Image se il formato è supportato, altrimenti None.
        """
        estensioni_supportate = ('.png', '.jpg', '.jpeg')
        
        # Verifica che il file esista
        if not os.path.exists(immagine_path):
            messagebox.showinfo(f"Errore: il file {immagine_path} non esiste.")
            return None
        
        # Verifica che il file sia in un formato supportato
        if not immagine_path.lower().endswith(estensioni_supportate):
            messagebox.showinfo(f"Errore: il file {immagine_path} non è in un formato supportato (PNG o JPG).")
            return None
        
        # Carica l'immagine
        immagine = Image.open(immagine_path)
        
        return immagine
    
    def scegli_immagine(self):
        immagine_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
        if immagine_path:
            self.immagine = self.carica_immagine(immagine_path)
            if self.immagine:
                self.mostra_immagine(self.immagine, originale=True)

    def ridimensiona_immagine(self, immagine, max_width=800, max_height=600):
        """
        Ridimensiona l'immagine mantenendo le proporzioni per adattarsi alle dimensioni massime specificate.
        """
        width, height = immagine.size
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_size = (int(width * ratio), int(height * ratio))
            immagine = immagine.resize(new_size)
        return immagine

    def mostra_immagine(self, immagine, originale=False):
        immagine_ridimensionata = self.ridimensiona_immagine(immagine)
        img_tk = ImageTk.PhotoImage(immagine_ridimensionata)
        self.label_img.config(image=img_tk)
        self.label_img.image = img_tk
        if originale:
            self.immagine_senza_sfondo = None

    def rimuovi_sfondo_e_mostra(self):
        if self.immagine and self.immagine_senza_sfondo is None:
            self.immagine_senza_sfondo = self.rimuovi_sfondo(self.immagine)
            self.mostra_immagine(self.immagine_senza_sfondo)

    def salva_immagine(self):
        if self.immagine_senza_sfondo:
            output_path = os.path.splitext(self.immagine.filename)[0] + "_WBG.png"
            self.immagine_senza_sfondo.save(output_path)
            messagebox.showinfo("Successo", f"Immagine senza sfondo salvata come {output_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RimuoviSfondoApp(root)
    root.mainloop()