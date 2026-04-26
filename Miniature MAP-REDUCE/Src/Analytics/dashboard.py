import sys
import os

# ✅ Fix import path (critical for Streamlit)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import streamlit as st
import json
import subprocess
import time

from config.paths import METRICS_FILE

st.set_page_config(page_title="Query Engine Dashboard", layout="wide")

st.title("📊 MapReduce vs SQL Server Dashboard")

# ---------------- RUN ENGINE BUTTON ----------------
if st.button("🚀 Run Query Engine"):
    with st.spinner("Running engine... this may take a moment ⏳"):

        # ✅ Ensure main.py runs from correct directory
        subprocess.run(
            ["python", "main.py"],
            cwd=BASE_DIR   # 🔥 THIS FIXES MANY HIDDEN ISSUES
        )

        time.sleep(1)

    st.success("Execution completed. Data refreshed.")

# ---------------- LOAD METRICS ----------------
if not os.path.exists(METRICS_FILE):
    st.warning("No metrics found yet.")
    st.info("Click '🚀 Run Query Engine' to generate results.")
    st.stop()

with open(METRICS_FILE, "r") as f:
    data = json.load(f)

# ---------------- SYSTEM INFO ----------------
st.header("🖥️ System Information")
st.json(data.get("system_info", {}))

# ---------------- EXECUTION CONFIG ----------------
st.header("⚙️ Execution Configuration")
st.json(data.get("execution_config", {}))

# ---------------- ENGINE PERFORMANCE ----------------
st.header("🚀 Engine Performance")

engine_metrics = data.get("engine_metrics", {})

if engine_metrics:

    engines = list(engine_metrics.keys())
    times = [engine_metrics[e]["time_sec"] for e in engines]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Execution Time (seconds)")
        chart_data = {engines[i]: times[i] for i in range(len(engines))}
        st.bar_chart(chart_data)

    with col2:
        st.subheader("Raw Metrics")
        st.json(engine_metrics)

else:
    st.warning("No engine metrics available.")

# ---------------- SUMMARY ----------------
st.header("📈 Summary")
st.json(data.get("summary", {}))