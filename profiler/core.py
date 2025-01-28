import tracemalloc
import psutil
import os
import time
from functools import wraps
import asyncio

class Profiler:
    def __init__(self):
        self.function_data = []

    def track_memory(self, func):
        """Decorator to track memory consumption of a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            start_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            result = func(*args, **kwargs)
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.function_data.append({
                'function': func.__name__,
                'current_memory': current,
                'peak_memory': peak,
                'execution_time': end_time - start_time
            })
            return result
        return wrapper

    def track_memory_async(self, func):
        """Decorator to track memory consumption of an async function."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracemalloc.start()
            start_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            result = await func(*args, **kwargs)
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.function_data.append({
                'function': func.__name__,
                'current_memory': current,
                'peak_memory': peak,
                'execution_time': end_time - start_time
            })
            return result
        return wrapper

    def get_function_data(self):
        return self.function_data
