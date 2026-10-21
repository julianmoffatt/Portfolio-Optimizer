from rest_framework import serializers
from .models import Portfolio, Position
from apps.market_data.models import Fundamentals
from apps.market_data.serializers import AssetSerializer, FundamentalsSerializer


class PositionSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    asset_id = serializers.IntegerField(write_only=True)
    fundamentals = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ['id', 'asset', 'asset_id', 'weight', 'fundamentals']

    def get_fundamentals(self, obj):
        latest = Fundamentals.objects.filter(asset=obj.asset).order_by('-date').first()
        if latest:
            return FundamentalsSerializer(latest).data
        return None


class PortfolioSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True, source='position_set')

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'description', 'created_at', 'positions']


class PortfolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'description']
