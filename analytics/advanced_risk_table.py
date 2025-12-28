import pandas as pd
from analytics.advanced_tail_risk import (
    downside_deviation,
    expected_shortfall_ratio,
    stress_cvar,
    cross_entropy
)
from analytics.tail_risk_metrics import portfolio_returns


def build_advanced_risk_table(
    portfolio_df,
    weights_after,
    stress_start="2020-02-15",
    stress_end="2020-05-31"
):
    """
    Advanced tail-risk comparison table
    """

    n = portfolio_df.shape[1]
    weights_before = pd.Series(1 / n, index=portfolio_df.columns)

    r_before = portfolio_returns(portfolio_df, weights_before)
    r_after = portfolio_returns(portfolio_df, weights_after)

    table = {
        "Before Optimization": [
            downside_deviation(r_before),
            expected_shortfall_ratio(r_before),
            stress_cvar(r_before, stress_start, stress_end),
            cross_entropy(r_before, r_after)
        ],
        "After Optimization": [
            downside_deviation(r_after),
            expected_shortfall_ratio(r_after),
            stress_cvar(r_after, stress_start, stress_end),
            cross_entropy(r_before, r_after)
        ]
    }

    index = [
        "Downside Deviation",
        "Expected Shortfall Ratio",
        "Stress-period CVaR (COVID)",
        "Cross Entropy (Before → After)"
    ]

    return pd.DataFrame(table, index=index).round(4)

