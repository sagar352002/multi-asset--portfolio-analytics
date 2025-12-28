import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

TRADING_DAYS = 252


def calculate_alpha_beta(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    rf: float = 0.0
):
    """
    Robust CAPM Alpha & Beta calculation
    Handles DD-MM-YYYY dates safely
    """

    # 🔥 FIX: Explicit date parsing
    portfolio_returns.index = pd.to_datetime(
        portfolio_returns.index,
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    benchmark_returns.index = pd.to_datetime(
        benchmark_returns.index,
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    # Drop invalid dates
    portfolio_returns = portfolio_returns.dropna()
    benchmark_returns = benchmark_returns.dropna()

    # Align on common dates
    df = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1,
        join="inner"
    ).dropna()

    if df.empty or len(df) < 2:
        raise ValueError(
            "Not enough overlapping dates between portfolio and benchmark to compute Alpha & Beta."
        )

    df.columns = ["Rp", "Rm"]

    rf_daily = rf / TRADING_DAYS

    y = df["Rp"] - rf_daily
    X = (df["Rm"] - rf_daily).values.reshape(-1, 1)

    model = LinearRegression().fit(X, y)

    beta = model.coef_[0]
    alpha_annual = model.intercept_ * TRADING_DAYS

    return {
        "Alpha (%)": round(alpha_annual * 100, 2),
        "Beta": round(beta, 3),
        "Observations": len(df)
    }
