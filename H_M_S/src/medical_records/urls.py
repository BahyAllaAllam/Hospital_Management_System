from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, MedicalRecordAttachmentViewSet


router = DefaultRouter()
router.register('attachments', MedicalRecordAttachmentViewSet)
router.register('', MedicalRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]