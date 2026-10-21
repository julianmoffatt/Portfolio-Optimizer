from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Asset, Fundamentals
from .serializers import AssetSerializer, FundamentalsSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by('ticker')
    serializer_class = AssetSerializer
    lookup_field = 'ticker'

    @action(detail=True, methods=['get'])
    def fundamentals(self, request, ticker=None):
        asset = self.get_object()
        latest = Fundamentals.objects.filter(asset=asset).order_by('-date').first()
        if not latest:
            return Response({'detail': 'No fundamentals available.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(FundamentalsSerializer(latest).data)
