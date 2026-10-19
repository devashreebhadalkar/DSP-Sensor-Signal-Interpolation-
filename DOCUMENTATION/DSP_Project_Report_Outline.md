# DSP Mini-Project Report

## Project Title
Interpolation for Smooth Reconstruction of Sensor Signals

## 1. Abstract
This project demonstrates interpolation of a sampled sensor signal using Python. The original signal is generated as a sine wave, and interpolation is applied to increase the number of sample points. Graphs and error measurements are used to study the reconstructed signal.

## 2. Introduction
Interpolation is a fundamental technique in digital signal processing (DSP). It increases the sampling rate by estimating intermediate sample values between existing samples. It is useful when a smoother signal representation is needed.

## 3. Problem Statement
A sampled sensor signal contains discrete values. This project investigates how interpolation adds intermediate samples and how closely the resulting signal matches a known reference signal.

## 4. Objectives
- Generate a simulated sensor signal.
- Apply interpolation using Python.
- Compare different interpolation factors.
- Calculate MSE and RMSE.
- Plot and analyze the results.

## 5. Software and Tools
- Python
- NumPy
- SciPy
- Matplotlib
- Visual Studio Code

## 6. Methodology
1. Generate a sine wave at 1 Hz.
2. Sample the signal at 10 Hz for 2 seconds.
3. Apply polyphase interpolation.
4. Compare interpolation factors 2, 4, and 8.
5. Compare the interpolated signal with the reference sine wave.
6. Calculate reconstruction-error metrics.
7. Save graphs and numerical results.

## 7. Results and Discussion
Insert the actual output graphs and numerical values obtained from the Python programs.

Discuss how interpolation changes the number of samples and how closely the interpolated signal follows the reference signal.

## 8. Applications
- Sensor signal processing
- Audio processing
- Biomedical signal processing
- Communication systems

## 9. Limitations
The current experiment uses a simulated sine wave rather than real sensor data. Interpolation estimates intermediate values and does not guarantee perfect reconstruction for every signal.

## 10. Future Scope
- Test real sensor datasets.
- Compare linear and other interpolation methods.
- Develop an interactive dashboard to display signals and error metrics.

## 11. Conclusion
The project demonstrates how interpolation increases the number of samples in a discrete-time signal. Python visualizations and error metrics help evaluate the resulting signal representation.

## 12. References
1. NumPy documentation: https://numpy.org/doc/
2. SciPy documentation: https://docs.scipy.org/doc/scipy/
3. Matplotlib documentation: https://matplotlib.org/stable/
