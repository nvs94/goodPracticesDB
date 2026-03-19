import pyodbc
from datetime import datetime

class SQLIngestion:

    def __init__(self, jdbc_url, query, user, password, logger=None):
        self.jdbc_url = jdbc_url
        self.query = query
        self.user = user
        self.password = password
        self.logger = logger

    def fetch_records(self, last_processed=None):
        conn = pyodbc.connect(self.jdbc_url, user=self.user, password=self.password)

        cursor = conn.cursor()

        if last_processed:
            cursor.execute(self.query, last_processed)
        else:
            cursor.execute(self.query.replace("WHERE updated_at > ?", ""))

        columns = [col[0] for col in cursor.description]

        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        return results
