# Memory Profiler and Visualizer

## Overview
This application provides a memory and performance profiling tool for Python functions. It captures CPU usage, memory consumption, and execution time, then generates reports and visualizations. Additionally, it can upload reports to Azure Storage.

## Features
- Decorators for profiling synchronous and asynchronous functions.
- JSON-based data logging.
- Visualizations for function execution over time.
- Azure Storage integration for storing reports.

## Installation
```sh
pip install -r requirements.txt
```

## Usage

### 1. Profiling Functions
To track memory and performance, use the `@track_memory` or `@track_memory_async` decorator.

#### Synchronous Function
```python
from core import Profiler

profiler = Profiler()

@profiler.track_memory
def example_function():
    x = [i ** 2 for i in range(100000)]
    return sum(x)

example_function()
```

#### Asynchronous Function
```python
@profiler.track_memory_async
async def async_example_function():
    await asyncio.sleep(1)
    return "Completed"

asyncio.run(async_example_function())
```

### 2. Generating Reports
The reports are saved as JSON files in the `reports/JsonData` directory. To finalize and visualize the data:
```python
profiler.finalize()
```

### 3. Uploading Reports to Azure
Ensure you have an Azure Storage connection string and container ready.

```python
from storage import AzureStorage

connection_string = "<your_connection_string>"
container_name = "profiling-reports"
file_path = "reports/JsonData/profiler_log.json"

storage = AzureStorage(connection_string)
storage.upload_report(container_name, file_path)
```

## Integration with Azure Timer Trigger Function
To integrate profiling with an Azure application, use an Azure Timer Trigger function to execute profiling at scheduled intervals and upload reports.

### Timer Trigger Function (Azure Functions)

```python
import azure.functions as func
import datetime
from core import Profiler
from storage import AzureStorage
import os

connection_string = "<your_connection_string>"
container_name = "profiling-reports"

profiler = Profiler()

def main(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        print("The timer is past due!")
    
    # Run profiling for a sample function
    @profiler.track_memory
    def sample_task():
        x = [i ** 2 for i in range(1000000)]
        return sum(x)
    
    sample_task()
    
    # Finalize profiling and generate reports
    profiler.finalize()
    
    # Upload reports to Azure
    storage = AzureStorage(connection_string)
    report_dir = "reports/JsonData"
    for file_name in os.listdir(report_dir):
        file_path = os.path.join(report_dir, file_name)
        storage.upload_report(container_name, file_path)

    print("Profiling completed and reports uploaded.")
```

## Conclusion
This application helps track memory and performance in Python applications and integrates seamlessly with Azure for automated profiling and reporting. Modify the timer function for your needs and scale accordingly.

