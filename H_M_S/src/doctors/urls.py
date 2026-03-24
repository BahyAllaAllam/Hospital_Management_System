from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, DepartmentViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='department')
router.register('', DoctorViewSet, basename='doctor')


urlpatterns = [
    path('', include(router.urls)),
]