from ..core import SourceBase
from ..utils.retry import retry
import pysftp
from typing import List, Dict
from datetime import datetime

class FTPIngestion(SourceBase):
    def __init__(self, host, username, password, port=22, logger=None):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.logger = logger

    @retry(retries=3, delay=2)
    def fetch_records(self, last_processed=None, path="/") -> List[Dict]:
        records = []
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.host, username=self.username, password=self.password, port=self.port, cnopts=cnopts) as conn:
            for file_attr in conn.listdir_attr(path):
                mdt = datetime.utcfromtimestamp(file_attr.st_mtime)
                if not last_processed or mdt > last_processed:
                    records.append({"filename": file_attr.filename, "modified_time": mdt})
        return records
