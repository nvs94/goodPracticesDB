import os
import pandas as pd
from datetime import datetime

class ExcelIngestion:
    """
    Ingestión de archivos Excel desde un directorio.

    Soporta:
    - Selección de sheet
    - Header configurable
    - Filtrado incremental
    - Selección de columnas
    """

    def __init__(
        self,
        base_path: str,
        sheet_name=0,
        header: int = 0,
        columns: list = None,
        logger=None
    ):
        self.base_path = base_path
        self.sheet_name = sheet_name
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
            self.logger.info(f"EXCEL#Scanning path: {self.base_path}")

        for file in os.listdir(self.base_path):

            if not (file.endswith(".xlsx") or file.endswith(".xls")):
                continue

            file_path = os.path.join(self.base_path, file)

            if not self._should_process(file_path, last_processed):
                continue

            try:
                if self.logger:
                    self.logger.info(f"EXCEL#Reading file: {file}")

                df = pd.read_excel(
                    file_path,
                    sheet_name=self.sheet_name,
                    header=self.header
                )

                # Si sheet devuelve dict (multi-sheet)
                if isinstance(df, dict):
                    df = pd.concat(df.values())

                # Selección de columnas
                if self.columns:
                    df = df[self.columns]

                # Limpieza básica
                df = df.dropna(how="all")

                records.extend(df.to_dict(orient="records"))

            except Exception as e:
                if self.logger:
                    self.logger.error(f"EXCEL#Error reading {file}: {str(e)}")

        if self.logger:
            self.logger.info(f"EXCEL#Total records: {len(records)}")

        return records
