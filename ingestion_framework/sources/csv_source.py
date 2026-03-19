# ingestion_framework/sources/csv_source.py

from pyspark.sql import DataFrame

class CSVIngestion:

    def __init__(
        self,
        path: str,
        delimiter: str = ",",
        header: bool = True,
        infer_schema: bool = True,
        schema=None,
        logger=None
    ):
        self.path = path
        self.delimiter = delimiter
        self.header = header
        self.infer_schema = infer_schema
        self.schema = schema
        self.logger = logger

    def fetch_dataframe(self, spark, last_processed=None) -> DataFrame:

        if self.logger:
            self.logger.info(f"CSV#Reading path: {self.path}")

        reader = (
            spark.read.format("csv")
            .option("sep", self.delimiter)
            .option("header", str(self.header).lower())
        )

        if self.schema:
            df = reader.schema(self.schema).load(self.path)
        else:
            df = reader.option("inferSchema", str(self.infer_schema).lower()).load(self.path)

        return df

''' -------------- EXAMPLE ---------------
from ingestion_framework.sources.csv_source import CSVIngestion

csv_source = CSVIngestion(
    base_path="/dbfs/mnt/data/csv/",
    delimiter=";",
    encoding="latin-1",
    header=0,
    columns=["id", "name", "value"]
)


csv_data = csv_source.fetch_records()
'''
