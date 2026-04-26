class SQLTranslator:

    @staticmethod
    def to_sql_server(query_str: str) -> str:
        """
        Converts logical query → SQL Server compatible query
        """
        return query_str.replace("FROM data", "FROM reviews")