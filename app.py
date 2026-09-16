from pathlib import Path
import io

import streamlit as st

from backend.anomaly_detection import detect_anomalies
from backend.data_processing import load_csv, clean_dataframe
from backend.database import initialize_database, log_processing
from backend.risk_scoring import calculate_risk_scores

from frontend.analytics_page import render_analytics
from frontend.anomaly_page import render_anomaly_page
from frontend.dashboard import render_dashboard
from frontend.reports_page import render_reports
from frontend.settings_page import render_settings


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PowerGuard AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM LIGHT UI
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN APPLICATION
       ===================================================== */

    [data-testid="stAppViewContainer"] {
        background-color: #f5f7fa;
        color: #1f2937;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] * {
        color: #1f2937;
    }

    .sidebar-title {
        color: #159570;
        font-weight: 800;
        font-size: 1.35rem;
        letter-spacing: 0.04em;
        margin-bottom: 1.5rem;
        padding-top: 0.5rem;
    }


    /* =====================================================
       MAIN TITLE
       ===================================================== */

    .powerguard-title {
        color: #172033;
        font-size: 2.15rem;
        font-weight: 750;
        letter-spacing: -0.035em;
        margin-bottom: 0.2rem;
    }

    .powerguard-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
    }

    div[data-testid="stMetricValue"] {
        color: #172033;
        font-weight: 700;
    }

    div[data-testid="stMetricDelta"] {
        color: #159570;
    }


    /* =====================================================
       STATUS BOX
       ===================================================== */

    .status-box {
        background-color: #f0fdf9;
        border: 1px solid #c7eee1;
        border-radius: 12px;
        padding: 14px;
        margin-top: 20px;
        font-size: 0.88rem;
        line-height: 1.8;
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1,
    h2,
    h3 {
        color: #172033;
    }

    h4,
    h5,
    h6 {
        color: #334155;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        background-color: #159570;
        color: #ffffff;
        border: 1px solid #159570;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.45rem 1rem;
    }

    .stButton > button:hover {
        background-color: #117d5e;
        color: #ffffff;
        border-color: #117d5e;
    }


    /* =====================================================
       DOWNLOAD BUTTON
       ===================================================== */

    .stDownloadButton > button {
        background-color: #ffffff;
        color: #159570;
        border: 1px solid #159570;
        border-radius: 8px;
        font-weight: 600;
    }

    .stDownloadButton > button:hover {
        background-color: #f0fdf9;
        color: #117d5e;
        border-color: #117d5e;
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    div[data-baseweb="select"] > div {
        background-color: #ffffff;
        border-radius: 8px;
        border-color: #dbe3ec;
    }

    div[data-baseweb="input"] > div {
        background-color: #ffffff;
        border-radius: 8px;
        border-color: #dbe3ec;
    }

    input {
        color: #1f2937;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {
        background-color: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 10px;
        padding: 5px;
    }


    /* =====================================================
       SIDEBAR NAVIGATION
       ===================================================== */

    [data-testid="stSidebar"] .stRadio label {
        color: #334155;
        font-weight: 500;
    }


    /* =====================================================
       SUCCESS MESSAGE
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =====================================================
       CAPTION
       ===================================================== */

    .stCaption {
        color: #64748b;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border-color: #e2e8f0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATASET PATH
# =========================================================

DATASET_PATH = Path(__file__).parent / "electricity_bill_dataset.csv"


# =========================================================
# LOAD AND ANALYZE DATA
# =========================================================

@st.cache_data(show_spinner="Loading and analyzing electricity data...")
def load_and_analyze(source_bytes=None):

    if source_bytes is None:
        df = load_csv(DATASET_PATH)

    else:
        df = load_csv_from_bytes(source_bytes)

    analyzed_df, _ = detect_anomalies(df)

    analyzed_df = calculate_risk_scores(analyzed_df)

    return analyzed_df


# =========================================================
# LOAD UPLOADED CSV
# =========================================================

def load_csv_from_bytes(source_bytes):

    df = clean_dataframe(
        __import__("pandas").read_csv(
            io.BytesIO(source_bytes)
        )
    )

    return df


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    # -----------------------------------------------------
    # INITIALIZE DATABASE
    # -----------------------------------------------------

    initialize_database()


    # -----------------------------------------------------
    # CHECK DATASET
    # -----------------------------------------------------

    if not DATASET_PATH.exists():

        st.error(
            "electricity_bill_dataset.csv was not found. "
            "Please place the dataset in the project root folder."
        )

        st.stop()


    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-title">⚡ POWERGUARD AI</div>',
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # CSV UPLOAD
        # -------------------------------------------------

        st.markdown("### Dataset")

        uploaded_file = st.file_uploader(
            "Optional replacement CSV",
            type=["csv"],
            help=(
                "Upload another electricity dataset. "
                "The file must contain the required columns."
            ),
        )


        # -------------------------------------------------
        # LOAD DATA
        # -------------------------------------------------

        try:

            if uploaded_file is not None:

                df = load_and_analyze(
                    uploaded_file.getvalue()
                )

                st.success(
                    "Uploaded dataset connected."
                )

            else:

                df = load_and_analyze()

                st.success(
                    "Default dataset connected."
                )

        except ValueError as error:

            st.error(str(error))

            st.stop()

        except Exception as error:

            st.error(
                f"Unable to process the dataset: {error}"
            )

            st.stop()


        # -------------------------------------------------
        # DATABASE LOG
        # -------------------------------------------------

        log_processing(len(df))


        # -------------------------------------------------
        # NAVIGATION
        # -------------------------------------------------

        st.markdown("### Navigation")

        page = st.radio(
            "Select a page",
            [
                "Dashboard",
                "Electricity Bills",
                "Consumption Analysis",
                "AI Anomaly Detection",
                "City Analysis",
                "Company Analysis",
                "Appliance Analysis",
                "Reports",
                "Settings",
            ],
            label_visibility="collapsed",
        )


        # -------------------------------------------------
        # AI MODEL STATUS
        # -------------------------------------------------

        st.markdown(
            """
            <div class="status-box">

            <b>AI Model Status</b><br>

            🟢 Isolation Forest<br>

            🟢 Statistical Analysis<br>

            🟢 Dataset Connected

            </div>
            """,
            unsafe_allow_html=True,
        )


    # =====================================================
    # MAIN HEADER
    # =====================================================

    st.markdown(
        """
        <div class="powerguard-title">
            AI Electricity Consumption & Anomaly Detection System
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="powerguard-subtitle">
            Smart Electricity Monitoring Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Dataset: electricity_bill_dataset.csv  |  "
        "Model: Isolation Forest + Statistical Rules"
    )


    # =====================================================
    # PAGE ROUTING
    # =====================================================

    if page == "Dashboard":

        render_dashboard(df)


    elif page == "Electricity Bills":

        render_electricity_bills(df)


    elif page == "Consumption Analysis":

        render_analytics(
            df,
            "Consumption Analysis"
        )


    elif page == "AI Anomaly Detection":

        render_anomaly_page(df)


    elif page == "City Analysis":

        render_analytics(
            df,
            "City Analysis"
        )


    elif page == "Company Analysis":

        render_analytics(
            df,
            "Company Analysis"
        )


    elif page == "Appliance Analysis":

        render_analytics(
            df,
            "Appliance Analysis"
        )


    elif page == "Reports":

        render_reports(df)


    elif page == "Settings":

        render_settings()


# =========================================================
# ELECTRICITY BILLS PAGE
# =========================================================

def render_electricity_bills(df):

    st.subheader("Electricity Bills")

    st.caption(
        "Search, filter and analyze electricity consumption records."
    )


    # =====================================================
    # FILTER SECTION
    # =====================================================

    left, right = st.columns(2)


    with left:

        cities = st.multiselect(
            "City",
            sorted(
                df["City"].unique()
            )
        )

        companies = st.multiselect(
            "Company",
            sorted(
                df["Company"].unique()
            )
        )

        months = st.multiselect(
            "Month",
            sorted(
                df["Month"].unique()
            )
        )


    with right:

        risks = st.multiselect(
            "Risk Level",
            [
                "LOW",
                "MODERATE",
                "HIGH",
            ],
        )


        bill_min = float(
            df["ElectricityBill"].min()
        )

        bill_max = float(
            df["ElectricityBill"].max()
        )


        bill_range = st.slider(
            "Electricity Bill Range",
            min_value=bill_min,
            max_value=bill_max,
            value=(
                bill_min,
                bill_max,
            ),
        )


    # =====================================================
    # APPLY FILTERS
    # =====================================================

    filtered = df.copy()


    if cities:

        filtered = filtered[
            filtered["City"].isin(cities)
        ]


    if companies:

        filtered = filtered[
            filtered["Company"].isin(companies)
        ]


    if months:

        filtered = filtered[
            filtered["Month"].isin(months)
        ]


    if risks:

        filtered = filtered[
            filtered["Risk Level"].isin(risks)
        ]


    filtered = filtered[
        filtered["ElectricityBill"].between(
            bill_range[0],
            bill_range[1]
        )
    ]


    # =====================================================
    # SEARCH
    # =====================================================

    search = st.text_input(
        "Search Record ID, City or Company"
    ).strip().lower()


    if search:

        filtered = filtered[
            filtered.apply(
                lambda row:
                search in (
                    str(row["Record ID"])
                    + " "
                    + str(row["City"])
                    + " "
                    + str(row["Company"])
                ).lower(),
                axis=1,
            )
        ]


    # =====================================================
    # RESULTS
    # =====================================================

    columns = [
        "Record ID",
        "City",
        "Company",
        "Month",
        "MonthlyHours",
        "TariffRate",
        "ElectricityBill",
        "Risk Score",
        "Risk Level",
    ]


    st.write(
        f"Showing {len(filtered):,} records"
    )


    st.dataframe(
        filtered[columns]
        .sort_values(
            "Risk Score",
            ascending=False
        )
        .head(1000),

        use_container_width=True,

        hide_index=True,
    )


    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.download_button(
        "Download Filtered CSV",

        filtered.to_csv(
            index=False
        ).encode("utf-8"),

        file_name="filtered_electricity_bills.csv",

        mime="text/csv",
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    main()