# ingestion_framework/sources/ftp_source.py

import pysftp
import tempfile
import os

class FTPIngestion:

    def __init__(self, host, username, password, path="/", logger=None):
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.logger = logger

    def fetch_dataframe(self, spark):

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        temp_dir = tempfile.mkdtemp()

        with pysftp.Connection(
            self.host,
            username=self.username,
            password=self.password,
            cnopts=cnopts
        ) as conn:

            conn.cwd(self.path)
            files = conn.listdir()

            for file in files:
                conn.get(file, os.path.join(temp_dir, file))

        # Leer con Spark
        df = spark.read.option("header", True).csv(temp_dir)

        return df
