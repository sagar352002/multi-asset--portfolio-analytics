from optimization.min_variance import minimum_variance_optimization
from optimization.max_sharpe import maximum_sharpe_optimization
from optimization.max_omega import maximum_omega_optimization
from optimization.equal_weight import equal_weight_allocation
from optimization.mean_variance import mean_variance_optimization
from visualization.donut_chart import plot_donut_chart
import streamlit as st
from visualization.cumulative_return_chart import plot_cumulative_returns



def render_optimization_methods(optimization_method, portfolio_df):
    """
    Render portfolio optimization output based on selected method
    """

    # ✅ ADD: initialize weights
    weights = None

    if portfolio_df is None or portfolio_df.shape[1] < 2:
        if optimization_method in [
            "Minimum Variance",
            "Maximum Sharpe Ratio",
            "Maximum Omega Ratio",
            "Equal Weight",
            "Mean-Variance (Markowitz)"
        ]:
            st.warning("Please select at least two funds.")
        else:
            st.info("Select an optimization method from the left panel.")
        return None   # ✅ explicit

    # ============================
    # Minimum Variance
    # ============================
    if optimization_method == "Minimum Variance":

        weights = minimum_variance_optimization(portfolio_df)

        fig = plot_donut_chart(
            weights,
            title="📊 Minimum Variance Asset Allocation"
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="donut_min_var"
        )

    # ============================
    # Maximum Sharpe Ratio
    # ============================
    elif optimization_method == "Maximum Sharpe Ratio":

        weights = maximum_sharpe_optimization(
            portfolio_df,
            risk_free_rate=0.0
        )

        fig = plot_donut_chart(
            weights,
            title="📈 Maximum Sharpe Ratio Asset Allocation"
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="donut_max_sharpe"
        )

    # ============================
    # Maximum Omega Ratio
    # ============================
    elif optimization_method == "Max Omega":

        weights = maximum_omega_optimization(
            portfolio_df,
            threshold=0.0
        )

        fig = plot_donut_chart(
            weights,
            title="⚖️ Maximum Omega Ratio Asset Allocation"
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="donut_max_omega"
        )

    # ============================
    # Equal Weight
    # ============================
    elif optimization_method == "Equal Weight":

        weights = equal_weight_allocation(portfolio_df)

        fig = plot_donut_chart(
            weights,
            title="⚖️ Equal Weight Asset Allocation"
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="donut_equal_weight"
        )

    # ============================
    # Mean–Variance (Markowitz)
    # ============================
    elif optimization_method == "Mean-Variance (Markowitz)":

        target_return_pct = st.slider(
            "Select Target Expected Return (%)",
            min_value=1,
            max_value=20,
            value=6,
            step=1
        )

        target_return = target_return_pct / 100

        weights = mean_variance_optimization(
            portfolio_df,
            target_return=target_return
        )

        fig = plot_donut_chart(
            weights,
            title=f"📐 Mean–Variance Allocation (Target Return = {target_return_pct}%)"
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="donut_markowitz"
        )

    else:
        st.info("Select an optimization method from the left panel.")
        return None

    # =========================
    # CUMULATIVE RETURN GRAPH
    # =========================
    cumulative_fig = plot_cumulative_returns(
        portfolio_df,
        weights,
        title="📈 Cumulative Returns: Funds vs Optimized Portfolio"
    )
    st.plotly_chart(
        cumulative_fig,
        use_container_width=True,
        key=f"cumret_{optimization_method}"
    )

    # ✅ ADD: RETURN weights
    return weights
