from apps.market_data.models import PriceHistory
from apps.market_data.pipeline import ingestion, preprocessing, repository
from datetime import date

TIMEFRAME_BASE = ['1d']


def run_pipeline_for_ticker(ticker: str, skip_fundamentals: bool = False) -> dict:
    today = date.today()
    result = {'ticker': ticker.upper(), 'prices_updated': False, 'fundamentals_updated': False}

    asset = repository.get_or_create_asset(ticker)

    for tf in TIMEFRAME_BASE:
        if PriceHistory.objects.filter(asset=asset, timeframe=tf, datetime__date=today).exists():
            continue
        df_raw = ingestion.loadBaseTimeframe(ticker, tf, premarket_postmarket=False)
        df_clean = preprocessing.preprocessing(df_raw, tf)
        repository.save_price_history(asset, df_clean, tf)
        result['prices_updated'] = True

    if not skip_fundamentals:
        result['fundamentals_updated'] = repository.save_fundamentals(asset)

    return result
