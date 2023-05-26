from utils import read_progress, write_header_file_ref,  get_all_filepaths, extract_text
from tqdm import tqdm
from multiprocessing import pool
# DONE
# SHA1
# PROGRESS INDICATOR (2 LISTS DONE AND NOT DONE)
# PROGRESS BAR
# LIST OF PROCESS FILE TYPE (Initial)

# TO DO
# MULTIPROCESSING


def main():

    progress = read_progress()
    write_header_file_ref()

    paths_list = get_all_filepaths()
    len_paths = len(paths_list)

    for i in tqdm(range(len_paths)):
        path = paths_list[i]
        if path.full_path in progress:
            print('here')
            pass
        else:
            extract_text(path)



if __name__ == '__main__':
    main()