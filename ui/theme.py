import streamlit as st

def apply_amc_theme():
    st.markdown(
        """
        <style>
        /* =====================================================
           AMC DESIGN TOKENS
        ====================================================== */
        :root {
            --bg-main: #0e1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #1f2633;
            --border-color: #2d333b;
            --text-main: #e6edf3;
            --text-muted: #9da7b3;
            --accent-red: #f04f4f;
            --positive: #2ecc71;
            --negative: #f04f4f;
        }

        /* =====================================================
           APP BACKGROUND
        ====================================================== */
        .stApp {
            background-color: var(--bg-main);
            color: var(--text-main);
        }

        /* =====================================================
           SIDEBAR
        ====================================================== */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
        }

        /* =====================================================
           METRIC CARDS
        ====================================================== */
        div[data-testid="metric-container"] {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: 10px;
        }

        /* =====================================================
           DATAFRAME / TABLE (REAL SELECTORS)
        ====================================================== */
        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            background-color: var(--bg-secondary);
            border-radius: 10px;
            border: 1px solid var(--border-color);
        }

        /* Header */
        div[data-testid="stDataFrame"] thead tr th {
            background-color: var(--bg-tertiary) !important;
            color: var(--text-main) !important;
            border-bottom: 1px solid var(--border-color);
        }

        /* Cells */
        div[data-testid="stDataFrame"] tbody tr td {
            background-color: var(--bg-secondary);
            color: var(--text-main);
            border-bottom: 1px solid var(--border-color);
        }

        /* =====================================================
           INPUTS / FILTERS (BASEWEB FIX)
        ====================================================== */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {
            background-color: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 6px !important;
            color: var(--text-main) !important;
        }

        /* Dropdown menu */
        ul[role="listbox"] {
            background-color: var(--bg-secondary) !important;
            border: 1px solid var(--border-color);
        }

        li[role="option"] {
            color: var(--text-main);
        }

        li[role="option"]:hover {
            background-color: var(--bg-tertiary);
        }

        /* =====================================================
           SLIDERS (THIS IS THE KEY FIX)
        ====================================================== */
        div[data-baseweb="slider"] > div > div {
            color: var(--accent-red);
        }

        div[data-baseweb="slider"] span {
            color: var(--text-main);
        }

        div[data-baseweb="slider"] div[role="slider"] {
            background-color: var(--accent-red) !important;
        }

        /* =====================================================
           BUTTONS
        ====================================================== */
        button[kind="primary"] {
            background-color: var(--accent-red) !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            border: none !important;
        }

        button[kind="secondary"] {
            background-color: var(--bg-tertiary) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--border-color) !important;
        }

        /* =====================================================
           TABS
        ====================================================== */
        button[data-baseweb="tab"] {
            color: var(--text-muted) !important;
            background-color: transparent !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--accent-red) !important;
            border-bottom: 2px solid var(--accent-red);
        }

        </style>
        """,
        unsafe_allow_html=True
    )
