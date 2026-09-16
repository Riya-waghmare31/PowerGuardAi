import pandas as pd


def overall_summary(df: pd.DataFrame) -> dict:
    return {
        "total_records": len(df),
        "average_bill": df["ElectricityBill"].mean(),
        "average_hours": df["MonthlyHours"].mean(),
        "average_tariff": df["TariffRate"].mean(),
        "high_risk": int((df["Risk Level"] == "HIGH").sum()),
        "average_risk": df["Risk Score"].mean(),
    }


def monthly_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Month", as_index=False)
        .agg(
            Average=("ElectricityBill", "mean"),
            Maximum=("ElectricityBill", "max"),
            Minimum=("ElectricityBill", "min"),
            Records=("ElectricityBill", "size"),
            AverageRisk=("Risk Score", "mean"),
        )
        .sort_values("Month")
    )


def city_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("City", as_index=False)
        .agg(
            Records=("ElectricityBill", "size"),
            AverageBill=("ElectricityBill", "mean"),
            TotalBill=("ElectricityBill", "sum"),
            AverageHours=("MonthlyHours", "mean"),
            AverageRisk=("Risk Score", "mean"),
        )
        .sort_values("AverageBill", ascending=False)
    )


def company_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Company", as_index=False)
        .agg(
            Records=("ElectricityBill", "size"),
            AverageBill=("ElectricityBill", "mean"),
            TotalBill=("ElectricityBill", "sum"),
            AverageHours=("MonthlyHours", "mean"),
            AverageRisk=("Risk Score", "mean"),
        )
        .sort_values("AverageBill", ascending=False)
    )


def appliance_analysis(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "Fan",
        "Refrigerator",
        "AirConditioner",
        "Television",
        "Monitor",
        "MotorPump",
    ]

    return pd.DataFrame(
        {
            "Appliance": columns,
            "Average Usage": [df[column].mean() for column in columns],
            "Total Usage": [df[column].sum() for column in columns],
            "Bill Correlation": [
                df[column].corr(df["ElectricityBill"]) for column in columns
            ],
        }
    )


def highest_risk_records(df: pd.DataFrame, limit: int = 100) -> pd.DataFrame:
    return df.sort_values("Risk Score", ascending=False).head(limit)


def bill_statistics(df: pd.DataFrame) -> dict:
    return df["ElectricityBill"].describe().to_dict()


def hours_statistics(df: pd.DataFrame) -> dict:
    return df["MonthlyHours"].describe().to_dict()


def tariff_statistics(df: pd.DataFrame) -> dict:
    return df["TariffRate"].describe().to_dict()
