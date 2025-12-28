import numpy as np
import plotly.graph_objects as go
from scipy.optimize import minimize

TRADING_DAYS = 252

def plot_covid_regime_efficient_frontier(portfolio_df, weights=None, method_name=None):
    """
    Efficient Frontier comparison across market regimes.
    Shows:
    - 3 Efficient Frontiers (Pre, COVID, Post)
    - 1 Portfolio Point (Post-COVID / current regime)
    """

    # =========================
    # Regime definitions
    # =========================
    regimes = {
        "Pre-COVID (2019)": portfolio_df.loc["2016-06-01":"2018-06-01"],
        "COVID Period (2020)": portfolio_df.loc["2018-06-02":"2020-06-03"],
        "Post-COVID (2021)": portfolio_df.loc["2020-06-04":"2022-06-05"]
    }

    colors = {
        "Pre-COVID (2019)": "#14532d",     # green
        "COVID Period (2020)": "#7a1f2b",  # maroon
        "Post-COVID (2021)": "#1f4ed8"     # blue
    }

    fig = go.Figure()

    # =========================
    # Efficient frontier solver
    # =========================
    def efficient_frontier(returns):
        mu = returns.mean() * TRADING_DAYS
        cov = returns.cov() * TRADING_DAYS
        n = len(mu)

        def portfolio_vol(w):
            return np.sqrt(w.T @ cov @ w)

        bounds = [(0, 1)] * n
        init = np.ones(n) / n
        sum_constraint = {"type": "eq", "fun": lambda w: np.sum(w) - 1}

        target_returns = np.linspace(mu.min(), mu.max(), 30)
        risks, rets = [], []

        for tr in target_returns:
            constraints = (
                sum_constraint,
                {"type": "eq", "fun": lambda w, tr=tr: w @ mu - tr}
            )
            res = minimize(portfolio_vol, init, bounds=bounds, constraints=constraints)
            if res.success:
                risks.append(res.fun)
                rets.append(tr)

        return risks, rets, mu, cov

    # =========================
    # Plot frontiers
    # =========================
    for label, df in regimes.items():
        returns = df.pct_change().dropna()
        if returns.shape[0] < 50:
            continue

        risks, rets, mu, cov = efficient_frontier(returns)

        # Frontier line
        fig.add_trace(go.Scatter(
            x=risks,
            y=rets,
            mode="lines",
            name=label,
            line=dict(width=3, color=colors[label])
        ))

        # ⭐ Plot ONLY current regime portfolio (Post-COVID)
        if weights is not None and label == "Post-COVID (2021)":
            # ===============================
            # Align weights with regime assets
            # ===============================
            common_assets = cov.index.intersection(weights.index)

            # Skip if insufficient assets
            if len(common_assets) < 2:
                continue

            w = weights.loc[common_assets].values
            cov_r = cov.loc[common_assets, common_assets].values
            mu_r = mu.loc[common_assets].values

            port_risk = np.sqrt(w.T @ cov_r @ w)
            port_return = w @ mu_r


            fig.add_trace(go.Scatter(
                x=[port_risk],
                y=[port_return],
                mode="markers",
                marker=dict(
                    size=16,
                    symbol="star",
                    color="#facc15",  # gold highlight
                    line=dict(width=1.5, color="white")
                ),
                name=f"Current Portfolio ({method_name})"
            ))

    # =========================
    # Layout (Institutional)
    # =========================
    fig.update_layout(
        height=560,
        margin=dict(t=90, b=50, l=60, r=60),

        title=dict(
            text=f"<b>🦠 Efficient Frontier Across COVID Regimes ({method_name})</b>",
            x=0.42,
            xanchor="center",
            font=dict(size=20)
        ),

        xaxis=dict(
            title="Risk (Annualized Volatility)",
            tickformat=".1%"
        ),

        yaxis=dict(
            title="Expected Return (Annualized)",
            tickformat=".1%"
        ),

        legend=dict(title="Market Regime"),

        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117"
    )

    return fig
