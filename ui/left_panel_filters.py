import streamlit as st

def render_left_panel():
    # ==================================================
    # 🔹 LEFT PANEL — FILTERS
    # ==================================================
    with st.sidebar:
        st.title("Filters")

        # Country
        country = st.selectbox(
            "Select Country",
            ["india", "usa", "europe"],
            index=0
        )

        # Fund selection
        selected_funds = st.multiselect(
            "Select Fund Type(s)",
            ["bond", "esg", "comm", "trad"],
            default=["bond", "esg", "comm", "trad"]
        )

        # Optimization method
        optimization_method = st.selectbox(
            "Select Optimization Method",
            [
                "Mean-Variance (Markowitz)",   # DEFAULT
                "Maximum Sharpe Ratio",
                "Minimum Variance",
                "Equal Weight",
                "Max Omega"
            ],
            index=1
        )

    # Return all selections
    return country, selected_funds, optimization_method
