import json
from config.paths import REPORT_FILE, METRICS_FILE


class ReportGenerator:

    @staticmethod
    def generate(report_data, file_path=REPORT_FILE):

        with open(file_path, "w") as f:

            f.write("=========== QUERY PERFORMANCE REPORT ===========\n\n")

            # ---------------- SYSTEM INFO ----------------
            f.write("SYSTEM INFORMATION\n")
            f.write("-----------------------------------------------\n")
            for k, v in report_data.get("system_info", {}).items():
                f.write(f"{k}: {v}\n")

            # ---------------- EXECUTION CONFIG ----------------
            f.write("\nEXECUTION CONFIG\n")
            f.write("-----------------------------------------------\n")
            for k, v in report_data.get("execution_config", {}).items():
                f.write(f"{k}: {v}\n")

            # ---------------- ENGINE METRICS ----------------
            f.write("\nENGINE METRICS\n")
            f.write("-----------------------------------------------\n")

            for engine, data in report_data.get("engine_metrics", {}).items():
                f.write(f"\n{engine}:\n")
                for k, v in data.items():
                    f.write(f"  {k}: {v}\n")

            # ---------------- SUMMARY ----------------
            f.write("\nSUMMARY\n")
            f.write("-----------------------------------------------\n")
            for k, v in report_data.get("summary", {}).items():
                f.write(f"{k}: {v}\n")

        # ---------------- JSON FOR DASHBOARD ----------------
        with open(METRICS_FILE, "w") as jf:
            json.dump(report_data, jf, indent=4)

        print(f"[REPORT] Generated → {file_path} & {METRICS_FILE}")