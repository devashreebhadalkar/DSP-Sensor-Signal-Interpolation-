# ============================================================
# Program 08: Analyze Real Sensor Dataset
# Project: Interpolation for Smooth Reconstruction of Sensor Signals
#
# Purpose:
# 1. Load the real sensor dataset.
# 2. Display the column names and first five rows.
# 3. Inspect data types and missing values.
# 4. Display basic statistics for numeric columns.
#
# ============================================================

from pathlib import Path
import pandas as pd


# ------------------------------------------------------------
# 1. Define project and dataset paths
# ------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_DIR
    / "DATASET"
    / "single+elder+home+monitoring+gas+and+position"
    / "DB elder monitoring"
    / "data_ref_until_2020-02-13.csv"
)


# ------------------------------------------------------------
# 2. Check whether the dataset file exists
# ------------------------------------------------------------

print("=" * 70)
print("REAL SENSOR DATASET ANALYSIS")
print("Interpolation for Smooth Reconstruction of Sensor Signals")
print("=" * 70)

print("\nDataset path:")
print(DATASET_FILE)

if not DATASET_FILE.exists():
    print("\nERROR: Dataset file was not found!")
    print("\nPlease check the actual folder structure.")
    raise SystemExit(1)


# ------------------------------------------------------------
# 3. Load the CSV file
# ------------------------------------------------------------

print("\nLoading the dataset...")

try:
    df = pd.read_csv(DATASET_FILE)
except Exception as error:
    print("\nERROR while reading the CSV file:")
    print(error)
    raise SystemExit(1)

print("Dataset loaded successfully!")


# ------------------------------------------------------------
# 4. Display dataset dimensions
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATASET DIMENSIONS")
print("=" * 70)

print(f"Number of rows: {df.shape[0]:,}")
print(f"Number of columns: {df.shape[1]}")


# ------------------------------------------------------------
# 5. Display column names
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COLUMN NAMES")
print("=" * 70)

for column in df.columns:
    print(f"- {column}")


# ------------------------------------------------------------
# 6. Display the first five rows
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FIRST FIVE ROWS")
print("=" * 70)

print(df.head().to_string())


# ------------------------------------------------------------
# 7. Display data types
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

print(df.dtypes.to_string())


# ------------------------------------------------------------
# 8. Check missing values
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)

missing_values = df.isnull().sum()

print(missing_values.to_string())

print(f"\nTotal missing cells: {df.isnull().sum().sum():,}")


# ------------------------------------------------------------
# 9. Display numeric column names
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMERIC COLUMNS")
print("=" * 70)

numeric_df = df.select_dtypes(include="number")

if numeric_df.empty:
    print("No numeric columns were detected.")
else:
    for column in numeric_df.columns:
        print(f"- {column}")


# ------------------------------------------------------------
# 10. Display descriptive statistics
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMERIC DATA STATISTICS")
print("=" * 70)

if numeric_df.empty:
    print("No numeric statistics are available.")
else:
    print(numeric_df.describe().to_string())


# ------------------------------------------------------------
# 11. Finish
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INITIAL DATASET INSPECTION COMPLETED")
print("=" * 70)

print(
    "\nNext, we will identify the timestamp and temperature columns "
    "before plotting or interpolating the real measurements."
)

# End of Program 08