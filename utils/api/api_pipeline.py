from datetime import datetime
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

from api_ingestion import paginate, incremental_filter


class APIPipeline:
    """
    Pipeline completo de ingestión desde API.
    """

    def __init__(
        self,
        client,
        state_manager,
        storage_client,
        endpoint: str,
        params: dict = None,
        incremental_field: str = None,
        max_workers: int = 4,
        logger=None,
    ):
        self.client = client
        self.state_manager = state_manager
        self.storage_client = storage_client
        self.endpoint = endpoint
        self.params = params or {}
        self.incremental_field = incremental_field
        self.max_workers = max_workers
        self.logger = logger or client.logger

    def _process_record(self, record: dict):
        """
        Procesa y almacena un registro en ADLS.
        """
        import json

        data = json.dumps(record).encode("utf-8")
        file_name = f"{record.get('id', 'record')}.json"

        self.storage_client.upload_bytes(data, file_name)

    def run(self) -> List[str]:

        # 1. Estado
        last_processed = self.state_manager.get_last_processed()

        if not last_processed:
            last_processed = datetime(1970, 1, 1)

        # 2. Paginación
        data = paginate(
            self.client,
            endpoint=self.endpoint,
            params=self.params
        )

        # 3. Incremental
        if self.incremental_field:
            data = incremental_filter(
                data,
                field=self.incremental_field,
                last_value=last_processed.isoformat()
            )

        if not data:
            self.logger.info("No new data")
            return []

        # 4. Paralelismo
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._process_record, data)

        # 5. Actualizar estado
        self.state_manager.update_last_processed(datetime.now())

        self.logger.info(f"Processed {len(data)} records")

        return [str(d.get("id")) for d in data]
