import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Market Analytics",
    page_icon="🌍",
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
st.title("🌍 Market Analytics Dashboard")
st.markdown("### Deep Market Share & Competitive Analysis")

st.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🎯 Filters")

industry = st.sidebar.multiselect(
    "Industry",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
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
st.subheader("📊 Market KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Market Share",
        f"{filtered_df['Market Share (%)'].sum():.2f}%"
    )

with col2:
    st.metric(
        "Average Market Share",
        f"{filtered_df['Market Share (%)'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Highest Market Share",
        f"{filtered_df['Market Share (%)'].max():.2f}%"
    )

with col4:
    leader = filtered_df.sort_values(
        "Market Share (%)",
        ascending=False
    ).iloc[0]["Startup Name"]

    st.metric(
        "Market Leader",
        leader
    )

st.markdown("---")

# --------------------------------------------------
# MARKET SHARE DISTRIBUTION
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Market Share (%)",
        nbins=25,
        title="📈 Market Share Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        y="Market Share (%)",
        title="📦 Market Share Spread"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# INDUSTRY MARKET SHARE
# --------------------------------------------------
st.markdown("---")

st.subheader("🏭 Market Share by Industry")

industry_market = (
    filtered_df
    .groupby("Industry")
    ["Market Share (%)"]
    .sum()
    .reset_index()
    .sort_values(
        by="Market Share (%)",
        ascending=False
    )
)

fig = px.bar(
    industry_market,
    x="Industry",
    y="Market Share (%)",
    color="Industry",
    text_auto=True,
    title="Industry Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REGION MARKET SHARE
# --------------------------------------------------
st.markdown("---")

st.subheader("🌎 Regional Market Share")

region_market = (
    filtered_df
    .groupby("Region")
    ["Market Share (%)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_market,
    names="Region",
    values="Market Share (%)",
    title="Regional Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP MARKET LEADERS
# --------------------------------------------------
st.markdown("---")

st.subheader("🏆 Top 20 Market Leaders")

top_market = (
    filtered_df
    .sort_values(
        by="Market Share (%)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_market[
        [
            "Startup Name",
            "Industry",
            "Market Share (%)",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# MARKET SHARE VS REVENUE
# --------------------------------------------------
st.markdown("---")

st.subheader("💰 Market Share vs Revenue")

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
# MARKET SHARE VS VALUATION
# --------------------------------------------------
st.markdown("---")

st.subheader("📈 Market Share vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Market Share (%)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Market Share Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TREEMAP
# --------------------------------------------------
st.markdown("---")

st.subheader("🌳 Industry Market Treemap")

fig = px.treemap(
    industry_market,
    path=["Industry"],
    values="Market Share (%)",
    title="Market Share Treemap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SUNBURST
# --------------------------------------------------
st.markdown("---")

st.subheader("☀️ Market Structure")

fig = px.sunburst(
    filtered_df,
    path=["Region", "Industry"],
    values="Market Share (%)",
    title="Region → Industry Market Structure"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------
st.markdown("---")

st.subheader("🔥 Industry vs Region Heatmap")

heatmap_data = (
    filtered_df
    .pivot_table(
        values="Market Share (%)",
        index="Industry",
        columns="Region",
        aggfunc="sum"
    )
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Industry vs Region Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# EMPLOYEES VS MARKET SHARE
# --------------------------------------------------
st.markdown("---")

st.subheader("👨‍💼 Employees vs Market Share")

fig = px.scatter(
    filtered_df,
    x="Employees",
    y="Market Share (%)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Workforce Impact on Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# COMPETITIVE LANDSCAPE
# --------------------------------------------------
st.markdown("---")

st.subheader("⚔️ Competitive Landscape")

competitive = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Startup Name": "count",
        "Market Share (%)": "sum"
    })
    .reset_index()
)

competitive.columns = [
    "Industry",
    "Startup Count",
    "Market Share"
]

fig = px.scatter(
    competitive,
    x="Startup Count",
    y="Market Share",
    size="Market Share",
    color="Industry",
    title="Industry Competition Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# AUTOMATED INSIGHTS
# --------------------------------------------------
st.markdown("---")

st.subheader("🤖 AI Market Insights")

top_industry = (
    filtered_df
    .groupby("Industry")
    ["Market Share (%)"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df
    .groupby("Region")
    ["Market Share (%)"]
    .sum()
    .idxmax()
)

market_leader = (
    filtered_df
    .sort_values(
        "Market Share (%)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

avg_market = (
    filtered_df["Market Share (%)"]
    .mean()
)

st.success(
    f"🏆 Highest market share industry: {top_industry}"
)

st.success(
    f"🌍 Dominant region: {top_region}"
)

st.success(
    f"🚀 Market leader startup: {market_leader}"
)

st.success(
    f"📊 Average market share: {avg_market:.2f}%"
)

st.markdown("---")
st.caption("Market Analytics Dashboard | Streamlit + Plotly")
