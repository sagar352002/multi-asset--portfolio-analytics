import streamlit as st
from ui.left_panel_filters import render_left_panel
from data_loader.load_fund_data import load_fund_data
from ui.fund_column_selector import render_fund_column_selector
from ui.tab1_portfolio import render_tab1_portfolio
from features.tab1_dashboard import render_tab1_dashboard

from features.tab2_covid_dashboard import render_tab2_covid_dashboard
from ui.theme import apply_amc_theme


# ==================================
# APPLY GLOBAL AMC THEME (ONE LINE)
# ==================================
apply_amc_theme()

# ==================================================
# PAGE CONFIG (ONLY ONCE)
# ==================================================
st.set_page_config(
    page_title="PortfolioIQ | Multi-Asset Analytics & Optimization",
    layout="wide"
)


# ==================================================
# DARK THEME HEADER (PLOTLY / AMC STYLE)
# ==================================================

st.markdown(
    """
    <div style="margin-bottom:16px;">
        <span style="
            background-color:#b83232;
            color:#ffffff;
            padding:8px 18px;
            border-radius:6px;
            font-weight:800;
            font-size:22px;
            display:inline-block;
            letter-spacing:0.4px;
        ">
            🏦 Multi-Asset Portfolio Analytics, Diversification & Optimization
        </span>
    </div>

    <div style="
        color:#b8b8b8;
        font-size:14.5px;
        line-height:1.65;
        max-width:1000px;
    ">
        <b style="color:#dedede;"33>
            An enterprise-grade statistical & AI-driven modeling framework 🤖
        </b>
         purpose-built for institutional asset management.

        Designed to systematically evaluate diversification benefits, optimize strategic asset allocation,
        and assess risk–return characteristics across evolving market regimes 📊.
        The platform combines rigorous quantitative finance methodologies with advanced machine learning techniques
        to generate actionable investment insights and support fiduciary-grade portfolio construction 💼.
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 🔹 LEFT PANEL — FILTERS
# ==================================================
country, selected_funds, optimization_method = render_left_panel()

# ==================================================
# 🔹 LOAD DATA (Shared Across Tabs)
# ==================================================
fund_data = load_fund_data(
    country=country,
    selected_funds=selected_funds
)

# ==================================================
# 🔹 FUND-WISE COLUMN FILTERS (Shared)
# ==================================================
fund_columns = render_fund_column_selector(fund_data)

# ==================================================
# 🔹 MAIN TABS
# ==================================================
tab1, tab2= st.tabs([
    "📊 Portfolio Dashboard",
    "🦠 COVID Comparison",
])

# ==================================================
# 🔹 TAB 1 — PORTFOLIO DASHBOARD
# ==================================================
# =========================================
# TAB 1 – PORTFOLIO OPTIMIZATION
# ========================================

with tab1:
    render_tab1_dashboard(
        fund_data=fund_data,
        fund_columns=fund_columns,
        optimization_method=optimization_method,
        country=country,
        render_tab1_portfolio=render_tab1_portfolio
    )

# AFTER computing weights



with tab2:
    render_tab2_covid_dashboard()



######################################################################################################

st.markdown(
    """
    <style>
    .footer-wrapper {
        display: flex;
        justify-content: flex-end;
        margin-top: 60px;
        margin-bottom: 20px;
    }

    .dev-box {
        text-align: center;
        padding: 14px 16px;
        border-radius: 16px;
        background: linear-gradient(145deg, #020617, #020c1b);
        border: 1px solid #1e293b;
        width: 200px;

        font-family: "Segoe UI", sans-serif;
        box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    }

    .dev-name {
        font-size: 16px;
        font-weight: 700;
        color: #e5e7eb;
        margin-bottom: 4px;
    }

    .dev-role {
        font-size: 13px;
        font-weight: 600;
        color: #c7d2fe;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
    }

    .icon-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #0f172a;
        border: 1px solid #334155;
        margin: 0 6px;
        transition: transform 0.2s ease;
    }

    .icon-circle:hover {
        transform: scale(1.1);
    }

    .icon-circle img {
        width: 18px;
        filter: brightness(0) invert(1);
    }
    </style>

    <div class="footer-wrapper">
        <div class="dev-box">
            <div class="dev-name">🧑‍💻 Sagar Kumar</div>
            <div class="dev-role">Data Science • AI • ML</div>
            <div>
                <a href="https://www.linkedin.com/in/sagar-kumar-40849b27b/"
                   target="_blank" class="icon-circle">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png">
                </a>
                <a href="https://github.com/sagar352002?tab=stars"
                   target="_blank" class="icon-circle">
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png">
                </a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)








 


  


































