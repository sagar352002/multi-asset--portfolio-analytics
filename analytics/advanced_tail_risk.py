import numpy as np
import pandas as pd

TRADING_DAYS = 252


# =========================
# Downside Deviation
# =========================
def downside_deviation(returns, rf=0.0):
    downside = np.minimum(returns - rf / TRADING_DAYS, 0)
    return np.sqrt(np.mean(downside**2)) * np.sqrt(TRADING_DAYS)


# =========================
# Expected Shortfall Ratio
# =========================
def expected_shortfall_ratio(returns, alpha=0.95):
    var = np.percentile(returns, (1 - alpha) * 100)
    cvar = returns[returns <= var].mean()
    vol = returns.std()
    return np.nan if vol == 0 else abs(cvar) / vol


# =========================
# Stress-period CVaR
# =========================
def stress_cvar(returns, stress_start, stress_end, alpha=0.95):
    stress_returns = returns.loc[stress_start:stress_end]
    if stress_returns.empty:
        return np.nan
    var = np.percentile(stress_returns, (1 - alpha) * 100)
    return stress_returns[stress_returns <= var].mean()


# =========================
# Cross-Entropy
# =========================
def cross_entropy(p_returns, q_returns, bins=50):
    p_hist, bin_edges = np.histogram(p_returns, bins=bins, density=True)
    q_hist, _ = np.histogram(q_returns, bins=bin_edges, density=True)

    mask = (p_hist > 0) & (q_hist > 0)
    return -np.sum(p_hist[mask] * np.log(q_hist[mask]))
