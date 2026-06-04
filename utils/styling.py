import streamlit as st


# --------------------------------------------------
# MAIN DASHBOARD THEME
# --------------------------------------------------
def apply_theme():

    st.markdown(
        """
        <style>

        /* Main App */
        .stApp {
            background-color: #F8FAFC;
        }

        /* Page Title */
        h1 {
            color: #0F172A;
            font-weight: 800;
        }

        h2 {
            color: #1E293B;
            font-weight: 700;
        }

        h3 {
            color: #334155;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #0F172A;
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        /* KPI Cards */
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 2px 15px rgba(0,0,0,0.08);
            text-align: center;
            margin-bottom: 15px;
        }

        .metric-value {
            font-size: 30px;
            font-weight: bold;
            color: #2563EB;
        }

        .metric-label {
            font-size: 14px;
            color: #64748B;
        }

        /* Custom Containers */
        .dashboard-card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }

        /* Success Message */
        .stSuccess {
            border-radius: 10px;
        }

        /* DataFrame */
        .stDataFrame {
            border-radius: 10px;
        }

        /* Plotly Chart Container */
        .js-plotly-plot {
            border-radius: 12px;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# KPI CARD
# --------------------------------------------------
def kpi_card(title, value):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# SECTION HEADER
# --------------------------------------------------
def section_header(title):

    st.markdown(
        f"""
        <div style="
            padding:10px;
            border-left:5px solid #2563EB;
            margin-top:20px;
            margin-bottom:15px;
        ">
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# INFO BOX
# --------------------------------------------------
def info_box(text):

    st.markdown(
        f"""
        <div class="dashboard-card">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# SUCCESS BOX
# --------------------------------------------------
def success_box(text):

    st.markdown(
        f"""
        <div style="
            background:#DCFCE7;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
        ">
            ✅ {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# WARNING BOX
# --------------------------------------------------
def warning_box(text):

    st.markdown(
        f"""
        <div style="
            background:#FEF3C7;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
        ">
            ⚠️ {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# INSIGHT BOX
# --------------------------------------------------
def insight_box(text):

    st.markdown(
        f"""
        <div style="
            background:#DBEAFE;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
        ">
            🤖 {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# DASHBOARD FOOTER
# --------------------------------------------------
def dashboard_footer():

    st.markdown(
        """
        <hr>
        <center>
            <p style="
                color:gray;
                font-size:14px;
            ">
            🚀 Startup Analytics Dashboard |
            Built with Streamlit + Plotly + Python
            </p>
        </center>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# PAGE BANNER
# --------------------------------------------------
def page_banner(title, subtitle):

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(
                90deg,
                #2563EB,
                #7C3AED
            );
            padding:25px;
            border-radius:15px;
            color:white;
            margin-bottom:20px;
        ">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# LOADING STYLE
# --------------------------------------------------
def loading_message():

    st.markdown(
        """
        <div style="
            padding:10px;
            color:#2563EB;
            font-weight:bold;
        ">
        ⏳ Loading Analytics...
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------
def empty_state():

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:40px;
            background:white;
            border-radius:15px;
        ">
            📊 No data available for selected filters.
        </div>
        """,
        unsafe_allow_html=True
    )
