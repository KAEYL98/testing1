from utils import read_progress, write_header_file_ref,  get_all_filepaths, extract_text
from tqdm import tqdm
from multiprocessing import Pool
# DONE
# SHA1
# PROGRESS INDICATOR (2 LISTS DONE AND NOT DONE)
# PROGRESS BAR
# LIST OF PROCESS FILE TYPE (Initial)

# TO DO
# MULTIPROCESSING
progress = read_progress()

def run(path):
    if path.full_path in progress:
        print('Skip', flush=True)
        pass
    else:
        extract_text(path) 


def main():

    write_header_file_ref()

    paths_list = get_all_filepaths()
    len_paths = len(paths_list)

    # for i in tqdm(range(len_paths)):
    #     path = paths_list[i]
    #     if path.full_path in progress:
    #         print('here')
    #         pass
    #     else:
    #         extract_text(path)

    p = Pool()

    for _ in tqdm(p.imap_unordered(run, paths_list), total=len_paths):
        pass


if __name__ == '__main__':
    main()