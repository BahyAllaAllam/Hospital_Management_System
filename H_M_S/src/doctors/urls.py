from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, DepartmentViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('', DoctorViewSet)


urlpatterns = [
    path('', include(router.urls)),
]