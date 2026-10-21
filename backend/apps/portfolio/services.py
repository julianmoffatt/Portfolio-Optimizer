from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from apps.market_data.models import PriceHistory
from .models import Portfolio, Position


PERIODS = {
    '1M': 30,
    '6M': 180,
    'YTD': None,
}


def _get_start_date(period):
    now = datetime.now()
    if period == 'YTD':
        return datetime(now.year, 1, 1)
    return now - timedelta(days=PERIODS[period])


def get_equity_curves(portfolio_id, period='6M'):
    positions = Position.objects.filter(portfolio_id=portfolio_id).select_related('asset')
    start_date = _get_start_date(period)
    curves = {}

    for position in positions:
        prices = list(
            PriceHistory.objects.filter(
                asset=position.asset,
                timeframe='1d',
                datetime__gte=start_date,
            ).order_by('datetime').values('datetime', 'close')
        )
        if not prices:
            continue

        df = pd.DataFrame(prices)
        df['return_pct'] = ((df['close'] / df['close'].iloc[0]) - 1) * 100

        curves[position.asset.ticker] = {
            'weight': float(position.weight),
            'dates': df['datetime'].dt.strftime('%Y-%m-%d').tolist(),
            'returns': df['return_pct'].round(2).tolist(),
        }

    return curves


def get_portfolio_header(portfolio_id, period='6M'):
    curves = get_equity_curves(portfolio_id, period)
    if not curves:
        return {'weighted_return': 0, 'alpha_vs_spy': None}

    weighted_return = sum(
        data['returns'][-1] * data['weight'] / 100
        for data in curves.values()
        if data['returns']
    )

    spy_data = curves.get('SPY')
    alpha = round(weighted_return - spy_data['returns'][-1], 2) if spy_data else None

    return {
        'weighted_return': round(weighted_return, 2),
        'alpha_vs_spy': alpha,
        'period': period,
    }


def get_correlation_matrix(portfolio_id):
    positions = Position.objects.filter(portfolio_id=portfolio_id).select_related('asset')
    start_date = datetime.now() - timedelta(days=365)
    returns = {}

    for position in positions:
        prices = list(
            PriceHistory.objects.filter(
                asset=position.asset,
                timeframe='1d',
                datetime__gte=start_date,
            ).order_by('datetime').values('datetime', 'close')
        )
        if len(prices) < 2:
            continue
        df = pd.DataFrame(prices).set_index('datetime')
        returns[position.asset.ticker] = df['close'].pct_change().dropna()

    if len(returns) < 2:
        return {}

    df_returns = pd.DataFrame(returns).dropna()
    corr = df_returns.corr().round(4)
    cov = df_returns.cov().round(6)

    return {
        'correlation': corr.to_dict(),
        'covariance': cov.to_dict(),
        'tickers': list(returns.keys()),
    }
