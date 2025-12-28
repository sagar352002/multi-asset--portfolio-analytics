import plotly.express as px

def plot_donut_chart(weights, title):
    """
    weights : pd.Series (index = fund names, values = weights)
    """

    allocation_df = (
        weights
        .reset_index()
        .rename(columns={"index": "Fund"})
    )

    fig = px.pie(
        allocation_df,
        values="Weight",
        names="Fund",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_traces(
        textinfo="percent",
        textfont_size=14,
        pull=[0.02] * len(allocation_df),
        marker=dict(line=dict(color="white", width=2))
    )

    fig.update_layout(
        width=520,
        height=500,  # ⬅️ slightly increased height
        margin=dict(
            t=95,
            b=100,   # ⬅️ bottom margin ≈ 2 lines
            l=30,
            r=150
        ),

        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.15,
            y=0.5,
            font=dict(size=12)
        ),

        title=dict(
            text=f"<b>{title}</b>",
            x=0.45,
            y=0.97,
            xanchor="center",
            yanchor="top",
            font=dict(size=20)
        )
    )

    # Center label
    fig.add_annotation(
        text="Asset<br>Allocation",
        x=0.5,
        y=0.55,
        font=dict(size=14, color="gray"),
        showarrow=False
    )

    # Caption (with ~2 line gap below)
    fig.add_annotation(
        text="Portfolio allocation across selected funds based on optimized weights.",
        x=0.45,
        y=-0.12,   # ⬅️ lifted caption slightly
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=12, color="#9e9e9e"),
        align="center"
    )

    return fig
