# ingestion_framework/sources/sql_source.py

class SQLIngestion:

    def __init__(
        self,
        jdbc_url,
        table=None,
        query=None,
        user=None,
        password=None,
        driver="com.microsoft.sqlserver.jdbc.SQLServerDriver",
        logger=None
    ):
        self.jdbc_url = jdbc_url
        self.table = table
        self.query = query
        self.user = user
        self.password = password
        self.driver = driver
        self.logger = logger

    def fetch_dataframe(self, spark, last_processed=None):

        if self.logger:
            self.logger.info("SQL#Reading data")

        reader = (
            spark.read.format("jdbc")
            .option("url", self.jdbc_url)
            .option("user", self.user)
            .option("password", self.password)
            .option("driver", self.driver)
        )

        if self.query:
            reader = reader.option("query", self.query)
        else:
            reader = reader.option("dbtable", self.table)

        df = reader.load()

        return df
