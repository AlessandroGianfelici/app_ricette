import json
import os
        
def write_json(obj: dict, filename : str) -> None:
    """
    Write a python dictionary into a json file.
    :param obj: the dictionary
    :type path: dict
    :param filename: the full path of the json file to be written
    :type path: str
    """
    with open(filename, 'w') as outfile:
        json.dump(obj, outfile)

def read_json(filename : str) -> dict:
    """
    Read a json file into a python dictionary.
    :param filename: the full path of the json file
    :type path: str
    """
    with open(filename, 'r') as outfile:
        return json.load(outfile)
    
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
