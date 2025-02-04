import os
import json
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm
from pathvalidate import sanitize_filename
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class Visualizer:
    def __init__(self, report_dir: str = None, debug: bool = False):
        self.report_dir = report_dir or os.path.join(os.getcwd(), "reports")
        self.debug = debug
        self._setup_paths()
        self._configure_plot_style()
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
            pd.set_option("display.max_columns", None)

    def _setup_paths(self) -> None:
        """Initialize directory structure for outputs"""
        self.json_dir = os.path.join(self.report_dir, "JsonData")
        self.vis_dir = os.path.join(self.report_dir, "Visualization")
        self.normal_dir = os.path.join(self.vis_dir, "NormalExecution")
        self.overtime_dir = os.path.join(self.vis_dir, "OverTime")
        
        for path in [self.vis_dir, self.normal_dir, self.overtime_dir]:
            os.makedirs(path, exist_ok=True)

    def _configure_plot_style(self) -> None:
        """Set consistent visualization style"""
        plt.style.use("ggplot")
        sns.set_theme(
            style="whitegrid",
            palette="husl",
            font_scale=1.1,
            rc={
                "figure.figsize": (12, 6),
                "axes.titlesize": 14,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
                "grid.alpha": 0.3,
            }
        )

    def _load_data(self, filename: str) -> List[Dict[str, Any]]:
        """Safely load JSON data with error handling"""
        filepath = os.path.join(self.json_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    return json.load(f)
            return []
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error loading {filepath}: {str(e)}")
            return []

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare data for visualization"""
        numeric_cols = ["peak_memory_mb", "cpu_usage", "execution_time"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        return df.dropna(subset=numeric_cols + ["timestamp"])

    def visualize_usage(self) -> None:
        """Generate bar charts for latest execution metrics"""
        data = self._load_data("profiler_log.json")
        if not data:
            logger.info("No profiling data available for visualization")
            return

        df = self._clean_data(pd.DataFrame(data))
        if df.empty:
            return

        # Get latest entry per function
        df_latest = df.sort_values("timestamp").drop_duplicates("function", keep="last")
        
        metrics = {
            "peak_memory_mb": "Peak Memory Usage (MB)",
            "cpu_usage": "CPU Usage (%)",
            "execution_time": "Execution Time (seconds)"
        }

        for metric, title in metrics.items():
            plt.figure()
            ax = sns.barplot(x="function", y=metric, data=df_latest)
            ax.set_title(f"Latest {title} by Function")
            ax.set_xlabel("Function Name")
            ax.set_ylabel(title)
            plt.xticks(rotation=45, ha="right")
            
            filename = sanitize_filename(f"latest_{metric}.png", replacement_text="_")
            plt.savefig(os.path.join(self.normal_dir, filename), 
                       bbox_inches="tight", dpi=150)
            plt.close()

        logger.info(f"Saved normal execution reports to {self.normal_dir}")

    def visualize_over_time(self) -> None:
        """Generate time-series plots for historical metrics"""
        time_series_data = self._load_data("profiler_time_series.json")
        if not time_series_data:
            logger.info("No time series data available")
            return

        for func_key, records in tqdm(time_series_data.items(), desc="Processing functions"):
            try:
                df = pd.DataFrame(records)
                df = self._clean_data(df)
                if df.empty:
                    continue

                filename = sanitize_filename(df["file"].iloc[0].replace(".py", ""), replacement_text="_")
                func_name = sanitize_filename(df["function"].iloc[0], replacement_text="_")
                self._plot_time_series(df, filename, func_name)
                
            except Exception as e:
                logger.error(f"Error processing {func_key}: {str(e)}")

    def _plot_time_series(self, df: pd.DataFrame, filename: str, func_name: str) -> None:
        """Create comprehensive time-series visualizations"""
        metric_dirs = {
            "cpu": os.path.join(self.overtime_dir, "cpu"),
            "memory": os.path.join(self.overtime_dir, "memory"),
            "execution_time": os.path.join(self.overtime_dir, "execution_time"),
            "combined": os.path.join(self.overtime_dir, "combined")
        }
        
        for dir_path in metric_dirs.values():
            os.makedirs(dir_path, exist_ok=True)

        # Individual metric plots
        metrics = [
            ("cpu_usage", "CPU Usage (%)", "cpu"),
            ("peak_memory_mb", "Memory Usage (MB)", "memory"),
            ("execution_time", "Execution Time (seconds)", "execution_time")
        ]

        for metric, ylabel, subdir in metrics:
            plt.figure(figsize=(10, 5))
            sns.lineplot(x="timestamp", y=metric, data=df, marker="o")
            plt.title(f"{filename} - {func_name}\n{ylabel}")
            plt.xlabel("Timestamp")
            plt.ylabel(ylabel)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
            
            plot_name = sanitize_filename(f"{filename}_{func_name}_{metric}.png")
            plt.savefig(os.path.join(metric_dirs[subdir], plot_name), 
                       bbox_inches="tight", dpi=150)
            plt.close()

        # Combined plot
        plt.figure(figsize=(14, 10))
        plt.suptitle(f"{filename} - {func_name}", y=1.02)
        
        for idx, (metric, ylabel, subdir) in enumerate(metrics, 1):
            plt.subplot(3, 1, idx)
            sns.lineplot(x="timestamp", y=metric, data=df, marker="o")
            plt.title(ylabel)
            plt.xlabel("")
            plt.ylabel(ylabel)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
        
        combined_name = sanitize_filename(f"{filename}_{func_name}_combined.png")
        plt.savefig(os.path.join(metric_dirs["combined"], combined_name),
                  bbox_inches="tight", dpi=150)
        plt.close()

        logger.debug(f"Generated reports for {filename}:{func_name}")