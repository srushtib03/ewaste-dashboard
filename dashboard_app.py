import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="EcoCycle India • E-Waste Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# MODERN EXECUTIVE CSS (ZERO RAW HTML LEAKS)
# ==============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-dark: #080d18;
    --card-bg: rgba(14, 23, 42, 0.72);
    --card-border: rgba(16, 185, 129, 0.16);
    --primary-emerald: #10b981;
    --mint-glow: #34d399;
    --cyan-accent: #06b6d4;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
}

/* Background canvas */
.stApp {
    background-color: #070c16;
    background-image: 
        radial-gradient(circle at 15% 10%, rgba(16, 185, 129, 0.08) 0%, transparent 35%),
        radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.06) 0%, transparent 35%),
        radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.4) 0%, transparent 100%);
    color: #f1f5f9;
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
}

/* Streamlit Header & Main menu clean up */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091122 0%, #070e1c 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

section[data-testid="stSidebar"] hr {
    margin: 1rem 0;
    border-color: rgba(255, 255, 255, 0.08);
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: rgba(13, 22, 41, 0.75);
    border: 1px solid rgba(16, 185, 129, 0.18);
    border-radius: 12px;
    padding: 14px 18px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: rgba(52, 211, 153, 0.45);
    box-shadow: 0 8px 26px rgba(16, 185, 129, 0.12);
}

div[data-testid="stMetricLabel"] p {
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8 !important;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 800;
    font-size: 1.65rem !important;
}

div[data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
    font-weight: 600;
}

/* Modern Tab Navigation */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(13, 22, 41, 0.6);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 18px;
    color: #94a3b8;
    font-weight: 600;
    font-size: 0.92rem;
    border: none;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #f8fafc;
    background: rgba(255, 255, 255, 0.04);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.22), rgba(6, 182, 212, 0.14)) !important;
    color: #34d399 !important;
    border: 1px solid rgba(52, 211, 153, 0.35) !important;
}

/* Bordered Containers as Sleek Cards */
div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
    border-color: rgba(255, 255, 255, 0.08) !important;
    background: rgba(13, 22, 41, 0.5);
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    background: linear-gradient(135deg, #059669, #10b981);
    color: #ffffff;
    font-weight: 600;
    border: none;
    padding: 0.5rem 1.2rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #10b981, #34d399);
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
    color: #ffffff;
}

/* Tables */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA LOADER & CACHING
# ==============================================================================

@st.cache_data
def load_ewaste_data():
    df = pd.read_csv("cleaned_ewaste.csv")
    df.columns = df.columns.str.strip()
    
    # Ensure numeric columns are properly typed
    numeric_cols = [
        "Year", "Month", "Population", "Population_Density", "Urbanization_Rate",
        "Daily_Waste_Generation_Tons", "Waste_Per_Capita_KG",
        "Collection_Efficiency_Percentage", "Waste_Segregation_Rate", "Recycling_Rate",
        "Composting_Rate", "Landfill_Dependency_Rate", "Waste_Processing_Capacity",
        "Municipal_Efficiency_Score", "Awareness_Campaigns_Count", "Smart_Bins_Count",
        "Waste_Collection_Vehicles", "Worker_Count", "Waste_Management_Budget_INR",
        "Cost_Per_Ton_INR", "Carbon_Emission_From_Waste", "Landfill_Capacity_Tons",
        "Landfill_Remaining_Capacity", "Latitude", "Longitude", "Air_Quality_Index",
        "Rainfall_MM", "Tourism_Impact_Score", "Industrial_Activity_Level",
        "Population_Growth_Rate", "Sustainability_Index"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    return df

df_raw = load_ewaste_data()

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def calc_weighted_avg(data, val_col, weight_col="Daily_Waste_Generation_Tons"):
    if data.empty or weight_col not in data.columns or val_col not in data.columns:
        return 0.0
    valid = data[[val_col, weight_col]].dropna()
    if valid.empty:
        return 0.0
    weights = valid[weight_col].clip(lower=0)
    if weights.sum() == 0:
        return float(valid[val_col].mean())
    return float(np.average(valid[val_col], weights=weights))

def apply_plotly_theme(fig, height=450):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#cbd5e1", size=12),
        margin=dict(l=20, r=20, t=50, b=20),
        title_font=dict(color="#f8fafc", size=15),
        legend=dict(
            bgcolor="rgba(13,22,41,0.6)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(color="#94a3b8")
        )
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(color="#94a3b8")
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(color="#94a3b8")
    )
    return fig

# ==============================================================================
# SIDEBAR FILTERS & CONTROLS
# ==============================================================================

with st.sidebar:
    st.markdown("## 🌿 EcoCycle India")
    st.caption("National E-Waste Intelligence & Telemetry")
    
    st.divider()
    st.subheader("Global Filters")
    
    # Year Filter
    avail_years = sorted(df_raw["Year"].dropna().unique().astype(int))
    selected_year = st.selectbox("Select Year", ["All Years"] + avail_years, index=0)
    
    # Region Filter
    avail_regions = sorted(df_raw["Region"].dropna().unique())
    selected_regions = st.multiselect("Select Regions", avail_regions, default=avail_regions)
    if not selected_regions:
        selected_regions = avail_regions
        
    # State Filter
    region_filtered_df = df_raw[df_raw["Region"].isin(selected_regions)]
    avail_states = sorted(region_filtered_df["State"].dropna().unique())
    selected_states = st.multiselect("Select States", avail_states, default=avail_states)
    if not selected_states:
        selected_states = avail_states
        
    # City Category Filter
    avail_categories = sorted(df_raw["City_Category"].dropna().unique())
    selected_categories = st.multiselect("City Categories", avail_categories, default=avail_categories)
    if not selected_categories:
        selected_categories = avail_categories

    # Performance Level
    avail_perf = sorted(df_raw["Waste_Management_Performance_Level"].dropna().unique())
    selected_perf = st.multiselect("Performance Tier", avail_perf, default=avail_perf)
    if not selected_perf:
        selected_perf = avail_perf

    st.divider()
    with st.container(border=True):
        st.markdown("**Dataset Snapshot**")
        st.caption(f"• Total Cities: {df_raw['City'].nunique()}")
        st.caption(f"• Total States & UTs: {df_raw['State'].nunique()}")
        st.caption(f"• Historical Records: {len(df_raw):,}")
        st.caption("• Target: 65% Recycling Rate")

# ==============================================================================
# APPLY FILTERING
# ==============================================================================

filtered_df = df_raw.copy()

if selected_year != "All Years":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

filtered_df = filtered_df[
    (filtered_df["Region"].isin(selected_regions)) &
    (filtered_df["State"].isin(selected_states)) &
    (filtered_df["City_Category"].isin(selected_categories)) &
    (filtered_df["Waste_Management_Performance_Level"].isin(selected_perf))
]

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filter combination. Please broaden your selection.")
    st.stop()

# Aggregations
total_waste = filtered_df["Daily_Waste_Generation_Tons"].sum()
weighted_recycling = calc_weighted_avg(filtered_df, "Recycling_Rate")
weighted_collection = calc_weighted_avg(filtered_df, "Collection_Efficiency_Percentage")
avg_processing = filtered_df["Waste_Processing_Capacity"].mean()
total_carbon = filtered_df["Carbon_Emission_From_Waste"].sum()
total_smart_bins = filtered_df["Smart_Bins_Count"].sum()
avg_sustainability = filtered_df["Sustainability_Index"].mean()

# Benchmark calculations
national_avg_recycling = calc_weighted_avg(df_raw, "Recycling_Rate")
national_avg_collection = calc_weighted_avg(df_raw, "Collection_Efficiency_Percentage")

# ==============================================================================
# HEADER & EXECUTIVE SUMMARY BANNER
# ==============================================================================

header_col, action_col = st.columns([3, 1])
with header_col:
    st.title("🌿 National E-Waste Intelligence Dashboard")
    st.caption(
        f"Real-time surveillance & analytics across **{filtered_df['City'].nunique()} cities** "
        f"and **{filtered_df['State'].nunique()} states** • Timeframe: **{selected_year}**"
    )

with action_col:
    st.write("")
    st.info(f"📊 Active Records: **{len(filtered_df):,}** / {len(df_raw):,}")

# ==============================================================================
# EXECUTIVE KPI RIBBON
# ==============================================================================

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.metric(
        label="Daily E-Waste",
        value=f"{total_waste:,.1f} TPD",
        delta=f"{(total_waste / len(filtered_df)):.2f} TPD/City"
    )

with k2:
    st.metric(
        label="Recycling Rate",
        value=f"{weighted_recycling:.1f}%",
        delta=f"{weighted_recycling - national_avg_recycling:+.1f}% vs National"
    )

with k3:
    st.metric(
        label="Collection Eff.",
        value=f"{weighted_collection:.1f}%",
        delta=f"{weighted_collection - national_avg_collection:+.1f}% vs National"
    )

with k4:
    st.metric(
        label="Processing Cap.",
        value=f"{avg_processing:,.1f} TPD",
        delta=f"{avg_processing - (total_waste / max(1, filtered_df['State'].nunique())):+.1f} Net Gap"
    )

with k5:
    st.metric(
        label="Carbon Footprint",
        value=f"{total_carbon:,.0f} MT",
        delta=f"{(total_carbon / max(1, total_waste)):.2f} MT/Ton",
        delta_color="inverse"
    )

with k6:
    st.metric(
        label="Sustainability",
        value=f"{avg_sustainability:.1f} / 100",
        delta=f"Score Tier: {'High' if avg_sustainability > 60 else 'Moderate' if avg_sustainability > 40 else 'Critical'}"
    )

st.write("")

# ==============================================================================
# TABBED NAVIGATION (CLEAN, MODERN, ZERO RAW HTML)
# ==============================================================================

tab_overview, tab_geo, tab_states, tab_trends, tab_sustainability, tab_explorer = st.tabs([
    "📊 Executive Overview",
    "🗺️ Geospatial Intelligence",
    "🏛️ State Benchmarking",
    "📈 Temporal Trends",
    "🌱 Carbon & Environment",
    "🔍 Data Explorer"
])

# ==============================================================================
# TAB 1: EXECUTIVE OVERVIEW
# ==============================================================================

with tab_overview:
    # Row 1: National Geographic Distribution & Strategic Quadrant
    col_map, col_quadrant = st.columns([1.2, 1])

    with col_map:
        with st.container(border=True):
            st.subheader("📍 National E-Waste Concentration Map")
            st.caption("Bubble size indicates daily generation; color indicates recycling performance.")

            # Aggregate by City for Clean Map Plotting
            city_geo = filtered_df.groupby(["City", "State", "Region"], as_index=False).agg({
                "Latitude": "first",
                "Longitude": "first",
                "Daily_Waste_Generation_Tons": "sum",
                "Recycling_Rate": "mean",
                "Collection_Efficiency_Percentage": "mean",
                "Air_Quality_Index": "mean"
            }).dropna(subset=["Latitude", "Longitude"])

            if not city_geo.empty:
                map_fig = px.scatter_map(
                    city_geo,
                    lat="Latitude",
                    lon="Longitude",
                    size="Daily_Waste_Generation_Tons",
                    color="Recycling_Rate",
                    color_continuous_scale="Mint",
                    hover_name="City",
                    hover_data={
                        "State": True,
                        "Daily_Waste_Generation_Tons": ":.1f",
                        "Recycling_Rate": ":.1f%",
                        "Collection_Efficiency_Percentage": ":.1f%",
                        "Latitude": False,
                        "Longitude": False
                    },
                    zoom=3.6,
                    center={"lat": 22.0, "lon": 79.5},
                    map_style="carto-darkmatter"
                )
                map_fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=460)
                st.plotly_chart(map_fig, use_container_width=True)
            else:
                st.info("No geospatial coordinates available for current selection.")

    with col_quadrant:
        with st.container(border=True):
            st.subheader("🎯 Strategic Performance Quadrant")
            st.caption("Collection Efficiency vs. Recycling Rate across states.")

            state_agg = filtered_df.groupby("State", as_index=False).agg({
                "Daily_Waste_Generation_Tons": "sum",
                "Recycling_Rate": lambda x: calc_weighted_avg(filtered_df[filtered_df["State"] == x.name], "Recycling_Rate"),
                "Collection_Efficiency_Percentage": lambda x: calc_weighted_avg(filtered_df[filtered_df["State"] == x.name], "Collection_Efficiency_Percentage"),
                "Region": "first"
            })

            scatter_fig = px.scatter(
                state_agg,
                x="Collection_Efficiency_Percentage",
                y="Recycling_Rate",
                size="Daily_Waste_Generation_Tons",
                color="Region",
                hover_name="State",
                labels={
                    "Collection_Efficiency_Percentage": "Collection Efficiency (%)",
                    "Recycling_Rate": "Recycling Rate (%)",
                    "Daily_Waste_Generation_Tons": "Waste Generated (TPD)"
                },
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            scatter_fig.add_hline(y=50, line_dash="dash", line_color="rgba(52, 211, 153, 0.4)", annotation_text="50% Target")
            scatter_fig.add_vline(x=70, line_dash="dash", line_color="rgba(6, 182, 212, 0.4)", annotation_text="70% Target")
            apply_plotly_theme(scatter_fig, height=460)
            st.plotly_chart(scatter_fig, use_container_width=True)

    # Row 2: Top Generators vs Recycling Leaders
    col_top_gen, col_top_rec = st.columns(2)

    with col_top_gen:
        with st.container(border=True):
            st.subheader("🗑️ Top 10 Waste Generating States")
            top_gen = state_agg.sort_values("Daily_Waste_Generation_Tons", ascending=False).head(10)
            fig_bar_gen = px.bar(
                top_gen,
                x="Daily_Waste_Generation_Tons",
                y="State",
                orientation="h",
                color="Daily_Waste_Generation_Tons",
                color_continuous_scale="Tealgrn",
                labels={"Daily_Waste_Generation_Tons": "Tons Per Day"}
            )
            fig_bar_gen.update_layout(yaxis=dict(autorange="reversed"))
            apply_plotly_theme(fig_bar_gen, height=380)
            st.plotly_chart(fig_bar_gen, use_container_width=True)

    with col_top_rec:
        with st.container(border=True):
            st.subheader("♻️ Top 10 Recycling Champions")
            top_rec = state_agg.sort_values("Recycling_Rate", ascending=False).head(10)
            fig_bar_rec = px.bar(
                top_rec,
                x="Recycling_Rate",
                y="State",
                orientation="h",
                color="Recycling_Rate",
                color_continuous_scale="Mint",
                labels={"Recycling_Rate": "Recycling Rate (%)"}
            )
            fig_bar_rec.update_layout(yaxis=dict(autorange="reversed"))
            apply_plotly_theme(fig_bar_rec, height=380)
            st.plotly_chart(fig_bar_rec, use_container_width=True)

# ==============================================================================
# TAB 2: GEOSPATIAL INTELLIGENCE
# ==============================================================================

with tab_geo:
    with st.container(border=True):
        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            st.subheader("🏙️ City-Level Granular Surveillance")
            st.caption("Explore city-level waste generation, infrastructure readiness, and environmental load.")
        with col_m2:
            geo_metric = st.selectbox(
                "Map Color Metric",
                ["Recycling_Rate", "Air_Quality_Index", "Collection_Efficiency_Percentage", "Smart_Bins_Count"],
                format_func=lambda x: x.replace("_", " ")
            )

        city_full = filtered_df.groupby(["City", "State", "Region", "City_Category"], as_index=False).agg({
            "Latitude": "first",
            "Longitude": "first",
            "Daily_Waste_Generation_Tons": "sum",
            "Recycling_Rate": "mean",
            "Collection_Efficiency_Percentage": "mean",
            "Air_Quality_Index": "mean",
            "Smart_Bins_Count": "sum",
            "Worker_Count": "sum",
            "Waste_Collection_Vehicles": "sum"
        }).dropna(subset=["Latitude", "Longitude"])

        city_map_fig = px.scatter_map(
            city_full,
            lat="Latitude",
            lon="Longitude",
            size="Daily_Waste_Generation_Tons",
            color=geo_metric,
            color_continuous_scale="Viridis" if geo_metric == "Air_Quality_Index" else "Emrld",
            hover_name="City",
            hover_data={
                "State": True,
                "City_Category": True,
                "Daily_Waste_Generation_Tons": ":.1f",
                "Recycling_Rate": ":.1f%",
                "Smart_Bins_Count": ":,",
                "Air_Quality_Index": ":.0f",
                "Latitude": False,
                "Longitude": False
            },
            zoom=3.8,
            center={"lat": 22.0, "lon": 79.5},
            map_style="carto-darkmatter"
        )
        city_map_fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=520)
        st.plotly_chart(city_map_fig, use_container_width=True)

    # City Category Infrastructure Breakdown
    c_cat1, c_cat2 = st.columns(2)
    with c_cat1:
        with st.container(border=True):
            st.subheader("📊 Performance by City Category")
            cat_summary = filtered_df.groupby("City_Category", as_index=False).agg({
                "Daily_Waste_Generation_Tons": "mean",
                "Recycling_Rate": "mean",
                "Collection_Efficiency_Percentage": "mean"
            })
            fig_cat = px.bar(
                cat_summary,
                x="City_Category",
                y=["Recycling_Rate", "Collection_Efficiency_Percentage"],
                barmode="group",
                color_discrete_sequence=["#10b981", "#06b6d4"],
                labels={"value": "Percentage (%)", "City_Category": "Tier"}
            )
            apply_plotly_theme(fig_cat, height=360)
            st.plotly_chart(fig_cat, use_container_width=True)

    with c_cat2:
        with st.container(border=True):
            st.subheader("🤖 Smart Bins & Fleet Deployment")
            cat_infra = filtered_df.groupby("City_Category", as_index=False).agg({
                "Smart_Bins_Count": "sum",
                "Waste_Collection_Vehicles": "sum"
            })
            fig_infra = px.bar(
                cat_infra,
                x="City_Category",
                y=["Smart_Bins_Count", "Waste_Collection_Vehicles"],
                barmode="group",
                color_discrete_sequence=["#38bdf8", "#f59e0b"],
                labels={"value": "Units Deployed", "City_Category": "Tier"}
            )
            apply_plotly_theme(fig_infra, height=360)
            st.plotly_chart(fig_infra, use_container_width=True)

# ==============================================================================
# TAB 3: STATE BENCHMARKING & RADAR COMPARISON
# ==============================================================================

with tab_states:
    state_metrics = filtered_df.groupby(["State", "Region"], as_index=False).agg({
        "Daily_Waste_Generation_Tons": "sum",
        "Recycling_Rate": "mean",
        "Collection_Efficiency_Percentage": "mean",
        "Waste_Processing_Capacity": "mean",
        "Municipal_Efficiency_Score": "mean",
        "Sustainability_Index": "mean",
        "Waste_Management_Budget_INR": "sum"
    })

    col_rank, col_radar = st.columns([1.1, 1])

    with col_rank:
        with st.container(border=True):
            st.subheader("🏆 State Performance Rankings")
            rank_col = st.selectbox(
                "Rank States By Metric",
                [
                    "Sustainability_Index",
                    "Recycling_Rate",
                    "Collection_Efficiency_Percentage",
                    "Daily_Waste_Generation_Tons",
                    "Municipal_Efficiency_Score",
                    "Waste_Processing_Capacity"
                ],
                format_func=lambda x: x.replace("_", " ")
            )
            sorted_states = state_metrics.sort_values(rank_col, ascending=False).head(15)
            fig_rank = px.bar(
                sorted_states,
                x=rank_col,
                y="State",
                orientation="h",
                color="Region",
                color_discrete_sequence=px.colors.qualitative.Dark24
            )
            fig_rank.update_layout(yaxis=dict(autorange="reversed"))
            apply_plotly_theme(fig_rank, height=480)
            st.plotly_chart(fig_rank, use_container_width=True)

    with col_radar:
        with st.container(border=True):
            st.subheader("⚔️ Head-to-Head State Matchup")
            st.caption("Compare two states across 5 key dimensions.")
            
            s1, s2 = st.columns(2)
            all_state_names = sorted(state_metrics["State"].unique())
            state_a = s1.selectbox("Primary State", all_state_names, index=0)
            state_b = s2.selectbox("Comparison State", all_state_names, index=min(1, len(all_state_names)-1))

            def get_state_normalized_scores(s_name):
                row = state_metrics[state_metrics["State"] == s_name]
                if row.empty:
                    return [0, 0, 0, 0, 0]
                r_rate = float(row["Recycling_Rate"].iloc[0])
                c_eff = float(row["Collection_Efficiency_Percentage"].iloc[0])
                m_score = float(row["Municipal_Efficiency_Score"].iloc[0]) * 20 # 5 scale to 100
                s_idx = float(row["Sustainability_Index"].iloc[0])
                proc_cap = min(100.0, float(row["Waste_Processing_Capacity"].iloc[0]) * 10)
                return [r_rate, c_eff, m_score, s_idx, proc_cap]

            categories = ["Recycling Rate", "Collection Eff", "Municipal Score", "Sustainability", "Capacity Index"]
            vals_a = get_state_normalized_scores(state_a)
            vals_b = get_state_normalized_scores(state_b)

            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(
                r=vals_a,
                theta=categories,
                fill="toself",
                name=state_a,
                line_color="#10b981",
                fillcolor="rgba(16, 185, 129, 0.25)"
            ))
            radar_fig.add_trace(go.Scatterpolar(
                r=vals_b,
                theta=categories,
                fill="toself",
                name=state_b,
                line_color="#06b6d4",
                fillcolor="rgba(6, 182, 212, 0.25)"
            ))
            radar_fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)"
                ),
                showlegend=True
            )
            apply_plotly_theme(radar_fig, height=480)
            st.plotly_chart(radar_fig, use_container_width=True)

# ==============================================================================
# TAB 4: TEMPORAL TRENDS & SEASONALITY
# ==============================================================================

with tab_trends:
    col_t1, col_t2 = st.columns([1.2, 1])

    with col_t1:
        with st.container(border=True):
            st.subheader("📈 Multi-Year National Progression")
            st.caption("Annual evolution of Recycling Rate and Collection Efficiency.")

            annual_trend = df_raw.groupby("Year", as_index=False).agg({
                "Daily_Waste_Generation_Tons": "sum",
                "Recycling_Rate": "mean",
                "Collection_Efficiency_Percentage": "mean"
            })

            trend_fig = go.Figure()
            trend_fig.add_trace(go.Scatter(
                x=annual_trend["Year"],
                y=annual_trend["Recycling_Rate"],
                mode="lines+markers",
                name="Recycling Rate (%)",
                line=dict(color="#10b981", width=3),
                marker=dict(size=7)
            ))
            trend_fig.add_trace(go.Scatter(
                x=annual_trend["Year"],
                y=annual_trend["Collection_Efficiency_Percentage"],
                mode="lines+markers",
                name="Collection Efficiency (%)",
                line=dict(color="#06b6d4", width=3, dash="dot"),
                marker=dict(size=7)
            ))
            apply_plotly_theme(trend_fig, height=380)
            st.plotly_chart(trend_fig, use_container_width=True)

    with col_t2:
        with st.container(border=True):
            st.subheader("🌦️ Seasonal Impact Analysis")
            st.caption("Waste generation variability across seasons.")

            season_df = filtered_df.groupby("Season", as_index=False).agg({
                "Daily_Waste_Generation_Tons": "mean",
                "Air_Quality_Index": "mean"
            })
            season_fig = px.bar(
                season_df,
                x="Season",
                y="Daily_Waste_Generation_Tons",
                color="Season",
                color_discrete_sequence=["#38bdf8", "#f59e0b", "#10b981", "#a855f7"],
                labels={"Daily_Waste_Generation_Tons": "Avg TPD"}
            )
            apply_plotly_theme(season_fig, height=380)
            st.plotly_chart(season_fig, use_container_width=True)

    # Budget vs Recycling ROI
    with st.container(border=True):
        st.subheader("💰 Municipal Budget vs. Recycling Outcome")
        st.caption("Assessing fiscal efficiency: Does higher budget allocation directly boost recycling outcomes?")
        
        budget_scatter = px.scatter(
            filtered_df,
            x="Waste_Management_Budget_INR",
            y="Recycling_Rate",
            color="Region",
            size="Daily_Waste_Generation_Tons",
            hover_name="City",
            labels={
                "Waste_Management_Budget_INR": "Budget (INR)",
                "Recycling_Rate": "Recycling Rate (%)"
            },
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        apply_plotly_theme(budget_scatter, height=400)
        st.plotly_chart(budget_scatter, use_container_width=True)

# ==============================================================================
# TAB 5: CARBON & ENVIRONMENT
# ==============================================================================

with tab_sustainability:
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        with st.container(border=True):
            st.subheader("♻️ Treatment Method Distribution")
            st.caption("How collected municipal e-waste is processed across India.")
            
            treatment_counts = filtered_df["Treatment_Method"].value_counts().reset_index()
            treatment_counts.columns = ["Treatment_Method", "Count"]

            fig_donut = px.pie(
                treatment_counts,
                names="Treatment_Method",
                values="Count",
                hole=0.62,
                color_discrete_sequence=["#10b981", "#f43f5e", "#f59e0b", "#06b6d4", "#8b5cf6"]
            )
            apply_plotly_theme(fig_donut, height=380)
            st.plotly_chart(fig_donut, use_container_width=True)

    with col_c2:
        with st.container(border=True):
            st.subheader("🏭 Carbon Emissions by Region")
            st.caption("Estimated metric tons of CO2 equivalent from unmanaged e-waste.")

            carbon_reg = filtered_df.groupby("Region", as_index=False)["Carbon_Emission_From_Waste"].sum()
            fig_carbon = px.bar(
                carbon_reg,
                x="Region",
                y="Carbon_Emission_From_Waste",
                color="Carbon_Emission_From_Waste",
                color_continuous_scale="Reds",
                labels={"Carbon_Emission_From_Waste": "MT CO2e"}
            )
            apply_plotly_theme(fig_carbon, height=380)
            st.plotly_chart(fig_carbon, use_container_width=True)

    # AQI vs Waste Generation Correlate
    with st.container(border=True):
        st.subheader("🌫️ Air Quality Index (AQI) vs Industrial Activity Level")
        st.caption("Examining the intersection between industrial presence and air quality in waste hubs.")

        fig_aqi = px.scatter(
            filtered_df,
            x="Industrial_Activity_Level",
            y="Air_Quality_Index",
            color="Sustainability_Category",
            size="Daily_Waste_Generation_Tons",
            hover_name="City",
            color_discrete_map={
                "Poor": "#ef4444",
                "Average": "#f59e0b",
                "Good": "#10b981",
                "Excellent": "#06b6d4"
            }
        )
        apply_plotly_theme(fig_aqi, height=380)
        st.plotly_chart(fig_aqi, use_container_width=True)

# ==============================================================================
# TAB 6: DATA EXPLORER & EXPORT
# ==============================================================================

with tab_explorer:
    with st.container(border=True):
        st.subheader("🔍 Master E-Waste Records Explorer")
        st.caption("Inspect, search, and download filtered municipal records.")

        search_query = st.text_input("Quick Search (City or State)", "")
        
        display_df = filtered_df.copy()
        if search_query:
            display_df = display_df[
                display_df["City"].str.contains(search_query, case=False, na=False) |
                display_df["State"].str.contains(search_query, case=False, na=False)
            ]

        # Key Columns for display
        cols_to_show = [
            "City", "State", "Region", "City_Category", "Year",
            "Daily_Waste_Generation_Tons", "Recycling_Rate",
            "Collection_Efficiency_Percentage", "Waste_Processing_Capacity",
            "Air_Quality_Index", "Smart_Bins_Count", "Sustainability_Index", "Treatment_Method"
        ]

        st.dataframe(
            display_df[cols_to_show],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Daily_Waste_Generation_Tons": st.column_config.NumberColumn("Daily Waste (TPD)", format="%.2f"),
                "Recycling_Rate": st.column_config.ProgressColumn("Recycling Rate", min_value=0, max_value=100, format="%.1f%%"),
                "Collection_Efficiency_Percentage": st.column_config.ProgressColumn("Collection Eff.", min_value=0, max_value=100, format="%.1f%%"),
                "Sustainability_Index": st.column_config.ProgressColumn("Sustainability", min_value=0, max_value=100, format="%.1f"),
                "Waste_Processing_Capacity": st.column_config.NumberColumn("Capacity (TPD)", format="%.2f"),
                "Air_Quality_Index": st.column_config.NumberColumn("AQI", format="%d"),
                "Smart_Bins_Count": st.column_config.NumberColumn("Smart Bins", format="%d")
            },
            height=480
        )

        # Export Buttons
        c_exp1, c_exp2 = st.columns([1, 4])
        with c_exp1:
            csv_data = display_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Export Filtered CSV",
                data=csv_data,
                file_name=f"ecocycle_india_{selected_year}.csv",
                mime="text/csv"
            )

# ==============================================================================
# FOOTER
# ==============================================================================

st.divider()
f1, f2 = st.columns([2, 1])
with f1:
    st.caption("🌿 **EcoCycle India Telemetry Dashboard** • National E-Waste Analytics Platform")
with f2:
    st.caption("Engineered with Python • Streamlit • Plotly • Machine Learning Ready")