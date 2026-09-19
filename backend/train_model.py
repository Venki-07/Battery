import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# -----------------------------
# 1. LOAD DATA
# -----------------------------

data = pd.read_csv("battery_data.csv")


# -----------------------------
# 2. INPUT FEATURES
# -----------------------------

features = [
    "voltage",
    "temperature",
    "capacity",
    "cycles",
    "resistance"
]

X = data[features]

y = data["soh"]


# -----------------------------
# 3. TRAIN / TEST SPLIT
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -----------------------------
# 4. CREATE MODEL
# -----------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


# -----------------------------
# 5. TRAIN
# -----------------------------

model.fit(X_train, y_train)


# -----------------------------
# 6. TEST
# -----------------------------

predictions = model.predict(X_test)


mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print("----------------------------")
print("MODEL TRAINING COMPLETE")
print("----------------------------")

print("MAE:", round(mae, 2))

print("R2:", round(r2, 2))


# -----------------------------
# 7. SAVE MODEL
# -----------------------------

joblib.dump(
    model,
    "battery_soh_model.pkl"
)

print("----------------------------")
print("Model saved as:")
print("battery_soh_model.pkl")
