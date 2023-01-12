from django.urls import path
from .views import CampaignViewSet, CustomerViewSet, InvestmentViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('campaign', CampaignViewSet)
router.register('customer', CustomerViewSet)
router.register('investment', InvestmentViewSet)


urlpatterns = router.urls
