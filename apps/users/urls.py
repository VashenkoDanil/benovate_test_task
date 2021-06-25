from rest_framework import routers
from .views import MoneyTransferHistoryViewSet

router = routers.SimpleRouter()

router.register(r'money-transfer-history', MoneyTransferHistoryViewSet, basename='money_transfer_history')

urlpatterns = router.urls
