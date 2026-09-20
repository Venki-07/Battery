from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from pathlib import Path


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)

# Allow requests from your Vercel frontend
CORS(app)


# ============================================================
# FIND MODEL FILE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "battery_soh_model.pkl"


# ============================================================
# LOAD ML MODEL
# ============================================================

try:

    model = joblib.load(MODEL_PATH)

    print("ML model loaded successfully.")

except Exception as error:

    print("ERROR: Could not load ML model.")
    print(error)

    model = None


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "RE-VOLT AI Battery API is running",
        "model_loaded": model is not None
    })


# ============================================================
# PREDICTION ROUTE
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    # Check model
    if model is None:

        return jsonify({
            "error": "ML model could not be loaded."
        }), 500


    # Get JSON data
    data = request.get_json()


    try:

        voltage = float(data["voltage"])

        temperature = float(
            data["temperature"]
        )

        capacity = float(
            data["capacity"]
        )

        cycles = float(
            data["cycles"]
        )

        resistance = float(
            data["resistance"]
        )


    except Exception:

        return jsonify({
            "error": "Invalid battery input."
        }), 400


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    input_data = pd.DataFrame([
        {
            "voltage": voltage,
            "temperature": temperature,
            "capacity": capacity,
            "cycles": cycles,
            "resistance": resistance
        }
    ])


    # ========================================================
    # ML PREDICTION
    # ========================================================

    try:

        predicted_soh = model.predict(
            input_data
        )[0]

    except Exception as error:

        return jsonify({
            "error": "Prediction failed.",
            "details": str(error)
        }), 500


    # Keep SOH between 0 and 100

    predicted_soh = max(
        0,
        min(100, predicted_soh)
    )

    predicted_soh = round(
        predicted_soh,
        2
    )


    # ========================================================
    # BATTERY DECISION
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
    # SAFETY WARNING
    # ========================================================

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


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return jsonify({

        "soh": predicted_soh,

        "condition": condition,

        "recommendation": recommendation,

        "applications": applications,

        "warning": warning

    })


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
