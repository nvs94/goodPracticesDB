# Databricks notebook source
# MAGIC %md
# MAGIC # 🚀 Enterprise Unified Ingestion Pipeline
# MAGIC Multi-source (API + FTP + SQL + Files) con retry, métricas y alertas

# COMMAND ----------

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time
import json

from ingestion_framework.sources.api_source import APIIngestion
from ingestion_framework.sources.ftp_source import FTPIngestion
from ingestion_framework.sources.sql_source import SQLIngestion
from ingestion_framework.sources.file_source import FileIngestion

from ingestion_framework.storage.adls_storage import ADLSClient
from ingestion_framework.state.state_manager import FileStateManager

from aqualiasharedutils import Logger

# COMMAND ----------
# -----------------------------
# CONFIGURACIÓN GLOBAL
# -----------------------------
PROCESS_NAME = "UNIFIED_INGESTION_ENTERPRISE"
MAX_WORKERS = 8

logger = Logger(
    use_case="DATA_PLATFORM",
    process=PROCESS_NAME,
    id_process=f"{PROCESS_NAME}_{int(time.time())}",
    monitor_tenant_id="TENANT",
    monitor_client_id="CLIENT",
    monitor_client_secret="SECRET",
    flag_test=False
)

start_time = time.time()

# COMMAND ----------
# -----------------------------
# STORAGE (ADLS)
# -----------------------------
storage = ADLSClient(
    account_name="myadls",
    file_system="landing",
    credential="secret"
)

# COMMAND ----------
# -----------------------------
# STATE (CHECKPOINT)
# -----------------------------
state = FileStateManager("/dbfs/tmp/unified_state.txt")

# COMMAND ----------
# -----------------------------
# ALERTING (HOOK)
# -----------------------------
def send_alert(message):
    """
    Hook para alertas (email, teams, datadog, etc.)
    """
    logger.error(f"🚨 ALERT: {message}")

# COMMAND ----------
# -----------------------------
# WRAPPER CON MÉTRICAS + RETRY
# -----------------------------
def run_with_metrics(name, func, *args, **kwargs):
    retries = 3
    delay = 2

    for attempt in range(retries):
        try:
            t0 = time.time()

            result = func(*args, **kwargs)

            duration = time.time() - t0

            logger.info(f"{name}#SUCCESS duration={duration:.2f}s records={len(result) if result else 0}")

            logger.log_metric(f"{name}_duration", duration)
            logger.log_metric(f"{name}_records", len(result) if result else 0)

            return result

        except Exception as e:
            logger.warn(f"{name}#RETRY {attempt+1}/{retries} error={str(e)}")

            if attempt == retries - 1:
                send_alert(f"{name} failed after retries: {str(e)}")
                raise

            time.sleep(delay ** attempt)

# COMMAND ----------
# -----------------------------
# SOURCES CONFIG
# -----------------------------

api_source = APIIngestion(
    base_url="https://api.example.com",
    auth=None,
    logger=logger
)

ftp_source = FTPIngestion(
    host="ftp.example.com",
    username="user",
    password="pass",
    logger=logger
)

sql_source = SQLIngestion(
    jdbc_url="jdbc:sqlserver://server.database.windows.net",
    query="SELECT * FROM table WHERE updated_at > ?",
    user="user",
    password="password",
    logger=logger
)

file_source = FileIngestion(
    base_path="/dbfs/mnt/raw/",
    file_type="csv",  # csv / excel
    logger=logger
)

sources = {
    "api": lambda: api_source.fetch_records(endpoint="/data"),
    "ftp": lambda: ftp_source.fetch_records(path="/"),
    "sql": lambda: sql_source.fetch_records(),
    "files": lambda: file_source.fetch_records()
}

# COMMAND ----------
# -----------------------------
# EJECUCIÓN PARALELA MULTI-SOURCE
# -----------------------------
results = {}

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    future_to_source = {
        executor.submit(run_with_metrics, name, func): name
        for name, func in sources.items()
    }

    for future in as_completed(future_to_source):
        source_name = future_to_source[future]

        try:
            records = future.result()
            results[source_name] = records

        except Exception as e:
            logger.error(f"{source_name}#FAILED {str(e)}")

# COMMAND ----------
# -----------------------------
# ESCRITURA EN ADLS
# -----------------------------
for source_name, records in results.items():

    if not records:
        continue

    for record in records:
        file_name = f"{source_name}/{datetime.now().strftime('%Y/%m/%d')}/{int(time.time()*1000)}.json"

        storage.upload_record(
            data=json.dumps(record).encode("utf-8"),
            file_name=file_name
        )

# COMMAND ----------
# -----------------------------
# UPDATE STATE
# -----------------------------
state.update_last_processed(datetime.now())

# COMMAND ----------
# -----------------------------
# MÉTRICAS FINALES
# -----------------------------
total_duration = time.time() - start_time

logger.log_metric("total_duration", total_duration)
logger.log_metric("total_sources", len(results))

logger.info(f"Pipeline finished in {total_duration:.2f}s")
