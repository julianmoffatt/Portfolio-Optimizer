import pandas as pd
from django.db import transaction
from apps.market_data.models import Asset, PriceHistory, Fundamentals
import yfinance as yf


def get_or_create_asset(ticker: str) -> Asset:
    info = {}
    try:
        info = yf.Ticker(ticker).info
    except Exception:
        pass

    asset, _ = Asset.objects.get_or_create(
        ticker=ticker.upper(),
        defaults={
            'name': info.get('longName', ''),
            'asset_type': info.get('quoteType', '').lower(),
            'sector': info.get('sector', ''),
            'currency': info.get('currency', 'USD'),
        }
    )
    return asset


@transaction.atomic
def save_price_history(asset: Asset, df: pd.DataFrame, timeframe: str):
    objs = []
    for dt, row in df.iterrows():
        objs.append(PriceHistory(
            asset=asset,
            datetime=dt,
            timeframe=timeframe,
            open=row.get('Open', 0),
            high=row.get('High', 0),
            low=row.get('Low', 0),
            close=row.get('Close', 0),
            volume=int(row.get('Volume', 0)),
        ))

    PriceHistory.objects.bulk_create(
        objs,
        update_conflicts=True,
        unique_fields=['asset', 'datetime', 'timeframe'],
        update_fields=['open', 'high', 'low', 'close', 'volume'],
    )


@transaction.atomic
def save_fundamentals(asset: Asset) -> bool:
    from datetime import date
    today = date.today()
    if Fundamentals.objects.filter(asset=asset, date=today).exists():
        return False

    info = {}
    try:
        info = yf.Ticker(asset.ticker).info
    except Exception:
        return False

    earnings_ts = info.get('earningsTimestamp')
    days_to_earnings = None
    if earnings_ts:
        from datetime import datetime
        earnings_date = datetime.fromtimestamp(earnings_ts).date()
        days_to_earnings = (earnings_date - date.today()).days

    Fundamentals.objects.update_or_create(
        asset=asset,
        date=today,
        defaults={
            'days_to_earnings': days_to_earnings,
            'pe_trailing': info.get('trailingPE'),
            'pe_forward': info.get('forwardPE'),
            'price_to_book': info.get('priceToBook'),
            'ev_to_ebitda': info.get('enterpriseToEbitda'),
            'price_to_sales': info.get('priceToSalesTrailingTwelveMonths'),
            'profit_margin': info.get('profitMargins'),
            'operating_margin': info.get('operatingMargins'),
            'roe': info.get('returnOnEquity'),
            'roa': info.get('returnOnAssets'),
            'revenue_growth': info.get('revenueGrowth'),
            'earnings_growth': info.get('earningsGrowth'),
            'debt_to_equity': info.get('debtToEquity'),
            'current_ratio': info.get('currentRatio'),
            'total_cash': info.get('totalCash'),
            'total_debt': info.get('totalDebt'),
            'market_cap': info.get('marketCap'),
            'enterprise_value': info.get('enterpriseValue'),
            'total_revenue': info.get('totalRevenue'),
            'ebitda': info.get('ebitda'),
            'dividend_yield': info.get('dividendYield'),
            'dividend_rate': info.get('dividendRate'),
            'payout_ratio': info.get('payoutRatio'),
        }
    )
    return True
