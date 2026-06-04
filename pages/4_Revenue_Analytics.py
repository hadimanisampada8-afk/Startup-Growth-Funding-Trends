import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Revenue Analytics",
    page_icon="💰",
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
# PAGE TITLE
# --------------------------------------------------
st.title("💰 Revenue Analytics Dashboard")
st.markdown("### Deep Revenue Analysis of Startup Ecosystem")

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
st.subheader("📊 Revenue KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"${filtered_df['Revenue (M USD)'].sum():,.0f}M"
    )

with col2:
    st.metric(
        "Average Revenue",
        f"${filtered_df['Revenue (M USD)'].mean():,.2f}M"
    )

with col3:
    st.metric(
        "Highest Revenue",
        f"${filtered_df['Revenue (M USD)'].max():,.2f}M"
    )

with col4:
    st.metric(
        "Revenue per Startup",
        f"${filtered_df['Revenue (M USD)'].sum()/len(filtered_df):,.2f}M"
    )

st.markdown("---")

# --------------------------------------------------
# REVENUE DISTRIBUTION
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Revenue (M USD)",
        nbins=30,
        title="📈 Revenue Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        y="Revenue (M USD)",
        title="📦 Revenue Spread Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# INDUSTRY REVENUE
# --------------------------------------------------
st.markdown("---")
st.subheader("🏭 Revenue by Industry")

industry_revenue = (
    filtered_df
    .groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        by="Revenue (M USD)",
        ascending=False
    )
)

fig = px.bar(
    industry_revenue,
    x="Industry",
    y="Revenue (M USD)",
    color="Industry",
    text_auto=True,
    title="Industry Revenue Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REGION REVENUE
# --------------------------------------------------
st.markdown("---")
st.subheader("🌍 Revenue by Region")

region_revenue = (
    filtered_df
    .groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_revenue,
    names="Region",
    values="Revenue (M USD)",
    title="Regional Revenue Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REVENUE VS EMPLOYEES
# --------------------------------------------------
st.markdown("---")
st.subheader("👨‍💼 Revenue vs Employees")

fig = px.scatter(
    filtered_df,
    x="Employees",
    y="Revenue (M USD)",
    color="Industry",
    size="Valuation (M USD)",
    hover_name="Startup Name",
    title="Revenue vs Workforce"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REVENUE VS VALUATION
# --------------------------------------------------
st.markdown("---")
st.subheader("📈 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP REVENUE STARTUPS
# --------------------------------------------------
st.markdown("---")
st.subheader("🏆 Top 20 Revenue Generating Startups")

top_revenue = (
    filtered_df
    .sort_values(
        by="Revenue (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_revenue[
        [
            "Startup Name",
            "Industry",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Employees",
            "Region"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# REVENUE TREEMAP
# --------------------------------------------------
st.markdown("---")
st.subheader("🌳 Revenue Treemap")

fig = px.treemap(
    industry_revenue,
    path=["Industry"],
    values="Revenue (M USD)",
    title="Revenue Contribution by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# YEARLY REVENUE TREND
# --------------------------------------------------
st.markdown("---")
st.subheader("📅 Revenue Trend by Founded Year")

yearly_revenue = (
    filtered_df
    .groupby("Year Founded")
    ["Revenue (M USD)"]
    .mean()
    .reset_index()
)

fig = px.line(
    yearly_revenue,
    x="Year Founded",
    y="Revenue (M USD)",
    markers=True,
    title="Average Revenue by Startup Year"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# MARKET SHARE VS REVENUE
# --------------------------------------------------
st.markdown("---")
st.subheader("🎯 Market Share vs Revenue")

fig = px.scatter(
    filtered_df,
    x="Market Share (%)",
    y="Revenue (M USD)",
    color="Industry",
    size="Valuation (M USD)",
    hover_name="Startup Name",
    title="Market Share Impact on Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------
st.markdown("---")
st.subheader("🔥 Revenue Heatmap")

heatmap_data = (
    filtered_df
    .pivot_table(
        values="Revenue (M USD)",
        index="Industry",
        columns="Region",
        aggfunc="sum"
    )
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Industry vs Region Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# PROFITABLE VS NON-PROFITABLE
# --------------------------------------------------
st.markdown("---")
st.subheader("📊 Revenue by Profitability")

profit_revenue = (
    filtered_df
    .groupby("Profitable")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
)

fig = px.bar(
    profit_revenue,
    x="Profitable",
    y="Revenue (M USD)",
    text_auto=True,
    title="Revenue by Profitability Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# AUTOMATED INSIGHTS
# --------------------------------------------------
st.markdown("---")
st.subheader("🤖 AI Revenue Insights")

highest_revenue_industry = (
    filtered_df
    .groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

highest_revenue_region = (
    filtered_df
    .groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

avg_revenue = (
    filtered_df["Revenue (M USD)"]
    .mean()
)

top_revenue_startup = (
    filtered_df
    .sort_values(
        by="Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"🏆 Highest revenue industry: {highest_revenue_industry}"
)

st.success(
    f"🌍 Highest revenue region: {highest_revenue_region}"
)

st.success(
    f"💰 Average revenue per startup: ${avg_revenue:.2f}M"
)

st.success(
    f"🚀 Top revenue startup: {top_revenue_startup}"
)

st.markdown("---")
st.caption("Revenue Analytics Dashboard | Streamlit + Plotly")
