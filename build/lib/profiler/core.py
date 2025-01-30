import tracemalloc
import psutil
import json
import os
import time
from functools import wraps
import asyncio

class Profiler:
    def __init__(self, log_file="profiler_log.json"):
        self.log_file = log_file
        self.function_data = self._load_existing_data()

    def _load_existing_data(self):
        """Load existing data from log file so multiple runs accumulate results."""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def _save_data(self):
        """Save function profiling data to a log file without overwriting previous runs."""
        with open(self.log_file, "w") as f:
            json.dump(self.function_data, f, indent=4)

    def track_performance(self, func):
        """Decorator to track memory, CPU, and execution time."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            process = psutil.Process(os.getpid())
            start_time = time.time()

            # Initial memory and CPU stats
            initial_cpu = process.cpu_percent(interval=None)

            result = func(*args, **kwargs)

            # Capture execution metrics
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            final_cpu = process.cpu_percent(interval=None)
            tracemalloc.stop()

            # Convert memory to MB (3 decimal places)
            current_memory_mb = round(current / (1024 ** 2), 3)
            peak_memory_mb = round(peak / (1024 ** 2), 3)
            execution_time = round(end_time - start_time, 3)
            cpu_usage = round(final_cpu, 3)

            data = {
                'function': func.__name__,
                'file': func.__module__,
                'current_memory_mb': current_memory_mb,
                'peak_memory_mb': peak_memory_mb,
                'cpu_usage': cpu_usage,
                'execution_time': execution_time
            }

            self.function_data.append(data)
            self._save_data()

            return result
        return wrapper
