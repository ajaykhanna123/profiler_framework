import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json

def visualize_usage(log_file="profiler_log.json"):
    """Visualize memory and CPU usage trends."""
    with open(log_file, 'r') as f:
        function_data = json.load(f)
    
    if not function_data:
        print("No profiling data available.")
        return
    
    df = pd.DataFrame(function_data)
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    
    sns.barplot(x='function', y='peak_memory', data=df, ax=ax[0])
    ax[0].set_title("Peak Memory Usage per Function")
    ax[0].set_ylabel("Memory (Bytes)")
    
    sns.barplot(x='function', y='cpu_usage', data=df, ax=ax[1])
    ax[1].set_title("CPU Usage per Function")
    ax[1].set_ylabel("CPU (%)")
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def highlight_heaviest_function(log_file="profiler_log.json"):
    """Highlight the function that consumed the most memory and CPU."""
    with open(log_file, 'r') as f:
        function_data = json.load(f)
    
    if not function_data:
        print("No profiling data recorded.")
        return
    
    heaviest_memory = max(function_data, key=lambda x: x['peak_memory'])
    heaviest_cpu = max(function_data, key=lambda x: x['cpu_usage'])
    
    print("Heaviest Memory Function:")
    print(f"Function: {heaviest_memory['function']}, Peak Memory: {heaviest_memory['peak_memory']} bytes")
    print("\nHeaviest CPU Function:")
    print(f"Function: {heaviest_cpu['function']}, CPU Usage: {heaviest_cpu['cpu_usage']}%")

