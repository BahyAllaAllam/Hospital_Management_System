from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, DoctorNoteViewSet, NurseNoteViewSet, LabResultViewSet


router = DefaultRouter()
router.register('doctor-notes', DoctorNoteViewSet, basename='doctor-note')
router.register('nurse-notes', NurseNoteViewSet, basename='nurse-note')
router.register('lab-results', LabResultViewSet, basename='lab-result')
router.register('', MedicalRecordViewSet, basename='medical-record')

urlpatterns = [
    path('', include(router.urls)),
]