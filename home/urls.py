from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vendor', views.VendorViewSet, basename="vendor")
router.register(r'purchase', views.PurchaseViewSet, basename="purchase")

urlpatterns = [
    path('', include(router.urls))
]
