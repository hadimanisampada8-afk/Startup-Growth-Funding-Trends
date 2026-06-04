import pandas as pd


# --------------------------------------------------
# EXECUTIVE INSIGHTS
# --------------------------------------------------
def generate_executive_insights(df):

    insights = []

    total_startups = len(df)

    total_funding = (
        df["Funding Amount (M USD)"]
        .sum()
    )

    total_revenue = (
        df["Revenue (M USD)"]
        .sum()
    )

    total_valuation = (
        df["Valuation (M USD)"]
        .sum()
    )

    profitability_rate = (
        df["Profitable"].mean() * 100
    )

    insights.append(
        f"Dataset contains {total_startups} startups."
    )

    insights.append(
        f"Total funding analyzed is ${total_funding:,.0f}M."
    )

    insights.append(
        f"Combined startup valuation is ${total_valuation:,.0f}M."
    )

    insights.append(
        f"Total revenue generated is ${total_revenue:,.0f}M."
    )

    insights.append(
        f"Overall profitability rate is {profitability_rate:.2f}%."
    )

    return insights


# --------------------------------------------------
# FUNDING INSIGHTS
# --------------------------------------------------
def funding_insights(df):

    insights = []

    top_industry = (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .idxmax()
    )

    avg_funding = (
        df["Funding Amount (M USD)"]
        .mean()
    )

    insights.append(
        f"Highest funded industry is {top_industry}."
    )

    insights.append(
        f"Most funded region is {top_region}."
    )

    insights.append(
        f"Average startup funding is ${avg_funding:.2f}M."
    )

    return insights


# --------------------------------------------------
# VALUATION INSIGHTS
# --------------------------------------------------
def valuation_insights(df):

    insights = []

    top_industry = (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby("Region")
        ["Valuation (M USD)"]
        .sum()
        .idxmax()
    )

    highest_startup = (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .iloc[0]["Startup Name"]
    )

    insights.append(
        f"Top valuation industry is {top_industry}."
    )

    insights.append(
        f"Highest valuation region is {top_region}."
    )

    insights.append(
        f"Most valuable startup is {highest_startup}."
    )

    return insights


# --------------------------------------------------
# REVENUE INSIGHTS
# --------------------------------------------------
def revenue_insights(df):

    insights = []

    top_industry = (
        df.groupby("Industry")
        ["Revenue (M USD)"]
        .sum()
        .idxmax()
    )

    avg_revenue = (
        df["Revenue (M USD)"]
        .mean()
    )

    top_company = (
        df.sort_values(
            "Revenue (M USD)",
            ascending=False
        )
        .iloc[0]["Startup Name"]
    )

    insights.append(
        f"Highest revenue industry is {top_industry}."
    )

    insights.append(
        f"Average startup revenue is ${avg_revenue:.2f}M."
    )

    insights.append(
        f"Top revenue generating startup is {top_company}."
    )

    return insights


# --------------------------------------------------
# MARKET INSIGHTS
# --------------------------------------------------
def market_insights(df):

    insights = []

    leader = (
        df.sort_values(
            "Market Share (%)",
            ascending=False
        )
        .iloc[0]["Startup Name"]
    )

    industry = (
        df.groupby("Industry")
        ["Market Share (%)"]
        .sum()
        .idxmax()
    )

    region = (
        df.groupby("Region")
        ["Market Share (%)"]
        .sum()
        .idxmax()
    )

    insights.append(
        f"Market leader startup is {leader}."
    )

    insights.append(
        f"{industry} dominates industry market share."
    )

    insights.append(
        f"{region} contributes the highest market presence."
    )

    return insights


# --------------------------------------------------
# PROFITABILITY INSIGHTS
# --------------------------------------------------
def profitability_insights(df):

    insights = []

    profitability = (
        df["Profitable"]
        .mean() * 100
    )

    top_industry = (
        df.groupby("Industry")
        ["Profitable"]
        .mean()
        .idxmax()
    )

    insights.append(
        f"Profitability rate stands at {profitability:.2f}%."
    )

    insights.append(
        f"Most profitable industry is {top_industry}."
    )

    return insights


# --------------------------------------------------
# UNICORN INSIGHTS
# --------------------------------------------------
def unicorn_insights(df):

    insights = []

    unicorns = df[
        df["Valuation (M USD)"] >= 1000
    ]

    insights.append(
        f"Total unicorn startups: {len(unicorns)}."
    )

    if len(unicorns) > 0:

        top_unicorn = (
            unicorns
            .sort_values(
                "Valuation (M USD)",
                ascending=False
            )
            .iloc[0]["Startup Name"]
        )

        insights.append(
            f"Top unicorn startup is {top_unicorn}."
        )

    return insights


# --------------------------------------------------
# GROWTH POTENTIAL
# --------------------------------------------------
def growth_potential(df):

    temp = df.copy()

    temp["Growth Score"] = (
        temp["Funding Amount (M USD)"] * 0.30 +
        temp["Revenue (M USD)"] * 0.30 +
        temp["Valuation (M USD)"] * 0.40
    )

    top_growth = (
        temp.sort_values(
            "Growth Score",
            ascending=False
        )
        .head(5)
    )

    insights = []

    for company in top_growth["Startup Name"]:
        insights.append(
            f"{company} shows strong growth potential."
        )

    return insights


# --------------------------------------------------
# FUNDING EFFICIENCY
# --------------------------------------------------
def funding_efficiency(df):

    temp = df.copy()

    temp["Efficiency"] = (
        temp["Revenue (M USD)"] /
        temp["Funding Amount (M USD)"]
    )

    best = (
        temp.sort_values(
            "Efficiency",
            ascending=False
        )
        .head(5)
    )

    insights = []

    for company in best["Startup Name"]:
        insights.append(
            f"{company} converts funding into revenue efficiently."
        )

    return insights


# --------------------------------------------------
# AI RECOMMENDATIONS
# --------------------------------------------------
def strategic_recommendations(df):

    recommendations = []

    recommendations.append(
        "Increase investment in high valuation industries."
    )

    recommendations.append(
        "Focus on startups with strong revenue efficiency."
    )

    recommendations.append(
        "Monitor unicorn startups for future growth opportunities."
    )

    recommendations.append(
        "Expand operations in regions with high funding concentration."
    )

    recommendations.append(
        "Improve profitability through operational optimization."
    )

    return recommendations


# --------------------------------------------------
# MASTER INSIGHT GENERATOR
# --------------------------------------------------
def generate_all_insights(df):

    insights = []

    insights.extend(
        generate_executive_insights(df)
    )

    insights.extend(
        funding_insights(df)
    )

    insights.extend(
        valuation_insights(df)
    )

    insights.extend(
        revenue_insights(df)
    )

    insights.extend(
        market_insights(df)
    )

    insights.extend(
        profitability_insights(df)
    )

    insights.extend(
        unicorn_insights(df)
    )

    return insights
