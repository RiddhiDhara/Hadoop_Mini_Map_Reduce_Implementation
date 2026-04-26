import platform
import psutil
from datetime import datetime


class MetricsCollector:

    def __init__(self):
        self.metrics = {}
        self.system_info = self._get_system_info()
        self.execution_config = {}

    # ---------------- SYSTEM INFO ----------------
    def _get_system_info(self):
        return {
            "os": platform.system() + " " + platform.release(),
            "processor": platform.processor(),
            "cpu_cores_physical": psutil.cpu_count(logical=False),
            "cpu_cores_logical": psutil.cpu_count(logical=True),
            "total_ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "python_version": platform.python_version(),
        }

    # ---------------- EXECUTION CONFIG ----------------
    def set_execution_config(self, partitions, reducers, threads):
        self.execution_config = {
            "num_partitions": partitions,
            "num_reducers": reducers,
            "num_threads": threads,
        }

    # ---------------- ENGINE METRICS ----------------
    def add(self, engine_name, execution_time, rows=None):
        self.metrics[engine_name] = {
            "time_sec": round(execution_time, 4),
            "rows_processed": rows,
        }

    # ---------------- SUMMARY ----------------
    def compute_summary(self):
        summary = {}

        mr = self.metrics.get("MapReduce")
        sql = self.metrics.get("SQL Server")

        if mr and sql:
            if sql["time_sec"] > 0:
                summary["speedup (MR / SQL)"] = round(
                    mr["time_sec"] / sql["time_sec"], 2
                )

        return summary

    # ---------------- FINAL REPORT ----------------
    def get_full_report(self):
        return {
            "timestamp": str(datetime.now()),
            "system_info": self.system_info,
            "execution_config": self.execution_config,
            "engine_metrics": self.metrics,
            "summary": self.compute_summary(),
        }