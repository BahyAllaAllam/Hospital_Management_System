from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, DepartmentViewSet

router = DefaultRouter()
router.register('', DoctorViewSet)
router.register('departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]