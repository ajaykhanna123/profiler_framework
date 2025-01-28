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

├── profiler_framework
│   ├── profiler
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── visualizer.py
│   │   └── tests
│   │       ├── __init__.py
│   │       └── test_core.py
│   ├── setup.py
│   ├── README.md
│   ├── requirements.txt
│   └── .gitignore