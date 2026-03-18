# 🚀 SFTP Ingestion Framework (Enterprise Ready)

Framework modular y production-ready para la ingesta de datos desde servidores SFTP hacia Azure Data Lake Storage (ADLS), diseñado para entornos de Data Engineering modernos (Databricks, Airflow, ADF).

---

## 🧠 Objetivo

Proporcionar una solución:

* Reutilizable
* Escalable
* Idempotente
* Desacoplada
* Preparada para cloud

para pipelines de ingesta de ficheros vía SFTP.

---

## 🏗️ Estructura del Proyecto

```
/ftp
├── ftp_client.py       # Cliente SFTP (conexión y operaciones básicas)
├── ftp_ingestion.py    # Lógica de filtrado e ingesta incremental
├── ftp_pipeline.py     # Orquestador principal del pipeline
├── state_manager.py    # Gestión de estado (checkpointing)
├── retry.py            # Reintentos con backoff exponencial
├── exceptions.py       # Excepciones custom
└── storage_adls.py     # Integración con Azure Data Lake
```

---

## 🔄 Flujo de Ejecución

```
SFTP Server
     ↓
SFTPClient
     ↓
FTPIngestion (filtrado incremental)
     ↓
FTPPipeline (paralelismo + orquestación)
     ↓
ADLS (Data Lake)
     ↓
StateManager (checkpoint)
```

---

## ⚡ Features Principales

### 🔄 Ingesta incremental

Solo procesa ficheros nuevos basándose en fecha de modificación (`st_mtime`).

### ⚡ Paralelismo

Descarga concurrente usando `ThreadPoolExecutor`.

### ☁️ Integración directa con ADLS

Streaming de ficheros sin pasar por disco local.

### 🔁 Reintentos automáticos

Backoff exponencial configurable.

### 💾 Gestión de estado desacoplada

Permite persistencia en:

* fichero
* memoria
* (extensible a DB, Blob, etc.)

### 🧩 Modularidad

Separación clara de responsabilidades.

---

## 🚀 Ejemplo de Uso

```python
from ftp_client import SFTPClient, default_logger
from ftp_pipeline import FTPPipeline
from state_manager import FileStateManager
from storage_adls import ADLSClient

logger = default_logger()

client = SFTPClient(
    host="your_sftp_host",
    username="user",
    password="password",
    logger=logger
)

adls = ADLSClient(
    account_name="your_storage_account",
    file_system="landing",
    credential="your_credential"
)

state = FileStateManager("/dbfs/tmp/ftp_state.txt")

pipeline = FTPPipeline(
    client=client,
    state_manager=state,
    remote_path="remote_folder",
    storage_client=adls,
    max_workers=8,
    logger=logger
)

files_processed = pipeline.run(extension=".csv")
```

---

## 🧩 Componentes

### 📦 `ftp_client.py`

Cliente SFTP reutilizable:

* Conexión segura
* Descarga/subida de ficheros
* Operaciones básicas (`list`, `exists`, etc.)
* Soporte para context manager (`with`)

---

### 📦 `ftp_ingestion.py`

Lógica de negocio de ingesta:

* Lectura de metadatos (`listdir_attr`)
* Filtrado por fecha
* Soporte para ingesta incremental

---

### 📦 `ftp_pipeline.py`

Orquestador principal:

* Controla flujo end-to-end
* Aplica paralelismo
* Ejecuta descarga + almacenamiento
* Actualiza estado

---

### 📦 `state_manager.py`

Gestión de estado (checkpoint):

Implementaciones incluidas:

* `InMemoryStateManager` → testing
* `FileStateManager` → persistencia simple

Extensible a:

* bases de datos
* Azure Blob
* Redis

---

### 📦 `storage_adls.py`

Cliente para Azure Data Lake:

* Subida directa desde memoria
* Evita uso de disco local
* Optimizado para cloud

---

### 📦 `retry.py`

Decorador de reintentos:

* Backoff exponencial
* Configurable
* Transparente para el pipeline

---

### 📦 `exceptions.py`

Errores tipados:

* Mejora trazabilidad
* Facilita debugging
* Base para observabilidad

---

## ⚙️ Configuración

### 🔐 Credenciales

Se recomienda usar:

* Azure Key Vault
* Variables de entorno
* Secret scopes (Databricks)

---

### ⚡ Paralelismo

```python
max_workers = 8
```

Guía:

| Tipo de fichero | Recomendación |
| --------------- | ------------- |
| Pequeños        | 8 - 16        |
| Medianos        | 4 - 8         |
| Grandes         | 2 - 4         |

---

## 🧠 Buenas Prácticas Aplicadas

* Separación de responsabilidades
* Inversión de dependencias
* Idempotencia
* Logging estructurado
* Evitar estado implícito
* Cloud-first design

---

## ⚠️ Consideraciones

### Seguridad

* No desactivar `host key verification` en producción
* Usar autenticación por clave siempre que sea posible

### Performance

* Evitar `/tmp` en cloud
* Usar streaming a ADLS

### Robustez

* Siempre usar retry
* Persistir estado

---

## 🧪 Testing (Recomendado)

* Mock de servidor SFTP
* Tests unitarios:

  * filtrado incremental
  * lógica de estado
  * retries

---

## 🔄 Extensiones Futuras

* Integración con Delta Lake
* Ingesta directa a Spark DataFrames
* Event-driven ingestion (Azure Functions)
* Métricas (Prometheus / Azure Monitor)
* Descarga distribuida (Spark)

---

## 👨‍💻 Uso Recomendado

Este framework está pensado para:

* Pipelines batch en Databricks
