import textract
import hashlib
import os
import csv
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
import sys

# FIX: ERROR LOADING IN PROGRESS

CWD = os.getcwd()
TEXT_PATH = os.path.join(CWD, 'DOCS')
OUT_PATH = os.path.join(CWD, 'REFS')
REF_OUT_PATH = os.path.join(OUT_PATH, 'file_reference.csv')
PROGRESS_OUT_PATH = os.path.join(OUT_PATH, 'file_progress.txt')
ERROR_OUT_PATH = error_path = os.path.join(OUT_PATH , "file_errors.txt")

class FilePath():
    def __init__(self, full_path: str, root_path: str) -> None:
        self.full_path:str = full_path
        self.rootless_path:str = full_path.removeprefix(root_path)
        self.path_id:str = self.__hash_str(self.rootless_path)

    def __hash_str(self, text:str) -> str:
        hashed = hashlib.sha1(text.encode("utf-8"))
        hex_hashed =  hashed.hexdigest()
        return hex_hashed
    

def get_all_filepaths(root_path:str = CWD, restricted_paths:list[str] = [TEXT_PATH, OUT_PATH])->list[FilePath]:
    paths = []
    for folder, subfolders, files in os.walk(root_path):
        if folder in restricted_paths:
            pass
        else:
            for file in files:
                file_path = os.path.abspath(os.path.join(folder, file))
                paths.append(FilePath(file_path, root_path))

    return paths 

def read_progress(input_path:str = PROGRESS_OUT_PATH, error_path:str = ERROR_OUT_PATH) -> list[str]:
    progress = []
    if os.path.exists(input_path):
            with open(input_path, 'r') as f:
                progress += f.read().splitlines()
    if os.path.exists(error_path):
            with open(error_path, 'r') as f:
                progress += f.read().splitlines()
    return progress

def extract_text(pathfile:FilePath, text_root:str = TEXT_PATH, out_root:str = OUT_PATH) -> None:
    textract_exts = ['.csv', '.doc', '.docx', '.eml', '.epub', 
                        '.json', '.html', '.pdf', '.pptx', '.txt',
                        '.xlsx', '.xls', '.msg']
    
    input_path = pathfile.full_path
    write_path = os.path.join(text_root , pathfile.path_id + ".txt")
    ext = Path(input_path).suffix

    if ext in textract_exts:
        try:
            byte_text = textract.process(input_path)
            decoded_text = byte_text.decode("utf-8")
            with open(write_path, 'a') as f:
                f.writelines(decoded_text)
            write_one_file_ref(pathfile, REF_OUT_PATH, PROGRESS_OUT_PATH)

        except Exception:
            
            with open(error_path, 'a') as f:
                f.writelines(input_path + "\n")

def write_one_file_ref(filepath:FilePath, ref_out_path:str, progress_out_path:str) -> None:
    # metadata
    path_id = filepath.path_id
    full_path = filepath.full_path
    file_name = os.path.basename(filepath.full_path)
    file_ext = Path(filepath.full_path).suffix
    size_in_mb = os.stat(filepath.full_path).st_size / (1024 * 1024)

    data = [path_id, full_path, file_name, file_ext, size_in_mb]
    with open(ref_out_path, 'a', encoding='UTF8') as f:
        # write out row
        writer = csv.writer(f)
        writer.writerow(data)
    
    with open(progress_out_path, 'a', encoding='UTF8') as f:
        f.write(filepath.full_path + "\n")

    

def write_header_file_ref(out_path:str = REF_OUT_PATH) -> None:
    if os.path.exists(out_path):
        return
    header = ['path_id', 'full_path', 'file_name', 'file_ext', 'size_in_mb']
    with open(out_path, 'a', encoding='UTF8') as f:
        # write the header
        writer = csv.writer(f)
        writer.writerow(header)


