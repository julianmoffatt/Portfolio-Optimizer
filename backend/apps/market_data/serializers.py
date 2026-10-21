from rest_framework import serializers
from .models import Asset, PriceHistory, Fundamentals


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'ticker', 'name', 'asset_type', 'sector', 'currency', 'created_at']


class FundamentalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fundamentals
        fields = [
            'date',
            'days_to_earnings',
            'pe_trailing', 'pe_forward',
            'price_to_book', 'ev_to_ebitda', 'price_to_sales',
            'profit_margin', 'operating_margin', 'roe', 'roa',
            'revenue_growth', 'earnings_growth',
            'debt_to_equity', 'current_ratio', 'total_cash', 'total_debt',
            'market_cap', 'enterprise_value', 'total_revenue', 'ebitda',
            'dividend_yield', 'dividend_rate', 'payout_ratio',
        ]


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['datetime', 'timeframe', 'open', 'high', 'low', 'close', 'volume']
