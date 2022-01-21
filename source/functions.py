import os

def file_folder_exists(path: str):
    """
    Return True if a file or folder exists.
    :param path: the full path to be checked
    :type path: str
    """
    try:
        os.stat(path)
        return True
    except:
        return False

def select_or_create(path: str):
    """
    Check if a folder exists. If it doesn't, it create the folder.
    :param path: path to be selected
    :type path: str
    """
    if not file_folder_exists(path):
        os.makedirs(path)
    return path
