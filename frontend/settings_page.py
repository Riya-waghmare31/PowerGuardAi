import streamlit as st


def render_settings():
    st.subheader("Settings")

    st.info("Risk thresholds are currently applied as LOW: 0–39, MODERATE: 40–69, HIGH: 70–100.")

    st.write("### AI Model")
    st.write("Isolation Forest")
    st.write("Statistical Analysis")

    st.write("### Risk Thresholds")

    low_threshold = st.number_input(
        "Maximum LOW score",
        min_value=1,
        max_value=98,
        value=39,
    )

    high_threshold = st.number_input(
        "Maximum MODERATE score",
        min_value=low_threshold + 1,
        max_value=99,
        value=69,
    )

    st.caption(
        f"Configured display thresholds: LOW 0–{low_threshold}, "
        f"MODERATE {low_threshold + 1}–{high_threshold}, "
        f"HIGH {high_threshold + 1}–100."
    )

    st.number_input(
        "Records per page",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
    )

    st.checkbox("Enable anomaly notifications", value=True)

    if st.button("Reset filters"):
        st.session_state.clear()
        st.rerun()
