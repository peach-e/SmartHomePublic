# ----------------------------------------------------------------- #
#  File   : path.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# For path-related operations.
import tsl.util.exception
import os
import shutil

HOME_DIRECTORY = os.path.expanduser('~')


def assert_dir_exists(path):
    if not exists_dir(path):
        raise cema.util.exception.PathError(path)


def assert_file_exists(path):
    if not exists_file(path):
        raise cema.util.exception.FileError(path)


def cd(target_path):
    # Change into the target path, which may be relative or absolute.
    os.chdir(target_path)


def copy(source, dest):
    # Copy the file or folder located at source to dest.
    # Source must exist.
    # Destination generally should not exist unless it's a file and
    # you want to overwrite it, but the path leading up to dest
    # should exist. More details available in the shutil docs.
    if exists_file(source):
        shutil.copy2(source, dest)
    elif exists_dir(source):
        shutil.copytree(source, dest)
    else:
        raise cema.util.exception.PathError(path)


def dir(directory=None):
    # List contents of directory
    if directory is None:
        directory = get_cwd()
    return os.listdir(directory)


def exists_dir(path):
    # A valid directory path should exist and not be a file.
    is_path = os.path.exists(path)
    is_file = os.path.isfile(path)
    is_dir = (is_path and not is_file)
    return is_dir


def exists_file(path):
    return os.path.isfile(path)


def find_files(path, criterion_cb):
    # Find all files in path where
    # criterion_cb(file_name) returns True.
    result = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if criterion_cb(file_name):
                result.append(os.path.join(root, file_name))
    return result


def get_cwd():
    return os.getcwd()


def get_parent_directory(filepath):
    return os.path.dirname(os.path.abspath(filepath))


def get_filename_from_path(filepath):
    return os.path.basename(filepath)


def join_paths(*paths):
    return os.path.join(*paths)


def make_directory(dirpath):
    # Behaves like mkdir -p. If already exists, just ignore.
    if exists_dir(dirpath):
        return
    os.makedirs(dirpath)


def delete(path):
    # Deletes a file or a directory by the specified name.
    if exists_file(path):
        os.remove(path)
    elif exists_dir(path):
        shutil.rmtree(path)
    else:
        raise cema.util.exception.PathError(path)
