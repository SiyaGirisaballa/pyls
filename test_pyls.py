import pytest
from pyls_sketch import list_files_in_directory

def test_list_files_in_directory():
    # Test with an existing directory
    result = list_files_in_directory(".")
    assert isinstance(result, list), "The result should be a list"
    
    # Test with a non-existent directory
    result = list_files_in_directory("non_existent_directory")
    assert result == [], "The result should be an empty list for a non-existent directory"
    
    # Test with a directory without permission
    # This test might need to be skipped or handled carefully to avoid permission issues
