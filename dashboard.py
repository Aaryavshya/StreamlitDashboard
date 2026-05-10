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

latest_value = latest_ref.get()

predicted_gas_value = db.reference("Pred_Gas/Gas")

predicted_gas = predicted_gas_value.get()

if latest_value is not None:
    st.metric("Current Voltage", latest_value)
else:
    st.metric("Current Voltage", "No data")

if predicted_gas is not None:
    st.metric("Predicted Gas: ",predicted_gas)
else:
    st.metric("Predicted Gas: Processing....")

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

    st.line_chart(df["voltage"])

else:
    st.write("No history data yet")

# Refresh dashboard
time.sleep(1)
st.rerun()
