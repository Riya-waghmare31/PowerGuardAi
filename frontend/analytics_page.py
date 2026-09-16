import plotly.express as px
import streamlit as st

from backend.analytics import appliance_analysis, city_analysis, company_analysis


def render_analytics(df, page: str):
    st.subheader(page)

    if page == "City Analysis":
        data = city_analysis(df)
        st.dataframe(data, use_container_width=True, hide_index=True)

        left, right = st.columns(2)

        with left:
            fig = px.bar(
                data,
                x="City",
                y="AverageBill",
                color="AverageBill",
                template="plotly_dark",
                title="Average Electricity Bill by City",
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.bar(
                data.sort_values("AverageRisk", ascending=False),
                x="City",
                y="AverageRisk",
                color="AverageRisk",
                color_continuous_scale="RdYlGn_r",
                template="plotly_dark",
                title="Average Risk Score by City",
            )
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Company Analysis":
        data = company_analysis(df)
        choice = st.radio("Companies to display", ["Top 5", "Top 10", "All"], horizontal=True)

        if choice == "Top 5":
            chart_data = data.head(5)
        elif choice == "Top 10":
            chart_data = data.head(10)
        else:
            chart_data = data

        st.dataframe(data, use_container_width=True, hide_index=True)

        fig = px.bar(
            chart_data,
            x="Company",
            y="AverageBill",
            color="AverageRisk",
            template="plotly_dark",
            title="Company Average Bill Comparison",
        )
        fig.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(fig, use_container_width=True)

    elif page == "Appliance Analysis":
        data = appliance_analysis(df)
        st.dataframe(data, use_container_width=True)

        left, right = st.columns(2)

        with left:
            fig = px.bar(
                data,
                x="Appliance",
                y="Average Usage",
                color="Appliance",
                template="plotly_dark",
                title="Average Appliance Usage",
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.bar(
                data,
                x="Appliance",
                y="Bill Correlation",
                color="Bill Correlation",
                color_continuous_scale="RdYlGn",
                template="plotly_dark",
                title="Appliance Correlation with Electricity Bill",
            )
            st.plotly_chart(fig, use_container_width=True)

        if df["MotorPump"].eq(0).all():
            st.info("MotorPump values are 0 across the current dataset.")

    elif page == "Consumption Analysis":
        render_consumption_analysis(df)


def render_consumption_analysis(df):
    cities = st.multiselect("City", sorted(df["City"].unique()))
    companies = st.multiselect("Company", sorted(df["Company"].unique()))
    months = st.multiselect("Month", sorted(df["Month"].unique()))

    filtered = df.copy()

    if cities:
        filtered = filtered[filtered["City"].isin(cities)]
    if companies:
        filtered = filtered[filtered["Company"].isin(companies)]
    if months:
        filtered = filtered[filtered["Month"].isin(months)]

    if filtered.empty:
        st.warning("No records match the selected filters.")
        return

    first, second = st.columns(2)

    with first:
        fig = px.scatter(
            filtered,
            x="MonthlyHours",
            y="ElectricityBill",
            color="Risk Level",
            hover_data=["Record ID", "City", "Company"],
            template="plotly_dark",
            title="Monthly Hours vs Electricity Bill",
        )
        st.plotly_chart(fig, use_container_width=True)

    with second:
        fig = px.scatter(
            filtered,
            x="TariffRate",
            y="ElectricityBill",
            color="Risk Level",
            hover_data=["Record ID", "City", "Company"],
            template="plotly_dark",
            title="Tariff Rate vs Electricity Bill",
        )
        st.plotly_chart(fig, use_container_width=True)

    first, second, third = st.columns(3)

    with first:
        st.plotly_chart(
            px.histogram(
                filtered,
                x="MonthlyHours",
                template="plotly_dark",
                title="Monthly Hours Distribution",
            ),
            use_container_width=True,
        )

    with second:
        st.plotly_chart(
            px.histogram(
                filtered,
                x="ElectricityBill",
                template="plotly_dark",
                title="Electricity Bill Distribution",
            ),
            use_container_width=True,
        )

    with third:
        st.plotly_chart(
            px.histogram(
                filtered,
                x="TariffRate",
                template="plotly_dark",
                title="Tariff Rate Distribution",
            ),
            use_container_width=True,
        )
