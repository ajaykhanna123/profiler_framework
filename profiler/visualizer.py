import seaborn as sns
import matplotlib.pyplot as plt
import psutil
import os

def visualize_usage(function_data):
    """Visualize memory and CPU usage."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    cpu_usage = process.cpu_percent(interval=1)

    fig, ax = plt.subplots(2, 1, figsize=(12, 8))

    # Memory Usage Visualization
    memory_data = [memory_info.rss / (1024 ** 2), memory_info.vms / (1024 ** 2)]
    memory_labels = ['RSS (MB)', 'VMS (MB)']
    sns.barplot(x=memory_labels, y=memory_data, ax=ax[0])
    ax[0].set_title("Memory Usage")
    ax[0].set_ylabel("Memory (MB)")

    # CPU Usage Visualization
    ax[1].bar(['CPU Usage'], [cpu_usage])
    ax[1].set_title("CPU Usage")
    ax[1].set_ylabel("Percentage")

    plt.tight_layout()
    plt.show()

def highlight_heaviest_function(function_data):
    if not function_data:
        print("No function data recorded.")
        return

    heaviest_function = max(function_data, key=lambda x: x['peak_memory'])
    print("Heaviest Function:")
    print(f"Function: {heaviest_function['function']}")
    print(f"Peak Memory: {heaviest_function['peak_memory'] / (1024 ** 2):.2f} MB")
    print(f"Execution Time: {heaviest_function['execution_time']:.2f} seconds")
