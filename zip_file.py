import os
import zipfile
from tqdm import tqdm

def compress_to_zip(lista_files, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for sources in lista_files:
            if os.path.isfile(sources):
                zipf.write(os.path.join(sources), os.path.basename(sources))  # Corretto da 'file_path' a 'sources'
            elif os.path.isdir(sources):
                for root, dirs, files in os.walk(sources):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if '.DS_Store' not in file_path and '__MACOSX' not in file_path:
                            archive_path = f"{os.path.basename(sources)}/{os.path.relpath(file_path, sources)}"
                            zipf.write(file_path, archive_path)
            else:
                print("no file or directory")


def compress_to_zip(lista_files, output_path):
    # Calcolare la dimensione totale dei file
    total_size = sum(os.path.getsize(f) for f in lista_files if os.path.isfile(f))
    compressed_size = 0

    # Creare una barra di progresso con tqdm
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Compressing') as pbar:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for sources in lista_files:
                if os.path.isfile(sources):
                    zipf.write(os.path.join(sources), os.path.basename(sources))
                    compressed_size += os.path.getsize(sources)
                    pbar.update(os.path.getsize(sources))
                elif os.path.isdir(sources):
                    for root, dirs, files in os.walk(sources):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if '.DS_Store' not in file_path and '__MACOSX' not in file_path and not file_path.startswith('._'):
                                archive_path = f"{os.path.basename(sources)}/{os.path.relpath(file_path, sources)}"
                                zipf.write(file_path, archive_path)
                                compressed_size += os.path.getsize(file_path)
                                pbar.update(os.path.getsize(file_path))
                else:
                    print("no file or directory")


if __name__ == "__main__":
    
    file_list_to_compress = ['/Volumes/SSD_EDO/Datasets/Coronary_dataset_original/Coronary_part_1', '/Volumes/SSD_EDO/Datasets/Coronary_dataset_original/Coronary_part_2', '/Volumes/SSD_EDO/Datasets/Coronary_dataset_original/Coronary_part_3']
    #file_list_to_compress = [f'/Volumes/SSD_EDO/Datasets/coro_cleaned_CFN_PAZ/{x}' for x in os.listdir('/Volumes/SSD_EDO/Datasets/coro_cleaned_CFN_PAZ/')]
    #print(file_list_to_compress)
    formato_compressione = ".zip"
    output_filename = '/Volumes/SSD_EDO/Datasets/Coronary_dataset_original'

    # Comprimi i file e le cartelle
    compress_to_zip(file_list_to_compress, f"{output_filename}{formato_compressione}")

    # Stampa un messaggio di successo
    print(f"I file e le cartelle sono stati compressi con successo in {output_filename}")
