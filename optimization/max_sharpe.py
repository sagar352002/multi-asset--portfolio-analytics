import numpy as np
import pandas as pd
from scipy.optimize import minimize


def maximum_sharpe_optimization(portfolio_df, risk_free_rate=0.0):
    """
    Maximum Sharpe Ratio Optimization
    --------------------------------
    portfolio_df     : DataFrame of daily prices / NAVs
    risk_free_rate   : annual risk-free rate (default = 0)
    returns          : pd.Series of optimal weights
    """

    # =========================
    # 1. Daily returns
    # =========================
    returns = portfolio_df.pct_change().dropna()

    # Annualized metrics
    mu = returns.mean() * 252
    cov = returns.cov() * 252

    assets = returns.columns.tolist()
    n_assets = len(assets)

    # =========================
    # 2. Portfolio functions
    # =========================
    def portfolio_return(weights):
        return np.dot(weights, mu)

    def portfolio_volatility(weights):
        return np.sqrt(weights.T @ cov @ weights)

    def negative_sharpe_ratio(weights):
        return -(
            (portfolio_return(weights) - risk_free_rate)
            / portfolio_volatility(weights)
        )

    # =========================
    # 3. Constraints
    # =========================
    constraints = (
        {"type": "eq", "fun": lambda w: np.sum(w) - 1}
    )

    bounds = [(0, 1) for _ in range(n_assets)]
    initial_weights = np.array([1 / n_assets] * n_assets)

    # =========================
    # 4. Optimization
    # =========================
    result = minimize(
        negative_sharpe_ratio,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    weights = pd.Series(result.x, index=assets, name="Weight")
    return weights
