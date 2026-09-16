from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


NUMERIC_COLUMNS = [
    "Fan",
    "Refrigerator",
    "AirConditioner",
    "Television",
    "Monitor",
    "MotorPump",
    "Month",
    "MonthlyHours",
    "TariffRate",
    "ElectricityBill",
]

CATEGORICAL_COLUMNS = ["City", "Company"]

REQUIRED_COLUMNS = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS


def validate_columns(df: pd.DataFrame) -> list[str]:
    """Return required columns missing from a DataFrame."""
    return [column for column in REQUIRED_COLUMNS if column not in df.columns]


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean the source data without modifying the CSV."""
    missing = validate_columns(df)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    result = df[REQUIRED_COLUMNS].copy()

    for column in NUMERIC_COLUMNS:
        result[column] = pd.to_numeric(result[column], errors="coerce")

    for column in CATEGORICAL_COLUMNS:
        result[column] = result[column].fillna("Unknown").astype(str).str.strip()

    result[NUMERIC_COLUMNS] = result[NUMERIC_COLUMNS].replace(
        [np.inf, -np.inf], np.nan
    )

    result[NUMERIC_COLUMNS] = result[NUMERIC_COLUMNS].fillna(
        result[NUMERIC_COLUMNS].median()
    )

    result = result.drop_duplicates().reset_index(drop=True)
    result.insert(0, "Record ID", [f"REC-{i:05d}" for i in range(1, len(result) + 1)])

    return result


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load and clean a CSV file."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            "electricity_bill_dataset.csv was not found. "
            "Please place the dataset in the project root folder."
        )

    return clean_dataframe(pd.read_csv(path))


def filter_dataframe(
    df: pd.DataFrame,
    cities: Optional[list[str]] = None,
    companies: Optional[list[str]] = None,
    months: Optional[list[int]] = None,
    risk_levels: Optional[list[str]] = None,
    min_bill: Optional[float] = None,
    max_bill: Optional[float] = None,
) -> pd.DataFrame:
    """Apply reusable dashboard filters."""
    result = df.copy()

    if cities:
        result = result[result["City"].isin(cities)]

    if companies:
        result = result[result["Company"].isin(companies)]

    if months:
        result = result[result["Month"].isin(months)]

    if risk_levels and "Risk Level" in result.columns:
        result = result[result["Risk Level"].isin(risk_levels)]

    if min_bill is not None:
        result = result[result["ElectricityBill"] >= min_bill]

    if max_bill is not None:
        result = result[result["ElectricityBill"] <= max_bill]

    return result


def basic_summary(df: pd.DataFrame) -> dict:
    """Return overall data summary."""
    return {
        "records": len(df),
        "cities": df["City"].nunique(),
        "companies": df["Company"].nunique(),
        "average_bill": df["ElectricityBill"].mean(),
        "average_hours": df["MonthlyHours"].mean(),
        "average_tariff": df["TariffRate"].mean(),
    }
