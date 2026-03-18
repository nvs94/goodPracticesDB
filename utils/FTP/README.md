# 📦 SFTP Client - Best Practices Module

Production-ready SFTP client for secure and scalable file ingestion pipelines.

---
## 🚀 Features

- Secure SFTP connection (password or private key)
- Context manager support (`with` statement)
- File download/upload utilities
- Bulk file operations
- Retention policy (automatic deletion of old files)
- Pluggable logging
- Clean and reusable design

---

## 📁 Structure
  * ftp_client.py
  * example_usage.py
  * ftp_ingestion.py

---
## 🔄 Incremental Ingestion (Recommended)

This module supports incremental file ingestion based on modification date.

### Example

```python
from datetime import datetime
from ftp_client import SFTPClient
from ftp_ingestion import incremental_download

with SFTPClient(...) as client:

    files = incremental_download(
        client=client,
        remote_path="FIC_FACT_AGUAS",
        local_path="/tmp",
        last_processed_datetime=datetime(2024, 1, 1),
        extension=".xlsx"
    )
```
---
## 🔐 Authentication

Supports:

- Username + password
- Private key authentication

---

## ⚠️ Security Notes

- In production, always provide a `known_hosts` file
- Avoid disabling host key verification

---

## 🧩 Usage Example

```python
from ftp_client import SFTPClient, build_filename

client = SFTPClient(
    host="your_host",
    username="user",
    password="password"
)

with client:
    client.download_file("remote.csv", "/tmp/remote.csv")
```
## 📥 Download Multiple Files
```python
files = ["file1.csv", "file2.csv"]

with client:
    client.download_files(files, "/tmp")
```
## 🧹 Retention Policy (Delete Old Files)
```python
from datetime import datetime

def extract_date(filename):
    return datetime.strptime(filename[-12:-4], "%Y%m%d")

with client:
    client.delete_old_files(
        days=7,
        date_extractor=extract_date
    )
```
## 🏗 Best Practices Applied

 * Separation of concerns

 * Reusable components

 * Explicit error handling

 * Logging-ready

 * Production-safe defaults

 * Extensible design

## 🔄 Recommended Extensions

 * Retry mechanism for transfers

 * Parallel downloads

 * Incremental ingestion logic

 * Integration with cloud storage (S3, ADLS)

## 🧪 Testing

Recommended:

 * Mock SFTP server (e.g. pytest-sftpserver)

 * Unit tests for:

   * filename parsing

   * retention logic

   * connection handling
## 📌 Notes

This module is designed to be integrated into data ingestion pipelines (ETL/ELT), especially in environments like:

 * Databricks

 * Airflow

 * Azure Data Factory

 * AWS Glue

## 👨‍💻 Authoring Guidelines

When extending:

 * Keep functions pure where possible

 * Avoid hardcoded paths

 * Inject dependencies (logger, credentials)

 * Maintain backward compatibility
