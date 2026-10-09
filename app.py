import streamlit as st
import pandas as pd
import plotly.express as px

from models.anomaly_detection import detect_anomalies
from sustainability_score import calculate_sustainability_score
from recommendation_engine import generate_recommendations
from demo_mode import create_demo_anomaly


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EcoSense AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. CUSTOM UI
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-top: 0px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 650;
        margin-top: 10px;
    }

    .insight-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 14px;
        color: #777;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #888;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/facility_data.csv")


data = load_data()

data["Date"] = pd.to_datetime(data["Date"])


# =========================================================
# 4. HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🌱 EcoSense AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Sustainable Facility Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Monitor resource consumption, detect abnormal patterns "
    "and receive actionable sustainability recommendations."
)


# =========================================================
# 5. SIDEBAR
# =========================================================

st.sidebar.title("🏢 Facility Controls")

facility = st.sidebar.selectbox(
    "Select Facility",
    data["Facility"].unique()
)


st.sidebar.divider()

st.sidebar.subheader("🎬 Demo Controls")

demo_mode = st.sidebar.checkbox(
    "Enable Live Anomaly Demo"
)


# =========================================================
# 6. DEMO MODE
# =========================================================

working_data = data.copy()


if demo_mode:

    working_data = create_demo_anomaly(
        working_data,
        facility
    )

    st.sidebar.warning(
        "⚠️ Demo Mode ON\n\n"
        "An artificial energy spike has been introduced "
        "for the selected facility."
    )


# =========================================================
# 7. AI ANOMALY DETECTION
# =========================================================

working_data = detect_anomalies(
    working_data
)


# =========================================================
# 8. FILTER SELECTED FACILITY
# =========================================================

filtered_data = working_data[
    working_data["Facility"] == facility
].copy()


# =========================================================
# 9. BASIC METRICS
# =========================================================

average_energy = filtered_data["Energy_kWh"].mean()
average_water = filtered_data["Water_L"].mean()
average_waste = filtered_data["Waste_kg"].mean()


latest = filtered_data.iloc[-1]


# =========================================================
# 10. SUSTAINABILITY SCORE
# =========================================================

score, status = calculate_sustainability_score(
    filtered_data
)


# =========================================================
# 11. FACILITY OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📊 Facility Overview</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Current monitoring facility: {facility}"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "⚡ Avg. Energy",
        f"{average_energy:,.0f} kWh"
    )


with col2:

    st.metric(
        "💧 Avg. Water",
        f"{average_water:,.0f} L"
    )


with col3:

    st.metric(
        "🗑️ Avg. Waste",
        f"{average_waste:,.0f} kg"
    )


with col4:

    st.metric(
        "🌱 Sustainability",
        f"{score}/100",
        status
    )


st.divider()


# =========================================================
# 12. FACILITY HEALTH
# =========================================================

st.markdown(
    '<div class="section-title">🌱 Facility Health</div>',
    unsafe_allow_html=True
)


score_col, status_col = st.columns([1, 2])


with score_col:

    st.metric(
        "Sustainability Score",
        f"{score}/100"
    )

    st.progress(
        int(score)
    )


with status_col:

    if score >= 80:

        st.success(
            f"🟢 **Excellent Facility Health**\n\n"
            f"The facility is currently operating within "
            f"a relatively sustainable consumption range."
        )

    elif score >= 60:

        st.info(
            f"🔵 **Good Facility Health**\n\n"
            f"The facility is performing reasonably well, "
            f"but some resource usage could be optimized."
        )

    elif score >= 40:

        st.warning(
            f"🟠 **Needs Attention**\n\n"
            f"The facility shows signs of inefficient "
            f"resource consumption."
        )

    else:

        st.error(
            f"🔴 **Critical Facility Health**\n\n"
            f"Significant resource inefficiencies have "
            f"been detected."
        )


st.caption(
    "Prototype score based on current resource consumption "
    "relative to the selected facility's baseline."
)


st.divider()


# =========================================================
# 13. AI INSIGHT
# =========================================================

st.markdown(
    '<div class="section-title">🤖 AI Facility Insight</div>',
    unsafe_allow_html=True
)


anomalies = filtered_data[
    filtered_data["Anomaly"] == -1
]


if not anomalies.empty:

    latest_anomaly = anomalies.iloc[-1]

    energy_difference = (
        latest_anomaly["Energy_kWh"] - average_energy
    )

    water_difference = (
        latest_anomaly["Water_L"] - average_water
    )

    waste_difference = (
        latest_anomaly["Waste_kg"] - average_waste
    )

    if energy_difference > 0:

        insight = (
            f"Energy consumption is currently above the "
            f"facility's recent baseline. The AI system detected "
            f"an unusual resource-consumption pattern. "
            f"Facility management should review HVAC, lighting "
            f"and equipment operating schedules."
        )

    elif water_difference > 0:

        insight = (
            f"Water consumption is currently above the "
            f"facility's recent baseline. The system recommends "
            f"checking pipelines, fixtures and possible leakage."
        )

    else:

        insight = (
            f"The AI system detected an unusual combined "
            f"resource-consumption pattern. The latest readings "
            f"should be reviewed to identify the source."
        )

    st.error(
        f"🚨 **AI Anomaly Detected**\n\n{insight}"
    )

else:

    st.success(
        "✅ **AI Insight: Normal Operation**\n\n"
        "No significant abnormal resource-consumption "
        "pattern has been detected in the selected facility."
    )


# =========================================================
# 14. FACILITY COMPARISON
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">🏢 Facility Comparison</div>',
    unsafe_allow_html=True
)

st.write(
    "Compare sustainability performance across all monitored "
    "facilities and identify which facility requires the most attention."
)


# ---------------------------------------------------------
# Calculate sustainability score for every facility
# ---------------------------------------------------------

facility_scores = []

for facility_name in data["Facility"].unique():

    facility_data = working_data[
        working_data["Facility"] == facility_name
    ].copy()

    facility_score, facility_status = (
        calculate_sustainability_score(
            facility_data
        )
    )

    facility_scores.append({
        "Facility": facility_name,
        "Score": facility_score,
        "Status": facility_status
    })


comparison_df = pd.DataFrame(
    facility_scores
)


# Sort from highest to lowest score
comparison_df = comparison_df.sort_values(
    "Score",
    ascending=False
).reset_index(drop=True)


# ---------------------------------------------------------
# Ranking table
# ---------------------------------------------------------

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# Visual comparison
# ---------------------------------------------------------

comparison_chart = px.bar(
    comparison_df,
    x="Facility",
    y="Score",
    text="Score",
    title="Sustainability Score by Facility"
)

comparison_chart.update_layout(
    xaxis_title="Facility",
    yaxis_title="Sustainability Score",
    yaxis_range=[0, 100]
)

st.plotly_chart(
    comparison_chart,
    use_container_width=True
)


# ---------------------------------------------------------
# Priority facility
# ---------------------------------------------------------

priority_facility = comparison_df.iloc[-1]

st.warning(
    f"🚨 **Priority Facility:** "
    f"{priority_facility['Facility']} "
    f"has the lowest sustainability score of "
    f"**{priority_facility['Score']}/100** "
    f"and may require additional attention."
)

# =========================================================
# 15. RESOURCE TRENDS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Resource Consumption Trends</div>',
    unsafe_allow_html=True
)


tab1, tab2, tab3 = st.tabs(
    [
        "⚡ Energy",
        "💧 Water",
        "🗑️ Waste"
    ]
)


with tab1:

    energy_chart = px.line(
        filtered_data,
        x="Date",
        y="Energy_kWh",
        markers=True,
        title="Daily Energy Consumption"
    )

    energy_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Energy (kWh)",
        hovermode="x unified"
    )

    st.plotly_chart(
        energy_chart,
        use_container_width=True
    )


with tab2:

    water_chart = px.line(
        filtered_data,
        x="Date",
        y="Water_L",
        markers=True,
        title="Daily Water Consumption"
    )

    water_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Water (L)",
        hovermode="x unified"
    )

    st.plotly_chart(
        water_chart,
        use_container_width=True
    )


with tab3:

    waste_chart = px.bar(
        filtered_data,
        x="Date",
        y="Waste_kg",
        title="Daily Waste Generation"
    )

    waste_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Waste (kg)"
    )

    st.plotly_chart(
        waste_chart,
        use_container_width=True
    )


# =========================================================
# 16. AI ANOMALY DETECTION
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">🔎 AI Anomaly Detection</div>',
    unsafe_allow_html=True
)

st.write(
    "EcoSense uses an Isolation Forest model to analyze "
    "energy, water and waste consumption together and "
    "identify unusual patterns."
)


if anomalies.empty:

    st.success(
        "✅ No unusual consumption patterns detected."
    )

else:

    st.warning(
        f"🚨 {len(anomalies)} unusual consumption "
        f"pattern(s) detected."
    )

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


# =========================================================
# 17. RECOMMENDATIONS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">💡 AI Sustainability Recommendations</div>',
    unsafe_allow_html=True
)

st.write(
    "EcoSense converts detected resource abnormalities "
    "into practical actions for facility management."
)


recommendations = generate_recommendations(
    filtered_data
)


for _, recommendation in recommendations.iterrows():

    category = recommendation["Category"]
    severity = recommendation["Severity"]
    problem = recommendation["Problem"]
    action = recommendation["Recommendation"]


    if severity == "High":

        st.error(
            f"🔴 **{category} Alert**\n\n"
            f"**Problem:** {problem}\n\n"
            f"**Recommended Action:** {action}"
        )


    elif severity == "Medium":

        st.warning(
            f"🟠 **{category} Alert**\n\n"
            f"**Problem:** {problem}\n\n"
            f"**Recommended Action:** {action}"
        )


    else:

        st.success(
            f"🟢 **{category}**\n\n"
            f"**Status:** {problem}\n\n"
            f"**Recommended Action:** {action}"
        )


# =========================================================
# 18. CARBON EMISSION CALCULATOR
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">☁️ Carbon Emission Estimator</div>',
    unsafe_allow_html=True
)

st.write(
    "Estimate CO₂ emissions associated with electricity consumption."
)


user_energy = st.number_input(
    "Electricity Consumption (kWh):",
    min_value=0.0,
    value=1000.0,
    step=100.0
)


emission_factor = 0.71

co2_emitted = user_energy * emission_factor


if user_energy > 0:

    st.info(
        f"☁️ **Estimated Emissions: "
        f"{co2_emitted:,.1f} kg CO₂**"
    )

# =========================================================
# 19. SUSTAINABILITY THEORY & BEST PRACTICES
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">📚 Sustainable Practices</div>',
    unsafe_allow_html=True
)

st.write(
    "Learn how data-driven monitoring supports real-world resource conservation."
)

with st.expander("View Theory & Guidelines"):
    st.markdown("""
    ### The Core Framework
    Sustainable facility management relies on a strict priority order: **Reduce, Optimize, Replace, and Monitor**[span_0](start_span)[span_0](end_span). 

    ### Key Action Areas
    *   **⚡ Electricity:** Reduce base demand by setting ACs to 24-26°C and utilizing natural daylight[span_1](start_span)[span_1](end_span). Optimize with LEDs and variable frequency drives (VFDs)[span_2](start_span)[span_2](end_span). Replace grid dependence with rooftop solar PV[span_3](start_span)[span_3](end_span).
    *   **💧 Water:** Detect and repair minor leaks immediately, as they compound into massive losses[span_4](start_span)[span_4](end_span). Optimize usage with low-flow fixtures and sensor taps[span_5](start_span)[span_5](end_span). Replace freshwater demand by treating and reusing greywater for landscaping and flushing[span_6](start_span)[span_6](end_span).
    *   **🗑️ Waste:** Apply the 5 Rs: Refuse, Reduce, Reuse, Recycle, and Rot[span_7](start_span)[span_7](end_span). Enforce strict source segregation to ensure organic waste is composted and dry/e-waste reaches authorized recyclers[span_8](start_span)[span_8](end_span).

    ### The Human Element
    Technology alone does not change habits; people do[span_9](start_span)[span_9](end_span). Dashboards like EcoSense convert abstract data into visible trends and actionable insights, allowing operations teams to shift equipment schedules and administrators to track long-term climate goals.
    """)

# =========================================================
# 20. RAW DATA
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">📋 Facility Data</div>',
    unsafe_allow_html=True
)


with st.expander("View Raw Facility Data"):

    st.dataframe(
        filtered_data,
        use_container_width=True
    )


# =========================================================
# 21. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🌱 <b>EcoSense AI</b><br>
        Sustainable Facility Intelligence<br>
        <small>AI-powered monitoring • anomaly detection • actionable insights</small>
    </div>
    """,
    unsafe_allow_html=True
)
