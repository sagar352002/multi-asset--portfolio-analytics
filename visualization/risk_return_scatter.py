import plotly.express as px

def plot_risk_return_scatter(portfolio_df, title):
    """
    portfolio_df : DataFrame of daily prices / NAVs
    """

    # =========================
    # 1. Daily returns
    # =========================
    returns = portfolio_df.pct_change().dropna()

    # =========================
    # 2. Annualized metrics
    # =========================
    mean_returns = returns.mean() * 252
    volatility = returns.std() * (252 ** 0.5)

    scatter_df = (
        mean_returns
        .rename("Expected Return")
        .to_frame()
        .join(volatility.rename("Risk"))
        .reset_index()
        .rename(columns={"index": "Fund"})
    )

    # =========================
    # 3. Dynamic axis padding
    # =========================
    x_min, x_max = scatter_df["Risk"].min(), scatter_df["Risk"].max()
    y_min, y_max = scatter_df["Expected Return"].min(), scatter_df["Expected Return"].max()

    x_pad = (x_max - x_min) * 0.25
    y_pad = (y_max - y_min) * 0.25

    # =========================
    # 4. Scatter Plot
    # =========================
    fig = px.scatter(
        scatter_df,
        x="Risk",
        y="Expected Return",
        color="Fund",
        text="Fund",
        title=title
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(size=14, opacity=0.85, line=dict(width=1, color="white"))
    )

    # =========================
    # 5. Layout (CENTERED TITLE)
    # =========================
    fig.update_layout(
        height=480,

        title=dict(
            text=title,
            x=0.5,
            xanchor="center"
        ),

        hovermode="closest",

        xaxis=dict(
            title="Risk (Annualized Volatility)",
            tickformat=".1%",
            range=[max(0, x_min - x_pad), x_max + x_pad]
        ),

        yaxis=dict(
            title="Expected Return (Annualized)",
            tickformat=".1%",
            range=[y_min - y_pad, y_max + y_pad]
        ),

        legend_title_text="Funds"
    )

    return fig
