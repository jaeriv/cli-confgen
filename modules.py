import os

CURRENT_DIR = os.getcwd()
    

# Validates if file exists, returns Boolean
def file_exists(file):
    return os.path.exists(file)


def get_current_var_files():
    return [file for file in os.listdir("variables")]


