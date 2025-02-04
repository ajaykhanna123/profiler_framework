import tracemalloc
import psutil
import os
import time
import json
import inspect
from functools import wraps
import asyncio
from collections import defaultdict
from datetime import datetime, timezone
import platform
from typing import Any, Dict, List, Union
import logging
from .visualizer import Visualizer

logger = logging.getLogger(__name__)

class Profiler:
    def __init__(self, report_dir: str = None, auto_finalize: bool = True):
        # Initialize system info first
        self.python_version = platform.python_version()
        self.system_info = self._get_system_info()
        
        # Set up report directories
        self.report_dir = report_dir or os.path.join(os.getcwd(), "reports")
        self.json_data_dir = os.path.join(self.report_dir, "JsonData")
        os.makedirs(self.json_data_dir, exist_ok=True)
        
        # File paths
        self.log_file = os.path.join(self.json_data_dir, "profiler_log.json")
        self.time_series_file = os.path.join(self.json_data_dir, "profiler_time_series.json")
        
        # Data storage
        self.function_data: List[Dict[str, Any]] = []
        self.time_series_data = defaultdict(list)
        self.load_existing_data()
        
        # Automatic finalization
        self.auto_finalize = auto_finalize
        self._finalized = False

    def __enter__(self):
        """Context manager entry point"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point - handles automatic finalization"""
        if self.auto_finalize and not self._finalized:
            self.finalize()
        return False

    def _get_system_info(self) -> Dict[str, Union[str, float, int]]:
        """Collect system hardware and OS information"""
        try:
            cpu_freq = psutil.cpu_freq()
            return {
                "os": f"{platform.system()} {platform.release()}",
                "architecture": platform.machine(),
                "total_ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 1),
                "cpu_cores_physical": psutil.cpu_count(logical=False),
                "cpu_cores_logical": psutil.cpu_count(logical=True),
                "cpu_max_freq": cpu_freq.max if cpu_freq else None,
                "python_version": self.python_version,
            }
        except Exception as e:
            logger.error(f"Failed to collect system info: {str(e)}")
            return {}

    def load_existing_data(self) -> None:
        """Load existing profiling data from JSON files"""
        for file_path, target in [
            (self.log_file, self.function_data),
            (self.time_series_file, self.time_series_data)
        ]:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            target.extend(data)
                        else:
                            self.time_series_data.update(data)
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Error loading {file_path}: {str(e)}")

    def save_profiling_data(self) -> None:
        """Save data to JSON files with atomic writes"""
        try:
            # Save function log data
            temp_log = f"{self.log_file}.tmp"
            with open(temp_log, "w") as f:
                json.dump(self.function_data, f, indent=4, default=str)
            os.replace(temp_log, self.log_file)
            
            # Save time series data
            temp_ts = f"{self.time_series_file}.tmp"
            with open(temp_ts, "w") as f:
                json.dump(dict(self.time_series_data), f, indent=4, default=str)
            os.replace(temp_ts, self.time_series_file)
            
        except Exception as e:
            logger.error(f"Failed to save profiling data: {str(e)}")

    def _get_filename(self, func: Any) -> str:
        """Resolve source filename for the decorated function"""
        try:
            module = inspect.getmodule(func)
            if module and hasattr(module, '__file__'):
                return os.path.basename(module.__file__)
            
            # Fallback to stack inspection
            stack = inspect.stack()
            for frame in stack:
                filename = os.path.basename(frame.filename)
                if filename not in {"core.py", "__init__.py"}:
                    return filename
            return "unknown_file.py"
        except Exception as e:
            logger.warning(f"Filename resolution failed: {str(e)}")
            return "unknown_file.py"

    def _create_profiling_entry(self, filename: str, func: Any,
                              start_time: float, end_time: float) -> Dict[str, Any]:
        """Create a complete profiling entry with resource metrics"""
        try:
            current, peak = tracemalloc.get_traced_memory()
            return {
                "file": filename,
                "function": func.__name__,
                "current_memory_mb": round(current / (1024 ** 2), 3),
                "peak_memory_mb": round(peak / (1024 ** 2), 3),
                "cpu_usage": round(psutil.cpu_percent(interval=0.1), 3),
                "execution_time": round(end_time - start_time, 3),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "system_info": self.system_info,
            }
        except Exception as e:
            logger.error(f"Failed to create profiling entry: {str(e)}")
            return {}

    def track_memory(self, func: Any) -> Any:
        """Decorator to track resource usage for synchronous functions"""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            filename = self._get_filename(func)
            func_key = f"{filename}:{func.__name__}"
            start_time = time.time()
            
            tracemalloc.start()
            try:
                result = func(*args, **kwargs)
            finally:
                end_time = time.time()
                entry = self._create_profiling_entry(filename, func, start_time, end_time)
                if entry:
                    self.function_data.append(entry)
                    self.time_series_data[func_key].append(entry)
                    self.save_profiling_data()
                tracemalloc.stop()
            
            return result
        return wrapper

    def track_memory_async(self, func: Any) -> Any:
        """Decorator to track resource usage for asynchronous functions"""
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            filename = self._get_filename(func)
            func_key = f"{filename}:{func.__name__}"
            start_time = time.time()
            
            tracemalloc.start()
            try:
                result = await func(*args, **kwargs)
            finally:
                end_time = time.time()
                entry = self._create_profiling_entry(filename, func, start_time, end_time)
                if entry:
                    self.function_data.append(entry)
                    self.time_series_data[func_key].append(entry)
                    self.save_profiling_data()
                tracemalloc.stop()
            
            return result
        return wrapper

    def finalize(self) -> None:
        """Finalize profiling and generate visual reports"""
        if self._finalized:
            return
            
        try:
            self.save_profiling_data()
            visualizer = Visualizer(report_dir=self.report_dir)
            visualizer.visualize_usage()
            visualizer.visualize_over_time()
            logger.info(f"Reports generated successfully at: {self.report_dir}")
            self._finalized = True
        except Exception as e:
            logger.error(f"Failed to generate reports: {str(e)}")
            raise

    def get_function_data(self) -> List[Dict[str, Any]]:
        """Get aggregated profiling data"""
        return self.function_data

    def get_time_series_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get time-series profiling data"""
        return dict(self.time_series_data)