import pytest
import os
from pyls import list_files_in_directory, list_files_with_details, list_files_with_classification, \
    format_detailed_listing, main, parser


def test_list_files_in_directory():
    """
    Test basic file listing in the specified directory.
    """
    # Test with the current directory
    result = list_files_in_directory(".")
    assert isinstance(result, list), "The result should be a list"
    assert len(result) > 0, "The directory should contain files or directories"

    # Test with a non-existent directory
    result = list_files_in_directory("non_existent_directory")
    assert result == [], "The result should be an empty list for a non-existent directory"

    # Test with a directory that exists but is empty
    os.mkdir("empty_dir")
    result = list_files_in_directory("empty_dir")
    assert result == [], "The result should be an empty list for an empty directory"
    os.rmdir("empty_dir")


def test_list_files_with_details():
    """
    Test listing files with detailed information in the specified directory.
    """
    # Test with the current directory
    result = list_files_with_details(".")
    assert isinstance(result, list), "The result should be a list"
    assert all(isinstance(item, tuple) for item in result), "Each item should be a tuple"

    # Test the formatting function
    formatted = format_detailed_listing(result)
    assert all(isinstance(line, str) for line in formatted), "Each formatted line should be a string"

    # Check for expected format in the first tuple (if result is not empty)
    if result:
        assert len(result[0]) == 3, "Each tuple should contain three elements (last_modified, size, entry)"
        assert isinstance(result[0][0], str), "The first element should be a string (last modified date)"
        assert isinstance(result[0][1], int), "The second element should be an integer (size)"
        assert isinstance(result[0][2], str), "The third element should be a string (filename)"


def test_list_files_with_classification():
    """
    Test classified listing of files and directories in the specified directory.
    """
    # Test with the current directory
    result = list_files_with_classification(".")
    assert isinstance(result, list), "The result should be a list"

    # Test classification: Expecting '/' for directories and '*' for executables (if any)
    assert any(item.endswith("/") for item in result), "There should be at least one directory classified with '/'"

    # Create a test executable file and directory to verify classification
    os.mkdir("test_dir")
    with open("test_script.sh", "w") as f:
        f.write("#!/bin/bash\necho Hello")
    os.chmod("test_script.sh", 0o755)

    result = list_files_with_classification(".")
    assert "test_dir/" in result, "Directory should be classified with '/'"
    assert "test_script.sh*" in result, "Executable file should be classified with '*'"

    # Cleanup
    os.remove("test_script.sh")
    os.rmdir("test_dir")


def test_format_detailed_listing():
    """
    Test the formatting of detailed listings.
    """
    details = [
        ("2024-04-12 16:04:23", 2454, "file1.txt"),
        ("2023-05-25 07:37:56", 1712, "file2.txt"),
        ("2024-06-20 01:23:12", 0, "dir3"),
    ]
    formatted = format_detailed_listing(details)

    assert isinstance(formatted, list), "The result should be a list of formatted strings"
    assert len(formatted) == 3, "The formatted list should have the same number of elements as the details list"
    assert formatted[
               0] == "2024-04-12 16:04:23       2454 file1.txt", "The formatted output does not match the expected format"


def test_main_no_args(monkeypatch, capsys):
    """
    Test the main function with no arguments (default behavior).
    """
    monkeypatch.setattr('sys.argv', ['pyls.py'])
    main(parser.parse_args())
    captured = capsys.readouterr()
    assert "test_pyls.py" in captured.out, "Output should include 'test_pyls.py' or other files in the current directory"


def test_main_long_format(monkeypatch, capsys):
    """
    Test the main function with the --long-format argument.
    """
    monkeypatch.setattr('sys.argv', ['pyls.py', '-l'])
    main(parser.parse_args())
    captured = capsys.readouterr()
    assert "test_pyls.py" in captured.out, "Output should include detailed information"


def test_main_filetype(monkeypatch, capsys):
    """
    Test the main function with the --filetype argument.
    """
    monkeypatch.setattr('sys.argv', ['pyls.py', '-F'])
    main(parser.parse_args())
    captured = capsys.readouterr()
    assert "test_pyls.py" in captured.out, "Output should include classification characters"


def test_main_combined(monkeypatch, capsys):
    """
    Test the main function with both --long-format and --filetype arguments.
    """
    monkeypatch.setattr('sys.argv', ['pyls.py', '-l', '-F'])
    main(parser.parse_args())
    captured = capsys.readouterr()
    assert "test_pyls.py" in captured.out, "Output should include detailed information with classification characters"
