from ..core import StorageBase
from azure.storage.filedatalake import DataLakeServiceClient

class ADLSClient(StorageBase):
    def __init__(self, account_name, file_system, credential):
        self.service_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=credential)
        self.file_system = self.service_client.get_file_system_client(file_system)

    def upload_record(self, data: bytes, file_name: str):
        file_client = self.file_system.get_file_client(file_name)
        file_client.upload_data(data, overwrite=True)
