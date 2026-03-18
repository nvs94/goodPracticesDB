from typing import Optional
from azure.storage.filedatalake import DataLakeServiceClient


class ADLSClient:
    """
    Cliente para Azure Data Lake Storage (Gen2)
    """

    def __init__(
        self,
        account_name: str,
        file_system: str,
        credential: str,
    ):
        self.account_name = account_name
        self.file_system = file_system

        self.service_client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net",
            credential=credential,
        )

        self.fs_client = self.service_client.get_file_system_client(file_system)

    def upload_bytes(self, data: bytes, path: str):
        """
        Sube contenido en memoria directamente a ADLS.
        """
        file_client = self.fs_client.get_file_client(path)

        file_client.create_file()
        file_client.append_data(data, offset=0, length=len(data))
        file_client.flush_data(len(data))

    def upload_file(self, local_path: str, remote_path: str):
        """
        Sube fichero desde disco (fallback).
        """
        with open(local_path, "rb") as f:
            self.upload_bytes(f.read(), remote_path)
