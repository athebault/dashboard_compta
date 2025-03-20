# utils/parse_content.py

# utils/load_initial_data.py

import pandas as pd
from app.config import file_name
from .data_processing import prepare_data


def load_initial_data():
    df = pd.read_excel(file_name, skiprows=2)
    df.columns.values[0] = "Soldes, comptes et écritures"
    data_long = prepare_data(df)
    return data_long
