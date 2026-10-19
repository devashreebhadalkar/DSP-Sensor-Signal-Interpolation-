
import numpy as np
import matplotlib.pyplot as plt

# Sampling settings
sampling_rate = 10
duration = 2

# Generate time values
time = np.arange(0, duration, 1 / sampling_rate)

# Simulate a sensor signal
frequency = 1
sensor_signal = np.sin(2 * np.pi * frequency * time)

# Display the signal
plt.figure(figsize=(10, 5))
plt.stem(time, sensor_signal)

plt.title("Original Sensor Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Sensor Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()


# Purpose of the Code:
# 1. To generate a simulated sensor signal using a sine wave.
# 2. To define the sampling rate and signal duration.
# 3. To create time values for sampling the signal.
# 4. To plot the original sampled sensor signal.
# 5. To provide the original signal for further interpolation
#    and smooth reconstruction.
