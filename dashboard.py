import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import time

# Initialize Firebase safely
if not firebase_admin._apps:
    firebase_config = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_config)

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://fir-iot-d62c6-default-rtdb.asia-southeast1.firebasedatabase.app/"
        },
    )

# Web Application
st.title("IoT Sensor Dashboard")

st.write("Web Application Dashboard: SnO2-BN based gas sensing ")

# Read latest voltage
latest_ref = db.reference("FireBaseIOT/R")

ref_gas = db.reference("Pred_Gas/Gas")
ref_concentration = db.reference("Pred_Gas/Concentration")
ref_timestamp = db.reference("Pred_Gas/TimeStamp")

latest_value = latest_ref.get()
predicted_gas = ref_gas.get()
predicted_concentration = ref_concentration.get()
session_timestamp = ref_timestamp.get()


col1, col2 = st.columns(2)

if session_timestamp is not None:
    col1.metric("Session Timestamp: ", session_timestamp)
else:
    col1.metric("Session Timestamp: ","fetching...")

if predicted_gas is not None:
    col1.metric("Predicted Gas: ", predicted_gas)
else:
    col1.metric("Predicted Gas: ","Processing...")

if predicted_concentration is not None:
    col2.metric("Predicted Concentration: ", predicted_concentration)
else:
    col2.metric("Predicted Concentration: ","Processing...")

if latest_value is not None:
    col1.metric("Current Resistance", latest_value)
else:
    col1.metric("Current Resistance", "No data")

# Read history
history_ref = db.reference("FireBaseIOT/Latest")

data = history_ref.get()

if data:

    rows = []

    for t, v in data.items():
        rows.append(
            {
                "timestamp": int(t),
                "voltage": v,
            }
        )

    df = pd.DataFrame(rows)

    df = df.sort_values("timestamp")

    st.line_chart(df["voltage"],x_label="Sample points",y_label="Resistance")

    # st.write()

else:
    st.write("No history data yet")

# Refresh dashboard
time.sleep(1)
st.rerun()
