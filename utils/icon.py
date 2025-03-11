import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to a resource (for PyInstaller compatibility). """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp directory
    except AttributeError:
        base_path = os.path.abspath(".")  # Normal execution

    return os.path.join(base_path, relative_path)
