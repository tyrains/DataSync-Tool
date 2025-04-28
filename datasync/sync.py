"""
Main synchronization module for DataSync-Tool.
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from loguru import logger
from tqdm import tqdm
from .storage_providers import StorageProvider

class DataSync:
    """Main synchronization class."""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.source_provider = self._create_provider(self.config['source'])
        self.destination_provider = self._create_provider(self.config['destination'])
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _create_provider(self, config: Dict[str, Any]) -> StorageProvider:
        """Create storage provider based on configuration."""
        provider_type = config['type']
        if provider_type == 'local':
            from .storage_providers.local import LocalStorage
            return LocalStorage(config['path'])
        elif provider_type == 'aws_s3':
            from .storage_providers.aws import AWSStorage
            return AWSStorage(
                bucket_name=config['bucket'],
                region=config.get('region'),
                access_key=config.get('access_key'),
                secret_key=config.get('secret_key')
            )
        # Add other providers here
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
    
    def sync(self) -> None:
        """Perform synchronization between source and destination."""
        try:
            logger.info("Starting synchronization...")
            
            # Connect to providers
            self.source_provider.connect()
            self.destination_provider.connect()
            
            # Get list of files from source
            source_files = self.source_provider.list_files(self.config['source']['path'])
            logger.info(f"Found {len(source_files)} files in source")
            
            # Sync each file
            for file_path in tqdm(source_files, desc="Syncing files"):
                try:
                    # Check if file needs to be synced
                    source_mtime = self.source_provider.get_file_modified_time(file_path)
                    dest_mtime = self.destination_provider.get_file_modified_time(file_path)
                    
                    if source_mtime > dest_mtime:
                        # Download to temporary location
                        temp_path = Path('/tmp') / file_path
                        self.source_provider.download_file(file_path, temp_path)
                        
                        # Upload to destination
                        self.destination_provider.upload_file(temp_path, file_path)
                        
                        # Clean up temporary file
                        temp_path.unlink()
                        
                        logger.info(f"Synced file: {file_path}")
                    else:
                        logger.debug(f"Skipping up-to-date file: {file_path}")
                
                except Exception as e:
                    logger.error(f"Error syncing file {file_path}: {e}")
        
        finally:
            # Disconnect from providers
            self.source_provider.disconnect()
            self.destination_provider.disconnect()
            logger.info("Synchronization completed") 