
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample_poly

# Sampling settings
sampling_rate = 10
duration = 2
frequency = 1

# Generate the original sensor signal
time = np.arange(0, duration, 1 / sampling_rate)
sensor_signal = np.sin(2 * np.pi * frequency * time)

# Interpolation factor
interpolation_factor = 4

# Perform interpolation
interpolated_signal = resample_poly(
    sensor_signal, interpolation_factor, 1
)

# Generate time values for the interpolated signal
interpolated_time = np.arange(
    len(interpolated_signal)
) / (sampling_rate * interpolation_factor)

# Plot original and interpolated signals
plt.figure(figsize=(10, 5))

plt.stem(
    time,
    sensor_signal,
    linefmt="C0-",
    markerfmt="C0o",
    basefmt="k-",
    label="Original Samples"
)

plt.plot(
    interpolated_time,
    interpolated_signal,
    "r-",
    label="Interpolated Signal"
)

plt.title("Sensor Signal Interpolation")
plt.xlabel("Time (seconds)")
plt.ylabel("Sensor Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Display information
print("Original number of samples:", len(sensor_signal))
print("Interpolated number of samples:", len(interpolated_signal))
print("Interpolation factor:", interpolation_factor)
print("New sampling rate:", sampling_rate * interpolation_factor, "Hz")

# Purpose of the Code:
# 1. To interpolate the original sampled sensor signal.
# 2. To insert additional samples between the original samples.
# 3. To use polyphase filtering for interpolation.
# 4. To compare the original samples with the interpolated signal.
# 5. To demonstrate how interpolation helps reconstruct a
#    smoother representation of a sampled signal.
