from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer, Invoice
from .serializers import (
    CustomerSerializer, 
    InvoiceSerializer,
    InvoiceStatusSerializer
)
from django.shortcuts import get_object_or_404

# Create your views here.


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class InvoiceCreateView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Invoice.objects.prefetch_related('items')
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return InvoiceStatusSerializer
        return InvoiceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Calculate total amount
        total_amount = sum(item.total for item in instance.items.all())
        response_data = serializer.data
        response_data['total_amount'] = total_amount
        
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)