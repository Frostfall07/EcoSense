def calculate_sustainability_score(df):

    # Calculate average resource consumption
    avg_energy = df["Energy_kWh"].mean()
    avg_water = df["Water_L"].mean()
    avg_waste = df["Waste_kg"].mean()

    # Latest facility readings
    latest = df.iloc[-1]

    # Calculate percentage deviation from average
    energy_deviation = 0
    water_deviation = 0
    waste_deviation = 0

    if avg_energy > 0:
        energy_deviation = (
            latest["Energy_kWh"] - avg_energy
        ) / avg_energy

    if avg_water > 0:
        water_deviation = (
            latest["Water_L"] - avg_water
        ) / avg_water

    if avg_waste > 0:
        waste_deviation = (
            latest["Waste_kg"] - avg_waste
        ) / avg_waste

    # Start with perfect score
    score = 100

    # Penalize unusually high consumption
    score -= max(0, energy_deviation * 30)
    score -= max(0, water_deviation * 25)
    score -= max(0, waste_deviation * 25)

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    # Determine status
    if score >= 80:
        status = "Excellent"

    elif score >= 60:
        status = "Good"

    elif score >= 40:
        status = "Needs Attention"

    else:
        status = "Critical"

    return round(score, 1), status