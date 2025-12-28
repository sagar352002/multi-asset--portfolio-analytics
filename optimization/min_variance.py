import numpy as np
import pandas as pd
from scipy.optimize import minimize


def minimum_variance_optimization(portfolio_df):
    """
    Markowitz Minimum Variance Optimization
    --------------------------------------
    portfolio_df : DataFrame of daily prices / NAVs
    returns      : pd.Series of optimal weights
    """

    # =========================
    # 1. Daily returns
    # =========================
    returns = portfolio_df.pct_change().dropna()

    # Annualized covariance matrix
    cov_matrix = returns.cov() * 252
    assets = returns.columns.tolist()
    n_assets = len(assets)

    # =========================
    # 2. Portfolio variance
    # =========================
    def portfolio_variance(weights):
        return weights.T @ cov_matrix @ weights

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
        portfolio_variance,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    weights = pd.Series(result.x, index=assets, name="Weight")
    return weights
