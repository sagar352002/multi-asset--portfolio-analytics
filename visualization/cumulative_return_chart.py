import plotly.express as px

def plot_cumulative_returns(portfolio_df, weights, title):
    """
    portfolio_df : DataFrame of prices / NAVs
    weights      : pd.Series of optimized weights
    """

    # =========================
    # 1. Daily returns
    # =========================
    returns = portfolio_df.pct_change().dropna()

    # =========================
    # 2. Portfolio daily returns
    # =========================
    portfolio_returns = returns @ weights

    # =========================
    # 3. Cumulative returns
    # =========================
    cumulative_funds = (1 + returns).cumprod()
    cumulative_portfolio = (1 + portfolio_returns).cumprod()

    cumulative_funds["Optimized Portfolio"] = cumulative_portfolio

    # =========================
    # 4. Long format for Plotly
    # =========================
    plot_df = cumulative_funds.reset_index().melt(
        id_vars=cumulative_funds.index.name,
        var_name="Asset",
        value_name="Cumulative Return"
    )

    # =========================
    # 5. Plot
    # =========================
    fig = px.line(
        plot_df,
        x=plot_df.columns[0],
        y="Cumulative Return",
        color="Asset"
    )

    fig.update_layout(
        height=580,
        margin=dict(t=90, b=70, l=40, r=40),

        # ✅ LEFT-SHIFTED + BOLD TITLE (~2 tabs)
        title=dict(
            text=f"<b>{title}</b>",
            x=0.42,
            xanchor="center",
            y=0.97,
            font=dict(size=20)
        ),

        hovermode="x unified",
        legend_title_text="Funds",

        yaxis=dict(
            title="Cumulative Return",
            tickmode="linear",
            tick0=0.0,
            dtick=0.5,
            tickformat=".0%"
        ),

        xaxis=dict(
            title="Date"
        )
    )

    # ✅ Caption (subtle, professional)
    fig.add_annotation(
        text="Cumulative performance comparison of individual funds versus the optimized portfolio based on historical returns.",
        x=0.5,
        y=-0.18,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=12, color="#9e9e9e"),
        align="center"
    )

    return fig
