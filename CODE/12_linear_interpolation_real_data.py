from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "RESULTS" / "11_temperature_segment.csv"
RESULTS_DIR = PROJECT_DIR / "RESULTS"
SCREENSHOTS_DIR = PROJECT_DIR / "SCREENSHOTS"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("LINEAR INTERPOLATION ON REAL SENSOR DATA")
print("=" * 60)

# Load the prepared real sensor segment
df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

df["temperature"] = pd.to_numeric(
    df["temperature"],
    errors="coerce"
)

df = (
    df.dropna(subset=["timestamp", "temperature"])
    .sort_values("timestamp")
    .drop_duplicates(subset=["timestamp"])
    .reset_index(drop=True)
)

if len(df) < 10:
    raise ValueError("At least 10 valid readings are required.")

# Convert timestamps into elapsed seconds.
# This handles irregular sampling intervals.
time_seconds = (
    df["timestamp"] - df["timestamp"].iloc[0]
).dt.total_seconds().to_numpy()

temperature = df["temperature"].to_numpy(dtype=float)

# Keep every fifth reading as a sparse sample.
# The remaining readings are used as interpolation reference points.
sample_indices = np.arange(0, len(df), 5)

if sample_indices[-1] != len(df) - 1:
    sample_indices = np.append(sample_indices, len(df) - 1)

sample_times = time_seconds[sample_indices]
sample_temperatures = temperature[sample_indices]

# Interpolate at the timestamps of all available readings.
interpolated_temperature = np.interp(
    time_seconds,
    sample_times,
    sample_temperatures
)

# Save comparison data
comparison = pd.DataFrame({
    "timestamp": df["timestamp"],
    "original_temperature_C": temperature,
    "linear_interpolated_temperature_C": interpolated_temperature
})

comparison_file = RESULTS_DIR / "12_linear_interpolation_results.csv"
comparison.to_csv(comparison_file, index=False)

# Calculate error only at timestamps not used as sparse samples.
# These original readings act as a reference for this experiment.
is_reference_sample = np.zeros(len(df), dtype=bool)
is_reference_sample[sample_indices] = True

test_mask = ~is_reference_sample

if test_mask.any():
    errors = (
        interpolated_temperature[test_mask]
        - temperature[test_mask]
    )

    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors ** 2))
else:
    mae = float("nan")
    rmse = float("nan")

print(f"\nTotal valid readings: {len(df)}")
print(f"Sparse samples used: {len(sample_indices)}")
print(f"Estimated values between samples: {test_mask.sum()}")
print(f"Mean absolute error (MAE): {mae:.6f} °C")
print(f"Root mean squared error (RMSE): {rmse:.6f} °C")

# Save a text summary
summary_file = RESULTS_DIR / "12_linear_interpolation_summary.txt"

with open(summary_file, "w", encoding="utf-8") as file:
    file.write("LINEAR INTERPOLATION RESULTS\n")
    file.write("=" * 40 + "\n")
    file.write(f"Total valid readings: {len(df)}\n")
    file.write(f"Sparse samples used: {len(sample_indices)}\n")
    file.write(f"Estimated values: {test_mask.sum()}\n")
    file.write(f"MAE: {mae:.6f} °C\n")
    file.write(f"RMSE: {rmse:.6f} °C\n")

# Plot original readings and interpolated signal
fig, ax = plt.subplots(figsize=(13, 6))

ax.plot(
    df["timestamp"],
    temperature,
    label="Original sensor readings",
    linewidth=1
)

ax.plot(
    df["timestamp"],
    interpolated_temperature,
    label="Linear interpolation",
    linewidth=1.5
)

ax.scatter(
    df["timestamp"].iloc[sample_indices],
    sample_temperatures,
    label="Sparse samples used",
    s=18,
    zorder=3
)

ax.set_title("Linear Interpolation of Real Temperature Sensor Data")
ax.set_xlabel("Timestamp")
ax.set_ylabel("Temperature (°C)")
ax.grid(True, alpha=0.3)
ax.legend()

fig.autofmt_xdate()
fig.tight_layout()

graph_file = SCREENSHOTS_DIR / "12_Linear_Interpolation_Real_Data.png"
fig.savefig(graph_file, dpi=200, bbox_inches="tight")

print(f"\nComparison data saved to:\n{comparison_file}")
print(f"Summary saved to:\n{summary_file}")
print(f"Graph saved to:\n{graph_file}")

plt.show()

print("\nLinear interpolation completed successfully.")