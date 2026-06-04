import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    """Load startup dataset."""

    try:
        df = pd.read_csv("startup_data.csv")
    except Exception as e:
        st.error(f"Error loading startup_data.csv: {e}")
        st.stop()

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()

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
            df[col] = pd.to_numeric(df[col], errors="coerce")
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
def get_filtered_data(industries=None, regions=None, exits=None):

    df = load_data()

    if industries:
        df = df[df["Industry"].isin(industries)]

    if regions:
        df = df[df["Region"].isin(regions)]

    if exits:
        df = df[df["Exit Status"].isin(exits)]

    return df


def get_kpis(df):

    profitability = 0

    if "Profitable" in df.columns:
        profitability = round(df["Profitable"].mean() * 100, 2)

    return {
        "total_startups": len(df),
        "total_funding": round(df["Funding Amount (M USD)"].sum(), 2),
        "avg_valuation": round(df["Valuation (M USD)"].mean(), 2),
        "total_revenue": round(df["Revenue (M USD)"].sum(), 2),
        "total_employees": int(df["Employees"].sum()),
        "profitability_rate": profitability
    }


def get_top_startups(df, top_n=10):

    return (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .head(top_n)
    )


def get_industry_summary(df):

    return (
        df.groupby("Industry")
        .agg(
            Funding=("Funding Amount (M USD)", "sum"),
            Revenue=("Revenue (M USD)", "sum"),
            Valuation=("Valuation (M USD)", "sum"),
            Employees=("Employees", "sum")
        )
        .reset_index()
    )


def get_region_summary(df):

    return (
        df.groupby("Region")
        .agg(
            Funding=("Funding Amount (M USD)", "sum"),
            Revenue=("Revenue (M USD)", "sum"),
            Valuation=("Valuation (M USD)", "sum")
        )
        .reset_index()
    )


def get_correlation_matrix(df):

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    return numeric_df.corr()


def get_unicorns(df):

    return df[
        df["Valuation (M USD)"] >= 1000
    ]
