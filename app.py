import streamlit as st
import pandas as pd
import plotly.express as px

from models.anomaly_detection import detect_anomalies


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="EcoSense",
    page_icon="🌱",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data = pd.read_csv("data/facility_data.csv")

# Convert Date column to datetime FIRST
data["Date"] = pd.to_datetime(data["Date"])

# Detect anomalies
data = detect_anomalies(data)

# Get only anomalous rows
anomalies = data[data["Anomaly"] == -1]


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🌱 EcoSense")
st.subheader("Sustainable Facility Intelligence Dashboard")

st.write(
    "Monitor energy, water and waste consumption "
    "and identify unusual consumption patterns."
)


# --------------------------------------------------
# CALCULATE AVERAGES
# --------------------------------------------------

average_energy = data["Energy_kWh"].mean()
average_water = data["Water_L"].mean()
average_waste = data["Waste_kg"].mean()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⚡ Average Energy",
        f"{average_energy:,.0f} kWh"
    )

with col2:
    st.metric(
        "💧 Average Water",
        f"{average_water:,.0f} L"
    )

with col3:
    st.metric(
        "🗑️ Average Waste",
        f"{average_waste:,.0f} kg"
    )


st.divider()


# --------------------------------------------------
# ENERGY GRAPH
# --------------------------------------------------

st.subheader("⚡ Energy Consumption")

energy_chart = px.line(
    data,
    x="Date",
    y="Energy_kWh",
    markers=True,
    title="Daily Energy Consumption"
)

st.plotly_chart(
    energy_chart,
    use_container_width=True
)


# --------------------------------------------------
# WATER GRAPH
# --------------------------------------------------

st.subheader("💧 Water Consumption")

water_chart = px.line(
    data,
    x="Date",
    y="Water_L",
    markers=True,
    title="Daily Water Consumption"
)

st.plotly_chart(
    water_chart,
    use_container_width=True
)


# --------------------------------------------------
# WASTE GRAPH
# --------------------------------------------------

st.subheader("🗑️ Waste Generation")

waste_chart = px.bar(
    data,
    x="Date",
    y="Waste_kg",
    title="Daily Waste Generation"
)

st.plotly_chart(
    waste_chart,
    use_container_width=True
)


st.divider()


# --------------------------------------------------
# ANOMALY DETECTION
# --------------------------------------------------

st.subheader("🤖 AI Anomaly Detection")


if anomalies.empty:

    st.success(
        "✅ No unusual consumption patterns detected."
    )

else:

    st.warning(
        f"⚠️ {len(anomalies)} unusual consumption "
        "pattern(s) detected."
    )

    # Historical averages
    avg_energy = data["Energy_kWh"].mean()
    avg_water = data["Water_L"].mean()
    avg_waste = data["Waste_kg"].mean()

    # Select the most significant anomaly
    anomaly = anomalies.sort_values(
        "Energy_kWh",
        ascending=False
    ).iloc[0]

    # Calculate percentage increases
    energy_increase = (
        (anomaly["Energy_kWh"] - avg_energy)
        / avg_energy
    ) * 100

    water_increase = (
        (anomaly["Water_L"] - avg_water)
        / avg_water
    ) * 100

    waste_increase = (
        (anomaly["Waste_kg"] - avg_waste)
        / avg_waste
    ) * 100

    # Alert
    st.error(
        f"""
⚠️ **Abnormal Consumption Detected**

**Date:** {anomaly["Date"].strftime("%d %B %Y")}

**Energy:** {anomaly["Energy_kWh"]:,.0f} kWh  
**Change:** {energy_increase:.1f}% above average

**Water:** {anomaly["Water_L"]:,.0f} L  
**Change:** {water_increase:.1f}% above average

**Waste:** {anomaly["Waste_kg"]:,.0f} kg  
**Change:** {waste_increase:.1f}% above average
"""
    )


    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader("💡 Recommended Actions")

    if energy_increase > 10:
        st.write(
            "⚡ **Energy:** Check HVAC systems, "
            "lighting and high-power equipment for "
            "unusual usage."
        )

    if water_increase > 10:
        st.write(
            "💧 **Water:** Inspect pipelines, taps "
            "and water-consuming facilities for "
            "possible abnormal usage."
        )

    if waste_increase > 10:
        st.write(
            "🗑️ **Waste:** Review waste generation "
            "activities and improve segregation "
            "and recycling."
        )


    # --------------------------------------------------
    # ANOMALY TABLE
    # --------------------------------------------------

    st.subheader("📋 Detected Anomalies")

    st.dataframe(
        anomalies[
            [
                "Date",
                "Energy_kWh",
                "Water_L",
                "Waste_kg"
            ]
        ],
        use_container_width=True
    )


# --------------------------------------------------
# EMISSION CALCULATOR
# --------------------------------------------------

st.divider()
st.subheader("☁️ Carbon Emission Calculator")

st.write("Estimate the CO₂ emissions for a specific energy value.")

# Create an input box that accepts a number
user_energy = st.number_input(
    "Enter Electricity Consumption (kWh):", 
    min_value=0.0, 
    value=1000.0,
    step=100.0
)

# Standard conversion: ~0.71 kg CO2 per kWh
emission_factor = 0.71
co2_emitted = user_energy * emission_factor

if user_energy > 0:
    st.info(f"**Estimated Emissions:** {co2_emitted:,.1f} kg CO₂")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "EcoSense 🌱 | Sustainable Facility Intelligence "
    "Prototype"
)
