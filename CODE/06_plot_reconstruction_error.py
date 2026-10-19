
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample_poly

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

# Calculate error
error = reference_signal - interpolated_signal

# Plot reconstruction error
plt.figure(figsize=(10, 5))
plt.plot(interpolated_time, error, "m-")

plt.title("Reconstruction Error of Interpolated Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Error Amplitude")
plt.axhline(y=0, color="black", linestyle="--")
plt.grid(True)
plt.tight_layout()
plt.show()

# Display error measurements
mse = np.mean(error ** 2)
rmse = np.sqrt(mse)

print("Interpolation factor:", interpolation_factor)
print("Mean Squared Error (MSE):", round(mse, 6))
print("Root Mean Squared Error (RMSE):", round(rmse, 6))
print("Maximum absolute error:", round(np.max(np.abs(error)), 6))

# Purpose of the Code:
# 1. To calculate the difference between the reference and
#    interpolated signals.
# 2. To plot the reconstruction error over time.
# 3. To calculate MSE, RMSE, and maximum absolute error.
# 4. To evaluate how closely the interpolated signal matches
#    the known reference sine wave.
