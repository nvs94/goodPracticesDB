# ingestion_framework/sources/api_source.py

import requests

class APIIngestion:

    def __init__(self, base_url, auth=None, logger=None):
        self.base_url = base_url
        self.auth = auth
        self.logger = logger

    def fetch_dataframe(self, spark, endpoint="/data", params=None):

        if self.logger:
            self.logger.info(f"API#Calling {endpoint}")

        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()

        data = response.json().get("data", [])

        return spark.createDataFrame(data)
