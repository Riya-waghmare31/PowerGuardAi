import numpy as np
import pandas as pd


def _absolute_zscore(series: pd.Series) -> pd.Series:
    deviation = series.std()
    if deviation == 0 or pd.isna(deviation):
        return pd.Series(0.0, index=series.index)

    return ((series - series.mean()) / deviation).abs().clip(0, 4) / 4


def calculate_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate an explainable risk score from 0 to 100."""
    result = df.copy()

    bill_deviation = _absolute_zscore(result["ElectricityBill"])
    hours_deviation = _absolute_zscore(result["MonthlyHours"])
    tariff_deviation = _absolute_zscore(result["TariffRate"])

    expected_bill = result["MonthlyHours"] * result["TariffRate"]
    bill_ratio = result["ElectricityBill"] / expected_bill.replace(0, np.nan)
    bill_ratio_deviation = _absolute_zscore(bill_ratio.fillna(bill_ratio.median()))

    appliance_columns = [
        "Fan",
        "Refrigerator",
        "AirConditioner",
        "Television",
        "Monitor",
        "MotorPump",
    ]

    appliance_deviations = pd.concat(
        [_absolute_zscore(result[column]) for column in appliance_columns],
        axis=1,
    ).mean(axis=1)

    anomaly_component = result["anomaly_score"].clip(0, 1)

    score = (
        anomaly_component * 40
        + bill_deviation * 20
        + hours_deviation * 15
        + tariff_deviation * 10
        + bill_ratio_deviation * 10
        + appliance_deviations * 5
    )

    result["Risk Score"] = score.clip(0, 100).round(2)
    result["Risk Level"] = pd.cut(
        result["Risk Score"],
        bins=[-np.inf, 39.999, 69.999, np.inf],
        labels=["LOW", "MODERATE", "HIGH"],
    ).astype(str)

    result["Anomaly Status"] = np.select(
        [
            result["Risk Level"].eq("HIGH"),
            result["Risk Level"].eq("MODERATE"),
        ],
        ["HIGH-RISK ANOMALY", "REVIEW"],
        default="NORMAL",
    )

    return result
