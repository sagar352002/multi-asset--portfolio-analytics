import numpy as np


def average_correlation(portfolio_df):
    returns = portfolio_df.pct_change().dropna()
    corr = returns.corr()

    # Remove diagonal
    upper = corr.where(
        np.triu(np.ones(corr.shape), k=1).astype(bool)
    )

    return upper.stack().mean()
