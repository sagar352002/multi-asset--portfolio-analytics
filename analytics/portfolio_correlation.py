import numpy as np
import pandas as pd


def portfolio_correlation_with_assets(portfolio_df, weights):
    """
    Correlation between optimized portfolio and each asset
    """

    returns = portfolio_df.pct_change().dropna()
    port_returns = returns @ weights

    return returns.apply(lambda x: x.corr(port_returns))
