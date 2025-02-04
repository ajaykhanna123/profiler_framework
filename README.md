# Profiler Framework
A Python framework for tracking and visualizing memory and CPU usage in synchronous and asynchronous functions.
## Features
- Memory tracking for synchronous and asynchronous functions.
- Visualization of memory and CPU usage.
- Identification of the heaviest functions in terms of memory consumption.

## Installation
```bash
pip install profiler-framework
```

## Usage
```python
from profiler.core import Profiler
from profiler.visualizer import visualize_usage, highlight_heaviest_function

profiler = Profiler()

@profiler.track_memory
def example_function():
    a = [i for i in range(100000)]
    return sum(a)

example_function()
visualize_usage(profiler.get_function_data())
highlight_heaviest_function(profiler.get_function_data())
```
# Project Structure
```
├── profiler_framework
│   ├── profiler
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── visualizer.py
│   │   ├── storage.py
│   │   └── tests
│   │       ├── __init__.py
│   │       └── test_core.py
│   ├── reports
│   │   ├── normal_execution
│   │   ├── over_time
│   ├── setup.py
│   ├── README.md
│   ├── requirements.txt
│   └── .gitignore

```
# Folder Structure
```
Reports/
│── JsonData/
│   ├── profiler_log.json
│   ├── profiler_time_series.json
│
│── Visualization/
│   ├── NormalExecution/
│   ├── OverTime/
│   │   ├── CPU/
│   │   │   ├── script1_function1_cpu_usage.png
│   │   │   ├── script2_function2_cpu_usage.png
│   │   ├── Memory/
│   │   │   ├── script1_function1_peak_memory.png
│   │   │   ├── script2_function2_peak_memory.png
│   │   ├── ExecutionTime/
│   │   │   ├── script1_function1_execution_time.png
│   │   │   ├── script2_function2_execution_time.png
```

# Current updates
```Now supports both sync and async functions
✔ All values formatted properly (MB & CPU in 3 decimal places)
✔ Timestamps included for tracking execution history
✔ JSON logs persist multiple executions instead of overwriting
✔ Supports multi-file function tracking (doesn't reset for each file)```