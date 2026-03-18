# 🌐 API Utilities Module

This module provides reusable, production-ready utilities to interact with REST APIs in a robust and scalable way.

It is designed for data engineering workflows (e.g., Databricks, batch ingestion pipelines) and focuses on:

* Reliability (retry, timeout, error handling)
* Reusability (decoupled components)
* Maintainability (clean architecture)

---

## 📁 Structure

```
utils/api/
├── base_client.py     # Core HTTP client with retry & error handling
├── pagination.py      # Generic pagination handler (parallel optional)
└── auth.py            # Token management with caching & auto-refresh

examples/api/
└── amper_example.py   # Real usage example
```

---

## 🧠 Design Principles

### 1. Separation of concerns

Each component has a single responsibility:

| Component              | Responsibility                   |
| ---------------------- | -------------------------------- |
| `BaseAPIClient`        | Handles HTTP requests            |
| `BearerTokenManager`   | Manages authentication lifecycle |
| `fetch_paginated_data` | Handles pagination logic         |

---

### 2. Composability

Utilities are designed to be combined:

* Client + Auth → authenticated requests
* Client + Pagination → scalable ingestion
* All together → production-ready pipelines

---

### 3. API-agnostic design

These utilities:

* Do NOT depend on specific APIs
* Can be reused across projects and providers

---

## 🚀 Quick Start

### 1. Create API client

```python
from utils.api.base_client import BaseAPIClient

client = BaseAPIClient(
    base_url="https://api.example.com",
    timeout=10,
    max_retries=3
)
```

---

### 2. Add authentication

```python
from utils.api.auth import BearerTokenManager

def login():
    return client.post("/login", data={"user": "...", "password": "..."})

token_manager = BearerTokenManager(get_token_fn=login)

token = token_manager.get_token()

client.set_headers({
    "Authorization": f"Bearer {token}"
})
```

---

### 3. Fetch paginated data

```python
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

---

## 🧠 When to Use

### ✅ Recommended

* Batch ingestion from REST APIs
* APIs with pagination
* Token-based authentication
* Moderate/high data volume

---

## ❌ When NOT to Use

* Simple one-off scripts
* APIs with cursor-based pagination (requires different pattern)
* Strict rate-limited APIs (needs throttling layer)

---

## ⚠️ Common Pitfalls

### 1. Calling APIs inside Spark workers ❌

Avoid patterns like:

```python
df.applyInPandas(...)
```

➡️ This can:

* Break rate limits
* Cause instability
* Create non-deterministic behavior

✔️ Instead:

* Call APIs outside Spark (driver)
* Store raw data (Delta / Bronze)
* Process with Spark afterwards

---

### 2. Not controlling parallelism

Too many threads can:

* Overload APIs
* Trigger throttling (429 errors)

✔️ Always tune:

```python
max_workers=5
```

---

### 3. Token misuse

Avoid:

* Requesting token on every call
* Not handling expiration

✔️ Use `BearerTokenManager`

---

## 🔥 Best Practices

* Always use timeout in API calls
* Centralize retry logic (never duplicate it)
* Keep API logic separate from business transformations
* Log failures and monitor API behavior
* Store raw responses before transforming (bronze layer)

---

## 📈 Future Improvements

* Rate limiting / throttling control
* Async requests (aiohttp)
* Integrated logging hooks
* Metrics collection (latency, error rate)
* Authenticated client abstraction

---

## 📌 Example

See:

```
examples/api/amper_example.py
```

for a full working example combining:

* client
* auth
* real API call

---

## 🧠 Final Note

These utilities are intended to evolve into a **personal data engineering playbook**.

Keep improving them as new patterns emerge.
