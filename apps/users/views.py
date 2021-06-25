from rest_framework import viewsets, mixins

from apps.users.models import MoneyTransferHistory
from apps.users.serializers import MoneyTransferHistorySerializer


class MoneyTransferHistoryViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = MoneyTransferHistory.objects.all()
    serializer_class = MoneyTransferHistorySerializer

