
import numpy as np
from scipy.signal import resample_poly
from pathlib import Path

# Signal settings
sampling_rate = 10
duration = 2
frequency = 1
interpolation_factor = 4

# Generate the original sensor signal
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

# Calculate reconstruction errors
error = reference_signal - interpolated_signal
mse = np.mean(error ** 2)
rmse = np.sqrt(mse)

# Prepare results
results = [
    "SENSOR SIGNAL INTERPOLATION PROJECT",
    "===================================",
    f"Original sampling rate: {sampling_rate} Hz",
    f"Signal frequency: {frequency} Hz",
    f"Signal duration: {duration} seconds",
    f"Interpolation factor: {interpolation_factor}",
    f"Interpolated sampling rate: {sampling_rate * interpolation_factor} Hz",
    f"Original sample count: {len(sensor_signal)}",
    f"Interpolated sample count: {len(interpolated_signal)}",
    f"Mean Squared Error (MSE): {mse:.6f}",
    f"Root Mean Squared Error (RMSE): {rmse:.6f}",
]

# Display results in the terminal
for line in results:
    print(line)

# Save results in the Results folder
project_folder = Path(__file__).resolve().parent.parent
results_folder = project_folder / "Results"
results_folder.mkdir(exist_ok=True)

output_file = results_folder / "04_signal_results.txt"
output_file.write_text("\n".join(results) + "\n", encoding="utf-8")

print("\nResults saved to:", output_file)

# Purpose of the Code:
# 1. To generate and interpolate the sensor signal.
# 2. To calculate MSE and RMSE against the reference sine wave.
# 3. To display important project parameters and results.
# 4. To save the numerical results in a text file for reporting.
