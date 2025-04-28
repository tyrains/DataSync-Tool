"""
AWS S3 storage provider implementation.
"""

import boto3
from pathlib import Path
from typing import List
from botocore.exceptions import ClientError
from .base import StorageProvider

class AWSStorage(StorageProvider):
    """AWS S3 storage provider."""
    
    def __init__(self, bucket_name: str, region: str = None, access_key: str = None, secret_key: str = None):
        self.bucket_name = bucket_name
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3_client = None
        self.s3_resource = None
    
    def connect(self) -> None:
        """Establish connection to AWS S3."""
        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )
        self.s3_client = session.client('s3')
        self.s3_resource = session.resource('s3')
    
    def disconnect(self) -> None:
        """Close connection to AWS S3."""
        self.s3_client = None
        self.s3_resource = None
    
    def list_files(self, path: str) -> List[str]:
        """List all files in the given path."""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=path
            )
            return [obj['Key'] for obj in response.get('Contents', [])]
        except ClientError as e:
            print(f"Error listing files: {e}")
            return []
    
    def download_file(self, remote_path: str, local_path: Path) -> None:
        """Download a file from S3."""
        try:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            self.s3_client.download_file(
                self.bucket_name,
                remote_path,
                str(local_path)
            )
        except ClientError as e:
            print(f"Error downloading file: {e}")
    
    def upload_file(self, local_path: Path, remote_path: str) -> None:
        """Upload a file to S3."""
        try:
            self.s3_client.upload_file(
                str(local_path),
                self.bucket_name,
                remote_path
            )
        except ClientError as e:
            print(f"Error uploading file: {e}")
    
    def delete_file(self, path: str) -> None:
        """Delete a file from S3."""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=path
            )
        except ClientError as e:
            print(f"Error deleting file: {e}")
    
    def get_file_size(self, path: str) -> int:
        """Get the size of a file in bytes."""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=path
            )
            return response['ContentLength']
        except ClientError:
            return 0
    
    def get_file_modified_time(self, path: str) -> float:
        """Get the last modified time of a file."""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=path
            )
            return response['LastModified'].timestamp()
        except ClientError:
            return 0 