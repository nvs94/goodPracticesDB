# ingestion_framework/sources/excel_source.py
com.crealytics:spark-excel_2.12:3.5.0
class ExcelIngestion:

    def __init__(
        self,
        path: str,
        sheet_name="Sheet1",
        header=True,
        infer_schema=True,
        logger=None
    ):
        self.path = path
        self.sheet_name = sheet_name
        self.header = header
        self.infer_schema = infer_schema
        self.logger = logger

    def fetch_dataframe(self, spark):

        if self.logger:
            self.logger.info(f"EXCEL#Reading: {self.path}")

        df = (
            spark.read.format("com.crealytics.spark.excel")
            .option("header", str(self.header).lower())
            .option("inferSchema", str(self.infer_schema).lower())
            .option("dataAddress", f"'{self.sheet_name}'!A1")
            .load(self.path)
        )

        return df
''' -------------- EXAMPLE ---------------
from ingestion_framework.sources.excel_source import ExcelIngestion

excel_source = ExcelIngestion(
    base_path="/dbfs/mnt/data/excel/",
    sheet_name="Sheet1",
    header=1,
    columns=["id", "amount"]
)

excel_data = excel_source.fetch_records()
'''
