"""
Local storage provider implementation.
"""

import os
from pathlib import Path
from typing import List
from .base import StorageProvider

class LocalStorage(StorageProvider):
    """Local filesystem storage provider."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def connect(self) -> None:
        """No connection needed for local storage."""
        pass
    
    def disconnect(self) -> None:
        """No disconnection needed for local storage."""
        pass
    
    def list_files(self, path: str) -> List[str]:
        """List all files in the given path."""
        full_path = self.base_path / path
        if not full_path.exists():
            return []
        return [str(f.relative_to(self.base_path)) for f in full_path.rglob('*') if f.is_file()]
    
    def download_file(self, remote_path: str, local_path: Path) -> None:
        """Copy file from source to destination."""
        source_path = self.base_path / remote_path
        local_path.parent.mkdir(parents=True, exist_ok=True)
        with open(source_path, 'rb') as src, open(local_path, 'wb') as dst:
            dst.write(src.read())
    
    def upload_file(self, local_path: Path, remote_path: str) -> None:
        """Copy file from source to destination."""
        dest_path = self.base_path / remote_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(local_path, 'rb') as src, open(dest_path, 'wb') as dst:
            dst.write(src.read())
    
    def delete_file(self, path: str) -> None:
        """Delete a file."""
        file_path = self.base_path / path
        if file_path.exists():
            file_path.unlink()
    
    def get_file_size(self, path: str) -> int:
        """Get the size of a file in bytes."""
        file_path = self.base_path / path
        return file_path.stat().st_size if file_path.exists() else 0
    
    def get_file_modified_time(self, path: str) -> float:
        """Get the last modified time of a file."""
        file_path = self.base_path / path
        return file_path.stat().st_mtime if file_path.exists() else 0 