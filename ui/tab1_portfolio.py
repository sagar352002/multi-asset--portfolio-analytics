import streamlit as st
import pandas as pd

def render_tab1_portfolio(fund_data, fund_columns):
    st.header("💼 Portfolio Overview")

    portfolio_parts = []
    selected_fund_names = []

    for fund_group, df in fund_data.items():
        selected_cols = fund_columns.get(fund_group, [])
        if not selected_cols:
            continue

        selected_fund_names.extend(selected_cols)

        temp = df[["date"] + selected_cols].copy()
        temp = temp.set_index("date")
        portfolio_parts.append(temp)

    if not portfolio_parts:
        st.warning("⚠️ No funds selected.")
        return None

    # Combine funds
    portfolio_df = pd.concat(portfolio_parts, axis=1, join="inner")

    # Save always
    st.session_state["portfolio_df"] = portfolio_df
    st.session_state["fund_count"] = portfolio_df.shape[1]

    # ================================
    # DISPLAY SELECTED FUNDS
    # ================================
    st.caption(f"Total Funds Selected: **{portfolio_df.shape[1]}**")

    for i, fund_name in enumerate(selected_fund_names, start=1):
        st.markdown(f"**{i}. {fund_name}**")

    # ================================
    # 🟢 SINGLE FUND MODE
    # ================================
    if portfolio_df.shape[1] == 1:


        fund_name = portfolio_df.columns[0]
        st.info(
            "ℹ️ Optimization, correlation & diversification metrics "
            "are enabled automatically when multiple funds are selected."
        )

        return portfolio_df

    # ================================
    # 🔵 MULTI FUND MODE
    # ================================
    st.subheader("📈 Portfolio Ready for Optimization & Risk Analysis")


    return portfolio_df
