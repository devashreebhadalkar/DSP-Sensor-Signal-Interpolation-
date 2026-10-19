from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_DIR
    / "DATASET"
    / "single+elder+home+monitoring+gas+and+position"
    / "DB elder monitoring"
    / "data_ref_until_2020-02-13.csv"
)

RESULTS_DIR = PROJECT_DIR / "RESULTS"
SCREENSHOTS_DIR = PROJECT_DIR / "SCREENSHOTS"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("PREPARING REAL TEMPERATURE SIGNAL")
print("=" * 60)

# Load the dataset
df = pd.read_csv(DATASET_FILE)

# Convert columns to appropriate data types
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

df["temperature"] = pd.to_numeric(
    df["temperature"],
    errors="coerce"
)

# Keep valid temperature readings and timestamps
df = df.dropna(subset=["timestamp", "temperature"])

# Sort readings chronologically
df = df.sort_values("timestamp").reset_index(drop=True)

# Select 500 consecutive readings
segment = df.head(500).copy()

if len(segment) < 10:
    raise ValueError("Not enough valid readings to prepare a segment.")

print(f"\nNumber of selected readings: {len(segment)}")
print(f"Start timestamp: {segment['timestamp'].iloc[0]}")
print(f"End timestamp:   {segment['timestamp'].iloc[-1]}")

print("\nTemperature statistics:")
print(f"Mean:   {segment['temperature'].mean():.3f} °C")
print(f"Minimum: {segment['temperature'].min():.3f} °C")
print(f"Maximum: {segment['temperature'].max():.3f} °C")

# Save the selected segment
output_csv = RESULTS_DIR / "11_temperature_segment.csv"

segment[
    ["timestamp", "temperature"]
].to_csv(output_csv, index=False)

# Plot the selected segment
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    segment["timestamp"],
    segment["temperature"],
    linewidth=1,
    label="Recorded temperature"
)

ax.set_title("Selected Real Temperature Signal Segment")
ax.set_xlabel("Timestamp")
ax.set_ylabel("Temperature (°C)")
ax.grid(True, alpha=0.3)
ax.legend()

fig.autofmt_xdate()
fig.tight_layout()

graph_file = SCREENSHOTS_DIR / "11_Temperature_Segment.png"

fig.savefig(
    graph_file,
    dpi=200,
    bbox_inches="tight"
)

print(f"\nSelected data saved to:\n{output_csv}")
print(f"\nGraph saved to:\n{graph_file}")

plt.show()

print("\nTemperature segment preparation completed successfully.")