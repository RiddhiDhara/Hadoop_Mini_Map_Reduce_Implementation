import time
import psutil


class Metrics:

    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        end_time = time.time()

        return {
            "execution_time_sec": round(end_time - self.start_time, 4),
            "cpu_usage": psutil.cpu_percent(interval=None)
        }