# Interpolation for Smooth Reconstruction of Sensor Signals

## 🌐 Live Application

Try the interactive DSP Sensor Signal Interpolation Dashboard:

**[Open Live Dashboard](https://n43rzuqzwzph8mb6wb7tgr.streamlit.app/)**

## ✨ Features

- Sensor signal visualization
- Linear and cubic interpolation
- MAE and RMSE performance evaluation
- Interactive data tables
- CSV upload and analysis
- Downloadable results

## 1. Project Overview
This DSP mini-project demonstrates how interpolation can increase the number of samples in a sampled sensor signal and create a smoother signal representation using Python.

## 2. Objectives
- Generate a simulated sensor signal.
- Apply interpolation to the sampled signal.
- Compare different interpolation factors.
- Calculate reconstruction error using MSE and RMSE.
- Visualize the original, interpolated, and reference signals.

## 3. Technologies Used
- Python
- NumPy
- SciPy
- Matplotlib
- Visual Studio Code

## 4. Methodology
1. Generate a 1 Hz sine wave sampled at 10 Hz for 2 seconds.
2. Apply polyphase interpolation using `scipy.signal.resample_poly()`.
3. Compare interpolation factors of 2, 4, and 8.
4. Generate the known reference sine wave.
5. Calculate MSE, RMSE, and maximum absolute error.
6. Plot the signals and save the results.

## 5. Project Structure
- `Code/` — Python programs
- `Dataset/` — Reserved for sensor data
- `Results/` — Numerical results and summaries
- `Screenshots/` — Graphs and implementation evidence
- `Documentation/` — Project report and supporting documents

## 6. Expected Outcome
The interpolated signal contains additional sample points and provides a smoother representation of the sampled signal. Error measurements help evaluate how closely it matches the known reference sine wave.

## 7. Applications
- Sensor signal processing
- Audio signal processing
- Image resizing
- Biomedical signal processing
- Communication systems

## 8. Limitations
The project uses a simulated sine wave rather than real sensor measurements. Interpolation does not create new measured information and may not perfectly reconstruct every continuous signal.

## 9. Future Scope
- Test the method on real sensor data.
- Compare additional interpolation methods.
- Build a simple dashboard to display signals and error measurements.

## 10. Conclusion
This project demonstrates the basic principles of interpolation in digital signal processing. It shows how additional samples can be generated and how reconstruction error can be measured using Python.
