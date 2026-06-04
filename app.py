import streamlit as st
from utils.styling import (
    apply_theme,
    page_banner,
    section_header,
    dashboard_footer,
    insight_box
)
from utils.data_loader import (
    load_data,
    get_kpis
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# APPLY CUSTOM STYLING
# --------------------------------------------------
apply_theme()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = load_data()

kpis = get_kpis(df)

# --------------------------------------------------
# HERO BANNER
# --------------------------------------------------
page_banner(
    "🚀 Startup Analytics Dashboard",
    "Executive Intelligence Platform for Startup Ecosystem Analysis"
)

# --------------------------------------------------
# WELCOME SECTION
# --------------------------------------------------
st.markdown("""
### Welcome to the Startup Analytics Platform

Analyze startup funding, valuation, revenue, market share,
profitability, growth potential and industry trends through
interactive dashboards and AI-powered insights.

Use the sidebar navigation to explore detailed analytics.
""")

st.markdown("---")

# --------------------------------------------------
# KPI OVERVIEW
# --------------------------------------------------
section_header("📊 Executive Snapshot")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚀 Total Startups",
        f"{kpis['total_startups']:,}"
    )

    st.metric(
        "💰 Total Funding",
        f"${kpis['total_funding']:,.0f}M"
    )

with col2:
    st.metric(
        "📈 Average Valuation",
        f"${kpis['avg_valuation']:,.0f}M"
    )

    st.metric(
        "💵 Total Revenue",
        f"${kpis['total_revenue']:,.0f}M"
    )

with col3:
    st.metric(
        "👨‍💼 Total Employees",
        f"{kpis['total_employees']:,}"
    )

    st.metric(
        "🏆 Profitability",
        f"{kpis['profitability_rate']:.2f}%"
    )

st.markdown("---")

# --------------------------------------------------
# DASHBOARD MODULES
# --------------------------------------------------
section_header("🧠 Analytics Modules")

module1, module2 = st.columns(2)

with module1:

    st.info("""
    ### 📊 Executive Dashboard

    - Startup KPIs
    - Industry Overview
    - Regional Analytics
    - Funding Overview
    - Valuation Snapshot
    """)

    st.info("""
    ### 💰 Funding Analytics

    - Funding Trends
    - Funding Distribution
    - Industry Funding
    - Region Funding
    - Funding Efficiency
    """)

    st.info("""
    ### 📈 Valuation Analytics

    - Valuation Distribution
    - Unicorn Analysis
    - Top Valued Startups
    - Valuation Heatmaps
    """)

with module2:

    st.info("""
    ### 💵 Revenue Analytics

    - Revenue Performance
    - Revenue Efficiency
    - Revenue Trends
    - Revenue vs Employees
    """)

    st.info("""
    ### 🌍 Market Analytics

    - Market Share
    - Competitive Landscape
    - Industry Dominance
    - Regional Analysis
    """)

    st.info("""
    ### 💹 Profitability Insights

    - Profitability Trends
    - Industry Comparison
    - Revenue Impact
    - Funding Impact
    """)

st.markdown("---")

# --------------------------------------------------
# AI INSIGHTS PREVIEW
# --------------------------------------------------
section_header("🤖 AI Insight Preview")

top_industry = (
    df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    df.groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

top_startup = (
    df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

insight_box(
    f"Highest funded industry: {top_industry}"
)

insight_box(
    f"Leading startup region: {top_region}"
)

insight_box(
    f"Most valuable startup: {top_startup}"
)

insight_box(
    f"Overall profitability rate is {kpis['profitability_rate']:.2f}%"
)

st.markdown("---")

# --------------------------------------------------
# DATA OVERVIEW
# --------------------------------------------------
section_header("📁 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("### Industries")
    st.write(df["Industry"].nunique())

with col2:
    st.write("### Regions")
    st.write(df["Region"].nunique())

with col3:
    st.write("### Exit Categories")
    st.write(df["Exit Status"].nunique())

st.markdown("---")

# --------------------------------------------------
# SAMPLE DATA
# --------------------------------------------------
section_header("🔍 Dataset Preview")

st.dataframe(
    df.head(15),
    use_container_width=True
)

st.markdown("---")

# --------------------------------------------------
# SIDEBAR NAVIGATION HELP
# --------------------------------------------------
st.sidebar.success("🚀 Startup Analytics Platform")

st.sidebar.markdown("""
### Navigation

📊 Executive Dashboard

💰 Funding Analytics

📈 Valuation Analytics

💵 Revenue Analytics

🌍 Market Analytics

💹 Profitability Insights

🤖 AI Insights
""")

st.sidebar.markdown("---")

st.sidebar.info(
    "Select a page from the sidebar to explore detailed analytics."
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
dashboard_footer()
