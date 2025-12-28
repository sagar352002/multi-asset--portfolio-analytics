import numpy as np
import pandas as pd
from scipy.optimize import minimize


def maximum_omega_optimization(portfolio_df, threshold=0.0):
    """
    Maximum Omega Ratio Optimization
    --------------------------------
    portfolio_df : DataFrame of daily prices / NAVs
    threshold    : minimum acceptable return (daily), default = 0
    returns      : pd.Series of optimal weights
    """

    # =========================
    # 1. Daily returns
    # =========================
    returns = portfolio_df.pct_change().dropna()
    assets = returns.columns.tolist()
    n_assets = len(assets)

    # =========================
    # 2. Portfolio returns
    # =========================
    def portfolio_returns(weights):
        return returns @ weights

    # =========================
    # 3. Negative Omega Ratio
    # =========================
    def negative_omega_ratio(weights):
        port_ret = portfolio_returns(weights)

        gains = np.maximum(port_ret - threshold, 0).sum()
        losses = np.maximum(threshold - port_ret, 0).sum()

        # avoid division by zero
        if losses == 0:
            return -1e6

        omega = gains / losses
        return -omega

    # =========================
    # 4. Constraints
    # =========================
    constraints = (
        {"type": "eq", "fun": lambda w: np.sum(w) - 1}
    )

    bounds = [(0, 1) for _ in range(n_assets)]
    initial_weights = np.array([1 / n_assets] * n_assets)

    # =========================
    # 5. Optimization
    # =========================
    result = minimize(
        negative_omega_ratio,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    weights = pd.Series(result.x, index=assets, name="Weight")
    return weights
