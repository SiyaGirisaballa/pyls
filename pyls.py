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


def list_files_with_details(dirname):
    """
    Lists files and directories in the specified directory with detailed information.

    Args:
        dirname (str): The name of the directory to list.

    Returns:
        list: A list of tuples containing detailed information about files and directories.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
        PermissionError: If the directory cannot be accessed.
    """
    assert isinstance(dirname, str), "dirname should be a string"

    try:
        entries = os.listdir(dirname)
        details = []
        for entry in entries:
            full_path = os.path.join(dirname, entry)
            stat = os.stat(full_path)
            last_modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            size = stat.st_size if not os.path.isdir(full_path) else 0
            details.append((last_modified, size, entry))
        return details
    except FileNotFoundError:
        print(f"Directory '{dirname}' not found.")
        return []
    except PermissionError:
        print(f"Permission denied to access '{dirname}'.")
        return []


def format_detailed_listing(details):
    """
    Formats the detailed listing of files and directories.

    Args:
        details (list): A list of tuples with detailed information about files and directories.

    Returns:
        list: A list of formatted strings representing the detailed file listings.
    """
    lines = []
    for last_modified, size, entry in details:
        line = f"{last_modified} {size:10} {entry}"
        lines.append(line)
    return lines


def main(args):
    dirname = args.dirname

    if args.long_format:
        details = list_files_with_details(dirname)
        formatted_details = format_detailed_listing(details)
        for line in formatted_details:
            print(line)
    else:
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

    parser.add_argument(
        "-l",
        "--long-format",
        help="Presents more details about files in columnar format",
        action="store_true",
    )

    args = parser.parse_args()

    main(args)

