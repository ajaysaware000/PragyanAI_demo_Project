import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# K-SIWAP | MODULE 4: DISTRICT SKILL PLANNER
# PPT-matched dashboard with illustrative demo data
# =========================================================

st.set_page_config(
    page_title="K-SIWAP | District Skill Planner",
    page_icon="📊",
    layout="wide",
)

# ----------------------- DESIGN ---------------------------

st.markdown("""
<style>
.stApp {
    background-color: #F3F6FA;
    color: #24364A;
}
[data-testid="stSidebar"] {
    background-color: #132840;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #132840, #1D3854);
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 20px;
    color: white;
}
.hero h1 {
    color: white;
    font-size: 38px;
    margin-bottom: 8px;
}
.hero p {
    color: #DCE7F0;
    font-size: 16px;
}
.kpi {
    background: white;
    border: 1px solid #DCE7F0;
    border-top: 4px solid #00A3A3;
    padding: 18px;
    border-radius: 12px;
    min-height: 110px;
}
.kpi-label {
    font-size: 12px;
    color: #6B7C8F;
    font-weight: bold;
}
.kpi-value {
    color: #132840;
    font-size: 27px;
    font-weight: 800;
    margin-top: 8px;
}
.section-title {
    color: #132840;
    font-size: 25px;
    font-weight: 800;
}
.small-note {
    color: #6B7C8F;
    font-size: 12px;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #DCE7F0;
    border-radius: 10px;
    padding: 14px;
}
.stDownloadButton button {
    background-color: #00A3A3;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------- DEMO DATA ------------------------
# Fictional values for presentation and testing only.

@st.cache_data
def load_data():
    return pd.DataFrame({
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

df = load_data()

# ----------------------- SIDEBAR --------------------------

with st.sidebar:
    st.markdown("## K-SIWAP")
    st.markdown("### District Skill Planner")
    st.caption("MODULE 4 | DEMO DASHBOARD")
    st.divider()

    st.markdown("### Dashboard filters")
    selected_districts = st.multiselect(
        "Select districts",
        df["District"].tolist(),
        default=df["District"].tolist(),
    )

    st.divider()
    st.markdown("### Priority scoring")

    demand_weight = st.slider(
        "Demand weight (%)",
        min_value=0,
        max_value=100,
        value=60,
        step=5,
    )

    st.caption(
        f"Seat-shortage weight: {100 - demand_weight}%"
    )

    st.divider()
    st.caption(
        "All built-in values are synthetic demo data, "
        "not official statistics."
    )

data = df[df["District"].isin(selected_districts)].copy()

if data.empty:
    st.warning("Select at least one district in the sidebar.")
    st.stop()

# ----------------------- CALCULATIONS ---------------------

data["Seat Shortage"] = (
    data["Estimated Demand"] - data["Available Seats"]
).clip(lower=0)

max_demand = data["Estimated Demand"].max()
max_shortage = data["Seat Shortage"].max()

data["Demand Score"] = (
    data["Estimated Demand"] / max_demand * 100
    if max_demand > 0 else 0
)

data["Shortage Score"] = (
    data["Seat Shortage"] / max_shortage * 100
    if max_shortage > 0 else 0
)

data["Priority Score"] = (
    data["Demand Score"] * demand_weight / 100
    + data["Shortage Score"] * (100 - demand_weight) / 100
).round(1)

data["Placement Rate (%)"] = (
    data["Placed"]
    / data["Completed Training"].replace(0, pd.NA)
    * 100
).round(1)

# ----------------------- HEADER ---------------------------

st.markdown("""
<div class="hero">
    <div style="color:#55D6CF;font-weight:bold;letter-spacing:2px">
        KARNATAKA SKILL INTELLIGENCE & WORKFORCE ANALYTICS PLATFORM
    </div>
    <h1>District Skill Planner</h1>
    <p>
        Prioritise districts | Plan training capacity |
        Explore budgets | Monitor programme outcomes
    </p>
</div>
""", unsafe_allow_html=True)

st.warning(
    "DEMO MODE: The values in this prototype are fictional examples. "
    "They are not verified Karnataka government statistics."
)

# ----------------------- KPI CARDS ------------------------

total_demand = int(data["Estimated Demand"].sum())
total_seats = int(data["Available Seats"].sum())
total_centres = int(data["Training Centres"].sum())
total_budget = int(data["Budget (₹ lakh)"].sum())

kpis = [
    ("ESTIMATED DEMAND", f"{total_demand:,}", "Illustrative people"),
    ("AVAILABLE SEATS", f"{total_seats:,}", "Illustrative seats"),
    ("TRAINING CENTRES", f"{total_centres:,}", "Illustrative centres"),
    ("DEMO BUDGET", f"₹{total_budget:,}L", "₹ lakh, illustrative"),
]

cols = st.columns(4)

for col, (label, value, note) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="small-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ----------------------- TABS -----------------------------

overview, priority, budget, centres, outcomes, methodology = st.tabs([
    "📊 Overview",
    "🏆 District Priority",
    "💰 Budget Planner",
    "🏢 Centre Capacity",
    "🎯 Programme Outcomes",
    "📁 Data & Method",
])

NAVY = "#132840"
BLUE = "#2D72B8"
TEAL = "#00A3A3"
AMBER = "#F2B134"

def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(color=NAVY, family="Arial"),
        margin=dict(l=20, r=20, t=65, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )
    return fig

# =========================================================
# OUTPUT 1: OVERVIEW
# =========================================================

with overview:
    st.markdown(
        '<div class="section-title">District Planning Overview</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Review estimated training demand, available seats "
        "and district-level resource indicators."
    )

    left, right = st.columns(2)

    with left:
        chart_data = data.sort_values(
            "Estimated Demand", ascending=True
        )

        fig = px.bar(
            chart_data,
            x="Estimated Demand",
            y="District",
            orientation="h",
            title="Estimated Training Demand by District",
            color_discrete_sequence=[BLUE],
            hover_data=["Available Seats", "Seat Shortage"],
        )
        fig.update_layout(
            xaxis_title="Illustrative people",
            yaxis_title="",
        )
        st.plotly_chart(
            style_chart(fig), use_container_width=True
        )

    with right:
        capacity_data = data.melt(
            id_vars="District",
            value_vars=["Estimated Demand", "Available Seats"],
            var_name="Measure",
            value_name="Count",
        )

        fig = px.bar(
            capacity_data,
            x="District",
            y="Count",
            color="Measure",
            barmode="group",
            title="Demand vs Available Seats",
            color_discrete_map={
                "Estimated Demand": BLUE,
                "Available Seats": TEAL,
            },
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="People / seats",
            xaxis_tickangle=-35,
        )
        st.plotly_chart(
            style_chart(fig), use_container_width=True
        )

    st.subheader("District Summary")

    st.dataframe(
        data[[
            "District",
            "Estimated Demand",
            "Available Seats",
            "Seat Shortage",
            "Training Centres",
            "Budget (₹ lakh)",
        ]],
        use_container_width=True,
        hide_index=True,
    )

# =========================================================
# OUTPUT 2: DISTRICT PRIORITY RANKING
# =========================================================

with priority:
    st.markdown(
        '<div class="section-title">District Priority Ranking</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Scores combine estimated demand and seat shortage. "
        "Change the weights in the sidebar to explore different scenarios."
    )

    ranking = data.sort_values(
        "Priority Score", ascending=False
    ).reset_index(drop=True)

    ranking.insert(0, "Rank", range(1, len(ranking) + 1))

    left, right = st.columns([1.1, 1])

    with left:
        fig = px.bar(
            ranking.sort_values(
                "Priority Score", ascending=True
            ),
            x="Priority Score",
            y="District",
            orientation="h",
            title="Illustrative District Priority Score",
            color="Priority Score",
            color_continuous_scale=["#BFECE8", TEAL, NAVY],
            hover_data=[
                "Estimated Demand",
                "Available Seats",
                "Seat Shortage",
            ],
        )
        fig.update_layout(
            xaxis_title="Relative score",
            yaxis_title="",
            coloraxis_showscale=False,
        )
        st.plotly_chart(
            style_chart(fig), use_container_width=True
        )

    with right:
        st.subheader("Ranked Districts")
        st.dataframe(
            ranking[[
                "Rank",
                "District",
                "Priority Score",
                "Estimated Demand",
                "Seat Shortage",
            ]],
            use_container_width=True,
            hide_index=True,
        )

    st.info(
        "A higher score indicates higher priority under the selected "
        "demo formula. It is not an official government ranking."
    )

# =========================================================
# OUTPUT 3: BUDGET PLANNER
# =========================================================

with budget:
    st.markdown(
        '<div class="section-title">Training Budget Planner</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Estimate training costs using planned seats and an assumed "
        "cost per seat."
    )

    left, right = st.columns(2)

    with left:
        budget_district = st.selectbox(
            "Select district",
            data["District"].tolist(),
        )

        district_row = data[
            data["District"] == budget_district
        ].iloc[0]

        planned_seats = st.number_input(
            "Training seats to fund",
            min_value=0,
            max_value=100000,
            value=int(district_row["Available Seats"]),
            step=25,
        )

        cost_per_seat = st.number_input(
            "Estimated cost per seat (₹)",
            min_value=0,
            max_value=1000000,
            value=15000,
            step=500,
        )

        available_budget_lakh = st.number_input(
            "Available budget (₹ lakh)",
            min_value=0,
            max_value=100000,
            value=int(district_row["Budget (₹ lakh)"]),
            step=5,
        )

    estimated_cost = planned_seats * cost_per_seat
    available_budget = available_budget_lakh * 100000
    balance = available_budget - estimated_cost

    with right:
        st.subheader("Scenario Result")

        st.metric(
            "Estimated Programme Cost",
            f"₹{estimated_cost:,.0f}",
        )

        st.metric(
            "Available Budget",
            f"₹{available_budget:,.0f}",
        )

        st.metric(
            "Remaining Budget / Shortfall",
            f"₹{balance:,.0f}",
        )

        if balance < 0:
            st.error("The estimated cost exceeds the budget.")
        else:
            st.success("The estimated cost is within the budget.")

    fig = px.bar(
        data.sort_values("Budget (₹ lakh)", ascending=True),
        x="Budget (₹ lakh)",
        y="District",
        orientation="h",
        title="Illustrative Budget by District",
        color_discrete_sequence=[TEAL],
    )
    fig.update_layout(xaxis_title="₹ lakh", yaxis_title="")
    st.plotly_chart(
        style_chart(fig), use_container_width=True
    )

    st.caption(
        "Budget and cost-per-seat figures are illustrative, not approved funding amounts."
    )

# =========================================================
# OUTPUT 4: TRAINING CENTRE CAPACITY
# =========================================================

with centres:
    st.markdown(
        '<div class="section-title">Training Centre Capacity</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Compare the number of training centres with available training seats."
    )

    fig = px.scatter(
        data,
        x="Training Centres",
        y="Available Seats",
        size="Available Seats",
        color="Seat Shortage",
        hover_name="District",
        color_continuous_scale=["#BFECE8", TEAL, AMBER],
        title="Centre Network vs Available Seats",
        size_max=40,
    )

    fig.update_layout(
        xaxis_title="Number of training centres",
        yaxis_title="Available seats",
    )

    st.plotly_chart(
        style_chart(fig), use_container_width=True
    )

    st.dataframe(
        data[[
            "District",
            "Training Centres",
            "Available Seats",
            "Estimated Demand",
            "Seat Shortage",
        ]],
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Centre counts alone do not measure course quality, accessibility "
        "or instructor availability. A geographic map requires verified "
        "district boundary data."
    )

# =========================================================
# OUTPUT 5: PROGRAMME OUTCOMES
# =========================================================

with outcomes:
    st.markdown(
        '<div class="section-title">Training Programme Outcomes</div>',
        unsafe_allow_html=True,
    )

    total_completed = int(data["Completed Training"].sum())
    total_placed = int(data["Placed"].sum())

    placement_rate = (
        total_placed / total_completed * 100
        if total_completed > 0 else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Completed Training", f"{total_completed:,}")
    c2.metric("Learners Placed", f"{total_placed:,}")
    c3.metric("Aggregate Placement Rate", f"{placement_rate:.1f}%")

    fig = px.bar(
        data.sort_values(
            "Placement Rate (%)", ascending=True
        ),
        x="Placement Rate (%)",
        y="District",
        orientation="h",
        title="Illustrative Placement Rate by District",
        color_discrete_sequence=[TEAL],
        hover_data=["Completed Training", "Placed"],
    )

    fig.update_layout(
        xaxis_title="Placement rate (%)",
        yaxis_title="",
    )

    st.plotly_chart(
        style_chart(fig), use_container_width=True
    )

    st.dataframe(
        data[[
            "District",
            "Completed Training",
            "Placed",
            "Placement Rate (%)",
        ]],
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Placement rate = learners placed ÷ learners completing training × 100. "
        "Use comparable reporting periods and placement definitions."
    )

# =========================================================
# OUTPUT 6: DATA, VALIDATION AND METHODOLOGY
# =========================================================

with methodology:
    st.markdown(
        '<div class="section-title">Data Validation and Transparency</div>',
        unsafe_allow_html=True,
    )

    st.warning(
        "The built-in dataset is synthetic. No live government database is connected."
    )

    st.subheader("Data fields used")

    st.write(
        "District, estimated demand, available seats, training centres, "
        "budget, completed training and placed learners."
    )

    st.subheader("Calculation definitions")

    st.markdown("""
    - **Seat shortage:** maximum of demand minus available seats, or zero.
    - **Priority score:** weighted combination of normalised demand and shortage.
    - **Programme cost:** planned training seats multiplied by cost per seat.
    - **Placement rate:** placed learners divided by training completers, multiplied by 100.
    """)

    st.subheader("Data quality checklist")

    st.checkbox("Confirm source and extraction date")
    st.checkbox("Confirm units and reporting periods")
    st.checkbox("Check missing values and duplicate records")
    st.checkbox("Validate calculations against known examples")

    st.caption(
        "Missing data should be recorded as unknown, not silently treated as zero. "
        "District comparisons require comparable definitions and coverage."
    )

    st.subheader("Export selected district data")

    csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="ksiwap_module4_district_data.csv",
        mime="text/csv",
    )

# ----------------------- FOOTER ---------------------------

st.divider()

st.caption(
    "K-SIWAP | Module 4: District Skill Planner | "
    "Demonstration prototype — synthetic data only. "
    "This application excludes Module 3 Skill Gap Analysis "
    "and an AI Report Generator."
)
