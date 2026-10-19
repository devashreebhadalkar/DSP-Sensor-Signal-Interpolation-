
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample_poly

# Signal settings
sampling_rate = 10
duration = 2
frequency = 1

# Generate original sensor signal
time = np.arange(0, duration, 1 / sampling_rate)
sensor_signal = np.sin(2 * np.pi * frequency * time)

# Interpolation factors to compare
factors = [2, 4, 8]

# Plot original samples
plt.figure(figsize=(11, 6))
plt.stem(
    time,
    sensor_signal,
    linefmt="C0-",
    markerfmt="C0o",
    basefmt="k-",
    label="Original Samples"
)

# Apply different interpolation factors
for factor in factors:
    interpolated_signal = resample_poly(
        sensor_signal, factor, 1
    )

    interpolated_time = np.arange(
        len(interpolated_signal)
    ) / (sampling_rate * factor)

    plt.plot(
        interpolated_time,
        interpolated_signal,
        label=f"Interpolation Factor = {factor}"
    )

# Graph settings
plt.title("Comparison of Interpolation Factors")
plt.xlabel("Time (seconds)")
plt.ylabel("Sensor Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Display sample counts
print("Original sample count:", len(sensor_signal))

for factor in factors:
    print(
        f"Factor {factor}: "
        f"{len(resample_poly(sensor_signal, factor, 1))} samples"
    )

# Purpose of the Code:
# 1. To compare interpolation factors 2, 4, and 8.
# 2. To observe how each factor increases the sample count.
# 3. To compare the interpolated signals with the original samples.
# 4. To demonstrate the effect of interpolation on signal representation.
