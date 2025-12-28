import streamlit as st
import pandas as pd

def render_tab1_portfolio(fund_data, fund_columns):
    st.header("💼 Portfolio Overview: Combined Fund Holdings")

    portfolio_parts = []
    selected_fund_names = []

    for fund_group, df in fund_data.items():
        selected_cols = fund_columns.get(fund_group, [])

        if not selected_cols:
            continue

        # Collect each selected fund/scheme name
        for col in selected_cols:
            selected_fund_names.append(col)

        # Prepare data for later use
        temp = df[["date"] + selected_cols].copy()
        temp = temp.set_index("date")
        portfolio_parts.append(temp)

    if not portfolio_parts:
        st.warning("⚠️ No funds selected. Use the sidebar to add funds to your portfolio.")
        return None

    # Combine all selected funds into ONE dataframe
    portfolio_df = pd.concat(
        portfolio_parts,
        axis=1,
        join="inner"
    )

    # Save for later tabs (risk, optimization, etc.)
    st.session_state["portfolio_df"] = portfolio_df

    # ================================
    # ✅ DISPLAY SELECTED FUNDS (CORRECT COUNT)
    # ================================

    st.caption(f"Total Funds Selected: **{len(selected_fund_names)}**")

    for i, fund_name in enumerate(selected_fund_names, start=1):
        st.markdown(f"**{i}. {fund_name}**")

    return portfolio_df





    # st.markdown("### 📊 Portfolio Return Matrix")  ################ show code
    # st.caption(f"Total Funds Selected: {portfolio_df.shape[1]}")

    # st.dataframe(
    #     portfolio_df,
    #     use_container_width=True
    # ) #show