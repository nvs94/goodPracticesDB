"""
Este archivo recoge las funciones y patrones MÁS IMPORTANTES de PySpark
orientados a Data Engineering en entornos productivos (Databricks).

Cada bloque incluye:
- Qué hace
- Cuándo usarlo
- Ejemplo práctico

IMPORTANTE:
Esto no es una librería para importar, sino una guía ejecutable/documentación.
"""

# ============================
# IMPORTS BASE
# ============================

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable


# ============================
# 1. LECTURA DE DATOS
# ============================

def read_examples(spark: SparkSession):
    """
    📥 LECTURA DE DATOS EN PYSPARK

    Casos de uso:
    - Leer datos desde Data Lake (Parquet/Delta)
    - Leer CSV/Excel
    - Leer desde bases de datos (JDBC)

    NOTA: Parquet y Delta son formatos recomendados en producción
    """

    # Leer Parquet (rápido y optimizado)
    df_parquet = spark.read.parquet("/path/to/data")

    # Leer Delta (formato recomendado en Databricks)
    df_delta = spark.read.format("delta").load("/delta/table")

    # Leer CSV
    df_csv = (
        spark.read
        .option("header", True)
        .option("delimiter", ",")
        .csv("/path/file.csv")
    )

    # Leer desde SQL Server (JDBC)
    df_jdbc = (
        spark.read.format("jdbc")
        .option("url", "jdbc:sqlserver://host:1433;databaseName=db")
        .option("dbtable", "schema.table")
        .option("user", "user")
        .option("password", "password")
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
        .load()
    )

    return df_parquet


# ============================
# 2. TRANSFORMACIONES BÁSICAS
# ============================

def transformation_examples(df):
    """
    🧱 TRANSFORMACIONES BÁSICAS

    Casos de uso:
    - Limpieza de datos
    - Selección de columnas
    - Creación de nuevas columnas
    """

    df_transformed = (
        df
        # Filtrar registros
        .filter(F.col("status") == "active")

        # Crear nueva columna
        .withColumn("amount_eur", F.col("amount") * 0.85)

        # Seleccionar columnas
        .select("id", "amount_eur", "country")
    )

    return df_transformed


# ============================
# 3. JOINS
# ============================

def join_examples(df_left, df_right):
    """
    🔗 JOINS EN PYSPARK

    Casos de uso:
    - Enriquecer datos (lookup tables)
    - Integrar múltiples fuentes

    Tip PRO:
    - Usar broadcast() cuando una tabla es pequeña
    """

    # Join normal
    df_joined = df_left.join(
        df_right,
        on="id",
        how="left"
    )

    # Join optimizado con broadcast
    df_joined_broadcast = df_left.join(
        F.broadcast(df_right),
        on="id",
        how="left"
    )

    return df_joined_broadcast


# ============================
# 4. WINDOW FUNCTIONS
# ============================

def window_examples(df):
    """
    🪟 WINDOW FUNCTIONS

    Casos de uso:
    - Obtener último registro (CDC)
    - Deduplicación
    - Ranking

    Este patrón es CLAVE en pipelines incrementales
    """

    window_spec = Window.partitionBy("id").orderBy(F.col("timestamp").desc())

    df_latest = (
        df
        .withColumn("row_num", F.row_number().over(window_spec))
        .filter(F.col("row_num") == 1)
        .drop("row_num")
    )

    return df_latest


# ============================
# 5. AGGREGATIONS
# ============================

def aggregation_examples(df):
    """
    📊 AGREGACIONES

    Casos de uso:
    - KPIs
    - Reporting
    """

    df_agg = (
        df
        .groupBy("country")
        .agg(
            F.count("*").alias("num_records"),
            F.sum("amount").alias("total_amount")
        )
    )

    return df_agg


# ============================
# 6. REPARTITION / COALESCE
# ============================

def partition_examples(df):
    """
    🔄 CONTROL DE PARTICIONES

    Casos de uso:
    - Optimizar rendimiento
    - Controlar número de ficheros

    Diferencias:
    - repartition → shuffle (costoso pero redistribuye bien)
    - coalesce → reduce particiones sin shuffle
    """

    df_repartitioned = df.repartition(10, "country")
    df_coalesced = df.coalesce(2)

    return df_repartitioned


# ============================
# 7. COLUMN EXPRESSIONS
# ============================

def column_expression_examples(df):
    """
    🧩 EXPRESIONES DE COLUMNA

    Casos de uso:
    - Lógica condicional (CASE WHEN)
    """

    df = df.withColumn(
        "category",
        F.when(F.col("amount") > 100, "high")
         .when(F.col("amount") > 50, "medium")
         .otherwise("low")
    )

    return df


# ============================
# 8. UDF (User Defined Function)
# ============================

def udf_examples(df):
    """
    ⚠️ UDFs (usar con cuidado)

    Casos de uso:
    - Lógica personalizada no soportada por Spark

    Problema:
    - Pierde optimización (Catalyst)
    - Más lento

    👉 Usar solo si no hay alternativa
    """

    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType

    @udf(StringType())
    def normalize(text):
        return text.lower().strip() if text else None

    df = df.withColumn("normalized", normalize("name"))

    return df


# ============================
# 9. PANDAS UDF (OPTIMIZADO)
# ============================

def pandas_udf_examples(df):
    """
    ⚡ PANDAS UDF (vectorizado)

    Casos de uso:
    - Lógica compleja con mejor rendimiento que UDF normal
    """

    from pyspark.sql.functions import pandas_udf
    import pandas as pd

    @pandas_udf("double")
    def multiply_by_two(s: pd.Series) -> pd.Series:
        return s * 2

    df = df.withColumn("value2", multiply_by_two("value"))

    return df


# ============================
# 10. ESCRITURA DE DATOS
# ============================

def write_examples(df):
    """
    📤 ESCRITURA

    Casos de uso:
    - Guardar resultados en Data Lake
    """

    df.write \
        .format("delta") \
        .mode("append") \
        .save("/delta/output")


def write_partitioned(df):
    """
    📦 ESCRITURA PARTICIONADA

    Mejora:
    - Performance de lectura
    - Costes en queries
    """

    df.write \
        .partitionBy("country") \
        .format("delta") \
        .mode("append") \
        .save("/delta/output_partitioned")


# ============================
# 11. MERGE (UPSERT) — DELTA
# ============================

def merge_example(spark, df_updates):
    """
    🔁 UPSERT (MERGE)

    Casos de uso:
    - CDC (Change Data Capture)
    - Cargas incrementales

    Esto es CRÍTICO en pipelines enterprise
    """

    delta_table = DeltaTable.forPath(spark, "/delta/table")

    (
        delta_table.alias("target")
        .merge(
            df_updates.alias("source"),
            "target.id = source.id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )


# ============================
# 12. CACHE
# ============================

def cache_example(df):
    """
    🧠 CACHE

    Casos de uso:
    - Reutilizar DataFrame varias veces

    IMPORTANTE:
    - Siempre forzar acción (count, write, etc.)
    """

    df.cache()
    df.count()

    return df


# ============================
# 13. VALIDACIÓN
# ============================

def validation_example(df):
    """
    🚦 VALIDACIONES

    Casos de uso:
    - Evitar pipelines vacíos
    """

    if df.rdd.isEmpty():
        raise Exception("No data available")


# ============================
# FIN
# ============================

"""
Este archivo cubre el 90% de lo que necesitas en PySpark real.

Recomendación:
- Guárdalo en utils/
- Úsalo como referencia rápida en proyectos
"""
