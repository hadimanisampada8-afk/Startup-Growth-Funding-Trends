import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    """
    Load startup dataset and perform basic cleaning.
    """

    df = pd.read_csv("startup_data.csv")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Fill missing values

    numeric_cols = [
        "Funding Rounds",
        "Funding Amount (M USD)",
        "Valuation (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)",
        "Year Founded"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    categorical_cols = [
        "Startup Name",
        "Industry",
        "Region",
        "Exit Status"
    ]

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


@st.cache_data
def get_filtered_data(
    industries=None,
    regions=None,
    exits=None
):
    """
    Return filtered dataframe.
    """

    df = load_data()

    if industries:
        df = df[df["Industry"].isin(industries)]

    if regions:
        df = df[df["Region"].isin(regions)]

    if exits:
        df = df[df["Exit Status"].isin(exits)]

    return df


@st.cache_data
def get_kpis(df):
    """
    Generate dashboard KPI metrics.
    """

    kpis = {
        "total_startups": len(df),

        "total_funding":
        round(
            df["Funding Amount (M USD)"].sum(),
            2
        ),

        "avg_valuation":
        round(
            df["Valuation (M USD)"].mean(),
            2
        ),

        "total_revenue":
        round(
            df["Revenue (M USD)"].sum(),
            2
        ),

        "total_employees":
        int(
            df["Employees"].sum()
        ),

        "profitability_rate":
        round(
            df["Profitable"].mean() * 100,
            2
        )
    }

    return kpis


@st.cache_data
def get_top_startups(
    df,
    top_n=10
):
    """
    Return top startups by valuation.
    """

    return (
        df.sort_values(
            by="Valuation (M USD)",
            ascending=False
        )
        .head(top_n)
    )


@st.cache_data
def get_industry_summary(df):
    """
    Industry-wise aggregation.
    """

    summary = (
        df.groupby("Industry")
        .agg(
            Funding=("Funding Amount (M USD)", "sum"),
            Revenue=("Revenue (M USD)", "sum"),
            Valuation=("Valuation (M USD)", "sum"),
            Employees=("Employees", "sum")
        )
        .reset_index()
    )

    return summary


@st.cache_data
def get_region_summary(df):
    """
    Region-wise aggregation.
    """

    summary = (
        df.groupby("Region")
        .agg(
            Funding=("Funding Amount (M USD)", "sum"),
            Revenue=("Revenue (M USD)", "sum"),
            Valuation=("Valuation (M USD)", "sum")
        )
        .reset_index()
    )

    return summary


@st.cache_data
def get_correlation_matrix(df):
    """
    Numeric correlation matrix.
    """

    numeric_df = df.select_dtypes(
        include=["int64", "float64"]
    )

    return numeric_df.corr()


@st.cache_data
def get_unicorns(df):
    """
    Startups valued at $1B+.
    """

    return df[
        df["Valuation (M USD)"] >= 1000
    ]
