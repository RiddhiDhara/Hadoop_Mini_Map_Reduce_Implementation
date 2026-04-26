from Utils.file_utils import load_csv
from Parser.sql_parser import parse_query
from Execution_Engine.context import ExecutionContext
from Execution_Engine.engine import ExecutionEngine
from Optimizer.optimizer import build_logical_plan

from SQL_Server.connection import SQLServerConnection
from SQL_Server.executor import SQLServerExecutor
from SQL_Server.adapter import SQLAdapter
from SQL_Server.translator import SQLTranslator

from Analytics.metrics import MetricsCollector
from Analytics.report import ReportGenerator

# ✅ CONFIG IMPORTS
from config.paths import CSV_PATH, SQL_QUERY_PATH, REPORT_FILE
from config.settings import (
    NUM_PARTITIONS,
    NUM_REDUCERS,
    NUM_THREADS,
    ENABLE_SQL_SERVER,
    ENABLE_MAPREDUCE
)

import time


def main():

    # ---------------- READ SQL ----------------
    with open(SQL_QUERY_PATH, "r") as f:
        query_str = f.read().strip()

    query = parse_query(query_str)

    # ---------------- LOAD DATA ----------------
    data = load_csv(CSV_PATH)

    # ---------------- CONTEXT ----------------
    context = ExecutionContext(
        num_partitions=NUM_PARTITIONS,
        num_reducers=NUM_REDUCERS
    )

    plan = build_logical_plan(query)

    final_result = {}
    sql_result = {}
    sql_metrics = {}

    mr_time = 0
    sql_time = 0

    # ================= MAPREDUCE =================
    if ENABLE_MAPREDUCE:
        start_mr = time.time()

        engine = ExecutionEngine(context)
        partial_results = engine.execute(data, query)

        for reducer_output in partial_results:
            for key, value in reducer_output.items():
                final_result[key] = value

        end_mr = time.time()
        mr_time = round(end_mr - start_mr, 4)

    # ================= SQL SERVER =================
    if ENABLE_SQL_SERVER:
        conn = SQLServerConnection()
        conn.connect()

        sql_executor = SQLServerExecutor(conn)
        sql_query = SQLTranslator.to_sql_server(query_str)

        start_sql = time.time()
        sql_output = sql_executor.execute(sql_query)
        end_sql = time.time()

        sql_time = round(end_sql - start_sql, 4)

        sql_rows = sql_output["rows"]
        sql_metrics = sql_output["metrics"]

        sql_result = SQLAdapter.format(sql_rows)

        conn.close()

    # ================= OUTPUT =================
    aggregations = query["select"]["aggregations"]
    headers = ["Score"] + [agg["func"] for agg in aggregations]

    if ENABLE_MAPREDUCE:
        print("\n================ MAPREDUCE RESULT ================\n")
        print("  ".join(f"{h:<12}" for h in headers))
        print("-" * (14 * len(headers)))

        for key in sorted(final_result.keys()):
            row = [str(key)]

            for agg in aggregations:
                func = agg["func"]
                value = final_result[key].get(func, 0)

                if isinstance(value, float):
                    value = round(value, 4)

                row.append(str(value))

            print("  ".join(f"{r:<12}" for r in row))

    if ENABLE_SQL_SERVER:
        print("\n================ SQL SERVER RESULT ================\n")
        print("  ".join(f"{h:<12}" for h in headers))
        print("-" * (14 * len(headers)))

        for key in sorted(sql_result.keys()):
            row = [str(key)]

            for value in sql_result[key]:
                if isinstance(value, float):
                    value = round(value, 4)

                row.append(str(value))

            print("  ".join(f"{r:<12}" for r in row))

    # ================= METRICS =================
    metrics = MetricsCollector()

    metrics.set_execution_config(
        partitions=NUM_PARTITIONS,
        reducers=NUM_REDUCERS,
        threads=NUM_THREADS
    )

    if ENABLE_MAPREDUCE:
        metrics.add("MapReduce", mr_time, rows=len(final_result))

    if ENABLE_SQL_SERVER:
        metrics.add("SQL Server", sql_time, rows=len(sql_result))

        if sql_metrics:
            metrics.metrics["SQL Server"]["details"] = sql_metrics

    full_report = metrics.get_full_report()

    # ✅ save using config path
    ReportGenerator.generate(full_report, file_path=REPORT_FILE)

    print("\n✔ Execution Completed. Check Results/ folder.")


if __name__ == "__main__":
    main()