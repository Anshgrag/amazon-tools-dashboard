import streamlit as st
import numpy as np
import math
import pandas as pd

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
CH4_CALORIFIC_VALUE = 9.97         # kWh per m³ CH4
LPG_ENERGY = 12.7                  # kWh per kg LPG
PHONE_CHARGE_KWH = 0.01
COOKING_BIOGAS_PER_HOUR = 0.30
AVG_LPG_CYLINDER_KWH = 180.34

# ---------------------------------------------------------
# WASTE TYPES
# ---------------------------------------------------------
waste_list = [
    {"name": "Agricultural Waste", "biogas_yield": 0.40, "methane_frac": 0.52, "decay_rate": 0.08, "vs_fraction": 0.80},
    {"name": "Household Waste",    "biogas_yield": 0.55, "methane_frac": 0.60, "decay_rate": 0.20, "vs_fraction": 0.85},
    {"name": "Garden Waste",       "biogas_yield": 0.33, "methane_frac": 0.50, "decay_rate": 0.06, "vs_fraction": 0.75},
    {"name": "Paper Waste",        "biogas_yield": 0.25, "methane_frac": 0.52, "decay_rate": 0.05, "vs_fraction": 0.90},
    {"name": "Cow Dung",           "biogas_yield": 0.25, "methane_frac": 0.55, "decay_rate": 0.10, "vs_fraction": 0.70},
]

waste_names = [w["name"] for w in waste_list]

# ---------------------------------------------------------
# TEMPERATURE CORRECTION
# ---------------------------------------------------------
def temperature_correction(base_Y, T):
    alpha = 0.02
    return base_Y * (1 + alpha * (T - 35))

# ---------------------------------------------------------
# SIMULATION FUNCTION
# ---------------------------------------------------------
def run_simulation(YB35, CH4_frac, k, VS_input, days, Tavg, Tvar):
    S0 = VS_input
    S_prev = S0

    records = []

    total_biogas = 0
    total_methane = 0
    total_energy = 0

    for t in range(1, days + 1):

        T_day = Tavg + ((-1) ** t) * Tvar
        YB_T = temperature_correction(YB35, T_day)

        S_now = S0 * math.exp(-k * t)
        dS = S_prev - S_now

        biogas = YB_T * dS
        methane = biogas * CH4_frac
        energy = methane * CH4_CALORIFIC_VALUE

        records.append([t, T_day, biogas, methane, energy])

        total_biogas += biogas
        total_methane += methane
        total_energy += energy

        S_prev = S_now

    df = pd.DataFrame(
        records, 
        columns=["Day", "Temperature (°C)", "Biogas (m³)", "Methane (m³)", "Energy (kWh)"]
    )

    return df, total_biogas, total_methane, total_energy

# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Biogas Energy Simulator",
    layout="wide",
    page_icon="♻️",
)

st.title("♻️ Waste-to-Energy Biogas Simulator (Anaerobic Digestion)")
st.caption("Inspired by your dashboard UI • Interactive Python Version")

st.markdown("---")

# =========================================================
# SIDEBAR INPUTS
# =========================================================
st.sidebar.header("⚙️ Simulation Controls")

mode = st.sidebar.radio("Simulation Mode", ["Individual Waste", "Mixed Waste"])

days = st.sidebar.slider("Days to Simulate", 5, 60, 30)
Tavg = st.sidebar.number_input("Average Temperature (°C)", 10.0, 55.0, 35.0)
Tvar = st.sidebar.number_input("Daily Temperature Variation (±°C)", 0.0, 10.0, 2.0)

# =========================================================
# INDIVIDUAL WASTE
# =========================================================
if mode == "Individual Waste":
    st.header("🗑️ Individual Waste Simulation")
    selected = st.selectbox("Select Waste Type", waste_names)
    weight = st.number_input("Enter waste weight (kg)", 1.0, 10000.0, 50.0)

    w = waste_list[waste_names.index(selected)]
    VS_input = weight * w["vs_fraction"]

    df, total_biogas, total_methane, total_energy = run_simulation(
        w["biogas_yield"],
        w["methane_frac"],
        w["decay_rate"],
        VS_input,
        days,
        Tavg,
        Tvar
    )

# =========================================================
# MIXED WASTE
# =========================================================
else:
    st.header("🍱 Mixed Waste Simulation")
    weight = st.number_input("Total Mixed Waste Weight (kg)", 1.0, 20000.0, 100.0)

    st.subheader("Composition (%)")
    col1, col2 = st.columns(2)

    percents = []
    for i, name in enumerate(waste_names):
        with (col1 if i % 2 == 0 else col2):
            p = st.number_input(f"{name}", 0.0, 100.0, 20.0)
            percents.append(p / 100)

    if abs(sum(percents) - 1.0) > 0.01:
        st.error("Percentages must add up to 100%.")
        st.stop()

    # weighted averages
    Y_mix = sum(percents[i] * waste_list[i]["biogas_yield"] for i in range(5))
    CH4_mix = sum(percents[i] * waste_list[i]["methane_frac"] for i in range(5))
    k_mix = sum(percents[i] * waste_list[i]["decay_rate"] for i in range(5))
    VS_mix = sum(percents[i] * waste_list[i]["vs_fraction"] for i in range(5))

    VS_input = weight * VS_mix

    df, total_biogas, total_methane, total_energy = run_simulation(
        Y_mix, CH4_mix, k_mix, VS_input, days, Tavg, Tvar
    )

# ---------------------------------------------------------
# DASHBOARD OUTPUT
# ---------------------------------------------------------
st.markdown("---")
st.header("📊 Simulation Results Dashboard")

colA, colB, colC = st.columns(3)

colA.metric("Total Biogas (m³)", f"{total_biogas:.2f}")
colB.metric("Total Methane (m³)", f"{total_methane:.2f}")
colC.metric("Total Energy (kWh)", f"{total_energy:.2f}")

colD, colE, colF = st.columns(3)
colD.metric("LPG Cylinders Saved", f"{total_energy / AVG_LPG_CYLINDER_KWH:.2f}")
colE.metric("Phone Charges", f"{total_energy / PHONE_CHARGE_KWH:.0f}")
colF.metric("Cooking Hours", f"{total_biogas / COOKING_BIOGAS_PER_HOUR:.2f}")

# ---------------------------------------------------------
# CHARTS
# ---------------------------------------------------------
st.subheader("📈 Biogas Production Trend")
st.line_chart(df.set_index("Day")["Biogas (m³)"])

st.subheader("🔥 Methane & Energy Output")
st.area_chart(df.set_index("Day")[["Methane (m³)", "Energy (kWh)"]])

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
with st.expander("📄 Full Simulation Data Table"):
    st.dataframe(df, use_container_width=True)

st.success("Simulation complete!")
