
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="K-SIWAP | District Skill Planner",
    page_icon="📊",
    layout="wide",
)

# --------------------------------------------------
# Demo data only — replace with verified data later.
# --------------------------------------------------
DISTRICTS = pd.DataFrame({
    "District": [
        "Bengaluru Urban",
        "Mysuru",
        "Belagavi",
        "Kalaburagi",
        "Dakshina Kannada",
        "Ballari",
        "Shivamogga",
        "Vijayapura",
    ],
    "Estimated Demand": [850, 620, 700, 680, 540, 590, 460, 510],
    "Available Seats": [620, 500, 420, 350, 460, 380, 340, 320],
    "Training Centres": [32, 20, 18, 16, 19, 15, 14, 13],
    "Budget (₹ lakh)": [180, 120, 130, 125, 110, 115, 95, 100],
    "Completed Training": [520, 410, 360, 300, 390, 320, 290, 270],
    "Placed": [350, 280, 230, 180, 275, 205, 190, 170],
})

st.title("K-SIWAP: District Skill Planner")
st.caption(
    "Karnataka Skill Intelligence & Workforce Analytics Platform "
    "| Module 4"
)

st.warning(
    "Demo mode: all figures are fictional and for demonstration only. "
    "Do not use them for real funding or policy decisions."
)

# Sidebar filters
st.sidebar.header("Planner Settings")
selected_districts = st.sidebar.multiselect(
    "Select districts",
    options=DISTRICTS["District"].tolist(),
    default=DISTRICTS["District"].tolist(),
)

data = DISTRICTS[
    DISTRICTS["District"].isin(selected_districts)
].copy()

if data.empty:
    st.info("Select at least one district from the sidebar.")
    st.stop()

# --------------------------------------------------
# Overview metrics
# --------------------------------------------------
total_demand = int(data["Estimated Demand"].sum())
total_seats = int(data["Available Seats"].sum())
total_centres = int(data["Training Centres"].sum())
total_budget = float(data["Budget (₹ lakh)"].sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Estimated Training Demand", f"{total_demand:,}")
col2.metric("Available Training Seats", f"{total_seats:,}")
col3.metric("Training Centres", f"{total_centres:,}")
col4.metric("Illustrative Budget", f"₹{total_budget:,.0f} lakh")

st.divider()

# --------------------------------------------------
# District priority ranking
# --------------------------------------------------
st.header("1. District Priority Ranking")
st.write(
    "Adjust the weights to explore how demand and seat availability "
    "affect the planning priority. This is a transparent demo score, "
    "not an official government ranking."
)

weight_demand = st.slider(
    "Weight for estimated demand",
    min_value=0,
    max_value=100,
    value=60,
    step=5,
)

weight_capacity = 100 - weight_demand
st.caption(
    f"Demand weight: {weight_demand}% | "
    f"Seat-shortage weight: {weight_capacity}%"
)

ranking = data.copy()

max_demand = ranking["Estimated Demand"].max()
max_shortage = (
    ranking["Estimated Demand"] - ranking["Available Seats"]
).clip(lower=0).max()

if max_demand > 0:
    demand_score = ranking["Estimated Demand"] / max_demand
else:
    demand_score = 0

shortage = (
    ranking["Estimated Demand"] - ranking["Available Seats"]
).clip(lower=0)

if max_shortage > 0:
    shortage_score = shortage / max_shortage
else:
    shortage_score = 0

ranking["Priority Score"] = (
    demand_score * weight_demand
    + shortage_score * weight_capacity
).round(1)

ranking = ranking.sort_values(
    "Priority Score", ascending=False
).reset_index(drop=True)

ranking.insert(0, "Priority Rank", range(1, len(ranking) + 1))

st.dataframe(
    ranking[
        [
            "Priority Rank",
            "District",
            "Estimated Demand",
            "Available Seats",
            "Priority Score",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

priority_chart = px.bar(
    ranking,
    x="District",
    y="Priority Score",
    color="Priority Score",
    title="Illustrative District Priority Scores",
    hover_data=["Estimated Demand", "Available Seats"],
)
priority_chart.update_layout(xaxis_tickangle=-35)
st.plotly_chart(priority_chart, use_container_width=True)

# --------------------------------------------------
# Demand and capacity comparison
# --------------------------------------------------
st.header("2. Training Demand and Capacity")

capacity_data = data.melt(
    id_vars="District",
    value_vars=["Estimated Demand", "Available Seats"],
    var_name="Measure",
    value_name="People",
)

capacity_chart = px.bar(
    capacity_data,
    x="District",
    y="People",
    color="Measure",
    barmode="group",
    title="Estimated Demand Compared with Available Seats",
)
capacity_chart.update_layout(xaxis_tickangle=-35)
st.plotly_chart(capacity_chart, use_container_width=True)

display_data = data.copy()
display_data["Estimated Seat Shortage"] = (
    display_data["Estimated Demand"]
    - display_data["Available Seats"]
).clip(lower=0)

st.dataframe(
    display_data[
        [
            "District",
            "Estimated Demand",
            "Available Seats",
            "Estimated Seat Shortage",
            "Training Centres",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# Budget planning calculator
# --------------------------------------------------
st.header("3. Training Budget Planner")

district_options = data["District"].tolist()
budget_district = st.selectbox(
    "Choose a district",
    options=district_options,
    key="budget_district",
)

district_row = data[data["District"] == budget_district].iloc[0]

col1, col2 = st.columns(2)

with col1:
    planned_seats = st.number_input(
        "Number of training seats to fund",
        min_value=0,
        max_value=100000,
        value=int(district_row["Available Seats"]),
        step=50,
    )

with col2:
    cost_per_seat = st.number_input(
        "Illustrative cost per seat (₹)",
        min_value=0,
        max_value=1000000,
        value=15000,
        step=500,
    )

estimated_cost = planned_seats * cost_per_seat
st.metric("Estimated Programme Cost", f"₹{estimated_cost:,.0f}")

available_budget = float(district_row["Budget (₹ lakh)"]) * 100000
st.write(f"Demo budget for {budget_district}: ₹{available_budget:,.0f}")

if estimated_cost > available_budget:
    st.error(
        "The proposed cost exceeds this district's illustrative budget."
    )
else:
    st.success(
        "The proposed cost is within this district's illustrative budget."
    )

st.caption(
    "Budget figures and per-seat costs are examples only. "
    "They must be replaced with approved funding and cost data."
)

# --------------------------------------------------
# Training outcomes
# --------------------------------------------------
st.header("4. Training Programme Outcomes")

outcomes = data.copy()
outcomes["Placement Rate (%)"] = (
    outcomes["Placed"]
    .div(outcomes["Completed Training"].replace(0, pd.NA))
    .mul(100)
).round(1)

outcome_chart = px.bar(
    outcomes,
    x="District",
    y="Placement Rate (%)",
    title="Illustrative Placement Rate by District",
    hover_data=["Completed Training", "Placed"],
)
outcome_chart.update_layout(xaxis_tickangle=-35)
st.plotly_chart(outcome_chart, use_container_width=True)

st.dataframe(
    outcomes[
        [
            "District",
            "Completed Training",
            "Placed",
            "Placement Rate (%)",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# Download demo data
# --------------------------------------------------
st.header("5. Data Export")

csv_data = data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download selected district data (CSV)",
    data=csv_data,
    file_name="ksiwap_district_demo_data.csv",
    mime="text/csv",
)

with st.expander("Data sources, formulas and limitations"):
    st.markdown(
        """
        **Data source:** fictional values embedded in this starter app.

        **Priority score:** weighted combination of normalized estimated
        demand and normalized positive seat shortage.

        **Placement rate:** placed learners divided by learners who
        completed training, multiplied by 100.

        **Important limitations:**
        - Values are not official district statistics.
        - The demo does not connect to live government databases.
        - A missing value should be recorded as unknown, not as zero.
        - Confirm data definitions, reporting periods and sources before
          using real figures.
        - No district boundary file is included, so this starter uses
          charts rather than a geographic map.
        """
    )

st.divider()
st.caption(
    "K-SIWAP | Module 4: District Skill Planner | "
    "Prototype for learning and demonstration"
)
