import plotly.express as px
import numpy as np

def plot_correlation_heatmap(portfolio_df):
    """
    AMC-style correlation heatmap
    """

    returns = portfolio_df.pct_change().dropna()
    corr = returns.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        aspect="auto"
    )

    fig.update_layout(
        height=520,

        # 🔹 one-line vertical gap between title & chart
        margin=dict(t=80, b=40, l=40, r=40),

        # ✅ BOLD + ~2 TAB LEFT SHIFT
        title=dict(
            text="<b>🔗 Asset Correlation Matrix & Diversification Analysis</b>",
            x=0.48,          # ~2 tabs left
            xanchor="center",
            y=0.96,          # keep title slightly higher
            font=dict(size=18)
        ),

        coloraxis_colorbar=dict(
            title=dict(
                text="Correlation"
            )
        )
    )

    return fig
