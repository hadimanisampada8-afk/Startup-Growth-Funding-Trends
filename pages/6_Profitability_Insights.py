import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Profitability Insights",
    page_icon="💹",
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
st.title("💹 Profitability Insights Dashboard")
st.markdown("### Deep Analysis of Startup Profitability")

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
# KPI SECTION
# --------------------------------------------------
profitable_count = filtered_df["Profitable"].sum()
non_profitable_count = len(filtered_df) - profitable_count
profit_rate = (profitable_count / len(filtered_df)) * 100

st.subheader("📊 Profitability KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Startups",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Profitable",
        profitable_count
    )

with col3:
    st.metric(
        "Non-Profitable",
        non_profitable_count
    )

with col4:
    st.metric(
        "Profitability Rate",
        f"{profit_rate:.2f}%"
    )

st.markdown("---")

# --------------------------------------------------
# PROFITABILITY OVERVIEW
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    profitability = (
        filtered_df["Profitable"]
        .value_counts()
        .reset_index()
    )

    profitability.columns = ["Status", "Count"]

    fig = px.pie(
        profitability,
        names="Status",
        values="Count",
        title="Profitability Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    profit_region = (
        filtered_df
        .groupby("Region")["Profitable"]
        .mean()
        .reset_index()
    )

    profit_region["Profitable"] = (
        profit_region["Profitable"] * 100
    )

    fig = px.bar(
        profit_region,
        x="Region",
        y="Profitable",
        text_auto=True,
        title="Profitability Rate by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# INDUSTRY PROFITABILITY
# --------------------------------------------------
st.markdown("---")

st.subheader("🏭 Profitability by Industry")

industry_profit = (
    filtered_df
    .groupby("Industry")["Profitable"]
    .mean()
    .reset_index()
)

industry_profit["Profitable"] = (
    industry_profit["Profitable"] * 100
)

fig = px.bar(
    industry_profit,
    x="Industry",
    y="Profitable",
    color="Industry",
    text_auto=True,
    title="Industry Profitability Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# PROFITABLE VS REVENUE
# --------------------------------------------------
st.markdown("---")

st.subheader("💰 Revenue Comparison")

revenue_profit = (
    filtered_df
    .groupby("Profitable")
    ["Revenue (M USD)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    revenue_profit,
    x="Profitable",
    y="Revenue (M USD)",
    text_auto=True,
    title="Average Revenue by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# PROFITABLE VS VALUATION
# --------------------------------------------------
st.markdown("---")

st.subheader("📈 Valuation Comparison")

valuation_profit = (
    filtered_df
    .groupby("Profitable")
    ["Valuation (M USD)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    valuation_profit,
    x="Profitable",
    y="Valuation (M USD)",
    text_auto=True,
    title="Average Valuation by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# PROFITABILITY SCATTER
# --------------------------------------------------
st.markdown("---")

st.subheader("🚀 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Profitable",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue vs Valuation by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# MARKET SHARE IMPACT
# --------------------------------------------------
st.markdown("---")

st.subheader("🎯 Market Share Impact")

fig = px.scatter(
    filtered_df,
    x="Market Share (%)",
    y="Revenue (M USD)",
    color="Profitable",
    size="Valuation (M USD)",
    hover_name="Startup Name",
    title="Market Share vs Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# FUNDING IMPACT
# --------------------------------------------------
st.markdown("---")

st.subheader("💸 Funding Impact on Profitability")

fig = px.box(
    filtered_df,
    x="Profitable",
    y="Funding Amount (M USD)",
    title="Funding Distribution by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------
st.markdown("---")

st.subheader("🔥 Industry Profitability Heatmap")

heatmap = (
    filtered_df
    .pivot_table(
        values="Profitable",
        index="Industry",
        columns="Region",
        aggfunc="mean"
    )
)

heatmap = heatmap * 100

fig = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto",
    title="Profitability % by Industry & Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP PROFITABLE STARTUPS
# --------------------------------------------------
st.markdown("---")

st.subheader("🏆 Top Profitable Startups")

profitable_df = filtered_df[
    filtered_df["Profitable"] == True
]

top_profit = profitable_df.sort_values(
    by="Revenue (M USD)",
    ascending=False
).head(20)

st.dataframe(
    top_profit[
        [
            "Startup Name",
            "Industry",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Market Share (%)",
            "Region"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# YEAR TREND
# --------------------------------------------------
st.markdown("---")

st.subheader("📅 Profitability Trend")

year_profit = (
    filtered_df
    .groupby("Year Founded")["Profitable"]
    .mean()
    .reset_index()
)

year_profit["Profitable"] *= 100

fig = px.line(
    year_profit,
    x="Year Founded",
    y="Profitable",
    markers=True,
    title="Profitability Trend by Founded Year"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------
st.markdown("---")

st.subheader("🤖 AI Profitability Insights")

top_industry = (
    industry_profit
    .sort_values(
        "Profitable",
        ascending=False
    )
    .iloc[0]["Industry"]
)

top_region = (
    profit_region
    .sort_values(
        "Profitable",
        ascending=False
    )
    .iloc[0]["Region"]
)

highest_revenue = (
    profitable_df
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"🏆 Most profitable industry: {top_industry}"
)

st.success(
    f"🌍 Most profitable region: {top_region}"
)

st.success(
    f"🚀 Highest revenue profitable startup: {highest_revenue}"
)

st.success(
    f"📈 Overall profitability rate: {profit_rate:.2f}%"
)

st.markdown("---")
st.caption("Profitability Insights Dashboard | Streamlit + Plotly")
