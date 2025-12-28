import os
import pandas as pd

def load_fund_data(country: str, selected_funds: list, base_dir="data"):
    """
    Load fund CSV files for a given country and selected fund types.

    Returns:
        dict: { fund_type : pandas.DataFrame }
    """
    data_path = os.path.join(base_dir, country)
    fund_data = {}

    for fund in selected_funds:
        file_name = f"{fund}_{country}.csv"
        file_path = os.path.join(data_path, file_name)

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            fund_data[fund] = df
        else:
            # file missing → skip silently (or log if needed)
            continue

    return fund_data
