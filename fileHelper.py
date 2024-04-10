import os
import shutil


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def copy_file(src_path, dst_path):
    newPath = dst_path + "/" + os.path.basename(src_path)
    if not os.path.exists(newPath):
        shutil.copy2(src_path, newPath)
    return newPath
