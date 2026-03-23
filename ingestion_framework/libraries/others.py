"""
Guía práctica de librerías clave para Data Engineering en entornos productivos.

Incluye:
- requests (APIs)
- logging (observabilidad)
- os (configuración)
- tenacity (resiliencia)
- paramiko (FTP/SFTP)
- pandas (data handling)
- pyarrow (optimización)
- openpyxl (Excel)
- azure-storage-blob (ADLS)
- azure-identity (autenticación)

Cada bloque incluye:
- Qué hace
- Cuándo usarlo
- Ejemplo práctico
"""

# ============================
# 1. REQUESTS (APIs)
# ============================

import requests

def requests_examples():
    """
    🌐 REQUESTS

    Casos de uso:
    - Llamadas a APIs REST
    - Integraciones externas

    Claves:
    - Manejar timeout
    - Controlar errores
    """

    url = "https://api.example.com/data"

    try:
        response = requests.get(url, timeout=10)

        # Validar status
        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:
        print("Timeout error")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return data


# ============================
# 2. LOGGING
# ============================

import logging

def logging_examples():
    """
    🧾 LOGGING

    Casos de uso:
    - Monitorización de pipelines
    - Debugging

    Buenas prácticas:
    - No usar print en producción
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger("my_pipeline")

    logger.info("Proceso iniciado")
    logger.warning("Posible problema")
    logger.error("Error en ejecución")


# ============================
# 3. OS (ENV VARIABLES)
# ============================

import os

def os_examples():
    """
    ⚙️ OS

    Casos de uso:
    - Leer variables de entorno
    - Configuración dinámica

    Ejemplo:
    """

    env = os.getenv("ENVIRONMENT", "pre")

    if env == "pro":
        print("Producción")
    else:
        print("Preproducción")


# ============================
# 4. TENACITY (RETRY)
# ============================

from tenacity import retry, stop_after_attempt, wait_exponential

def tenacity_examples():
    """
    🔁 TENACITY

    Casos de uso:
    - Reintentos automáticos (APIs, DB, FTP)

    Claves:
    - Backoff exponencial
    - Evitar caídas por errores temporales
    """

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2)
    )
    def unstable_call():
        print("Intentando...")
        raise Exception("Fallo simulado")

    try:
        unstable_call()
    except Exception:
        print("Falló tras varios intentos")


# ============================
# 5. PARAMIKO (SFTP)
# ============================

import paramiko

def paramiko_examples():
    """
    📂 PARAMIKO (SFTP)

    Casos de uso:
    - Descarga de ficheros FTP/SFTP
    """

    host = "example.com"
    username = "user"
    password = "password"

    transport = paramiko.Transport((host, 22))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    # Listar ficheros
    files = sftp.listdir()

    # Descargar fichero
    sftp.get("remote.csv", "/local/remote.csv")

    sftp.close()
    transport.close()


# ============================
# 6. PANDAS
# ============================

import pandas as pd

def pandas_examples():
    """
    🐼 PANDAS

    Casos de uso:
    - Transformaciones pequeñas
    - Preprocesado antes de Spark

    NO usar para grandes volúmenes
    """

    df = pd.read_csv("file.csv")

    df["amount_eur"] = df["amount"] * 0.85

    df_grouped = df.groupby("country")["amount"].sum()

    return df_grouped


# ============================
# 7. PYARROW
# ============================

import pyarrow.parquet as pq

def pyarrow_examples():
    """
    ⚡ PYARROW

    Casos de uso:
    - Lectura/escritura eficiente en Parquet
    - Interoperabilidad Spark/Pandas
    """

    table = pq.read_table("file.parquet")
    df = table.to_pandas()

    return df


# ============================
# 8. OPENPYXL (EXCEL)
# ============================

from openpyxl import load_workbook

def openpyxl_examples():
    """
    📊 OPENPYXL

    Casos de uso:
    - Lectura de Excel complejos
    - Manipulación de hojas

    """

    wb = load_workbook("file.xlsx")
    sheet = wb.active

    value = sheet["A1"].value

    print(value)


# ============================
# 9. AZURE STORAGE BLOB (ADLS)
# ============================

from azure.storage.blob import BlobServiceClient

def azure_blob_examples():
    """
    ☁️ AZURE STORAGE BLOB

    Casos de uso:
    - Subir/bajar ficheros
    - Integración con Data Lake
    """

    conn_str = "your_connection_string"

    client = BlobServiceClient.from_connection_string(conn_str)

    container = client.get_container_client("data")

    # Subir fichero
    with open("file.csv", "rb") as data:
        container.upload_blob(name="file.csv", data=data)

    # Descargar fichero
    blob = container.download_blob("file.csv")
    content = blob.readall()

    return content


# ============================
# 10. AZURE IDENTITY
# ============================

from azure.identity import DefaultAzureCredential

def azure_identity_examples():
    """
    🔐 AZURE IDENTITY

    Casos de uso:
    - Autenticación segura (Managed Identity)

    Recomendado en producción en lugar de connection strings
    """

    credential = DefaultAzureCredential()

    print("Autenticación inicializada")


# ============================
# FIN
# ============================

"""
Este archivo cubre el stack típico de Data Engineering moderno:

- APIs → requests
- Resiliencia → tenacity
- FTP → paramiko
- Data → pandas / pyarrow
- Cloud → azure sdk
- Logging → logging

Recomendación:
- Guardar en utils/
- Usar como referencia en proyectos reales
"""
