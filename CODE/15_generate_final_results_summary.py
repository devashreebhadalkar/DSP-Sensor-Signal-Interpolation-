from pathlib import Path
import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "RESULTS"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

METRICS_FILE = (
    RESULTS_DIR / "14_interpolation_performance_metrics.csv"
)

OUTPUT_FILE = RESULTS_DIR / "15_final_results_summary.txt"

print("=" * 60)
print("FINAL DSP RESULTS SUMMARY")
print("=" * 60)

# Load measured interpolation metrics
if not METRICS_FILE.exists():
    raise FileNotFoundError(
        f"Cannot find {METRICS_FILE}. "
        "Please run Step 14 successfully first."
    )

metrics = pd.read_csv(METRICS_FILE)

required_columns = {"Method", "MAE_C", "RMSE_C"}

if not required_columns.issubset(metrics.columns):
    raise ValueError(
        "The metrics file does not contain the expected columns."
    )

if len(metrics) < 2:
    raise ValueError(
        "Expected results for both linear and cubic interpolation."
    )

# Identify methods by name
metrics["Method"] = metrics["Method"].astype(str)

linear_rows = metrics[
    metrics["Method"].str.contains("Linear", case=False)
]

cubic_rows = metrics[
    metrics["Method"].str.contains("Cubic", case=False)
]

if linear_rows.empty or cubic_rows.empty:
    raise ValueError(
        "Could not identify both linear and cubic interpolation results."
    )

linear = linear_rows.iloc[0]
cubic = cubic_rows.iloc[0]

# Determine the lower-error method for each metric
mae_winner = (
    "Linear interpolation"
    if linear["MAE_C"] < cubic["MAE_C"]
    else "Cubic interpolation"
    if cubic["MAE_C"] < linear["MAE_C"]
    else "Both methods have equal MAE"
)

rmse_winner = (
    "Linear interpolation"
    if linear["RMSE_C"] < cubic["RMSE_C"]
    else "Cubic interpolation"
    if cubic["RMSE_C"] < linear["RMSE_C"]
    else "Both methods have equal RMSE"
)

# Build the report from actual computed values
report = f"""
DSP MINI-PROJECT: FINAL RESULTS SUMMARY
=======================================

Project title:
Interpolation for Smooth Reconstruction of Sensor Signals

Dataset:
UCI Single Elder Home Monitoring dataset

Signal analyzed:
Real temperature sensor measurements

INTERPOLATION METHODS
---------------------
1. Linear interpolation
2. Cubic interpolation

PERFORMANCE METRICS
-------------------
Linear interpolation:
MAE  = {linear['MAE_C']:.6f} °C
RMSE = {linear['RMSE_C']:.6f} °C

Cubic interpolation:
MAE  = {cubic['MAE_C']:.6f} °C
RMSE = {cubic['RMSE_C']:.6f} °C

COMPARISON
----------
Method with lower MAE:  {mae_winner}
Method with lower RMSE: {rmse_winner}

INTERPRETATION
--------------
MAE represents the mean absolute difference between interpolated
estimates and held-out recorded temperature readings.

RMSE represents the root mean squared difference and gives greater
weight to larger errors.

Lower values indicate closer agreement with the held-out readings
for this particular experiment.

The comparison uses recorded readings excluded from the sparse
sample set as reference values. These are not independent ground-truth
measurements of the true temperature.

CONCLUSION
----------
Both interpolation methods were evaluated on the selected real
temperature signal segment.

The method with lower error performed better according to that
metric for this experiment. Results may vary with the dataset,
sampling pattern, and signal characteristics.

Interpolation estimates values between existing samples; it does
not create new sensor measurements.

Note:
This report summarizes the calculated metrics. Verify the plots,
dataset details, and experimental settings before final submission.
"""

# Save the summary
OUTPUT_FILE.write_text(report.strip() + "\n", encoding="utf-8")

print(report)
print(f"\nFinal summary saved to:\n{OUTPUT_FILE}")
print("\nStep 15 completed successfully.")