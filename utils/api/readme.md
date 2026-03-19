# 🚀 API Ingestion Framework (Enterprise Ready)

Framework modular para ingestión de datos desde APIs hacia Azure Data Lake.

---

## 🧠 Features

* 🔄 Ingesta incremental (based on `updated_at`)
* ⚡ Paralelismo
* 🔁 Retry automático
* 🔐 Soporte de autenticación (API Key, Bearer, OAuth2)
* ☁️ Integración con ADLS
* 💾 Checkpointing

---

## 🏗️ Arquitectura

```
API → APIClient → Ingestion → Pipeline → ADLS
                         ↓
                   StateManager
```

---

## 🚀 Uso rápido

```python
pipeline = APIPipeline(
    client=client,
    state_manager=state,
    storage_client=adls,
    endpoint="/data",
    incremental_field="updated_at"
)

pipeline.run()
```

---

## 🔑 Autenticación soportada

* API Key
* Bearer Token
* OAuth2 Client Credentials

---

## 🔄 Incremental

Se basa en un campo tipo:

* `updated_at`
* `created_at`
* `timestamp`

---

## ⚡ Paralelismo

Configurado con:

```python
max_workers=8
```

---

## 🧠 Buenas prácticas

* No acoplar lógica al cliente
* Externalizar estado
* Usar retry siempre
* Evitar reprocesamiento

---

## ☁️ Destino

Azure Data Lake Storage (ADLS)

---

## 🧪 Testing

* Mock APIs
* Test de paginación
* Test de incremental

---

## 🏁 Conclusión

Este módulo permite construir pipelines API robustos, escalables y reutilizables en entornos enterprise.
