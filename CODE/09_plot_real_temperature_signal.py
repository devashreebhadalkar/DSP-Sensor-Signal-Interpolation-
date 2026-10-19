# ============================================================
# Program 09: Plot Real Temperature Sensor Signal
#
# Project:
# Interpolation for Smooth Reconstruction of Sensor Signals
#
# Purpose:
# 1. Load real temperature measurements.
# 2. Convert timestamps to datetime values.
# 3. Plot temperature against time.
# 4. Save the graph in the Screenshots folder.
# ============================================================

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# ------------------------------------------------------------
# 1. Define project paths
# ------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_DIR
    / "DATASET"
    / "single+elder+home+monitoring+gas+and+position"
    / "DB elder monitoring"
    / "data_ref_until_2020-02-13.csv"
)

SCREENSHOTS_DIR = PROJECT_DIR / "SCREENSHOTS"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load the real sensor dataset
# ------------------------------------------------------------

print("=" * 65)
print("REAL TEMPERATURE SENSOR SIGNAL")
print("=" * 65)

df = pd.read_csv(DATASET_FILE)

print(f"\nTotal records loaded: {len(df):,}")


# ------------------------------------------------------------
# 3. Convert timestamps to datetime
# ------------------------------------------------------------

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

df["temperature"] = pd.to_numeric(
    df["temperature"],
    errors="coerce"
)

# Remove rows with invalid timestamps or temperature readings.
df = df.dropna(subset=["timestamp", "temperature"])

# Sort readings chronologically.
df = df.sort_values("timestamp")

print(f"Valid temperature readings: {len(df):,}")
print(f"First timestamp: {df['timestamp'].iloc[0]}")
print(f"Last timestamp:  {df['timestamp'].iloc[-1]}")


# ------------------------------------------------------------
# 4. Display temperature statistics
# ------------------------------------------------------------

print("\nTemperature statistics:")

print(f"Mean:   {df['temperature'].mean():.3f} °C")
print(f"Median: {df['temperature'].median():.3f} °C")
print(f"Minimum: {df['temperature'].min():.3f} °C")
print(f"Maximum: {df['temperature'].max():.3f} °C")


# ------------------------------------------------------------
# 5. Plot the real temperature signal
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    df["timestamp"],
    df["temperature"],
    linewidth=0.8,
    label="Recorded temperature"
)

ax.set_title(
    "Real Sensor Temperature Measurements",
    fontsize=15
)

ax.set_xlabel("Timestamp")
ax.set_ylabel("Temperature (°C)")

ax.grid(True, alpha=0.3)
ax.legend()

# Format the time axis for readability.
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(
    mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
)

fig.autofmt_xdate()
fig.tight_layout()


# ------------------------------------------------------------
# 6. Save the graph
# ------------------------------------------------------------

OUTPUT_FILE = (
    SCREENSHOTS_DIR
    / "08_Real_Temperature_Signal.png"
)

fig.savefig(
    OUTPUT_FILE,
    dpi=200,
    bbox_inches="tight"
)

print(f"\nGraph saved to:\n{OUTPUT_FILE}")


# ------------------------------------------------------------
# 7. Display the graph
# ------------------------------------------------------------

plt.show()

print("\nTemperature plotting completed successfully.")

# End of Program 09