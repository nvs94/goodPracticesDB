"""
Guía práctica de uso de dbutils en Databricks.

Incluye:
- secrets (Key Vault)
- widgets (parámetros)
- filesystem (DBFS)
- jobs / taskValues
- notebooks (orquestación)

"""

# ============================
# 1. SECRETS (KEY VAULT)
# ============================

def secrets_examples():
    """
    🔐 dbutils.secrets

    Casos de uso:
    - Obtener credenciales seguras
    - Evitar hardcodear passwords

    Requiere:
    - Scope configurado en Databricks (Key Vault o secret scope)
    """

    # Obtener secreto
    password = dbutils.secrets.get(
        scope="my-scope",
        key="db-password"
    )

    print("Secret obtenido correctamente (no imprimir en producción)")

    return password


# ============================
# 2. WIDGETS (PARÁMETROS)
# ============================

def widgets_examples():
    """
    🎛️ dbutils.widgets

    Casos de uso:
    - Parametrizar notebooks
    - Pasar variables desde jobs

    Muy usado en pipelines productivos
    """

    # Crear widget
    dbutils.widgets.text("start_date", "2025-01-01")

    # Leer valor
    start_date = dbutils.widgets.get("start_date")

    print(f"Start date: {start_date}")

    return start_date


# ============================
# 3. FILESYSTEM (DBFS)
# ============================

def filesystem_examples():
    """
    📁 dbutils.fs

    Casos de uso:
    - Gestionar ficheros en DBFS / ADLS montado
    """

    # Listar archivos
    files = dbutils.fs.ls("/mnt/data")

    # Copiar archivo
    dbutils.fs.cp("/mnt/source/file.csv", "/mnt/dest/file.csv")

    # Borrar archivo
    dbutils.fs.rm("/mnt/data/file.csv", recurse=True)

    return files


# ============================
# 4. NOTEBOOKS (ORQUESTACIÓN)
# ============================

def notebook_examples():
    """
    📓 dbutils.notebook

    Casos de uso:
    - Llamar notebooks desde otros notebooks
    - Orquestación simple (tipo mini Airflow)

    """

    # Ejecutar otro notebook
    result = dbutils.notebook.run(
        "/path/to/notebook",
        timeout_seconds=3600,
        arguments={"param1": "value1"}
    )

    print(f"Resultado: {result}")

    # Salir de notebook actual
    dbutils.notebook.exit("OK")


# ============================
# 5. JOBS / TASK VALUES
# ============================

def jobs_examples():
    """
    🔁 dbutils.jobs.taskValues

    Casos de uso:
    - Pasar valores entre tasks de un job
    - Comunicación entre etapas del pipeline
    """

    # Guardar valor
    dbutils.jobs.taskValues.set(
        key="output_path",
        value="/mnt/data/output"
    )

    # Leer valor
    value = dbutils.jobs.taskValues.get(
        taskKey="previous_task",
        key="output_path"
    )

    print(value)

    return value


# ============================
# 6. CONTROL DE EJECUCIÓN (PATRÓN REAL)
# ============================

def execution_pattern():
    """
    🧠 PATRÓN REAL DE USO EN PRODUCCIÓN

    Combina:
    - widgets
    - secrets
    - logging
    """

    # Obtener entorno
    try:
        env = dbutils.widgets.get("env")
    except:
        env = "pre"

    # Obtener secret
    password = dbutils.secrets.get(
        scope=f"kv-{env}",
        key="db-password"
    )

    # Parámetros de ejecución
    start_date = dbutils.widgets.get("start_date")
    end_date = dbutils.widgets.get("end_date")

    print(f"Running in {env} from {start_date} to {end_date}")

    return env


# ============================
# 7. BUENAS PRÁCTICAS
# ============================

"""
🔥 BEST PRACTICES

1. ❌ NUNCA hardcodear secretos
   ✔️ Siempre usar dbutils.secrets

2. ❌ No abusar de notebooks como scripts gigantes
   ✔️ Modularizar lógica en utils/

3. ❌ No usar widgets sin control
   ✔️ Validar siempre valores

4. ❌ No usar dbutils.fs en grandes volúmenes
   ✔️ Usar Spark para data pesada

5. ❌ No imprimir secretos
   ✔️ Solo usarlos en memoria

6. ✔️ Usar dbutils.jobs.taskValues para pipelines complejos

7. ✔️ Usar dbutils.notebook.run solo para orquestación simple
   (para algo más complejo → Jobs o frameworks)
"""


# ============================
# FIN
# ============================

"""
dbutils es el pegamento de Databricks:

- secrets → seguridad
- widgets → parametrización
- notebook → orquestación
- jobs → comunicación entre tasks
- fs → gestión de ficheros

Dominar esto = trabajar bien en Databricks real
"""
