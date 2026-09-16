import streamlit as st

from backend.analytics import (
    appliance_analysis,
    city_analysis,
    company_analysis,
    highest_risk_records,
    monthly_analysis,
)


def _csv_download(data, filename: str, label: str):
    st.download_button(
        label=label,
        data=data.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
    )


def render_reports(df):
    st.subheader("Reports")

    report_type = st.selectbox(
        "Select report",
        [
            "Monthly Electricity Report",
            "City Electricity Report",
            "Company Electricity Report",
            "Appliance Consumption Report",
            "High-Risk Anomaly Report",
            "Complete Dataset Report",
        ],
    )

    if report_type == "Monthly Electricity Report":
        report = monthly_analysis(df)
        filename = "monthly_electricity_report.csv"

    elif report_type == "City Electricity Report":
        report = city_analysis(df)
        filename = "city_electricity_report.csv"

    elif report_type == "Company Electricity Report":
        report = company_analysis(df)
        filename = "company_electricity_report.csv"

    elif report_type == "Appliance Consumption Report":
        report = appliance_analysis(df)
        filename = "appliance_consumption_report.csv"

    elif report_type == "High-Risk Anomaly Report":
        report = highest_risk_records(df)
        filename = "high_risk_anomaly_report.csv"

    else:
        report = df
        filename = "complete_dataset_report.csv"

    st.dataframe(report.head(500), use_container_width=True, hide_index=True)
    _csv_download(report, filename, "Download CSV Report")
