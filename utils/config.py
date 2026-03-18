import yaml
import os
from yaml.loader import SafeLoader

def get_config(key, filename="config.yaml"):
    """
    Recupera configuración de un archivo YAML según el entorno.
    """
    environment = os.getenv("ENVIRONMENT", "pre").lower()
    with open(filename) as f:
        cfg = yaml.load(f, Loader=SafeLoader)
    return cfg.get(key, {}).get(environment)

def get_key_vault_scope():
    return get_config("key-vault")

def get_config_elastic():
    return get_config("elastic")

def get_sql_server_config():
    return get_config("sql-server")
