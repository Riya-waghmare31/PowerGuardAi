# PowerGuard AI

PowerGuard AI is a Python and Streamlit application for electricity consumption analytics and anomaly detection.

The system uses:

- Pandas for data processing
- Scikit-learn Isolation Forest for anomaly detection
- Statistical rules for risk explanations
- Plotly for interactive charts
- Streamlit for the complete frontend and application runtime

The application does not confirm electricity theft or fraud. It identifies unusual consumption patterns that may require investigation.

## Dataset

Place the following file in the project root:

```text
electricity_bill_dataset.csv
