import pandas as pd


def create_demo_anomaly(df, facility):

    demo_df = df.copy()

    facility_records = demo_df[
        demo_df["Facility"] == facility
    ]

    if facility_records.empty:
        return demo_df

    latest_index = facility_records.index[-1]

    # Introduce an artificial energy spike
    demo_df.loc[latest_index, "Energy_kWh"] *= 2.5

    return demo_df