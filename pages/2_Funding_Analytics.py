import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Funding Analytics",
    page_icon="💰",
    layout="wide"
)

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# ----------------------------------
# TITLE
# ----------------------------------
st.title("💰 Funding Analytics Dashboard")
st.markdown("### Deep Analysis of Startup Funding Trends")

st.markdown("---")

# ----------------------------------
# SIDEBAR FILTERS
# ----------------------------------
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

# ----------------------------------
# KPI SECTION
# ----------------------------------
st.subheader("📊 Funding KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Funding",
        f"${filtered_df['Funding Amount (M USD)'].sum():,.0f}M"
    )

with col2:
    st.metric(
        "Average Funding",
        f"${filtered_df['Funding Amount (M USD)'].mean():,.2f}M"
    )

with col3:
    st.metric(
        "Maximum Funding",
        f"${filtered_df['Funding Amount (M USD)'].max():,.2f}M"
    )

with col4:
    st.metric(
        "Funding Rounds",
        int(filtered_df["Funding Rounds"].sum())
    )

st.markdown("---")

# ----------------------------------
# FUNDING DISTRIBUTION
# ----------------------------------
col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Funding Amount (M USD)",
        nbins=30,
        title="📈 Funding Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        y="Funding Amount (M USD)",
        title="📦 Funding Spread Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------
# INDUSTRY FUNDING
# ----------------------------------
st.markdown("---")
st.subheader("🏭 Industry-wise Funding")

industry_funding = (
    filtered_df
    .groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        by="Funding Amount (M USD)",
        ascending=False
    )
)

fig = px.bar(
    industry_funding,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry",
    text_auto=True,
    title="Funding by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# REGION FUNDING
# ----------------------------------
st.markdown("---")
st.subheader("🌎 Regional Funding Analysis")

region_funding = (
    filtered_df
    .groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_funding,
    names="Region",
    values="Funding Amount (M USD)",
    title="Funding Share by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# FUNDING VS VALUATION
# ----------------------------------
st.markdown("---")
st.subheader("💸 Funding vs Valuation")

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

# ----------------------------------
# FUNDING ROUNDS ANALYSIS
# ----------------------------------
st.markdown("---")
st.subheader("🔄 Funding Rounds Analysis")

rounds = (
    filtered_df
    .groupby("Funding Rounds")
    .size()
    .reset_index(name="Count")
)

fig = px.line(
    rounds,
    x="Funding Rounds",
    y="Count",
    markers=True,
    title="Funding Rounds Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# TREEMAP
# ----------------------------------
st.markdown("---")
st.subheader("🌳 Industry Funding Treemap")

fig = px.treemap(
    industry_funding,
    path=["Industry"],
    values="Funding Amount (M USD)",
    title="Industry Funding Treemap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# TOP FUNDED STARTUPS
# ----------------------------------
st.markdown("---")
st.subheader("🏆 Top 15 Funded Startups")

top_funded = (
    filtered_df
    .sort_values(
        by="Funding Amount (M USD)",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    top_funded[
        [
            "Startup Name",
            "Industry",
            "Funding Amount (M USD)",
            "Valuation (M USD)",
            "Revenue (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# ----------------------------------
# FUNDING HEATMAP DATA
# ----------------------------------
st.markdown("---")
st.subheader("🔥 Funding Heatmap")

heatmap_data = (
    filtered_df
    .pivot_table(
        values="Funding Amount (M USD)",
        index="Industry",
        columns="Region",
        aggfunc="sum"
    )
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Industry vs Region Funding"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# AUTOMATED INSIGHTS
# ----------------------------------
st.markdown("---")
st.subheader("🤖 Funding Insights")

top_industry = (
    filtered_df
    .groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df
    .groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

avg_funding = (
    filtered_df["Funding Amount (M USD)"]
    .mean()
)

st.success(
    f"🚀 Highest funded industry: {top_industry}"
)

st.success(
    f"🌍 Highest funded region: {top_region}"
)

st.success(
    f"💰 Average funding per startup: ${avg_funding:.2f}M"
)

st.success(
    f"📈 Total funding analyzed: ${filtered_df['Funding Amount (M USD)'].sum():,.0f}M"
)

st.markdown("---")
st.caption("Funding Analytics | Streamlit + Plotly")
