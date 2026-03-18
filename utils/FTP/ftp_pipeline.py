from datetime import datetime
from typing import List, Optional
from ftp_client import SFTPClient
from ftp_ingestion import (
    list_files_with_metadata,
    filter_files_by_modification_date
)
from state_manager import StateManager
from retry import retry


class FTPPipeline:
    """
    Pipeline completo de ingestión FTP:

    - Conexión
    - Descarga incremental
    - Gestión de estado
    - Reintentos
    - Logging
    """

    def __init__(
        self,
        client: SFTPClient,
        state_manager: StateManager,
        remote_path: str,
        local_path: str,
        logger=None,
    ):
        self.client = client
        self.state_manager = state_manager
        self.remote_path = remote_path
        self.local_path = local_path
        self.logger = logger or client.logger

    @retry(retries=3, delay=2)
    def run(self, extension: Optional[str] = None) -> List[str]:
        """
        Ejecuta el pipeline completo.
        """

        with self.client:

            # 1. Obtener último estado
            last_processed = self.state_manager.get_last_processed()

            if not last_processed:
                last_processed = datetime(1970, 1, 1)
                self.logger.info("No previous state found. Full load.")

            self.logger.info(f"Last processed: {last_processed}")

            # 2. Cambiar directorio
            self.client.conn.cwd(self.remote_path)

            # 3. Listar ficheros con metadata
            files_attr = list_files_with_metadata(self.client)

            # 4. Filtrar incremental
            files_to_download = filter_files_by_modification_date(
                files_attr,
                min_datetime=last_processed,
                extension=extension,
            )

            if not files_to_download:
                self.logger.info("No new files to process")
                return []

            self.logger.info(f"Files to download: {files_to_download}")

            # 5. Descargar
            downloaded = self.client.download_files(
                files_to_download,
                self.local_path
            )

            # 6. Actualizar estado (checkpoint)
            new_state = datetime.now()
            self.state_manager.update_last_processed(new_state)

            self.logger.info(f"State updated: {new_state}")

            return downloaded
