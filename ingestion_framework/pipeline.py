from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from datetime import datetime

class IngestionPipeline:
    """
    Pipeline genérico de ingestion.
    Funciona para cualquier SourceBase + StorageBase + StateManagerBase.
    """

    def __init__(self, source, storage, state_manager, max_workers=4, logger=None):
        self.source = source
        self.storage = storage
        self.state_manager = state_manager
        self.max_workers = max_workers
        self.logger = logger or self.source.logger

    def _process_record(self, record: Dict):
        """Almacena un registro en el storage"""
        import json
        file_name = f"{record.get('id', 'record')}_{int(datetime.now().timestamp())}.json"
        data = json.dumps(record).encode("utf-8")
        self.storage.upload_record(data, file_name)

    def run(self, **fetch_kwargs) -> List[str]:
        # 1. Obtener estado incremental
        last_processed = self.state_manager.get_last_processed()
        if not last_processed:
            last_processed = datetime(1970, 1, 1)

        # 2. Obtener registros desde la fuente
        records = self.source.fetch_records(last_processed=last_processed, **fetch_kwargs)
        if not records:
            self.logger.info("No new records found.")
            return []

        # 3. Paralelismo
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._process_record, records)

        # 4. Actualizar estado
        self.state_manager.update_last_processed(datetime.now())
        self.logger.info(f"Processed {len(records)} records")
        return [str(r.get("id")) for r in records]
