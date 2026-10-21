import pandas as pd
from apps.market_data.pipeline.data_validation import clean_ohlcv

def last_X_years(df, num_years):
    df.index = pd.to_datetime(df.index)
    last_date = df.index.max()
    cutoff_date = last_date - pd.DateOffset(years=num_years)
    return df.loc[df.index >= cutoff_date].copy()


def preprocessing(df, t, symbol=None):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index = pd.to_datetime(df.index, utc=True)

    df.index = df.index.normalize()
    df = df.sort_index()
    df = clean_ohlcv(df)
    return df
