# 🌐 Aqualia Utilities Module

This module provides reusable, production-ready utilities for data engineering workflows (Databricks, batch ingestion pipelines, ETL), focusing on:

* Reliability (retry, timeout, error handling)
* Reusability (decoupled components)
* Maintainability (clean architecture)
* Centralized configuration and logging

---

## 📁 Structure
utils/
├── config.py # Configuration loader by environment
├── helpers.py # Reusable helpers: get_previous_day, unix_to_utc_string, pairwise, etc.
├── logger.py # Simplified logger for pipelines
└── api/
├── base_client.py # Core HTTP client with retry & error handling
├── pagination.py # Generic pagination handler (parallel optional)
└── auth.py # Token management with caching & auto-refresh

---

## 🧠 Design Principles

### 1. Separation of concerns

Each component has a single responsibility:

| Component              | Responsibility                                   |
| ---------------------- | ----------------------------------------------- |
| `config.py`            | Loads environment-based configuration          |
| `helpers.py`           | Provides reusable helper functions              |
| `logger.py`            | Simplified logging for pipelines                |
| `BaseAPIClient`        | Handles HTTP requests                            |
| `BearerTokenManager`   | Manages authentication lifecycle                |
| `fetch_paginated_data` | Handles pagination logic                         |

---

### 2. Composability

Utilities are designed to be combined:

* Config + Logger → centralized and standardized environment
* Client + Auth → authenticated API requests
* Client + Pagination → scalable API ingestion
* All together → production-ready pipelines

---

### 3. API-agnostic design

These utilities:

* Do NOT depend on specific APIs
* Can be reused across projects and providers
* Can integrate with any REST API, Azure Key Vault, Elasticsearch, or SQL Server configuration

---

## 🚀 Quick Start

### 1. Load configuration
```python
from utils.config import get_config_elastic, get_sql_server_config

elastic_cfg = get_config_elastic()
sql_cfg = get_sql_server_config()
print(elastic_cfg, sql_cfg)

### 2. Initialize logger
from utils.logger import Logger

logger = Logger(process="MyETL")
logger.info("Pipeline started")
### 3. Create API client
from utils.api.base_client import BaseAPIClient

client = BaseAPIClient(
    base_url="https://api.example.com",
    timeout=10,
    max_retries=3
)
### 4. Add authentication
from utils.api.auth import BearerTokenManager

def login():
    return client.post("/login", data={"user": "...", "password": "..."})

token_manager = BearerTokenManager(get_token_fn=login)

token = token_manager.get_token()

client.set_headers({
    "Authorization": f"Bearer {token}"
})
### 5. Fetch paginated data
from utils.api.pagination import fetch_paginated_data

def fetch_page(page):
    return client.get("/resource", params={"page": page})

def extract_items(response):
    return response.get("items", [])

def get_total_pages(response):
    return response.get("pages", 1)

data = fetch_paginated_data(
    fetch_page_fn=fetch_page,
    extract_items_fn=extract_items,
    get_total_pages_fn=get_total_pages,
    parallel=True,
    max_workers=5
)
```
# 🧠 When to Use
### ✅ Recommended

* Batch ingestion from REST APIs

* APIs with pagination

* Token-based authentication

* Moderate/high data volume

* Pipelines with centralized logging and environment-based configuration
### ❌ When NOT to Use

* Simple one-off scripts

* APIs with cursor-based pagination (requires different pattern)

* Strict rate-limited APIs (needs throttling layer)

* Projects where configuration and logging are not required

## ⚠️ Common Pitfalls
### 1. Calling APIs inside Spark workers ❌

Avoid patterns like:
df.applyInPandas(...)
### ➡️ This can:

* Break rate limits

* Cause instability

* Create non-deterministic behavior

### ✔️ Instead:

* Call APIs outside Spark (driver)

* Store raw data (Delta / Bronze)

* Process with Spark afterwards

### 2. Not controlling parallelism

Too many threads can:

* Overload APIs

* Trigger throttling (429 errors)

✔️ Always tune:
### 3. Token misuse

Avoid:

* Requesting token on every call

* Not handling expiration

✔️ Use BearerTokenManager with caching

##🔥 Best Practices

* Always use timeout in API calls

* Centralize retry logic (never duplicate it)

* Keep API logic separate from business transformations

* Log failures and monitor API behavior

* Store raw responses before transforming (bronze layer)

* Use environment-based configuration via config.py

* Use Logger for consistent logging and metrics

## 📈 Future Improvements

* Rate limiting / throttling control

* Async requests (aiohttp)

* Integrated logging hooks

* Metrics collection (latency, error rate)

* Authenticated client abstraction

* Extend helpers for more reusable ETL functions

## 📌 Example

See:
examples/api/amper_example.py

for a full working example combining:

* client
* auth
* paginated API fetch
* logging
* configuration
## 🧠 Final Note

These utilities are intended to evolve into a personal data engineering playbook.

Keep improving them as new patterns emerge.
