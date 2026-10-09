import pandas as pd


def generate_recommendations(df):

    recommendations = []

    average_energy = df["Energy_kWh"].mean()
    average_water = df["Water_L"].mean()
    average_waste = df["Waste_kg"].mean()

    latest = df.iloc[-1]

    # ENERGY
    if average_energy > 0:

        energy_deviation = (
            latest["Energy_kWh"] - average_energy
        ) / average_energy

        if energy_deviation >= 0.30:

            recommendations.append({
                "Category": "Energy",
                "Severity": "High",
                "Problem": (
                    "Energy consumption is significantly "
                    "above the facility baseline."
                ),
                "Recommendation": (
                    "Inspect HVAC systems, lighting and "
                    "equipment operating during non-working hours."
                )
            })

        elif energy_deviation >= 0.20:

            recommendations.append({
                "Category": "Energy",
                "Severity": "Medium",
                "Problem": (
                    "Energy consumption is above the "
                    "normal facility baseline."
                ),
                "Recommendation": (
                    "Review HVAC, lighting and equipment "
                    "usage for possible inefficiencies."
                )
            })

    # WATER
    if average_water > 0:

        water_deviation = (
            latest["Water_L"] - average_water
        ) / average_water

        if water_deviation >= 0.30:

            recommendations.append({
                "Category": "Water",
                "Severity": "High",
                "Problem": (
                    "Water consumption is significantly "
                    "above the facility baseline."
                ),
                "Recommendation": (
                    "Inspect pipelines, fixtures and storage "
                    "systems for possible leakage or excessive usage."
                )
            })

        elif water_deviation >= 0.20:

            recommendations.append({
                "Category": "Water",
                "Severity": "Medium",
                "Problem": (
                    "Water consumption is above the "
                    "normal facility baseline."
                ),
                "Recommendation": (
                    "Check for leakage and review water usage "
                    "across the facility."
                )
            })

    # WASTE
    if average_waste > 0:

        waste_deviation = (
            latest["Waste_kg"] - average_waste
        ) / average_waste

        if waste_deviation >= 0.30:

            recommendations.append({
                "Category": "Waste",
                "Severity": "High",
                "Problem": (
                    "Waste generation is significantly "
                    "above the facility baseline."
                ),
                "Recommendation": (
                    "Identify the source of excess waste and "
                    "improve segregation and waste-handling practices."
                )
            })

        elif waste_deviation >= 0.20:

            recommendations.append({
                "Category": "Waste",
                "Severity": "Medium",
                "Problem": (
                    "Waste generation is above the "
                    "normal facility baseline."
                ),
                "Recommendation": (
                    "Review waste sources and strengthen "
                    "segregation practices."
                )
            })

    # AI anomaly fallback
    if (
        not recommendations
        and "Anomaly" in df.columns
        and latest["Anomaly"] == -1
    ):

        recommendations.append({
            "Category": "AI Alert",
            "Severity": "High",
            "Problem": (
                "The AI model detected an unusual combined "
                "resource-consumption pattern."
            ),
            "Recommendation": (
                "Review the latest energy, water and waste "
                "readings and investigate the cause."
            )
        })

    # Normal condition
    if not recommendations:

        recommendations.append({
            "Category": "System",
            "Severity": "Low",
            "Problem": (
                "No significant resource abnormality detected."
            ),
            "Recommendation": (
                "Continue monitoring the facility and "
                "maintain current sustainability practices."
            )
        })

    return pd.DataFrame(recommendations)