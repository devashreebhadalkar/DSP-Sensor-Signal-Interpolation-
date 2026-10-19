from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Project paths
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
print("SAMPLING INTERVAL ANALYSIS")
print("=" * 60)

# Load dataset
df = pd.read_csv(DATASET_FILE)

# Convert timestamps and remove invalid timestamps
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

df = df.dropna(subset=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

# Calculate time differences in seconds
df["sampling_interval_seconds"] = (
    df["timestamp"].diff().dt.total_seconds()
)

# Remove the first row and invalid or non-positive intervals
intervals = df["sampling_interval_seconds"].dropna()
intervals = intervals[intervals > 0]

if intervals.empty:
    raise ValueError("No valid positive sampling intervals were found.")

# Calculate statistics
mean_interval = intervals.mean()
median_interval = intervals.median()
minimum_interval = intervals.min()
maximum_interval = intervals.max()

print(f"\nNumber of valid intervals: {len(intervals):,}")
print(f"Mean interval:              {mean_interval:.3f} seconds")
print(f"Median interval:            {median_interval:.3f} seconds")
print(f"Minimum interval:           {minimum_interval:.3f} seconds")
print(f"Maximum interval:           {maximum_interval:.3f} seconds")

# Save statistics
report_file = RESULTS_DIR / "10_sampling_interval_results.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("SAMPLING INTERVAL ANALYSIS\n")
    file.write("=" * 40 + "\n")
    file.write(f"Valid intervals: {len(intervals):,}\n")
    file.write(f"Mean interval: {mean_interval:.3f} seconds\n")
    file.write(f"Median interval: {median_interval:.3f} seconds\n")
    file.write(f"Minimum interval: {minimum_interval:.3f} seconds\n")
    file.write(f"Maximum interval: {maximum_interval:.3f} seconds\n")

# Plot sampling intervals
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(intervals.to_numpy(), linewidth=0.7)

ax.set_title("Sampling Intervals in the Real Sensor Dataset")
ax.set_xlabel("Consecutive Reading Number")
ax.set_ylabel("Time Between Readings (seconds)")
ax.grid(True, alpha=0.3)

fig.tight_layout()

graph_file = SCREENSHOTS_DIR / "10_Sampling_Interval_Analysis.png"
fig.savefig(graph_file, dpi=200, bbox_inches="tight")

print(f"\nResults saved to:\n{report_file}")
print(f"\nGraph saved to:\n{graph_file}")

plt.show()

print("\nSampling interval analysis completed successfully.")