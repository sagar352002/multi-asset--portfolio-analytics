import numpy as np
import pandas as pd
from scipy.optimize import minimize

TRADING_DAYS = 252

def build_covid_regime_allocation_table(
    portfolio_df,
    optimization_method="Minimum Variance"
):
    """
    Optimal asset allocation across market regimes:
    Pre-COVID, COVID, Post-COVID
    """

    regimes = {
        "Pre-COVID Allocation": portfolio_df.loc["2016-04-01":"2019-12-01"],
        "COVID Allocation": portfolio_df.loc["2019-12-02":"2020-06-03"],
        "Post-COVID Allocation": portfolio_df.loc["2020-06-04":"2024-12-31"]
    }

    allocations = {}

    for label, df in regimes.items():
        returns = df.pct_change().dropna()

        if returns.shape[0] < 50:
            allocations[label] = np.nan
            continue

        mu = returns.mean() * TRADING_DAYS
        cov = returns.cov() * TRADING_DAYS
        n = len(mu)

        # --------------------------
        # Optimization objectives
        # --------------------------
        if optimization_method == "Minimum Variance":
            def objective(w):
                return w.T @ cov @ w

        elif optimization_method == "Maximum Sharpe Ratio":
            def objective(w):
                return -(w @ mu) / np.sqrt(w.T @ cov @ w)

        else:  # Equal Weight
            allocations[label] = np.ones(n) / n
            continue

        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        bounds = [(0, 1)] * n
        init = np.ones(n) / n

        res = minimize(objective, init, bounds=bounds, constraints=constraints)

        allocations[label] = res.x if res.success else np.ones(n) / n

    # --------------------------
    # Build allocation table
    # --------------------------
    alloc_df = pd.DataFrame(
        allocations,
        index=portfolio_df.columns
    )

    return (alloc_df * 100).round(2)
