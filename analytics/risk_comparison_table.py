import pandas as pd
from analytics.tail_risk_metrics import (
    var_cvar,
    evar,
    entropy,
    cross_entropy,
    portfolio_returns
)
from scipy.stats import skew, kurtosis


def build_risk_comparison_table(portfolio_df, weights_after, alpha=0.95):
    """
    Compare tail & distribution risk:
    - Before: Equal-weight portfolio
    - After : Optimized portfolio
    """

    n_assets = portfolio_df.shape[1]

    # =========================
    # Returns
    # =========================
    w_before = pd.Series(1 / n_assets, index=portfolio_df.columns)

    r_before = portfolio_returns(portfolio_df, w_before)
    r_after = portfolio_returns(portfolio_df, weights_after)

    # =========================
    # Metrics
    # =========================
    var_b, cvar_b = var_cvar(r_before, alpha)
    var_a, cvar_a = var_cvar(r_after, alpha)

    table = {
        "Before Optimization": [
            var_b,
            cvar_b,
            evar(r_before, alpha),
            entropy(r_before),
            skew(r_before),
            kurtosis(r_before, fisher=True)
        ],
        "After Optimization": [
            var_a,
            cvar_a,
            evar(r_after, alpha),
            entropy(r_after),
            skew(r_after),
            kurtosis(r_after, fisher=True)
        ]
    }

    index = [
        "VaR (95%)",
        "CVaR (95%)",
        "EVaR (95%)",
        "Entropy",
        "Skewness",
        "Kurtosis"
    ]

    return pd.DataFrame(table, index=index).round(4)
