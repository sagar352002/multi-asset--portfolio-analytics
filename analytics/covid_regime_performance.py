import numpy as np
import pandas as pd

TRADING_DAYS = 252

# =========================
# Helper metric functions
# =========================
def cagr(returns):
    total_return = (1 + returns).prod()
    years = len(returns) / TRADING_DAYS
    return total_return ** (1 / years) - 1

def volatility(returns):
    return returns.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(returns, rf=6.0):
    vol = volatility(returns)
    return np.nan if vol == 0 else (returns.mean() * TRADING_DAYS - rf) / vol

def sortino_ratio(returns, rf=6.0):
    downside = returns[returns < 0]
    if downside.std() == 0:
        return np.nan
    return (returns.mean() * TRADING_DAYS - rf) / (downside.std() * np.sqrt(TRADING_DAYS))

def omega_ratio(returns, threshold=0.0):
    gains = np.maximum(returns - threshold, 0).sum()
    losses = np.maximum(threshold - returns, 0).sum()
    return np.nan if losses == 0 else gains / losses

def max_drawdown(returns):
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    return ((cum - peak) / peak).min()

# =========================
# MAIN TABLE FUNCTION
# =========================
def build_covid_regime_performance_table(
    portfolio_df,
    weights,
    rf=0.0
):
    """
    Portfolio performance metrics across market regimes:
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

        # Skip regime if insufficient assets
        if len(common_assets) < 1:
            results[label] = [np.nan] * 6
            continue

        port_returns = returns[common_assets] @ weights.loc[common_assets]


        results[label] = [
            cagr(port_returns) * 100,
            volatility(port_returns) * 100,
            sharpe_ratio(port_returns, rf),
            omega_ratio(port_returns),
            sortino_ratio(port_returns, rf),
            max_drawdown(port_returns) * 100
        ]

    index = [
        "Annual Return (CAGR %) ",
        "Volatility (%)",
        "Sharpe Ratio",
        "Omega Ratio",
        "Sortino Ratio",
        "Max Drawdown (%)"
    ]

    return pd.DataFrame(results, index=index).round(2)
