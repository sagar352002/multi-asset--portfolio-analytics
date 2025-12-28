import numpy as np
import pandas as pd

TRADING_DAYS = 252


# ======================
# Metric functions
# ======================
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
    return np.nan if downside.std() == 0 else (
        (returns.mean() * TRADING_DAYS - rf) /
        (downside.std() * np.sqrt(TRADING_DAYS))
    )


def omega_ratio(returns, threshold=0.0):
    gains = np.maximum(returns - threshold, 0).sum()
    losses = np.maximum(threshold - returns, 0).sum()
    return np.nan if losses == 0 else gains / losses


def max_drawdown(returns):
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    return ((cum - peak) / peak).min()


def rolling_return_avg(returns, years):
    window = years * TRADING_DAYS
    if len(returns) < window:
        return np.nan

    rolling = (
        (1 + returns)
        .rolling(window)
        .apply(lambda x: x.prod() - 1, raw=False)
    )
    return rolling.dropna().mean()


# ======================
# MAIN TABLE FUNCTION
# ======================
def build_portfolio_metrics_table(portfolio_df, weights, rf=6.0):
    """
    portfolio_df : price / NAV dataframe
    weights      : optimized weights
    """

    returns = portfolio_df.pct_change().dropna()
    port_returns = returns @ weights

    periods = {
        "1Y": 1,
        "3Y": 3,
        "5Y": 5,
        "7Y": 7,
        # "Since Inception": None
    }

    table = {}

    for label, yrs in periods.items():

        # Only fixed-year windows (1Y, 3Y, 5Y, 7Y)
        window = port_returns.iloc[-yrs * TRADING_DAYS:]

        if len(window) < yrs * TRADING_DAYS:
            table[label] = [np.nan] * 7
            continue

        rolling_ret = rolling_return_avg(window, yrs)

        table[label] = [
            cagr(window) * 100,
            rolling_ret * 100,
            volatility(window) * 100,
            sharpe_ratio(window, rf),
            sortino_ratio(window, rf),
            omega_ratio(window),
            max_drawdown(window) * 100
        ]

    index = [
        "CAGR (%)",
        "Avg Rolling Return (%)",
        "Volatility (%)",
        "Sharpe Ratio",
        "Sortino Ratio",
        "Omega Ratio",
        "Max Drawdown (%)"
    ]


    return pd.DataFrame(table, index=index).round(2)
