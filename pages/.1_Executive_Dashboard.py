import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🚀 Executive Startup Dashboard")
st.markdown("### Deep Analytics of Startup Ecosystem")

st.markdown("---")

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------
st.sidebar.header("🎯 Dashboard Filters")

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

exit_status = st.sidebar.multiselect(
    "Exit Status",
    options=df["Exit Status"].unique(),
    default=df["Exit Status"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region)) &
    (df["Exit Status"].isin(exit_status))
]

# -----------------------------------
# KPI METRICS
# -----------------------------------
st.subheader("📊 Key Performance Indicators")

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:
    st.metric(
        "Total Startups",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Total Funding",
        f"${filtered_df['Funding Amount (M USD)'].sum():,.0f}M"
    )

with col3:
    st.metric(
        "Avg Valuation",
        f"${filtered_df['Valuation (M USD)'].mean():,.0f}M"
    )

with col4:
    st.metric(
        "Total Revenue",
        f"${filtered_df['Revenue (M USD)'].sum():,.0f}M"
    )

with col5:
    st.metric(
        "Employees",
        f"{filtered_df['Employees'].sum():,}"
    )

with col6:
    st.metric(
        "Profitability %",
        f"{filtered_df['Profitable'].mean()*100:.1f}%"
    )

st.markdown("---")

# -----------------------------------
# CHARTS ROW 1
# -----------------------------------
col1,col2 = st.columns(2)

with col1:

    industry_funding = (
        filtered_df
        .groupby("Industry")["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="💰 Funding by Industry",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    region_funding = (
        filtered_df
        .groupby("Region")["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_funding,
        names="Region",
        values="Funding Amount (M USD)",
        title="🌍 Funding Distribution by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------------
# CHARTS ROW 2
# -----------------------------------
col1,col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        size="Revenue (M USD)",
        color="Industry",
        hover_name="Startup Name",
        title="📈 Funding vs Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    profitability = (
        filtered_df["Profitable"]
        .value_counts()
        .reset_index()
    )

    profitability.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        profitability,
        names="Status",
        values="Count",
        title="🏆 Profitability Breakdown"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------------
# TOP STARTUPS
# -----------------------------------
st.markdown("---")

st.subheader("🏅 Top 10 Most Valuable Startups")

top10 = (
    filtered_df
    .sort_values(
        by="Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10,
    use_container_width=True
)

# -----------------------------------
# MARKET SHARE ANALYSIS
# -----------------------------------
st.markdown("---")

st.subheader("📊 Market Share Analysis")

market_share = (
    filtered_df
    .groupby("Industry")["Market Share (%)"]
    .sum()
    .reset_index()
)

fig = px.treemap(
    market_share,
    path=["Industry"],
    values="Market Share (%)",
    title="Industry Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# STARTUP FOUNDATION TREND
# -----------------------------------
st.markdown("---")

st.subheader("📅 Startup Foundation Trend")

yearly = (
    filtered_df
    .groupby("Year Founded")
    .size()
    .reset_index(name="Count")
)

fig = px.line(
    yearly,
    x="Year Founded",
    y="Count",
    markers=True,
    title="Startups Founded Per Year"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# REVENUE ANALYSIS
# -----------------------------------
st.markdown("---")

st.subheader("💵 Revenue by Industry")

revenue = (
    filtered_df
    .groupby("Industry")["Revenue (M USD)"]
    .sum()
    .reset_index()
)

fig = px.bar(
    revenue,
    x="Industry",
    y="Revenue (M USD)",
    color="Industry",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# INSIGHTS SECTION
# -----------------------------------
st.markdown("---")

st.subheader("🤖 Automated Business Insights")

highest_funding_industry = (
    filtered_df
    .groupby("Industry")["Funding Amount (M USD)"]
    .mean()
    .idxmax()
)

highest_valuation_industry = (
    filtered_df
    .groupby("Industry")["Valuation (M USD)"]
    .mean()
    .idxmax()
)

top_region = (
    filtered_df
    .groupby("Region")["Valuation (M USD)"]
    .sum()
    .idxmax()
)

st.success(
    f"🚀 Highest average funding industry: {highest_funding_industry}"
)

st.success(
    f"💎 Highest valuation industry: {highest_valuation_industry}"
)

st.success(
    f"🌍 Top valuation region: {top_region}"
)

st.success(
    f"📈 Profitability Rate: {filtered_df['Profitable'].mean()*100:.2f}%"
)

st.markdown("---")

st.caption("Created using Streamlit + Plotly + Startup Dataset Analytics")
