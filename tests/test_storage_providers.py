import pytest
from pathlib import Path
from datasync.storage_providers import LocalStorage

def test_local_storage():
    # Create a temporary directory for testing
    test_dir = Path("test_storage")
    test_dir.mkdir(exist_ok=True)
    
    try:
        # Initialize storage
        storage = LocalStorage(str(test_dir))
        
        # Test file operations
        test_file = test_dir / "test.txt"
        test_file.write_text("test content")
        
        # Test list_files
        files = storage.list_files("")
        assert "test.txt" in files
        
        # Test get_file_size
        size = storage.get_file_size("test.txt")
        assert size > 0
        
        # Test get_file_modified_time
        mtime = storage.get_file_modified_time("test.txt")
        assert mtime > 0
        
    finally:
        # Clean up
        test_file.unlink()
        test_dir.rmdir() 