import numpy as np
import pandas as pd
from scipy.optimize import minimize   # ✅ REQUIRED IMPORT


def mean_variance_optimization(portfolio_df, target_return):
    """
    Mean–Variance (Markowitz) Optimization with Expected Return
    """

    # =========================
    # 1. Daily returns
    # =========================
    returns = portfolio_df.pct_change().dropna()

    mu = returns.mean() * 252
    cov = returns.cov() * 252

    assets = returns.columns.tolist()
    n_assets = len(assets)

    # =========================
    # 2. Portfolio functions
    # =========================
    def portfolio_return(weights):
        return weights @ mu

    def portfolio_variance(weights):
        return weights.T @ cov @ weights

    # =========================
    # 3. Constraints
    # =========================
    constraints = (
        {"type": "eq", "fun": lambda w: np.sum(w) - 1},
        {"type": "eq", "fun": lambda w: portfolio_return(w) - target_return}
    )

    bounds = [(0, 1)] * n_assets
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

    return pd.Series(result.x, index=assets, name="Weight")
