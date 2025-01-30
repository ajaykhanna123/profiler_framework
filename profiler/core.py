import tracemalloc
import psutil
import os
import time
import json
from functools import wraps
import asyncio

class Profiler:
    def __init__(self, log_file="profiler_log.json"):
        self.function_data = []
        self.log_file = log_file

    def track_performance(self, func):
        """Decorator to track memory and CPU consumption of a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            start_time = time.time()
            start_cpu = psutil.cpu_percent(interval=None)
            current, peak = tracemalloc.get_traced_memory()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_cpu = psutil.cpu_percent(interval=None)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            self.function_data.append({
                'function': func.__name__,
                'current_memory': current,
                'peak_memory': peak,
                'cpu_usage': end_cpu - start_cpu,
                'execution_time': end_time - start_time,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.save_logs()
            return result
        return wrapper

    def track_performance_async(self, func):
        """Decorator to track memory and CPU consumption of an async function."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracemalloc.start()
            start_time = time.time()
            start_cpu = psutil.cpu_percent(interval=None)
            current, peak = tracemalloc.get_traced_memory()
            
            result = await func(*args, **kwargs)
            
            end_time = time.time()
            end_cpu = psutil.cpu_percent(interval=None)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            self.function_data.append({
                'function': func.__name__,
                'current_memory': current,
                'peak_memory': peak,
                'cpu_usage': end_cpu - start_cpu,
                'execution_time': end_time - start_time,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.save_logs()
            return result
        return wrapper

    def get_function_data(self):
        return self.function_data

    def save_logs(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.function_data, f, indent=4)
