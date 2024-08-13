import argparse
import os
from datetime import datetime

def list_files_in_directory(dirname):
    """
    Lists the files and directories in the specified directory.

    Args:
        dirname (str): The name of the directory to list.

    Returns:
        list: A list of filenames in the directory.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
        PermissionError: If the directory cannot be accessed.
    """
    assert isinstance(dirname, str), "dirname should be a string"
    
    try:
        return os.listdir(dirname)
    except FileNotFoundError:
        print(f"Directory '{dirname}' not found.")
        return []
    except PermissionError:
        print(f"Permission denied to access '{dirname}'.")
        return []

def main(args):
    dirname = args.dirname
    files = list_files_in_directory(dirname)
    
    for file in files:
        print(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pyls",
        description="Lists files in given or current directory",
        epilog="Poor man's ls",
    )

    parser.add_argument(
        "dirname",
        help="Name of directory to list the contents of",
        action="store",
        nargs="?",
        default=".",
    )

    args = parser.parse_args()

    main(args)
