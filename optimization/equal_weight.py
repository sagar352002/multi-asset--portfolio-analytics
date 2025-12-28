import pandas as pd


def equal_weight_allocation(portfolio_df):
    """
    Equal Weight Portfolio Allocation
    --------------------------------
    portfolio_df : DataFrame of prices / NAVs
    returns      : pd.Series of equal weights
    """

    assets = portfolio_df.columns.tolist()
    n_assets = len(assets)

    if n_assets == 0:
        return pd.Series(dtype=float)

    weights = pd.Series(
        1 / n_assets,
        index=assets,
        name="Weight"
    )

    return weights
