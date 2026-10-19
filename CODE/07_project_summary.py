
import numpy as np
from scipy.signal import resample_poly
from pathlib import Path

# Signal settings
sampling_rate = 10
duration = 2
frequency = 1
interpolation_factor = 4

# Generate original sensor signal
time = np.arange(0, duration, 1 / sampling_rate)
sensor_signal = np.sin(2 * np.pi * frequency * time)

# Interpolate the signal
interpolated_signal = resample_poly(
    sensor_signal, interpolation_factor, 1
)

# Generate interpolated time values
interpolated_time = np.arange(
    len(interpolated_signal)
) / (sampling_rate * interpolation_factor)

# Generate reference signal
reference_signal = np.sin(
    2 * np.pi * frequency * interpolated_time
)

# Calculate error metrics
error = reference_signal - interpolated_signal
mse = np.mean(error ** 2)
rmse = np.sqrt(mse)
max_error = np.max(np.abs(error))

# Prepare project summary
summary = [
    "DSP MINI PROJECT SUMMARY",
    "Interpolation for Smooth Reconstruction of Sensor Signals",
    "=" * 55,
    "",
    "SIGNAL SETTINGS",
    f"Original sampling rate: {sampling_rate} Hz",
    f"Signal frequency: {frequency} Hz",
    f"Signal duration: {duration} seconds",
    f"Interpolation factor: {interpolation_factor}",
    f"New sampling rate: {sampling_rate * interpolation_factor} Hz",
    "",
    "SAMPLE INFORMATION",
    f"Original sample count: {len(sensor_signal)}",
    f"Interpolated sample count: {len(interpolated_signal)}",
    "",
    "ERROR MEASUREMENTS",
    f"Mean Squared Error (MSE): {mse:.6f}",
    f"Root Mean Squared Error (RMSE): {rmse:.6f}",
    f"Maximum absolute error: {max_error:.6f}",
    "",
    "CONCLUSION",
    "Interpolation increases the number of samples and provides",
    "a smoother representation of the sampled sensor signal.",
    "Error measurements help compare it with the reference signal."
]

# Display summary
print("\n".join(summary))

# Save summary in the Results folder
project_folder = Path(__file__).resolve().parent.parent
results_folder = project_folder / "Results"
results_folder.mkdir(exist_ok=True)

output_file = results_folder / "07_project_summary.txt"
output_file.write_text(
    "\n".join(summary) + "\n",
    encoding="utf-8"
)

print("\nProject summary saved to:", output_file)

# Purpose of the Code:
# 1. To combine the main DSP calculations in one program.
# 2. To summarize signal settings and sample counts.
# 3. To calculate and report reconstruction error metrics.
# 4. To save a summary for the project report and presentation.
