# Utils

Módulos de utilidades para ETL y Data Engineering:

## config.py
- Carga configuraciones de `config.yaml`.
- Funciones: `get_config`, `get_key_vault_scope`, `get_config_elastic`, `get_sql_server_config`.

## helpers.py
- Funciones reutilizables:
  - `get_previous_day(ts)`
  - `unix_to_utc_string(unix_timestamp)`
  - `pairwise(iterable)`

## logger.py
- Logger simplificado.
- Métodos: `info`, `warn`, `error`, `log_metric`, `log_end`.

## api/
- Contiene módulos `auth.py`, `base_client.py` y `pagination.py` para integración con APIs externas.
