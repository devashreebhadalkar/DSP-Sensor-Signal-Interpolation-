from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "RESULTS"
SCREENSHOTS_DIR = PROJECT_DIR / "SCREENSHOTS"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Input files
LINEAR_FILE = RESULTS_DIR / "12_linear_interpolation_results.csv"
COMPARISON_FILE = RESULTS_DIR / "13_interpolation_comparison.csv"

print("=" * 60)
print("INTERPOLATION PERFORMANCE COMPARISON")
print("=" * 60)

# Load results
linear_df = pd.read_csv(LINEAR_FILE)
comparison_df = pd.read_csv(COMPARISON_FILE)

required_columns = {
    "original_temperature_C",
    "linear_interpolation_C",
    "cubic_interpolation_C",
    "used_as_sparse_sample"
}

missing = required_columns - set(comparison_df.columns)

if missing:
    raise ValueError(f"Missing columns in comparison file: {missing}")

# Identify readings that were not used as sparse samples
sample_mask = comparison_df["used_as_sparse_sample"].astype(bool)
test_mask = ~sample_mask

if not test_mask.any():
    raise ValueError("No held-out readings available for evaluation.")

reference = comparison_df.loc[
    test_mask, "original_temperature_C"
].to_numpy()

linear_estimate = comparison_df.loc[
    test_mask, "linear_interpolation_C"
].to_numpy()

cubic_estimate = comparison_df.loc[
    test_mask, "cubic_interpolation_C"
].to_numpy()

# Calculate performance metrics on the same held-out readings
def calculate_metrics(estimate, actual):
    error = estimate - actual

    mae = abs(error).mean()
    rmse = (error ** 2).mean() ** 0.5

    return mae, rmse

linear_mae, linear_rmse = calculate_metrics(
    linear_estimate, reference
)

cubic_mae, cubic_rmse = calculate_metrics(
    cubic_estimate, reference
)

# Create comparison table
metrics_df = pd.DataFrame({
    "Method": ["Linear Interpolation", "Cubic Interpolation"],
    "MAE_C": [linear_mae, cubic_mae],
    "RMSE_C": [linear_rmse, cubic_rmse]
})

metrics_file = RESULTS_DIR / "14_interpolation_performance_metrics.csv"
metrics_df.to_csv(metrics_file, index=False)

print("\nPerformance Metrics")
print("-" * 45)
print(metrics_df.to_string(index=False))

# Determine which method has lower error
if linear_mae < cubic_mae:
    mae_winner = "Linear interpolation"
elif cubic_mae < linear_mae:
    mae_winner = "Cubic interpolation"
else:
    mae_winner = "Both methods have equal MAE"

if linear_rmse < cubic_rmse:
    rmse_winner = "Linear interpolation"
elif cubic_rmse < linear_rmse:
    rmse_winner = "Cubic interpolation"
else:
    rmse_winner = "Both methods have equal RMSE"

print(f"\nLower MAE:  {mae_winner}")
print(f"Lower RMSE: {rmse_winner}")

# Plot MAE comparison
fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    metrics_df["Method"],
    metrics_df["MAE_C"]
)

ax.set_title("MAE Comparison: Linear vs Cubic Interpolation")
ax.set_ylabel("Mean Absolute Error (°C)")
ax.grid(axis="y", alpha=0.3)

fig.tight_layout()

mae_graph = SCREENSHOTS_DIR / "14_MAE_Comparison.png"
fig.savefig(mae_graph, dpi=200, bbox_inches="tight")

plt.show()

# Plot RMSE comparison
fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    metrics_df["Method"],
    metrics_df["RMSE_C"]
)

ax.set_title("RMSE Comparison: Linear vs Cubic Interpolation")
ax.set_ylabel("Root Mean Squared Error (°C)")
ax.grid(axis="y", alpha=0.3)

fig.tight_layout()

rmse_graph = SCREENSHOTS_DIR / "14_RMSE_Comparison.png"
fig.savefig(rmse_graph, dpi=200, bbox_inches="tight")

plt.show()

print(f"\nMetrics saved to:\n{metrics_file}")
print(f"MAE graph saved to:\n{mae_graph}")
print(f"RMSE graph saved to:\n{rmse_graph}")

print("\nPerformance comparison completed successfully.")