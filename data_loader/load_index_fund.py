import pandas as pd


def load_index_fund(country):
    """
    Load benchmark index fund prices.
    Expects CSV with columns:
    - date
    - index_fund_name (numeric, possibly stored as string)
    """

    df = pd.read_csv(
        f"data/{country.lower()}/index_fund.csv",
        parse_dates=["date"]
    )

    df = df.set_index("date")

    # 👉 Explicitly pick the price column
    if "index_fund_name" not in df.columns:
        raise ValueError(
            f"'index_fund_name' column not found in index_fund.csv for {country}"
        )

    prices = df["index_fund_name"]

    # 🔥 Force numeric conversion (handles commas, symbols, strings)
    prices = (
        prices
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("$", "", regex=False)
    )

    prices = pd.to_numeric(prices, errors="coerce").dropna()

    if prices.empty:
        raise ValueError(
            f"Index fund price column could not be converted to numeric for {country}"
        )

    return prices
