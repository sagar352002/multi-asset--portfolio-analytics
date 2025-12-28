import streamlit as st

def render_fund_column_selector(fund_data: dict):
    """
    Renders fund-wise column selection in the sidebar.

    Args:
        fund_data (dict): { fund_name : pandas.DataFrame }

    Returns:
        dict: { fund_name : selected_columns }
    """
    fund_columns = {}

    with st.sidebar:
        st.markdown("---")
        st.subheader("Fund-wise Selection")

        for fund, df in fund_data.items():
            st.markdown(f"**{fund.upper()} Fund**")

            # Exclude date column
            cols = [c for c in df.columns if c.lower() != "date"]

            fund_columns[fund] = st.multiselect(
                f"Select {fund.upper()} columns",
                options=cols,
                key=f"{fund}_columns"
            )

    return fund_columns
