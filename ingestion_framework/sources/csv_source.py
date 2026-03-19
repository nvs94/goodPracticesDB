import os
import pandas as pd
from datetime import datetime

class CSVIngestion:
    """
    Ingestión de archivos CSV desde un directorio.

    Soporta:
    - Configuración de delimiter, encoding, header
    - Filtrado incremental por fecha de modificación
    - Selección de columnas
    """

    def __init__(
        self,
        base_path: str,
        delimiter: str = ",",
        encoding: str = "utf-8",
        header: int = 0,
        columns: list = None,
        logger=None
    ):
        self.base_path = base_path
        self.delimiter = delimiter
        self.encoding = encoding
        self.header = header
        self.columns = columns
        self.logger = logger

    def _should_process(self, file_path, last_processed):
        """Filtra archivos por fecha de modificación"""
        if not last_processed:
            return True

        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        return modified_time > last_processed

    def fetch_records(self, last_processed=None):
        records = []

        if self.logger:
            self.logger.info(f"CSV#Scanning path: {self.base_path}")

        for file in os.listdir(self.base_path):

            if not file.endswith(".csv"):
                continue

            file_path = os.path.join(self.base_path, file)

            if not self._should_process(file_path, last_processed):
                continue

            try:
                if self.logger:
                    self.logger.info(f"CSV#Reading file: {file}")

                df = pd.read_csv(
                    file_path,
                    sep=self.delimiter,
                    encoding=self.encoding,
                    header=self.header
                )

                # Selección de columnas si aplica
                if self.columns:
                    df = df[self.columns]

                # Limpieza básica
                df = df.dropna(how="all")

                records.extend(df.to_dict(orient="records"))

            except Exception as e:
                if self.logger:
                    self.logger.error(f"CSV#Error reading {file}: {str(e)}")

        if self.logger:
            self.logger.info(f"CSV#Total records: {len(records)}")

        return records

''' -------------- EXAMPLE ---------------
from ingestion_framework.sources.csv_source import CSVIngestion

csv_source = CSVIngestion(
    base_path="/dbfs/mnt/data/csv/",
    delimiter=";",
    encoding="latin-1",
    header=0,
    columns=["id", "name", "value"]
)


csv_data = csv_source.fetch_records()
'''
