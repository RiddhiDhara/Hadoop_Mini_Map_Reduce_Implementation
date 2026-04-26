from SQL_Server.connection import SQLServerConnection
from SQL_Server.loader import SQLServerLoader
import os


CSV_PATH = "Data/Processed Data/processed_data.csv"


def is_table_empty(cursor):
    cursor.execute("SELECT COUNT(*) FROM reviews")
    count = cursor.fetchone()[0]
    return count == 0


def main():

    print("\n[BOOTSTRAP] Initializing SQL Server setup...\n")

    conn = SQLServerConnection()
    conn.connect()

    loader = SQLServerLoader(conn)

    # Step 1: Create table
    loader.create_table()

    # Step 2: Check if data already loaded
    cursor = conn.cursor()

    try:
        if is_table_empty(cursor):
            print("[BOOTSTRAP] Table empty. Loading CSV into SQL Server...")
            loader.load_csv(CSV_PATH)
            print("[BOOTSTRAP] Data load complete.")
        else:
            print("[BOOTSTRAP] Data already exists. Skipping load.")

    except Exception as e:
        print("[BOOTSTRAP ERROR]", e)

    conn.close()

    print("\n[BOOTSTRAP] Setup complete. Ready to run main.py\n")


if __name__ == "__main__":
    main()