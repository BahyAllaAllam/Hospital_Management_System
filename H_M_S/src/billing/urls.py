from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, InvoiceItemViewSet


router = DefaultRouter()
router.register('items', InvoiceItemViewSet)
router.register('', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]