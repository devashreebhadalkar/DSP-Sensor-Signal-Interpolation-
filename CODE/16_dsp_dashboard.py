from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.interpolate import interp1d


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="DSP Sensor Signal Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_DIR / "RESULTS"

DATASET_FILE = (
    PROJECT_DIR
    / "DATASET"
    / "single+elder+home+monitoring+gas+and+position"
    / "DB elder monitoring"
    / "data_ref_until_2020-02-13.csv"
)


# =========================================================
# CUSTOM STYLING — DARK BLUE AND WHITE THEME
# =========================================================

st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #0b1530;
        color: #ffffff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #101d36;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* Main text */
    p, li, label {
        color: #ffffff;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #17294a;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #ffffff;
    }

    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    [data-testid="stMetricDelta"] {
        color: #ffffff !important;
    }

    /* Subtitle */
    .project-caption {
        color: #ffffff !important;
        font-size: 1rem;
    }

    /* Divider */
    hr {
        border-color: #ffffff !important;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #ffffff;
        border-radius: 8px;
    }

    /* Slider text */
    [data-testid="stSlider"] label {
        color: #ffffff !important;
    }

    /* Radio labels */
    [data-testid="stRadio"] label {
        color: #ffffff !important;
    }

    /* Buttons */
    .stDownloadButton button {
        background-color: #ffffff;
        color: #0b1530 !important;
        border-radius: 8px;
        border: 1px solid #ffffff;
    }

    .stDownloadButton button:hover {
        background-color: #dbeafe;
        color: #0b1530 !important;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Links */
    a {
        color: #93c5fd !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.title("📈 Real Sensor Signal Interpolation Dashboard")

st.markdown(
    """
    <p class="project-caption">
    Interpolation for Smooth Reconstruction of Sensor Signals
    · Digital Signal Processing Mini-Project
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()


# =========================================================
# LOAD REAL SENSOR DATA
# =========================================================

@st.cache_data
def load_data(file_path, modified_time):
    df = pd.read_csv(file_path)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
        utc=True,
    )

    df["temperature"] = pd.to_numeric(
        df["temperature"],
        errors="coerce",
    )

    df = df.dropna(
        subset=["timestamp", "temperature"]
    )

    df = df.sort_values("timestamp")

    df = df.drop_duplicates(
        subset=["timestamp"]
    ).reset_index(drop=True)

    return df


# Optional CSV upload — when no file is selected, use the original dataset.
uploaded_file = st.file_uploader(
    "📂 Upload a CSV dataset (optional)",
    type=["csv"],
    help="CSV must contain columns named timestamp and temperature. Leave empty to use the original dataset.",
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [str(col).strip() for col in df.columns]

        required_columns = ["timestamp", "temperature"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(
                "Uploaded CSV is missing required column(s): "
                + ", ".join(missing_columns)
                + ". Required columns are timestamp and temperature."
            )
            st.stop()

        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce", utc=True
        )
        df["temperature"] = pd.to_numeric(
            df["temperature"], errors="coerce"
        )
        df = df.dropna(subset=["timestamp", "temperature"])
        df = df[np.isfinite(df["temperature"].to_numpy(dtype=float))]
        df = df.sort_values("timestamp")
        df = df.drop_duplicates(
            subset=["timestamp"]
        ).reset_index(drop=True)

        if len(df) < 20:
            st.error("The uploaded CSV must contain at least 20 valid readings.")
            st.stop()

        st.success(f"Using uploaded dataset: {uploaded_file.name}")
    except Exception as exc:
        st.error(f"Could not read the uploaded CSV: {exc}")
        st.stop()
else:
    if not DATASET_FILE.exists():
        st.error(
            "The real sensor dataset could not be found."
        )

        st.write(
            "Please check that the dataset is located inside "
            "the DATASET folder, including the nested "
            "'DB elder monitoring' folder."
        )

        st.stop()

    df = load_data(
        str(DATASET_FILE),
        DATASET_FILE.stat().st_mtime,
    )


if len(df) < 20:
    st.error(
        "The dataset does not contain enough valid "
        "temperature readings."
    )
    st.stop()


# =========================================================
# PREPARE THE SIGNAL
# =========================================================

# Work with actual elapsed time, not row numbers.
time_seconds = (
    df["timestamp"] - df["timestamp"].iloc[0]
).dt.total_seconds().to_numpy()

temperature = df["temperature"].to_numpy(
    dtype=float
)

if not np.all(np.isfinite(temperature)):
    st.error("Temperature data contains invalid values.")
    st.stop()

if np.any(np.diff(time_seconds) <= 0):
    st.error(
        "Sensor timestamps must be strictly increasing."
    )
    st.stop()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("📊 DSP Mini-Project")

st.sidebar.caption(
    "Interpolation for Smooth Reconstruction "
    "of Sensor Signals"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Sensor Signal",
        "Interpolation Results",
        "Performance Comparison",
        "Data Table",
        "Project Summary",
    ],
)

st.sidebar.divider()

st.sidebar.subheader("Dataset Information")

st.sidebar.write(
    "Dataset: UCI Single Elder Home Monitoring"
)

st.sidebar.write(
    "Signal: Temperature (°C)"
)

st.sidebar.write(
    f"Valid readings: {len(df):,}"
)

st.sidebar.caption(
    "Interpolation estimates intermediate values. "
    "It does not create new sensor measurements."
)


# =========================================================
# EXPERIMENT CONTROLS
# =========================================================

st.subheader("⚙️ Experiment Controls")

control1, control2 = st.columns([2, 2])

with control1:
    sparse_count = st.slider(
        "Number of sparse samples",
        min_value=4,
        max_value=min(250, len(df)),
        value=min(20, len(df)),
        step=1,
        help=(
            "Choose the number of recorded samples used "
            "to reconstruct the signal."
        ),
    )

with control2:
    display_method = st.radio(
        "Interpolation method",
        [
            "Both",
            "Linear only",
            "Cubic only",
        ],
        horizontal=True,
    )


# =========================================================
# SELECT SPARSE SAMPLES
# =========================================================

sample_indices = np.unique(
    np.linspace(
        0,
        len(df) - 1,
        num=sparse_count,
        dtype=int,
    )
)

sample_times = time_seconds[sample_indices]

sample_temperatures = temperature[sample_indices]


# =========================================================
# PERFORM INTERPOLATION
# =========================================================

linear_values = np.interp(
    time_seconds,
    sample_times,
    sample_temperatures,
)

cubic_values = None

if len(sample_indices) >= 4:
    cubic_function = interp1d(
        sample_times,
        sample_temperatures,
        kind="cubic",
        bounds_error=True,
    )

    cubic_values = cubic_function(
        time_seconds
    )


# =========================================================
# HELD-OUT EVALUATION
# =========================================================

sample_mask = np.zeros(
    len(df),
    dtype=bool,
)

sample_mask[sample_indices] = True

test_mask = ~sample_mask


def calculate_metrics(estimate, actual, mask):
    """Calculate MAE and RMSE on held-out readings."""

    if not np.any(mask):
        return float("nan"), float("nan")

    errors = estimate[mask] - actual[mask]

    mae = float(
        np.mean(np.abs(errors))
    )

    rmse = float(
        np.sqrt(np.mean(errors ** 2))
    )

    return mae, rmse


linear_mae, linear_rmse = calculate_metrics(
    linear_values,
    temperature,
    test_mask,
)

if cubic_values is not None:
    cubic_mae, cubic_rmse = calculate_metrics(
        cubic_values,
        temperature,
        test_mask,
    )
else:
    cubic_mae = float("nan")
    cubic_rmse = float("nan")


# =========================================================
# REUSABLE SIGNAL PLOT
# =========================================================

def plot_signal(show_linear=True, show_cubic=True):
    """Plot the original signal and interpolation estimates."""

    fig, ax = plt.subplots(
        figsize=(14, 6)
    )

    # White graph background for readability.
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.plot(
        df["timestamp"],
        temperature,
        label="Original sensor readings",
        color="#1687d9",
        linewidth=1.1,
        alpha=0.95,
    )

    if show_linear:
        ax.plot(
            df["timestamp"],
            linear_values,
            label="Linear interpolation",
            color="#ff8c00",
            linewidth=1.8,
        )

    if show_cubic and cubic_values is not None:
        ax.plot(
            df["timestamp"],
            cubic_values,
            label="Cubic interpolation",
            color="#159447",
            linewidth=1.8,
        )

    ax.scatter(
        df["timestamp"].iloc[sample_indices],
        sample_temperatures,
        label="Sparse samples",
        color="#1769aa",
        s=28,
        zorder=3,
    )

    ax.set_title(
        "Real Sensor Temperature Reconstruction",
        fontsize=15,
        color="#172033",
    )

    ax.set_xlabel(
        "Timestamp",
        color="#172033",
    )

    ax.set_ylabel(
        "Temperature (°C)",
        color="#172033",
    )

    ax.tick_params(
        axis="both",
        colors="#172033",
    )

    ax.grid(
        True,
        color="#d8dee8",
        alpha=0.7,
    )

    ax.legend(
        facecolor="white",
        edgecolor="#cbd5e1",
        labelcolor="#172033",
    )

    ax.xaxis.set_major_locator(
        mdates.AutoDateLocator()
    )

    ax.xaxis.set_major_formatter(
        mdates.ConciseDateFormatter(
            ax.xaxis.get_major_locator()
        )
    )

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    st.subheader("🏠 Project Overview")

    st.write(
        "This interactive dashboard demonstrates how "
        "linear and cubic interpolation estimate "
        "intermediate values from real temperature "
        "sensor measurements."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Readings",
        f"{len(df):,}",
    )

    col2.metric(
        "Mean Temperature",
        f"{temperature.mean():.2f} °C",
    )

    col3.metric(
        "Minimum Temperature",
        f"{temperature.min():.2f} °C",
    )

    col4.metric(
        "Maximum Temperature",
        f"{temperature.max():.2f} °C",
    )

    st.divider()

    st.subheader("📈 Temperature Signal Comparison")

    fig = plot_signal(
        show_linear=display_method in [
            "Both",
            "Linear only",
        ],
        show_cubic=display_method in [
            "Both",
            "Cubic only",
        ],
    )

    st.pyplot(
        fig,
        use_container_width=True,
    )

    plt.close(fig)

    st.caption(
        "Change the sparse sample count above to observe "
        "how reconstruction changes."
    )


# =========================================================
# SENSOR SIGNAL PAGE
# =========================================================

elif page == "Sensor Signal":

    st.subheader("📈 Real Temperature Sensor Signal")

    st.write(
        "This graph displays the original recorded "
        "temperature measurements together with the "
        "selected interpolation estimates."
    )

    fig = plot_signal(
        show_linear=display_method in [
            "Both",
            "Linear only",
        ],
        show_cubic=display_method in [
            "Both",
            "Cubic only",
        ],
    )

    st.pyplot(
        fig,
        use_container_width=True,
    )

    plt.close(fig)

    st.subheader("Signal Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Mean",
        f"{temperature.mean():.3f} °C",
    )

    c2.metric(
        "Standard Deviation",
        f"{temperature.std():.3f} °C",
    )

    c3.metric(
        "Temperature Range",
        f"{temperature.max() - temperature.min():.3f} °C",
    )

    st.write(
        f"First timestamp: {df['timestamp'].iloc[0]}"
    )

    st.write(
        f"Last timestamp: {df['timestamp'].iloc[-1]}"
    )


# =========================================================
# INTERPOLATION RESULTS PAGE
# =========================================================

elif page == "Interpolation Results":

    st.subheader("🔬 Interpolation Results")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Original Readings",
        f"{len(df):,}",
    )

    c2.metric(
        "Sparse Samples",
        f"{len(sample_indices):,}",
    )

    c3.metric(
        "Held-Out Readings",
        f"{int(test_mask.sum()):,}",
    )

    st.info(
        "The held-out readings are excluded from the "
        "sparse sample set and are used to evaluate "
        "interpolation estimates. They are recorded "
        "sensor values, not independent ground truth."
    )

    fig = plot_signal(
        show_linear=display_method in [
            "Both",
            "Linear only",
        ],
        show_cubic=display_method in [
            "Both",
            "Cubic only",
        ],
    )

    st.pyplot(
        fig,
        use_container_width=True,
    )

    plt.close(fig)

    results = pd.DataFrame({
        "timestamp": df["timestamp"],
        "original_temperature_C": temperature,
        "linear_interpolation_C": linear_values,
        "used_as_sparse_sample": sample_mask,
    })

    if cubic_values is not None:
        results["cubic_interpolation_C"] = cubic_values

    st.subheader("Estimated and Recorded Values")

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇️ Download interpolation results CSV",
        data=results.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="dsp_interpolation_results.csv",
        mime="text/csv",
    )


# =========================================================
# PERFORMANCE COMPARISON PAGE
# =========================================================

elif page == "Performance Comparison":

    st.subheader("📊 Interpolation Performance Comparison")

    st.write(
        "Lower MAE and RMSE indicate closer agreement "
        "with the held-out recorded readings in this experiment."
    )

    st.caption(
        "Metrics are recalculated for the selected sparse "
        "sample count. The same held-out readings are used "
        "to compare both interpolation methods."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Linear Interpolation")

        st.metric(
            "Mean Absolute Error (MAE)",
            f"{linear_mae:.5f} °C",
        )

        st.metric(
            "Root Mean Squared Error (RMSE)",
            f"{linear_rmse:.5f} °C",
        )

    with col2:
        st.markdown("### Cubic Interpolation")

        if cubic_values is not None:
            st.metric(
                "Mean Absolute Error (MAE)",
                f"{cubic_mae:.5f} °C",
            )

            st.metric(
                "Root Mean Squared Error (RMSE)",
                f"{cubic_rmse:.5f} °C",
            )
        else:
            st.warning(
                "Cubic interpolation requires at least "
                "four sparse samples."
            )

    if cubic_values is not None:

        metrics_df = pd.DataFrame({
            "Method": [
                "Linear Interpolation",
                "Cubic Interpolation",
            ],
            "MAE (°C)": [
                linear_mae,
                cubic_mae,
            ],
            "RMSE (°C)": [
                linear_rmse,
                cubic_rmse,
            ],
        })

        st.subheader("Performance Metrics Table")

        st.dataframe(
            metrics_df,
            use_container_width=True,
            hide_index=True,
        )

        fig, ax = plt.subplots(
            figsize=(9, 5)
        )

        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        x = np.arange(2)
        width = 0.32

        ax.bar(
            x - width / 2,
            [linear_mae, cubic_mae],
            width,
            label="MAE",
            color="#1687d9",
        )

        ax.bar(
            x + width / 2,
            [linear_rmse, cubic_rmse],
            width,
            label="RMSE",
            color="#159447",
        )

        ax.set_xticks(x)

        ax.set_xticklabels([
            "Linear",
            "Cubic",
        ])

        ax.set_ylabel(
            "Error (°C)",
            color="#172033",
        )

        ax.set_title(
            "Interpolation Error Comparison",
            color="#172033",
        )

        ax.tick_params(
            axis="both",
            colors="#172033",
        )

        ax.legend(
            facecolor="white",
            labelcolor="#172033",
        )

        ax.grid(
            axis="y",
            color="#d8dee8",
            alpha=0.7,
        )

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True,
        )

        plt.close(fig)

        if (
            linear_mae < cubic_mae
            and linear_rmse < cubic_rmse
        ):
            st.success(
                "Linear interpolation has lower MAE and RMSE "
                "for this selected experiment."
            )

        elif (
            cubic_mae < linear_mae
            and cubic_rmse < linear_rmse
        ):
            st.success(
                "Cubic interpolation has lower MAE and RMSE "
                "for this selected experiment."
            )

        else:
            st.info(
                "The methods have mixed results across MAE "
                "and RMSE, or their errors are equal."
            )

        st.download_button(
            "⬇️ Download performance metrics CSV",
            data=metrics_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="interpolation_performance_metrics.csv",
            mime="text/csv",
        )


# =========================================================
# DATA TABLE PAGE
# =========================================================

elif page == "Data Table":

    st.subheader("📋 Temperature Dataset")

    st.write(
        "Browse the recorded temperature readings."
    )

    st.dataframe(
        df[
            [
                "timestamp",
                "temperature",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇️ Download temperature sensor data",
        data=df[
            [
                "timestamp",
                "temperature",
            ]
        ].to_csv(
            index=False
        ).encode("utf-8"),
        file_name="temperature_sensor_data.csv",
        mime="text/csv",
    )


# =========================================================
# PROJECT SUMMARY PAGE
# =========================================================

elif page == "Project Summary":

    st.subheader("📝 Project Summary")

    st.markdown(
        """
        ### Project Title

        **Interpolation for Smooth Reconstruction of Sensor Signals**

        ### Objective

        Study interpolation methods that estimate values
        between recorded temperature sensor samples.

        ### Dataset

        UCI Single Elder Home Monitoring dataset.

        ### Methods

        - Linear interpolation
        - Cubic interpolation

        ### Evaluation Metrics

        - **MAE:** Mean Absolute Error
        - **RMSE:** Root Mean Squared Error

        ### Conclusion

        The dashboard lets users compare the estimated
        signals and evaluate errors against held-out
        recorded readings.

        ### Limitations

        - Interpolation estimates values; it does not
          create new sensor measurements.
        - Cubic interpolation may overshoot between samples.
        - Results depend on sample count and signal behavior.
        - Held-out sensor readings are reference values,
          not independent ground truth.
        """
    )

    st.divider()

    st.subheader("Current Experiment")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Readings",
        f"{len(df):,}",
    )

    c2.metric(
        "Sparse Samples",
        f"{len(sample_indices):,}",
    )

    c3.metric(
        "Mean Temperature",
        f"{temperature.mean():.3f} °C",
    )

    st.write(
        f"Minimum temperature: {temperature.min():.3f} °C"
    )

    st.write(
        f"Maximum temperature: {temperature.max():.3f} °C"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#ffffff;">
        <p>
        DSP Mini-Project · Real Sensor Signal Interpolation
        </p>
        <p>
        Built with Python, Streamlit, NumPy, Pandas,
        SciPy and Matplotlib
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

