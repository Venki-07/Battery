from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib
import pandas as pd


app = Flask(__name__)

CORS(app)


# -----------------------------
# LOAD ML MODEL
# -----------------------------

model = joblib.load(
    "battery_soh_model.pkl"
)


# -----------------------------
# HOME
# -----------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "RE-VOLT AI Battery API is running"
    })


# -----------------------------
# BATTERY PREDICTION
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()


    # -------------------------
    # GET INPUTS
    # -------------------------

    voltage = float(data["voltage"])

    temperature = float(data["temperature"])

    capacity = float(data["capacity"])

    cycles = float(data["cycles"])

    resistance = float(data["resistance"])


    # -------------------------
    # CREATE DATAFRAME
    # -------------------------

    input_data = pd.DataFrame([{

        "voltage": voltage,

        "temperature": temperature,

        "capacity": capacity,

        "cycles": cycles,

        "resistance": resistance

    }])


    # -------------------------
    # ML PREDICTION
    # -------------------------

    predicted_soh = model.predict(
        input_data
    )[0]


    predicted_soh = max(
        0,
        min(100, predicted_soh)
    )


    predicted_soh = round(
        predicted_soh,
        2
    )


    # -------------------------
    # CONDITION
    # -------------------------

    if (
        predicted_soh >= 80
        and temperature <= 45
        and resistance <= 80
    ):

        condition = "REUSE"

        recommendation = (
            "The battery shows relatively strong "
            "health in this prototype assessment. "
            "Professional safety testing is required "
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
            "The battery may be suitable for "
            "lower-demand second-life applications "
            "after proper electrical and safety testing."
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
            "Additional battery diagnostics are "
            "recommended before deciding on reuse."
        )

        applications = [
            "Diagnostic Testing",
            "Cell-Level Assessment"
        ]


    else:

        condition = "RECYCLE"

        recommendation = (
            "The prototype assessment indicates "
            "poor condition. Professional end-of-life "
            "evaluation and recycling should be considered."
        )

        applications = [
            "Material Recovery",
            "Battery Recycling"
        ]


    # -------------------------
    # SAFETY WARNING
    # -------------------------

    warning = None


    if temperature > 45:

        warning = (
            "Elevated temperature detected. "
            "Do not rely on this prototype result "
            "for battery safety decisions."
        )


    elif resistance > 120:

        warning = (
            "High internal resistance detected. "
            "Additional diagnostic testing is required."
        )


    # -------------------------
    # RETURN RESULT
    # -------------------------

    return jsonify({

        "soh": predicted_soh,

        "condition": condition,

        "recommendation": recommendation,

        "applications": applications,

        "warning": warning

    })


# -----------------------------
# RUN SERVER
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
