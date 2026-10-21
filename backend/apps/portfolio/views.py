from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Portfolio, Position
from .serializers import PortfolioSerializer, PortfolioCreateSerializer, PositionSerializer
from . import services
from apps.market_data.services import run_pipeline_for_ticker


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PortfolioCreateSerializer
        return PortfolioSerializer

    @action(detail=True, methods=['get'])
    def positions(self, request, pk=None):
        portfolio = self.get_object()
        positions = Position.objects.filter(portfolio=portfolio).select_related('asset')
        return Response(PositionSerializer(positions, many=True).data)

    @action(detail=True, methods=['post'], url_path='positions/add')
    def add_position(self, request, pk=None):
        portfolio = self.get_object()
        ticker = request.data.get('ticker', '').upper()
        weight = request.data.get('weight')

        if not ticker:
            return Response({'detail': 'ticker is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if weight is None:
            return Response({'detail': 'weight is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            run_pipeline_for_ticker(ticker)
        except Exception as e:
            return Response({'detail': f'Pipeline failed for {ticker}: {e}'}, status=status.HTTP_502_BAD_GATEWAY)

        from apps.market_data.models import Asset
        asset = Asset.objects.get(ticker=ticker)

        position, created = Position.objects.get_or_create(
            portfolio=portfolio,
            asset=asset,
            defaults={'weight': weight},
        )
        if not created:
            position.weight = weight
            position.save()

        return Response(PositionSerializer(position).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='positions/(?P<asset_id>[^/.]+)/remove')
    def remove_position(self, request, pk=None, asset_id=None):
        portfolio = self.get_object()
        try:
            position = Position.objects.get(portfolio=portfolio, asset_id=asset_id)
            position.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Position.DoesNotExist:
            return Response({'detail': 'Position not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        self.get_object()
        period = request.query_params.get('period', '6M')
        curves = services.get_equity_curves(pk, period)
        header = services.get_portfolio_header(pk, period)
        return Response({'header': header, 'curves': curves})

    @action(detail=True, methods=['get'])
    def risk(self, request, pk=None):
        self.get_object()
        data = services.get_correlation_matrix(pk)
        return Response(data)
