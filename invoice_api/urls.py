from django.urls import path
from .views import (
    CustomerListCreateView,
    InvoiceCreateView,
    InvoiceRetrieveUpdateView
)

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('invoices/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoices/<int:id>/', InvoiceRetrieveUpdateView.as_view(), name='invoice-retrieve-update'),
]