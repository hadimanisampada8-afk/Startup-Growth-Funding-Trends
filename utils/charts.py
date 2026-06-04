import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# FUNDING BY INDUSTRY
# --------------------------------------------------
def funding_by_industry(df):

    data = (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        data,
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        text_auto=True,
        title="Funding by Industry"
    )

    return fig


# --------------------------------------------------
# FUNDING BY REGION
# --------------------------------------------------
def funding_by_region(df):

    data = (
        df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        data,
        names="Region",
        values="Funding Amount (M USD)",
        title="Funding Distribution by Region"
    )

    return fig


# --------------------------------------------------
# VALUATION BY INDUSTRY
# --------------------------------------------------
def valuation_by_industry(df):

    data = (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry",
        text_auto=True,
        title="Valuation by Industry"
    )

    return fig


# --------------------------------------------------
# REVENUE BY INDUSTRY
# --------------------------------------------------
def revenue_by_industry(df):

    data = (
        df.groupby("Industry")
        ["Revenue (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Industry",
        y="Revenue (M USD)",
        color="Industry",
        text_auto=True,
        title="Revenue by Industry"
    )

    return fig


# --------------------------------------------------
# MARKET SHARE TREEMAP
# --------------------------------------------------
def market_share_treemap(df):

    data = (
        df.groupby("Industry")
        ["Market Share (%)"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        data,
        path=["Industry"],
        values="Market Share (%)",
        title="Market Share Treemap"
    )

    return fig


# --------------------------------------------------
# FUNDING VS VALUATION
# --------------------------------------------------
def funding_vs_valuation(df):

    fig = px.scatter(
        df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        color="Industry",
        size="Revenue (M USD)",
        hover_name="Startup Name",
        title="Funding vs Valuation"
    )

    return fig


# --------------------------------------------------
# REVENUE VS VALUATION
# --------------------------------------------------
def revenue_vs_valuation(df):

    fig = px.scatter(
        df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        color="Industry",
        size="Employees",
        hover_name="Startup Name",
        title="Revenue vs Valuation"
    )

    return fig


# --------------------------------------------------
# REVENUE VS EMPLOYEES
# --------------------------------------------------
def revenue_vs_employees(df):

    fig = px.scatter(
        df,
        x="Employees",
        y="Revenue (M USD)",
        color="Industry",
        size="Valuation (M USD)",
        hover_name="Startup Name",
        title="Revenue vs Employees"
    )

    return fig


# --------------------------------------------------
# MARKET SHARE VS REVENUE
# --------------------------------------------------
def market_share_vs_revenue(df):

    fig = px.scatter(
        df,
        x="Market Share (%)",
        y="Revenue (M USD)",
        color="Industry",
        size="Valuation (M USD)",
        hover_name="Startup Name",
        title="Market Share vs Revenue"
    )

    return fig


# --------------------------------------------------
# PROFITABILITY PIE
# --------------------------------------------------
def profitability_chart(df):

    data = (
        df["Profitable"]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        data,
        names="Status",
        values="Count",
        title="Profitability Breakdown"
    )

    return fig


# --------------------------------------------------
# INDUSTRY HEATMAP
# --------------------------------------------------
def industry_region_heatmap(
    df,
    value_column
):

    heatmap = (
        df.pivot_table(
            values=value_column,
            index="Industry",
            columns="Region",
            aggfunc="sum"
        )
    )

    fig = px.imshow(
        heatmap,
        text_auto=True,
        aspect="auto",
        title=f"{value_column} Heatmap"
    )

    return fig


# --------------------------------------------------
# STARTUP TREND
# --------------------------------------------------
def startup_trend(df):

    data = (
        df.groupby("Year Founded")
        .size()
        .reset_index(name="Count")
    )

    fig = px.line(
        data,
        x="Year Founded",
        y="Count",
        markers=True,
        title="Startup Formation Trend"
    )

    return fig


# --------------------------------------------------
# INDUSTRY SUNBURST
# --------------------------------------------------
def industry_sunburst(df):

    fig = px.sunburst(
        df,
        path=["Region", "Industry"],
        values="Valuation (M USD)",
        title="Region → Industry Valuation"
    )

    return fig


# --------------------------------------------------
# CORRELATION HEATMAP
# --------------------------------------------------
def correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include=["int64", "float64"]
    )

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix"
    )

    return fig


# --------------------------------------------------
# TOP STARTUPS BAR
# --------------------------------------------------
def top_startups_chart(
    df,
    top_n=10
):

    top = (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        top,
        x="Startup Name",
        y="Valuation (M USD)",
        color="Industry",
        text_auto=True,
        title=f"Top {top_n} Startups"
    )

    return fig


# --------------------------------------------------
# FUNDING DISTRIBUTION
# --------------------------------------------------
def funding_distribution(df):

    fig = px.histogram(
        df,
        x="Funding Amount (M USD)",
        nbins=30,
        title="Funding Distribution"
    )

    return fig


# --------------------------------------------------
# REVENUE DISTRIBUTION
# --------------------------------------------------
def revenue_distribution(df):

    fig = px.histogram(
        df,
        x="Revenue (M USD)",
        nbins=30,
        title="Revenue Distribution"
    )

    return fig


# --------------------------------------------------
# VALUATION DISTRIBUTION
# --------------------------------------------------
def valuation_distribution(df):

    fig = px.histogram(
        df,
        x="Valuation (M USD)",
        nbins=30,
        title="Valuation Distribution"
    )

    return fig
