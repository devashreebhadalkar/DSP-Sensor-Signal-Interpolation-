from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "RESULTS" / "11_temperature_segment.csv"
RESULTS_DIR = PROJECT_DIR / "RESULTS"
SCREENSHOTS_DIR = PROJECT_DIR / "SCREENSHOTS"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("CUBIC INTERPOLATION ON REAL SENSOR DATA")
print("=" * 60)

# Load prepared data
df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce", utc=True
)
df["temperature"] = pd.to_numeric(
    df["temperature"], errors="coerce"
)

df = (
    df.dropna(subset=["timestamp", "temperature"])
    .sort_values("timestamp")
    .drop_duplicates(subset=["timestamp"])
    .reset_index(drop=True)
)

if len(df) < 20:
    raise ValueError("At least 20 unique timestamp readings are required.")

# Represent timestamps as elapsed seconds
time_seconds = (
    df["timestamp"] - df["timestamp"].iloc[0]
).dt.total_seconds().to_numpy()

temperature = df["temperature"].to_numpy(dtype=float)

# Keep every fifth reading as a sparse sample
sample_indices = np.arange(0, len(df), 5)

if sample_indices[-1] != len(df) - 1:
    sample_indices = np.append(sample_indices, len(df) - 1)

sample_times = time_seconds[sample_indices]
sample_temperatures = temperature[sample_indices]

# Linear interpolation
linear_values = np.interp(
    time_seconds, sample_times, sample_temperatures
)

# Cubic interpolation
cubic_function = interp1d(
    sample_times,
    sample_temperatures,
    kind="cubic",
    bounds_error=True
)

cubic_values = cubic_function(time_seconds)

# Evaluate only readings excluded from the sparse sample set
sample_mask = np.zeros(len(df), dtype=bool)
sample_mask[sample_indices] = True
test_mask = ~sample_mask

def calculate_metrics(estimate, reference, mask):
    errors = estimate[mask] - reference[mask]
    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors ** 2))
    return mae, rmse

linear_mae, linear_rmse = calculate_metrics(
    linear_values, temperature, test_mask
)

cubic_mae, cubic_rmse = calculate_metrics(
    cubic_values, temperature, test_mask
)

# Save comparison data
comparison = pd.DataFrame({
    "timestamp": df["timestamp"],
    "original_temperature_C": temperature,
    "linear_interpolation_C": linear_values,
    "cubic_interpolation_C": cubic_values,
    "used_as_sparse_sample": sample_mask
})

comparison_file = RESULTS_DIR / "13_interpolation_comparison.csv"
comparison.to_csv(comparison_file, index=False)

# Save metrics
summary_file = RESULTS_DIR / "13_interpolation_comparison.txt"

with open(summary_file, "w", encoding="utf-8") as file:
    file.write("INTERPOLATION METHOD COMPARISON\n")
    file.write("=" * 45 + "\n")
    file.write(f"Total readings: {len(df)}\n")
    file.write(f"Sparse samples: {len(sample_indices)}\n")
    file.write(f"Test readings: {test_mask.sum()}\n\n")
    file.write("Linear interpolation:\n")
    file.write(f"MAE:  {linear_mae:.6f} °C\n")
    file.write(f"RMSE: {linear_rmse:.6f} °C\n\n")
    file.write("Cubic interpolation:\n")
    file.write(f"MAE:  {cubic_mae:.6f} °C\n")
    file.write(f"RMSE: {cubic_rmse:.6f} °C\n")

print(f"\nTotal readings: {len(df)}")
print(f"Sparse samples: {len(sample_indices)}")
print(f"Test readings: {test_mask.sum()}")

print("\nLINEAR INTERPOLATION")
print(f"MAE:  {linear_mae:.6f} °C")
print(f"RMSE: {linear_rmse:.6f} °C")

print("\nCUBIC INTERPOLATION")
print(f"MAE:  {cubic_mae:.6f} °C")
print(f"RMSE: {cubic_rmse:.6f} °C")

# Plot comparison
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(
    df["timestamp"], temperature,
    label="Original sensor readings",
    linewidth=1
)

ax.plot(
    df["timestamp"], linear_values,
    label="Linear interpolation",
    linewidth=1.3
)

ax.plot(
    df["timestamp"], cubic_values,
    label="Cubic interpolation",
    linewidth=1.3
)

ax.scatter(
    df["timestamp"].iloc[sample_indices],
    sample_temperatures,
    label="Sparse samples",
    s=18,
    zorder=3
)

ax.set_title("Linear vs Cubic Interpolation of Real Temperature Data")
ax.set_xlabel("Timestamp")
ax.set_ylabel("Temperature (°C)")
ax.grid(True, alpha=0.3)
ax.legend()

fig.autofmt_xdate()
fig.tight_layout()

graph_file = SCREENSHOTS_DIR / "13_Linear_vs_Cubic_Interpolation.png"
fig.savefig(graph_file, dpi=200, bbox_inches="tight")

print(f"\nComparison CSV saved to:\n{comparison_file}")
print(f"Metrics saved to:\n{summary_file}")
print(f"Graph saved to:\n{graph_file}")

plt.show()

print("\nCubic interpolation completed successfully.")