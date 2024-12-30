import fitz  # PyMuPDF

# Funzione per verificare se una stringa inizia con un numero (es. "1", "2", "2.1")
import fitz  # PyMuPDF
import re

# Funzione per determinare se il testo rappresenta un capitolo, sezione o sottosezione
def identify_section(text):
    # Cerca pattern di tipo "CAPITOLO I", "1", "2.1", "2.1.1", ecc.
    if re.match(r"CAPITOLO\s+\w+\s+-", text):  # Es. "CAPITOLO I - RELAZIONE GEOTECNICA"
        return 'chapter'
    elif re.match(r"^\d+\s*-\s*", text):  # Es. "1 - INTRODUZIONE"
        return 'section'
    elif re.match(r"^\d+(\.\d+)+\s", text):  # Es. "2.1 Relazione Geotecnica"
        return 'subsection'
    else:
        return None

# Funzione per creare un indice con i numeri di pagina reali
def create_index_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    index = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text").splitlines()

        for line in text:
            line = line.strip()
            section_type = identify_section(line)
            if section_type:
                index.append((line, page_num + 1, section_type))  # Numero di pagina inizia da 1

    return index

# Funzione per stampare l'indice con puntini e numeri di pagina
def print_index(index):
    for title, page, section_type in index:
        # Modifica il formato a seconda del tipo di sezione
        if section_type == 'chapter':
            title = f"{title} (Capitolo)"
        elif section_type == 'section':
            title = f"    {title} (Sezione)"
        elif section_type == 'subsection':
            title = f"        {title} (Sottosezione)"
        
        dots = '.' * (80 - len(title) - len(str(page)))  # Calcola quanti puntini usare
        print(f'{title}{dots}{page}')

# Percorso del file PDF
pdf_file = '/Users/edoardoderose/Desktop/RELAZIONE GEOTECNICA.pdf'

# Creiamo l'indice
indice = create_index_from_pdf(pdf_file)

# Stampiamo l'indice
print_index(indice)