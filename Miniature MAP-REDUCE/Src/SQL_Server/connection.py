import pyodbc
from config import db_config


class SQLServerConnection:

    def __init__(self):
        self.conn = None

    def connect(self):
        conn_str = (
            f"Driver={{{db_config.DRIVER}}};"
            f"Server={db_config.SERVER};"
            f"Database={db_config.DATABASE};"
            f"Trusted_Connection={db_config.TRUSTED_CONNECTION};"
        )
        self.conn = pyodbc.connect(conn_str)
        return self.conn

    def cursor(self):
        if not self.conn:
            self.connect()
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()