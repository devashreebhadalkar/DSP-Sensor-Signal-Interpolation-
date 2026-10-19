
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample_poly

# Signal settings
sampling_rate = 10
duration = 2
frequency = 1
interpolation_factor = 4

# Generate the original sampled sensor signal
time = np.arange(0, duration, 1 / sampling_rate)
sensor_signal = np.sin(2 * np.pi * frequency * time)

# Interpolate the sampled signal
interpolated_signal = resample_poly(
    sensor_signal, interpolation_factor, 1
)

# Generate time values for the interpolated signal
interpolated_time = np.arange(
    len(interpolated_signal)
) / (sampling_rate * interpolation_factor)

# Generate the known reference sine wave
reference_signal = np.sin(
    2 * np.pi * frequency * interpolated_time
)

# Calculate reconstruction error
error = reference_signal - interpolated_signal
mse = np.mean(error ** 2)
rmse = np.sqrt(mse)

# Display results
print("Original samples:", len(sensor_signal))
print("Interpolated samples:", len(interpolated_signal))
print("Interpolation factor:", interpolation_factor)
print("Mean Squared Error (MSE):", round(mse, 6))
print("Root Mean Squared Error (RMSE):", round(rmse, 6))

# Plot reference and interpolated signals
plt.figure(figsize=(10, 5))
plt.plot(
    interpolated_time,
    reference_signal,
    "g--",
    label="Reference Sine Wave"
)
plt.plot(
    interpolated_time,
    interpolated_signal,
    "r-",
    label="Interpolated Signal"
)

plt.title("Signal Reconstruction Comparison")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Purpose of the Code:
# 1. To interpolate the sampled sensor signal.
# 2. To generate the known reference sine wave.
# 3. To calculate the difference between the two signals.
# 4. To measure reconstruction error using MSE and RMSE.
# 5. To compare the reference and interpolated signals visually.
