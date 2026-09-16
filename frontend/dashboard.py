import plotly.express as px
import streamlit as st

from backend.analytics import city_analysis, monthly_analysis, overall_summary


def _money(value: float) -> str:
    return f"{value:,.2f}"


def render_dashboard(df):
    summary = overall_summary(df)

    st.subheader("Dashboard")
    st.caption("Smart Electricity Monitoring Dashboard")

    cards = [
        ("Total Records", f"{summary['total_records']:,}"),
        ("Average Electricity Bill", _money(summary["average_bill"])),
        ("Average Monthly Hours", f"{summary['average_hours']:,.2f}"),
        ("Average Tariff Rate", f"{summary['average_tariff']:,.2f}"),
        ("High-Risk Records", f"{summary['high_risk']:,}"),
        ("Average Risk Score", f"{summary['average_risk']:,.2f}/100"),
    ]

    columns = st.columns(6)
    for column, (label, value) in zip(columns, cards):
        with column:
            st.metric(label, value)

    st.markdown("### Monthly Electricity Bill Trend")

    monthly = monthly_analysis(df)
    measure = st.selectbox(
        "Trend metric",
        ["Average", "Maximum", "Minimum"],
        key="dashboard_month_metric",
    )

    figure = px.line(
        monthly,
        x="Month",
        y=measure,
        markers=True,
        template="plotly_dark",
        labels={measure: "Electricity Bill"},
    )
    figure.update_layout(height=390, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(figure, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Average Bill by City")
        cities = city_analysis(df).sort_values("AverageBill", ascending=False)
        figure = px.bar(
            cities,
            x="City",
            y="AverageBill",
            color="AverageBill",
            template="plotly_dark",
        )
        figure.update_layout(height=380, xaxis_tickangle=-40)
        st.plotly_chart(figure, use_container_width=True)

    with right:
        st.markdown("### Average Risk by City")
        figure = px.bar(
            cities.sort_values("AverageRisk", ascending=False),
            x="City",
            y="AverageRisk",
            color="AverageRisk",
            color_continuous_scale="RdYlGn_r",
            template="plotly_dark",
        )
        figure.update_layout(height=380, xaxis_tickangle=-40)
        st.plotly_chart(figure, use_container_width=True)
