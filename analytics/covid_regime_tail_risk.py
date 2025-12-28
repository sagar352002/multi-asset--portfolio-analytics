import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from scipy.optimize import minimize

TRADING_DAYS = 252

# =========================
# Tail-risk metric helpers
# =========================
def semi_variance(returns):
    downside = returns[returns < 0]
    return downside.var() if len(downside) > 0 else np.nan

def var_historical(returns, alpha=0.05):
    return np.percentile(returns, alpha * 100)

def cvar_historical(returns, alpha=0.05):
    var = var_historical(returns, alpha)
    tail_losses = returns[returns <= var]
    return tail_losses.mean() if len(tail_losses) > 0 else np.nan


def evar(returns, alpha=0.05):
    """
    Correct EVaR (loss-based, tail-probability formulation)
    returns : daily portfolio returns
    alpha   : tail probability (e.g. 0.05)
    """

    losses = -np.asarray(returns)  # convert returns → losses

    def objective(theta):
        if theta <= 0:
            return np.inf
        moment = np.mean(np.exp(theta * losses))
        return (np.log(moment) - np.log(alpha)) / theta

    res = minimize(
        objective,
        x0=0.5,
        bounds=[(1e-6, 10)],
        method="L-BFGS-B"
    )

    return res.fun if res.success else np.nan


# =========================
# MAIN TABLE FUNCTION
# =========================
def build_covid_regime_tail_risk_table(
    portfolio_df,
    weights
):
    """
    Tail-risk metrics across market regimes:
    Pre-COVID, COVID, Post-COVID
    """

    regimes = {
        "Pre-COVID": portfolio_df.loc["2016-04-01":"2019-12-31"],
        "COVID": portfolio_df.loc["2020-01-01":"2020-09-31"],
        "Post-COVID": portfolio_df.loc["2020-10-01":"2025-03-26"]
    }

    results = {}

    for label, df in regimes.items():
        returns = df.pct_change().dropna()

        if returns.shape[0] < 50:
            results[label] = [np.nan] * 7
            continue

        # ===============================
        # Align assets (CRITICAL FIX)
        # ===============================
        common_assets = returns.columns.intersection(weights.index)

        # Skip regime if no usable assets
        if len(common_assets) < 1:
            results[label] = [np.nan] * 6
            continue

        port_returns = returns[common_assets] @ weights.loc[common_assets]


        results[label] = [
            var_historical(port_returns) * 100,
            cvar_historical(port_returns) * 100,
            evar(port_returns),                 # ✅ no scaling
            skew(port_returns),
            kurtosis(port_returns, fisher=True),
            semi_variance(port_returns) * TRADING_DAYS * 100
        ]

    index = [
        "VaR (5%) %",
        "CVaR (5%) %",
        "EVaR %",
        "Skewness",
        "Kurtosis",
        "Semi-Variance (%)"
    ]

    return pd.DataFrame(results, index=index).round(3)
