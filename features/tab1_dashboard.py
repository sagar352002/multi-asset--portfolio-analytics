import streamlit as st
import plotly.express as px

from visualization.risk_return_scatter import plot_risk_return_scatter
from visualization.correlation_heatmap import plot_correlation_heatmap

from analytics.portfolio_performance_table import build_portfolio_metrics_table
from analytics.alpha_beta import calculate_alpha_beta
from analytics.risk_comparison_table import build_risk_comparison_table
from analytics.advanced_risk_table import build_advanced_risk_table

from visualization.diversification_score import average_correlation
from analytics.portfolio_correlation import portfolio_correlation_with_assets

from features.optimization_methods import render_optimization_methods
from data_loader.load_index_fund import load_index_fund



def render_tab1_dashboard(
    fund_data,
    fund_columns,
    optimization_method,
    country,
    render_tab1_portfolio
):
    """
    Full Tab-1 Portfolio Dashboard
    """

    # =========================
    # PORTFOLIO INPUT
    # =========================
    portfolio_df = render_tab1_portfolio(
        fund_data=fund_data,
        fund_columns=fund_columns
    )

    if portfolio_df is None or portfolio_df.shape[1] < 2:
        return

    # =========================
    # Risk vs Return
    # =========================
    # st.subheader("📌 Risk vs Return (Annualized)")
    st.markdown(
        "<h4 style='text-align:center; font-weight:800;'>📊 Risk vs (Annualized) Return of Selected Funds</h4>",
        unsafe_allow_html=True
    )

    st.plotly_chart(
        plot_risk_return_scatter(
            portfolio_df,
            title=""   # remove Plotly title to avoid duplicate
        ),
        use_container_width=True,
        key="risk_return_scatter"
    )

    st.caption(
        "Funds are plotted based on their annualized risk and return characteristics to support "
        "comparative portfolio analysis."
    )

    st.write("")
    st.write("")






    # =========================
    # OPTIMIZATION
    weights = render_optimization_methods(
        optimization_method=optimization_method,
        portfolio_df=portfolio_df
    )

    if weights is None:
        # 🔒 Explicitly mark optimization as NOT done
        st.session_state["optimization_done"] = False
        return

    # ✅ HARD GUARANTEE: set state immediately
    st.session_state["portfolio_df"] = portfolio_df
    st.session_state["optimized_weights"] = weights
    st.session_state["optimization_method"] = optimization_method
    st.session_state["optimization_done"] = True

    

    # # ✅ SAVE STATE FOR OTHER TABS (CRITICAL)
    # st.session_state["portfolio_df"] = portfolio_df
    # st.session_state["optimized_weights"] = weights
    # st.session_state["optimization_method"] = optimization_method
    # st.session_state["optimization_done"] = True

    st.write("")
    st.write("")
 

    # =========================
    # PERFORMANCE TABLE
    # =========================
    st.subheader("🎯 Optimization Results & Performance Summary")
    st.dataframe(
        build_portfolio_metrics_table(
            portfolio_df=portfolio_df,
            weights=weights,
            rf=0.0
        ),
        use_container_width=True
    )
    st.write("")
    st.write("")
    # =========================
    # ALPHA / BETA / CORRELATION
    # =========================
    port_returns = portfolio_df.pct_change().dropna() @ weights
    benchmark_prices = load_index_fund(country)
    benchmark_returns = benchmark_prices.pct_change().dropna()

    alpha_beta = calculate_alpha_beta(
        portfolio_returns=port_returns,
        benchmark_returns=benchmark_returns,
        rf=0.0
    )

    avg_corr = average_correlation(portfolio_df)


    st.subheader("🎯 Market Exposure & Diversification")

    c1, c2, c3 = st.columns(3)
    c1.metric("Alpha (Annualized)", f"{alpha_beta['Alpha (%)']}%")
    c2.metric("Beta", alpha_beta["Beta"])
    c3.metric("Avg Inter-Fund Correlation", f"{avg_corr:.2f}")
    st.write("")
    st.write("")
    st.write("")


    # =========================
    # Portfolio–Fund Correlation
    # =========================
    corr_series = portfolio_correlation_with_assets(portfolio_df, weights)

    fig = px.bar(
        corr_series,
        color=corr_series.values,
        color_continuous_scale="RdBu"
    )

    fig.update_layout(
        yaxis_range=[-1, 1],

        # ✅ BOLD + CENTERED but slightly LEFT (~2 tabs)
        title=dict(
            text="<b>📊 Understanding Fund Relationships & Portfolio Correlation</b>",
            x=0.42,              # ⬅️ ~2-tab left alignment
            xanchor="center",
            font=dict(size=18)
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write("")
    st.write("")


    # =========================
    # Correlation Heatmap
    # =========================
    # st.subheader("🔗 Fund Correlation Matrix")
    st.plotly_chart(
        plot_correlation_heatmap(portfolio_df),
        use_container_width=True,
        key="correlation_heatmap"
    )


    st.write("")
    st.write("")






    # =========================
    # Tail Risk (Before vs After)
    # =========================
    if optimization_method in [
        "Minimum Variance",
        "Maximum Sharpe Ratio",
        "Max Omega",
        "Equal Weight",
        "Mean-Variance (Markowitz)"
    ]:

        st.subheader("📊 Tail Risk & Distribution Analysis: Optimization Impact")
        st.dataframe(
            build_risk_comparison_table(
                portfolio_df=portfolio_df,
                weights_after=weights
            ),
            use_container_width=True
        )
        st.write("")
        st.write("")
        # =========================
        # Advanced Tail KPIs
        # =========================
        adv = build_advanced_risk_table(
            portfolio_df=portfolio_df,
            weights_after=weights
        )

        st.subheader("⚠️ Extreme Risk Indicators & Tail Metrics")

        k1, k2, k3 = st.columns(3)

        k1.metric("Downside Deviation", f"{adv.loc['Downside Deviation','After Optimization']:.2f}")
        k2.metric("ES Ratio", f"{adv.loc['Expected Shortfall Ratio','After Optimization']:.2f}")
        k3.metric("Stress CVaR", f"{adv.loc['Stress-period CVaR (COVID)','After Optimization']:.2%}")
    