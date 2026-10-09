import numpy as np


def detect_anomalies(data):

    # Select the features used for anomaly detection
    features = data[
        [
            "Energy_kWh",
            "Water_L",
            "Waste_kg"
        ]
    ].astype(float)

    # Convert data to NumPy array
    values = features.to_numpy()

    # Calculate median and standard deviation
    median = np.median(values, axis=0)
    std = np.std(values, axis=0)

    # Prevent division by zero
    std[std == 0] = 1

    # Calculate standardized distance from normal values
    z_scores = np.abs((values - median) / std)

    # Combine the three feature scores
    anomaly_score = np.mean(z_scores, axis=1)

    # Detect the highest 10% as anomalies
    threshold = np.percentile(anomaly_score, 90)

    predictions = np.where(
        anomaly_score >= threshold,
        -1,   # Anomaly
        1     # Normal
    )

    # Make a copy of the original data
    result = data.copy()

    # Add anomaly prediction
    result["Anomaly"] = predictions

    # Add anomaly score for transparency
    result["Anomaly_Score"] = np.round(anomaly_score, 3)

    return result