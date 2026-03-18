import yaml
import os
from yaml.loader import SafeLoader

def get_config(key, filename="../config.yaml"):
    """
    Recupera configuración de un archivo YAML según el entorno.
    :param key: Clave de configuración
    :param filename: Ruta del YAML
    :return: Diccionario con la configuración del entorno
    """
    environment = os.getenv("ENVIRONMENT", "pre").lower()
    with open(filename) as f:
        cfg = yaml.load(f, Loader=SafeLoader)
    return cfg.get(key, {}).get(environment)

def get_key_vault_scope():
    """Obtiene configuración de Key Vault según el entorno."""
    return get_config("key-vault")

def get_config_elastic():
    """Obtiene configuración de Elasticsearch según el entorno."""
    return get_config("elastic")

def get_sql_server_config():
    """Obtiene configuración de SQL Server según el entorno."""
    return get_config("sql-server")
