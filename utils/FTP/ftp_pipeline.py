from datetime import datetime
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ftp_client import SFTPClient
from ftp_ingestion import (
    list_files_with_metadata,
    filter_files_by_modification_date
)
from state_manager import StateManager
from retry import retry


class FTPPipeline:
    """
    Pipeline enterprise:

    - Descarga incremental
    - Paralelismo
    - Escritura directa a ADLS
    """

    def __init__(
        self,
        client: SFTPClient,
        state_manager: StateManager,
        remote_path: str,
        storage_client=None,
        local_path: Optional[str] = None,
        max_workers: int = 4,
        logger=None,
    ):
        self.client = client
        self.state_manager = state_manager
        self.remote_path = remote_path
        self.storage_client = storage_client
        self.local_path = local_path
        self.max_workers = max_workers
        self.logger = logger or client.logger

    def _download_and_store(self, filename: str) -> str:
        """
        Descarga un fichero y lo envía a destino (ADLS o local)
        """

        # Descargar en memoria (evita disco)
        with self.client.conn.open(filename, "rb") as remote_file:
            data = remote_file.read()

        if self.storage_client:
            # Escribir en ADLS directamente
            self.storage_client.upload_bytes(data, filename)
            self.logger.info(f"Uploaded to ADLS: {filename}")

        elif self.local_path:
            # Fallback local
            local_file = f"{self.local_path}/{filename}"
            with open(local_file, "wb") as f:
                f.write(data)

            self.logger.info(f"Saved locally: {local_file}")

        return filename

    @retry(retries=3, delay=2)
    def run(self, extension: Optional[str] = None) -> List[str]:

        with self.client:

            # 1. Estado previo
            last_processed = self.state_manager.get_last_processed()

            if not last_processed:
                last_processed = datetime(1970, 1, 1)
                self.logger.info("Full load (no state)")

            # 2. Posicionarse en carpeta
            self.client.conn.cwd(self.remote_path)

            # 3. Listar + filtrar
            files_attr = list_files_with_metadata(self.client)

            files_to_download = filter_files_by_modification_date(
                files_attr,
                min_datetime=last_processed,
                extension=extension,
            )

            if not files_to_download:
                self.logger.info("No new files")
                return []

            self.logger.info(f"{len(files_to_download)} files to process")

            # 4. PARALELISMO
            results = []

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:

                futures = [
                    executor.submit(self._download_and_store, f)
                    for f in files_to_download
                ]

                for future in as_completed(futures):
                    results.append(future.result())

            # 5. Actualizar estado
            new_state = datetime.now()
            self.state_manager.update_last_processed(new_state)

            self.logger.info(f"Checkpoint updated: {new_state}")

            return resultsn downloaded
