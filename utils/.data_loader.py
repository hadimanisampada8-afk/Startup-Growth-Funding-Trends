import os
import sys
import streamlit as st

# Fix imports on Streamlit Cloud
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from utils.data_loader import load_data, get_kpis
from utils.styling import (
    apply_theme,
    page_banner,
    section_header,
    dashboard_footer
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="🚀 Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

apply_theme()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = load_data()
    kpis = get_kpis(df)

except Exception as e:
    st.error(f"Data Loading Error: {e}")
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

page_banner(
    "🚀 Startup Analytics Dashboard",
    "Executive Intelligence Platform"
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

section_header("Executive Snapshot")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Startups",
        kpis["total_startups"]
    )

    st.metric(
        "Total Funding",
        f"${kpis['total_funding']:,.0f}M"
    )

with c2:
    st.metric(
        "Average Valuation",
        f"${kpis['avg_valuation']:,.0f}M"
    )

    st.metric(
        "Total Revenue",
        f"${kpis['total_revenue']:,.0f}M"
    )

with c3:
    st.metric(
        "Employees",
        f"{kpis['total_employees']:,}"
    )

    st.metric(
        "Profitability",
        f"{kpis['profitability_rate']}%"
    )

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

section_header("Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.success(
    "Startup Analytics Platform"
)

st.sidebar.info(
    "Use the Pages menu to navigate through analytics."
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

dashboard_footer()
