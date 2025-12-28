import streamlit as st

from analytics.covid_frontier import plot_covid_regime_efficient_frontier
from analytics.pre_post_covid_allocation import (
    build_covid_regime_allocation_table
)
from analytics.covid_regime_performance import (
    build_covid_regime_performance_table
)
from analytics.covid_regime_tail_risk import (
    build_covid_regime_tail_risk_table
)


def render_tab2_covid_dashboard():
    """
    TAB-2: COVID Regime Comparison Dashboard
    Uses portfolio + optimization results from Tab-1 (session_state)
    """

    st.subheader("🦠 COVID Regime Comparison")

    # =========================
    # Guard condition
    # =========================

    if (
        not st.session_state.get("optimization_done", False)
        or "optimized_weights" not in st.session_state
        or "portfolio_df" not in st.session_state
    ):
        st.info("Run portfolio optimization in Tab-1 to view COVID regime analysis.")
        return

    portfolio_df = st.session_state["portfolio_df"]
    weights = st.session_state["optimized_weights"]
    method = st.session_state["optimization_method"]
    st.write("")
    st.write("")



    # =========================
    # Efficient Frontier
    # =========================
# =========================
# Efficient Frontier (with validation)
# =========================
    if portfolio_df.shape[1] < 2:
        st.warning(
            "⚠️ COVID regime comparison requires at least **two funds**. "
            "Please select two or more funds to view efficient frontiers."
        )
    else:
        fig = plot_covid_regime_efficient_frontier(
            portfolio_df=portfolio_df,
            weights=weights,
            method_name=method
        )

        # 🔍 Check if figure actually has data
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(
                "⚠️ Insufficient overlapping data across regimes to compute "
                "efficient frontiers. Please select additional funds."
            )


    st.write("")
    st.write("")


    # =========================
    # Allocation comparison
    # =========================
    st.subheader("📊 Asset Allocation Across Market Regimes")

    alloc_table = build_covid_regime_allocation_table(
        portfolio_df=portfolio_df,
        optimization_method=method
    )

    st.dataframe(
        alloc_table,
        use_container_width=True
    )

    st.caption(
        "The table presents optimal asset allocations computed independently under "
        "Pre-COVID, COVID, and Post-COVID market regimes, highlighting structural "
        "shifts driven by changes in volatility and correlation dynamics."
    )

    st.write("")
    st.write("")


    # =========================
    # Performance metrics
    # =========================
    st.subheader("📊 Portfolio Performance Across Market Regimes")

    perf_table = build_covid_regime_performance_table(
        portfolio_df=portfolio_df,
        weights=weights,
        rf=0.0
    )

    st.dataframe(
        perf_table,
        use_container_width=True
    )

    st.caption(
        "This table summarizes annual return, volatility, and risk-adjusted performance "
        "of the optimized portfolio across different market regimes."
    )

    st.write("")
    st.write("")


    # =========================
    # Tail risk metrics
    # =========================
    st.subheader("⚠️ Tail Risk & Downside Risk Metrics Across Market Regimes")

    tail_risk_table = build_covid_regime_tail_risk_table(
        portfolio_df=portfolio_df,
        weights=weights
    )

    st.dataframe(
        tail_risk_table,
        use_container_width=True
    )

    st.caption(
        "Tail-risk measures—including VaR, CVaR, EVaR, skewness, kurtosis, and "
        "semi-variance—quantify extreme downside risk under Pre-COVID, COVID, "
        "and Post-COVID market conditions."
    )
