from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceItemSerializer
from accounts.permissions import IsAdmin, IsAdminOrSupervisor, IsReceptionist, IsAccountant, IsPatient

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Invoice.objects.select_related(
                'patient__user', 'appointment'
            ).prefetch_related('items').filter(patient__user=user)
        return Invoice.objects.select_related(
            'patient__user', 'appointment'
        ).prefetch_related('items').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsReceptionist()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsAdminOrSupervisor()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]

    def partial_update(self, request, *args, **kwargs):
        invoice = self.get_object()
        user = request.user

        if user.role == 'receptionist':
            # receptionist can only update status between paid and unpaid
            allowed_fields = {'status'}
            if set(request.data.keys()) - allowed_fields:
                return Response(
                    {'error': 'Receptionist can only update status'},
                    status=status.HTTP_403_FORBIDDEN
                )
            if request.data.get('status') == 'refunded':
                return Response(
                    {'error': 'Receptionist cannot refund invoices'},
                    status=status.HTTP_403_FORBIDDEN
                )
        if user.role == 'supervisor':
            # supervisor can refund and edit total
            if request.data.get('status') == 'refunded':
                request.data['refunded_by'] = user.id
        return super().partial_update(request, *args, **kwargs)


class InvoiceItemViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceItemSerializer

    def get_queryset(self):
        return InvoiceItem.objects.select_related('invoice').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsReceptionist()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]