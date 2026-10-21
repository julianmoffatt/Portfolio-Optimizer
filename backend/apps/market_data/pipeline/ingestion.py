import pandas as pd
import yfinance as yf


def loadBaseTimeframe(symbol, timeframe_base, premarket_postmarket):
    df = yf.download(
        name_sustitution(symbol),
        interval=timeframe_base,
        auto_adjust=False,
        progress=False,
        period="max",
        prepost=premarket_postmarket,
    )
    if df.empty:
        raise ValueError(f"No data found on Yahoo Finance for '{symbol}'")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

FOREX_PAIRS = {"EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURGBP", "EURJPY", "GBPJPY"}

# se hace en ingest y no hace falta mas
def name_sustitution(name):
    key = name.upper()
    if key == "SP500":
        return "^GSPC"
    elif key == "NASDAQ":
        return "^IXIC"
    elif key == "GOLD":
        return "GC=F"
    elif key == "SILVER":
        return "SI=F"
    elif key == "OIL":
        return "CL=F"
    elif key == "PLATINUM":
        return "PL=F"
    elif key == "PALLADIUM":
        return "PA=F"
    elif key == "BTC":
        return "BTC-USD"
    elif key == "ETH":
        return "ETH-USD"
    elif key in FOREX_PAIRS:
        return f"{key}=X"
    else:
        return name


