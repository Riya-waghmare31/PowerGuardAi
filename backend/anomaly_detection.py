import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


MODEL_FEATURES = [
    "Fan",
    "Refrigerator",
    "AirConditioner",
    "Television",
    "Monitor",
    "MotorPump",
    "MonthlyHours",
    "TariffRate",
    "ElectricityBill",
]


def _safe_zscore(series: pd.Series) -> pd.Series:
    standard_deviation = series.std()
    if standard_deviation == 0 or pd.isna(standard_deviation):
        return pd.Series(0.0, index=series.index)

    return ((series - series.mean()) / standard_deviation).abs().fillna(0)


def generate_reasons(df: pd.DataFrame) -> pd.Series:
    """Generate explanations from actual row values and dataset statistics."""
    bill_z = _safe_zscore(df["ElectricityBill"])
    hours_z = _safe_zscore(df["MonthlyHours"])
    tariff_z = _safe_zscore(df["TariffRate"])

    expected_bill = df["MonthlyHours"] * df["TariffRate"]
    ratio_z = _safe_zscore(
        df["ElectricityBill"] / expected_bill.replace(0, np.nan)
    )

    appliance_columns = [
        "Fan",
        "Refrigerator",
        "AirConditioner",
        "Television",
        "Monitor",
        "MotorPump",
    ]
    appliance_z = pd.concat(
        [_safe_zscore(df[column]) for column in appliance_columns], axis=1
    ).max(axis=1)

    reasons = []

    for index in df.index:
        checks = []

        if bill_z.loc[index] >= 2:
            checks.append("Electricity bill is significantly higher than the dataset average.")

        if hours_z.loc[index] >= 2:
            checks.append("Monthly usage hours are unusually high.")

        if ratio_z.loc[index] >= 2:
            checks.append("Unusual relationship between monthly hours, tariff and bill.")

        if tariff_z.loc[index] >= 2:
            checks.append("Tariff rate differs significantly from typical records.")

        if appliance_z.loc[index] >= 2:
            checks.append("One or more appliance usage values differ significantly from normal patterns.")

        if len(checks) >= 2:
            reasons.append("Multiple consumption indicators differ significantly from normal patterns.")
        elif checks:
            reasons.append(checks[0])
        else:
            reasons.append("Consumption pattern is within the expected range.")

    return pd.Series(reasons, index=df.index)


def detect_anomalies(
    df: pd.DataFrame,
    contamination: float = 0.03,
    random_state: int = 42,
) -> tuple[pd.DataFrame, IsolationForest]:
    """Train Isolation Forest and append anomaly fields."""
    result = df.copy()

    features = result[MODEL_FEATURES].astype(float)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    model = IsolationForest(
        n_estimators=180,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )

    predictions = model.fit_predict(scaled_features)
    raw_scores = -model.score_samples(scaled_features)

    min_score = raw_scores.min()
    max_score = raw_scores.max()

    if max_score == min_score:
        normalized_scores = np.zeros(len(raw_scores))
    else:
        normalized_scores = (raw_scores - min_score) / (max_score - min_score)

    result["anomaly_flag"] = predictions == -1
    result["anomaly_score"] = normalized_scores
    result["anomaly_reason"] = generate_reasons(result)

    return result, model
