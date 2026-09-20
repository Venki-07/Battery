import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# 1. PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="RE-VOLT AI",
    page_icon="🔋",
    layout="wide"
)


# ============================================================
# 2. FIND THE MODEL FILE
# ============================================================

# Get the folder where this streamlit_app.py file is located
BASE_DIR = Path(__file__).resolve().parent

# The model should be in the same folder
MODEL_PATH = BASE_DIR / "battery_soh_model.pkl"


# ============================================================
# 3. LOAD THE ML MODEL
# ============================================================

try:

    model = joblib.load(MODEL_PATH)

except FileNotFoundError:

    st.error("❌ battery_soh_model.pkl was not found.")

    st.write("Streamlit is looking in:")
    st.code(str(MODEL_PATH))

    st.write("Files found in the backend folder:")

    try:
        files = [file.name for file in BASE_DIR.iterdir()]
        st.write(files)
    except Exception:
        st.write("Unable to display files.")

    st.warning(
        "Make sure battery_soh_model.pkl is uploaded "
        "inside the backend folder of your GitHub repository."
    )

    st.stop()


# ============================================================
# 4. TITLE
# ============================================================

st.title("🔋 RE-VOLT AI")

st.subheader(
    "EV Battery Circularity & Second-Life Assessment"
)

st.write(
    "Enter the battery parameters below to estimate "
    "the battery State of Health (SOH) using machine learning."
)


# ============================================================
# 5. BATTERY INPUT
# ============================================================

st.header("🔧 Battery Information")

col1, col2 = st.columns(2)


# ---------- LEFT COLUMN ----------

with col1:

    voltage = st.number_input(
        "Battery Voltage (V)",
        min_value=0.0,
        max_value=5.0,
        value=3.90,
        step=0.01
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-20.0,
        max_value=100.0,
        value=30.0,
        step=0.5
    )

    capacity = st.number_input(
        "Measured Capacity (Ah)",
        min_value=0.0,
        value=3.70,
        step=0.01
    )


# ---------- RIGHT COLUMN ----------

with col2:

    cycles = st.number_input(
        "Cycle Count",
        min_value=0,
        value=350,
        step=10
    )

    resistance = st.number_input(
        "Internal Resistance (mΩ)",
        min_value=0.0,
        value=30.0,
        step=1.0
    )


# ============================================================
# 6. ANALYZE BUTTON
# ============================================================

st.divider()

analyze = st.button(
    "🔍 Analyze Battery",
    use_container_width=True
)


# ============================================================
# 7. ML PREDICTION
# ============================================================

if analyze:

    # Create input dataframe
    input_data = pd.DataFrame([
        {
            "voltage": voltage,
            "temperature": temperature,
            "capacity": capacity,
            "cycles": cycles,
            "resistance": resistance
        }
    ])


    # --------------------------------------------------------
    # Predict SOH
    # --------------------------------------------------------

    try:

        predicted_soh = model.predict(input_data)[0]

        # Keep SOH between 0 and 100
        predicted_soh = max(
            0,
            min(100, predicted_soh)
        )

        predicted_soh = round(
            predicted_soh,
            2
        )

    except Exception as error:

        st.error(
            "❌ Error while running the ML model."
        )

        st.write(error)

        st.stop()


    # ========================================================
    # 8. BATTERY DECISION
    # ========================================================

    if (
        predicted_soh >= 80
        and temperature <= 45
        and resistance <= 80
    ):

        condition = "REUSE"

        recommendation = (
            "The battery shows relatively strong health "
            "in this prototype assessment. Professional "
            "electrical and safety testing is required "
            "before continued use."
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
            "before deciding on reuse or second-life deployment."
        )

        applications = [
            "Diagnostic Testing",
            "Cell-Level Assessment"
        ]


    else:

        condition = "RECYCLE"

        recommendation = (
            "The prototype assessment indicates poor condition. "
            "Professional end-of-life evaluation and appropriate "
            "battery recycling should be considered."
        )

        applications = [
            "Material Recovery",
            "Battery Recycling"
        ]


    # ========================================================
    # 9. DISPLAY RESULTS
    # ========================================================

    st.divider()

    st.header("📊 Battery Assessment")


    result_col1, result_col2 = st.columns(2)


    # SOH
    with result_col1:

        st.metric(
            label="Estimated SOH",
            value=f"{predicted_soh}%"
        )


    # Condition
    with result_col2:

        st.metric(
            label="Battery Status",
            value=condition
        )


    # ========================================================
    # 10. RECOMMENDATION
    # ========================================================

    st.subheader("💡 Recommendation")

    st.info(recommendation)


    # ========================================================
    # 11. SECOND-LIFE APPLICATIONS
    # ========================================================

    st.subheader("🔋 Suggested Applications")

    for application in applications:

        st.write(
            "• " + application
        )


    # ========================================================
    # 12. SAFETY WARNINGS
    # ========================================================

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


    # ========================================================
    # 13. INPUT SUMMARY
    # ========================================================

    st.subheader("📋 Battery Input Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)


    with summary_col1:

        st.write(
            f"**Voltage:** {voltage} V"
        )

        st.write(
            f"**Temperature:** {temperature} °C"
        )


    with summary_col2:

        st.write(
            f"**Capacity:** {capacity} Ah"
        )

        st.write(
            f"**Cycles:** {cycles}"
        )


    with summary_col3:

        st.write(
            f"**Resistance:** {resistance} mΩ"
        )

        st.write(
            f"**Predicted SOH:** {predicted_soh}%"
        )


# ============================================================
# 14. DISCLAIMER
# ============================================================

st.divider()

st.caption(
    "⚠️ Prototype ML assessment only. "
    "This application is not a certified battery diagnostic "
    "or safety system. Professional battery testing is required "
    "before reuse or second-life deployment."
)
