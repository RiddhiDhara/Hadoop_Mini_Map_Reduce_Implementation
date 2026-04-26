import pandas as pd


class SQLServerLoader:

    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        cursor = self.connection.cursor()

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='reviews' AND xtype='U')
        CREATE TABLE reviews (
            ProductId VARCHAR(50),
            UserId VARCHAR(50),
            HelpfulnessNumerator INT,
            HelpfulnessDenominator INT,
            Score INT,
            Time DATE
        )
        """)

        self.connection.conn.commit()

    def load_csv(self, csv_path, batch_size=50000):

        print("[LOADER] Reading CSV...")
        df = pd.read_csv(csv_path)

        print(f"[LOADER] Total rows: {len(df)}")

        cursor = self.connection.cursor()
        cursor.fast_executemany = True  # 🔥 critical for speed

        insert_query = """
            INSERT INTO reviews (
                ProductId,
                UserId,
                HelpfulnessNumerator,
                HelpfulnessDenominator,
                Score,
                Time
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        # Convert DataFrame → list of tuples
        data = [
            (
                row["ProductId"],
                row["UserId"],
                int(row["HelpfulnessNumerator"]),
                int(row["HelpfulnessDenominator"]),
                int(row["Score"]),
                row["Time"]
            )
            for _, row in df.iterrows()
        ]

        print("[LOADER] Starting batch insert...")

        # Batch insertion
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            cursor.executemany(insert_query, batch)

            print(f"[LOADER] Inserted rows: {i + len(batch)} / {len(data)}")

        self.connection.conn.commit()

        print("[LOADER] Data load complete 🚀")