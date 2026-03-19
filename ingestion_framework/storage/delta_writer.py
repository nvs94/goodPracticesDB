from delta.tables import DeltaTable

class DeltaWriter:

    def __init__(self, spark, path):
        self.spark = spark
        self.path = path

    def write_append(self, df):
        df.write.format("delta").mode("append").save(self.path)

    def write_overwrite(self, df):
        df.write.format("delta").mode("overwrite").save(self.path)

    def write_overwrite_partition(self, df, condition):
        df.write.format("delta") \
            .mode("overwrite") \
            .option("replaceWhere", condition) \
            .save(self.path)

    def upsert(self, df, merge_condition):
        delta_table = DeltaTable.forPath(self.spark, self.path)

        (
            delta_table.alias("target")
            .merge(df.alias("source"), merge_condition)
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )

    def delete(self, condition):
        delta_table = DeltaTable.forPath(self.spark, self.path)
        delta_table.delete(condition)

    def update(self, condition, set_dict):
        delta_table = DeltaTable.forPath(self.spark, self.path)
        delta_table.update(condition, set=set_dict)
