import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from scipy.optimize import minimize

TRADING_DAYS = 252


# =========================
# Core tail-risk metrics
# =========================
def var_cvar(returns, alpha=0.95):
    """
    Historical VaR & CVaR
    """
    var = np.percentile(returns, (1 - alpha) * 100)
    cvar = returns[returns <= var].mean()
    return var, cvar


def evar(returns, alpha=0.95):
    """
    Entropic Value at Risk (EVaR)
    """
    returns = np.asarray(returns)

    def objective(theta):
        return (np.log(np.mean(np.exp(-theta * returns))) - np.log(1 - alpha)) / theta

    res = minimize(
        objective,
        x0=1.0,
        bounds=[(1e-6, None)],
        method="L-BFGS-B"
    )

    return -res.fun if res.success else np.nan


def entropy(returns, bins=50):
    """
    Shannon entropy of return distribution
    """
    hist, _ = np.histogram(returns, bins=bins, density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log(hist))


def cross_entropy(p_returns, q_returns, bins=50):
    """
    Cross entropy between two return distributions
    """
    p_hist, bin_edges = np.histogram(p_returns, bins=bins, density=True)
    q_hist, _ = np.histogram(q_returns, bins=bin_edges, density=True)

    mask = (p_hist > 0) & (q_hist > 0)
    return -np.sum(p_hist[mask] * np.log(q_hist[mask]))


# =========================
# Portfolio return helper
# =========================
def portfolio_returns(portfolio_df, weights):
    returns = portfolio_df.pct_change().dropna()
    return returns @ weights
