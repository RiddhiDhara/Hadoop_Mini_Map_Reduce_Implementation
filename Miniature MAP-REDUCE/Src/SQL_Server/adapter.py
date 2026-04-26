class SQLAdapter:

    @staticmethod
    def format(rows):

        result = {}

        for row in rows:

            key = row[0]        # GROUP BY column
            values = row[1:]    # aggregations

            result[key] = values

        return result