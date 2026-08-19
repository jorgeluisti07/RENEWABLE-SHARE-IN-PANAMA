"""Reshape wide-format hourly demand data (e.g. DEM2025.csv) into a
long-format time series: one row per hour, a datetime index, and a single
'Demand MW' column.

Source format: one row per day (first column = date), with columns
H1..H24 holding that day's 24 hourly demand values.
"""

import sys

import pandas as pd


def transform_demand(path: str) -> pd.DataFrame:
    """Melt a DEM-style wide CSV (date rows x H1..H24 columns) into an
    hourly time series indexed by datetime, with one 'Demand MW' column.

    Assumes H1..H24 are hour-ending labels, i.e. H1 = 00:00-01:00 and
    H24 = 23:00-00:00, so H<n> maps to timestamp Date + (n-1) hours.
    """
    df = pd.read_csv(path)
    df = df.rename(columns={df.columns[0]: "Date"})
    df["Date"] = pd.to_datetime(df["Date"])

    hour_cols = sorted(
        (c for c in df.columns if c.startswith("H") and c[1:].isdigit()),
        key=lambda c: int(c[1:]),
    )

    long_df = df.melt(id_vars="Date", value_vars=hour_cols, var_name="Hour", value_name="Demand MW")
    long_df["Hour"] = long_df["Hour"].str.extract(r"(\d+)").astype(int)
    long_df["Datetime"] = long_df["Date"] + pd.to_timedelta(long_df["Hour"] - 1, unit="h")

    return long_df.sort_values("Datetime").set_index("Datetime")[["Demand MW"]]


def transform_demand_daily(hourly: pd.DataFrame) -> pd.DataFrame:
    """Aggregate an hourly 'Demand MW' series (see transform_demand) to daily totals."""
    return hourly.resample("D").sum()


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "DEM2025.csv"
    hourly = transform_demand(src)
    hourly.to_csv("DEM2025_hourly.csv")
    transform_demand_daily(hourly).to_csv("DEM2025_daily.csv")
    print(hourly.head(24))
