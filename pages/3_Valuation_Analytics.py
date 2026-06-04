import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Valuation Analytics",
    page_icon="📈",
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
st.title("📈 Startup Valuation Analytics")
st.markdown("### Deep Insights into Startup Valuations")

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

exit_status = st.sidebar.multiselect(
    "Exit Status",
    options=df["Exit Status"].unique(),
    default=df["Exit Status"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
    &
    (df["Exit Status"].isin(exit_status))
]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
st.subheader("📊 Valuation KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Valuation",
        f"${filtered_df['Valuation (M USD)'].sum():,.0f}M"
    )

with col2:
    st.metric(
        "Average Valuation",
        f"${filtered_df['Valuation (M USD)'].mean():,.2f}M"
    )

with col3:
    st.metric(
        "Highest Valuation",
        f"${filtered_df['Valuation (M USD)'].max():,.2f}M"
    )

with col4:
    st.metric(
        "Median Valuation",
        f"${filtered_df['Valuation (M USD)'].median():,.2f}M"
    )

st.markdown("---")

# --------------------------------------------------
# VALUATION DISTRIBUTION
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Valuation (M USD)",
        nbins=30,
        title="📊 Valuation Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        y="Valuation (M USD)",
        title="📦 Valuation Spread"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# INDUSTRY VALUATION
# --------------------------------------------------
st.markdown("---")
st.subheader("🏭 Industry-wise Valuation")

industry_valuation = (
    filtered_df
    .groupby("Industry")
    ["Valuation (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        by="Valuation (M USD)",
        ascending=False
    )
)

fig = px.bar(
    industry_valuation,
    x="Industry",
    y="Valuation (M USD)",
    color="Industry",
    text_auto=True,
    title="Valuation by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REGION VALUATION
# --------------------------------------------------
st.markdown("---")
st.subheader("🌎 Regional Valuation")

region_valuation = (
    filtered_df
    .groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_valuation,
    names="Region",
    values="Valuation (M USD)",
    title="Valuation Share by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# FUNDING VS VALUATION
# --------------------------------------------------
st.markdown("---")
st.subheader("💰 Funding vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Funding Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REVENUE VS VALUATION
# --------------------------------------------------
st.markdown("---")
st.subheader("💵 Revenue vs Valuation")

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
# TOP VALUED STARTUPS
# --------------------------------------------------
st.markdown("---")
st.subheader("🏆 Top 20 Most Valuable Startups")

top20 = (
    filtered_df
    .sort_values(
        by="Valuation (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top20[
        [
            "Startup Name",
            "Industry",
            "Valuation (M USD)",
            "Funding Amount (M USD)",
            "Revenue (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# TREEMAP
# --------------------------------------------------
st.markdown("---")
st.subheader("🌳 Industry Valuation Treemap")

fig = px.treemap(
    industry_valuation,
    path=["Industry"],
    values="Valuation (M USD)",
    title="Valuation Treemap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# YEARLY TREND
# --------------------------------------------------
st.markdown("---")
st.subheader("📅 Startup Valuation Trend")

yearly = (
    filtered_df
    .groupby("Year Founded")
    ["Valuation (M USD)"]
    .mean()
    .reset_index()
)

fig = px.line(
    yearly,
    x="Year Founded",
    y="Valuation (M USD)",
    markers=True,
    title="Average Valuation by Founded Year"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------
st.markdown("---")
st.subheader("🔥 Industry vs Region Valuation Heatmap")

heatmap_data = (
    filtered_df
    .pivot_table(
        values="Valuation (M USD)",
        index="Industry",
        columns="Region",
        aggfunc="sum"
    )
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Valuation Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# UNICORN ANALYSIS
# --------------------------------------------------
st.markdown("---")
st.subheader("🦄 Unicorn Startups")

unicorns = filtered_df[
    filtered_df["Valuation (M USD)"] >= 1000
]

st.metric(
    "Total Unicorns",
    len(unicorns)
)

st.dataframe(
    unicorns[
        [
            "Startup Name",
            "Industry",
            "Valuation (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------
st.markdown("---")
st.subheader("🤖 AI Valuation Insights")

top_industry = (
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

avg_val = (
    filtered_df["Valuation (M USD)"]
    .mean()
)

max_val = (
    filtered_df["Valuation (M USD)"]
    .max()
)

st.success(
    f"🏆 Highest valuation industry: {top_industry}"
)

st.success(
    f"🌍 Top valuation region: {top_region}"
)

st.success(
    f"💰 Average valuation: ${avg_val:.2f}M"
)

st.success(
    f"🚀 Highest startup valuation: ${max_val:.2f}M"
)

st.markdown("---")
st.caption("Valuation Analytics Dashboard | Streamlit + Plotly")
