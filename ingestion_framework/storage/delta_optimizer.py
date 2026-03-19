from delta.tables import DeltaTable

class DeltaOptimizer:
    """
    Utility class for Delta Lake optimization operations.
    """

    def __init__(self, spark, path):
        self.spark = spark
        self.path = path
        self.delta_table = DeltaTable.forPath(spark, path)

    def compact(self):
        """
        Compact small files into larger ones.
        """
        self.delta_table.optimize().executeCompaction()

    def zorder(self, columns):
        """
        Apply Z-Ordering for query performance.
        """
        if isinstance(columns, str):
            columns = [columns]

        self.delta_table.optimize().executeZOrderBy(columns)

    def vacuum(self, retention_hours=168):
        """
        Clean old versions of data.
        """
        self.delta_table.vacuum(retentionHours=retention_hours)

    def enable_auto_optimize(self):
        """
        Enable Databricks auto optimization configs.
        """
        self.spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
        self.spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
