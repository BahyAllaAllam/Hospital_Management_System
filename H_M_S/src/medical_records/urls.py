from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, DoctorNoteViewSet, NurseNoteViewSet, LabResultViewSet


router = DefaultRouter()
router.register('doctor-notes', DoctorNoteViewSet)
router.register('nurse-notes', NurseNoteViewSet)
router.register('lab-results', LabResultViewSet)
router.register('', MedicalRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]