import streamlit as st
import pandas as pd
import joblib


# -----------------------------
# Load trained ML model
# -----------------------------
model = joblib.load("battery_soh_model.pkl")


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="RE-VOLT AI",
    page_icon="🔋",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------
st.title("🔋 RE-VOLT AI")
st.subheader("EV Battery Circularity & Second-Life Assessment")

st.write(
    "Enter battery parameters to estimate State of Health (SOH) "
    "using the machine learning model."
)


# -----------------------------
# Input section
# -----------------------------
st.header("Battery Information")

col1, col2 = st.columns(2)

with col1:
    voltage = st.number_input(
        "Battery Voltage (V)",
        min_value=0.0,
        max_value=5.0,
        value=3.9
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-20.0,
        max_value=100.0,
        value=30.0
    )

    capacity = st.number_input(
        "Measured Capacity (Ah)",
        min_value=0.0,
        value=3.7
    )

with col2:
    cycles = st.number_input(
        "Cycle Count",
        min_value=0,
        value=350
    )

    resistance = st.number_input(
        "Internal Resistance (mΩ)",
        min_value=0.0,
        value=30.0
    )


# -----------------------------
# Analyze button
# -----------------------------
if st.button("🔍 Analyze Battery"):

    input_data = pd.DataFrame([{
        "voltage": voltage,
        "temperature": temperature,
        "capacity": capacity,
        "cycles": cycles,
        "resistance": resistance
    }])

    # ML prediction
    predicted_soh = model.predict(input_data)[0]

    # Keep SOH between 0 and 100
    predicted_soh = max(0, min(100, predicted_soh))

    predicted_soh = round(predicted_soh, 2)


    # -----------------------------
    # Decision logic
    # -----------------------------
    if (
        predicted_soh >= 80
        and temperature <= 45
        and resistance <= 80
    ):

        condition = "REUSE"

        recommendation = (
            "The battery shows relatively strong health "
            "in this prototype assessment. Professional "
            "safety testing is required before continued use."
        )

        applications = [
            "EV / Mobility",
            "Energy Storage",
            "High-demand applications"
        ]


    elif (
        predicted_soh >= 60
        and temperature <= 50
        and resistance <= 120
    ):

        condition = "SECOND LIFE"

        recommendation = (
            "The battery may be suitable for lower-demand "
            "second-life applications after proper electrical "
            "and safety testing."
        )

        applications = [
            "Solar Energy Storage",
            "Backup Power",
            "Telecom Backup",
            "Street Lighting",
            "Microgrid Storage"
        ]


    elif predicted_soh >= 40:

        condition = "FURTHER TESTING"

        recommendation = (
            "Additional battery diagnostics are recommended "
            "before deciding on reuse."
        )

        applications = [
            "Diagnostic Testing",
            "Cell-Level Assessment"
        ]


    else:

        condition = "RECYCLE"

        recommendation = (
            "The prototype assessment indicates poor condition. "
            "Professional end-of-life evaluation and recycling "
            "should be considered."
        )

        applications = [
            "Material Recovery",
            "Battery Recycling"
        ]


    # -----------------------------
    # Display result
    # -----------------------------
    st.divider()

    st.header("🔋 Battery Assessment")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Estimated SOH",
            f"{predicted_soh}%"
        )

    with col2:
        st.metric(
            "Condition",
            condition
        )


    st.subheader("Recommendation")

    st.info(recommendation)


    st.subheader("Suggested Applications")

    for application in applications:
        st.write("•", application)


    # -----------------------------
    # Safety warning
    # -----------------------------
    if temperature > 45:

        st.warning(
            "⚠️ Elevated temperature detected. "
            "Do not rely on this prototype result "
            "for battery safety decisions."
        )

    elif resistance > 120:

        st.warning(
            "⚠️ High internal resistance detected. "
            "Additional diagnostic testing is required."
        )


st.divider()

st.caption(
    "Prototype ML assessment — not a certified battery diagnostic system."
)
