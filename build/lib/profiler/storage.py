# from azure.storage.blob import BlobServiceClient

# def save_to_azure(container_name, file_path, blob_name, connection_string):
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
#     with open(file_path, "rb") as data:
#         blob_client.upload_blob(data, overwrite=True)

from azure.storage.blob import BlobServiceClient
import logging
import os

logger = logging.getLogger(__name__)

class AzureStorage:
    def __init__(self, connection_string: str):
        self.service_client = BlobServiceClient.from_connection_string(connection_string)
        
    def upload_report(self, container_name: str, file_path: str, blob_name: str = None) -> bool:
        """Upload a report file to Azure Blob Storage"""
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False

            blob_name = blob_name or os.path.basename(file_path)
            blob_client = self.service_client.get_blob_client(container=container_name, blob=blob_name)
            
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
                
            logger.info(f"Successfully uploaded {file_path} to {container_name}/{blob_name}")
            return True
            
        except Exception as e:
            logger.error(f"Azure upload failed: {str(e)}")
            return False

def save_to_azure(connection_string: str, container_name: str, file_path: str, blob_name: str = None) -> bool:
    """Legacy function for backward compatibility"""
    return AzureStorage(connection_string).upload_report(container_name, file_path, blob_name)