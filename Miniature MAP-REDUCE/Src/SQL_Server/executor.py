from SQL_Server.metrics import Metrics


class SQLServerExecutor:

    def __init__(self, connection):
        self.connection = connection
        self.metrics = Metrics()

    def execute(self, query):

        cursor = self.connection.cursor()

        self.metrics.start()

        cursor.execute(query)
        rows = cursor.fetchall()

        self.connection.conn.commit()

        metrics = self.metrics.stop()

        return {
            "rows": rows,
            "metrics": metrics
        }