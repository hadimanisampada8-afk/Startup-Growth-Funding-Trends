import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("🤖 AI-Powered Startup Insights")
st.markdown("### Automated Intelligence & Executive Recommendations")

st.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🎯 Filters")

industry = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
]

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------
st.subheader("📋 Executive Summary")

total_startups = len(filtered_df)
total_funding = filtered_df["Funding Amount (M USD)"].sum()
total_revenue = filtered_df["Revenue (M USD)"].sum()
total_valuation = filtered_df["Valuation (M USD)"].sum()
profitability_rate = filtered_df["Profitable"].mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Startups", total_startups)
col2.metric("Funding", f"${total_funding:,.0f}M")
col3.metric("Revenue", f"${total_revenue:,.0f}M")
col4.metric("Valuation", f"${total_valuation:,.0f}M")
col5.metric("Profitability", f"{profitability_rate:.1f}%")

st.markdown("---")

# --------------------------------------------------
# CORRELATION HEATMAP
# --------------------------------------------------
st.subheader("🔥 Correlation Intelligence")

numeric_df = filtered_df.select_dtypes(
    include=["int64", "float64"]
)

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# INDUSTRY RANKING
# --------------------------------------------------
st.markdown("---")
st.subheader("🏆 Industry Performance Ranking")

industry_rank = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "sum",
        "Market Share (%)": "sum"
    })
    .reset_index()
)

industry_rank["Performance Score"] = (
    industry_rank["Funding Amount (M USD)"] +
    industry_rank["Revenue (M USD)"] +
    industry_rank["Valuation (M USD)"]
)

industry_rank = industry_rank.sort_values(
    "Performance Score",
    ascending=False
)

st.dataframe(
    industry_rank,
    use_container_width=True
)

# --------------------------------------------------
# TOP INDUSTRIES
# --------------------------------------------------
st.markdown("---")
st.subheader("🚀 Top Performing Industries")

fig = px.bar(
    industry_rank.head(10),
    x="Industry",
    y="Performance Score",
    color="Industry",
    text_auto=True,
    title="Industry Performance Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# FUNDING EFFICIENCY
# --------------------------------------------------
st.markdown("---")
st.subheader("💰 Funding Efficiency Analysis")

efficiency = filtered_df.copy()

efficiency["Funding Efficiency"] = (
    efficiency["Revenue (M USD)"] /
    efficiency["Funding Amount (M USD)"]
)

top_efficiency = efficiency.sort_values(
    "Funding Efficiency",
    ascending=False
).head(20)

fig = px.bar(
    top_efficiency,
    x="Startup Name",
    y="Funding Efficiency",
    color="Industry",
    title="Top Funding Efficient Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REVENUE EFFICIENCY
# --------------------------------------------------
st.markdown("---")
st.subheader("📈 Revenue Per Employee")

efficiency["Revenue Per Employee"] = (
    efficiency["Revenue (M USD)"] /
    efficiency["Employees"]
)

top_emp = efficiency.sort_values(
    "Revenue Per Employee",
    ascending=False
).head(20)

fig = px.bar(
    top_emp,
    x="Startup Name",
    y="Revenue Per Employee",
    color="Industry",
    title="Revenue Generated Per Employee"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# UNICORN ANALYSIS
# --------------------------------------------------
st.markdown("---")
st.subheader("🦄 Unicorn Intelligence")

unicorns = filtered_df[
    filtered_df["Valuation (M USD)"] >= 1000
]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Unicorns",
        len(unicorns)
    )

with col2:
    st.metric(
        "Unicorn Valuation",
        f"${unicorns['Valuation (M USD)'].sum():,.0f}M"
    )

st.dataframe(
    unicorns[
        [
            "Startup Name",
            "Industry",
            "Valuation (M USD)",
            "Revenue (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# REGION ANALYSIS
# --------------------------------------------------
st.markdown("---")
st.subheader("🌎 Regional Intelligence")

region_analysis = (
    filtered_df
    .groupby("Region")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "sum"
    })
    .reset_index()
)

fig = px.sunburst(
    region_analysis,
    path=["Region"],
    values="Valuation (M USD)",
    title="Regional Valuation Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# PREDICTIVE SCORE
# --------------------------------------------------
st.markdown("---")
st.subheader("📊 Startup Growth Potential")

growth = filtered_df.copy()

growth["Growth Score"] = (
    growth["Funding Amount (M USD)"] * 0.3 +
    growth["Revenue (M USD)"] * 0.3 +
    growth["Valuation (M USD)"] * 0.4
)

top_growth = growth.sort_values(
    "Growth Score",
    ascending=False
).head(20)

fig = px.bar(
    top_growth,
    x="Startup Name",
    y="Growth Score",
    color="Industry",
    title="Future Growth Potential Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# AI GENERATED INSIGHTS
# --------------------------------------------------
st.markdown("---")
st.subheader("🤖 AI Generated Insights")

top_funding_industry = (
    filtered_df
    .groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_revenue_industry = (
    filtered_df
    .groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

top_valuation_industry = (
    filtered_df
    .groupby("Industry")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df
    .groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

top_startup = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"🚀 Highest funded industry: {top_funding_industry}"
)

st.success(
    f"💰 Highest revenue industry: {top_revenue_industry}"
)

st.success(
    f"📈 Highest valuation industry: {top_valuation_industry}"
)

st.success(
    f"🌎 Leading startup region: {top_region}"
)

st.success(
    f"🏆 Most valuable startup: {top_startup}"
)

# --------------------------------------------------
# STRATEGIC RECOMMENDATIONS
# --------------------------------------------------
st.markdown("---")
st.subheader("🎯 Strategic Recommendations")

recommendations = [
    "Increase investments in industries showing highest valuation growth.",
    "Focus on regions generating strong funding-to-revenue conversion.",
    "Monitor unicorn startups for acquisition opportunities.",
    "Improve employee productivity through revenue efficiency benchmarking.",
    "Target high-growth startups with strong funding efficiency ratios."
]

for rec in recommendations:
    st.info(rec)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption(
    "AI Insights Dashboard | Streamlit + Plotly | Startup Ecosystem Intelligence"
)
