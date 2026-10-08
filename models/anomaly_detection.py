from sklearn.ensemble import IsolationForest


def detect_anomalies(data):

    features = data[
        ["Energy_kWh", "Water_L", "Waste_kg"]
    ]

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    result = data.copy()

    result["Anomaly"] = model.fit_predict(features)

    return result