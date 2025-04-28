"""
Base class for storage providers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path

class StorageProvider(ABC):
    """Abstract base class for storage providers."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the storage service."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to the storage service."""
        pass
    
    @abstractmethod
    def list_files(self, path: str) -> List[str]:
        """List all files in the given path."""
        pass
    
    @abstractmethod
    def download_file(self, remote_path: str, local_path: Path) -> None:
        """Download a file from the storage service."""
        pass
    
    @abstractmethod
    def upload_file(self, local_path: Path, remote_path: str) -> None:
        """Upload a file to the storage service."""
        pass
    
    @abstractmethod
    def delete_file(self, path: str) -> None:
        """Delete a file from the storage service."""
        pass
    
    @abstractmethod
    def get_file_size(self, path: str) -> int:
        """Get the size of a file in bytes."""
        pass
    
    @abstractmethod
    def get_file_modified_time(self, path: str) -> float:
        """Get the last modified time of a file."""
        pass 