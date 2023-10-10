import os
import shutil
from concurrent.futures import ThreadPoolExecutor


def remove_all_files(folder_path):
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(os.remove, file_path)

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                executor.submit(shutil.rmtree, dir_path)


def main():
    folder_path = r'C:\path\to\folder'
    remove_all_files(folder_path)


if __name__ == '__main__':
    main()
