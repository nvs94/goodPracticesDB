# 🏗️ Unified Ingestion Framework

Framework modular y enterprise-ready para ingestión de datos desde múltiples orígenes hacia ADLS, con soporte de paralelismo, logging y estado incremental.

---

## 📂 Estructura del repositorio
```python
/ingestion_framework
├── init.py
├── core.py # Clases base, interfaces y utilidades comunes
├── pipeline.py # Pipeline genérico y paralelizable
├── sources
│ ├── init.py
│ ├── api_source.py # APIClient + ingestión incremental + paralelismo
│ └── ftp_source.py # FTPClient + ingestión incremental + paralelismo
├── storage
│ ├── init.py
│ └── adls_storage.py # Cliente ADLS genérico
├── state
│ ├── init.py
│ └── state_manager.py # Checkpointing y estado incremental
├── utils
│ ├── init.py
│ ├── retry.py # Decorador de reintentos con backoff simple
│ └── exceptions.py # Excepciones personalizadas
└── README.md

```
---

## ⚡ Features principales

- Conectividad con **API** y **FTP** (expandible a otros orígenes)  
- **Paralelismo configurable** para acelerar la ingestión  
- **Retry automático** configurable en fuentes de datos  
- **Estado incremental** persistido para procesamientos idempotentes  
- **Almacenamiento en ADLS** con abstracción para otros destinos  
- **Logging centralizado**, compatible con tus sistemas de monitorización  

---

## 🏗️ Arquitectura
SourceBase (API, FTP) -> Pipeline -> StorageBase (ADLS)
-> StateManager (checkpoint incremental)

- `SourceBase`: Clase base de cualquier fuente (API, FTP, etc.)  
- `StorageBase`: Clase base para almacenar registros en cualquier destino (ADLS, S3, local, etc.)  
- `StateManagerBase`: Clase base para mantener estado incremental entre ejecuciones  
- `IngestionPipeline`: Orquesta la ingestión, procesando en paralelo y gestionando el estado  

---

## 📌 Uso básico

```python
from ingestion_framework.pipeline import IngestionPipeline
from ingestion_framework.sources.api_source import APIIngestion
from ingestion_framework.sources.ftp_source import FTPIngestion
from ingestion_framework.storage.adls_storage import ADLSClient
from ingestion_framework.state.state_manager import FileStateManager

# Configuración de las fuentes
api_source = APIIngestion(base_url="https://api.example.com", auth=None, logger=None)
ftp_source = FTPIngestion(host="ftp.example.com", username="user", password="pass", logger=None)

# Configuración del storage
adls_client = ADLSClient(account_name="myaccount", file_system="landing", credential="my_secret")

# Configuración del estado incremental
state_manager = FileStateManager("/tmp/state_ingestion.txt")

# Crear pipeline unificado para API
api_pipeline = IngestionPipeline(source=api_source, storage=adls_client, state_manager=state_manager, max_workers=8)
api_pipeline.run(endpoint="/data")

# Crear pipeline unificado para FTP
ftp_pipeline = IngestionPipeline(source=ftp_source, storage=adls_client, state_manager=state_manager, max_workers=4)
ftp_pipeline.run(path="/remote/path")
```
## 🔄 Extensibilidad

 * Para agregar nuevas fuentes de datos, crear una clase que implemente SourceBase

 * Para agregar nuevos destinos de almacenamiento, crear una clase que implemente StorageBase

 * Para cambiar el método de checkpointing, implementar StateManagerBase

## 📝 Buenas prácticas

 * Mantener la lógica de conexión y retries dentro de las clases de fuentes

 * Evitar lógica de negocio en los pipelines; estos solo orquestan ejecución y paralelismo

 * Persistir estado incremental para poder reiniciar la ingestión sin duplicados

 * Loggear cada paso crítico (inicio, fin, errores, métricas)

## 🔧 Requisitos

 * Python >= 3.8

 * PySpark (si se usa en Databricks)

 * pysftp para FTP

 * requests para APIs

 * azure-storage-file-datalake para ADLS
