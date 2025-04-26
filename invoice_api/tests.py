from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer, Invoice

# Create your tests here.


class InvoiceAPITests(APITestCase):
    def setUp(self):
        # Create a test customer
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
        
        self.invoice_data = {
            "customer": self.customer.id,
            "issue_date": "2023-01-01",
            "due_date": "2023-02-01",
            "status": "pending",
            "items": [
                {
                    "description": "Test Item 1",
                    "quantity": 2,
                    "unit_price": "10.00"
                },
                {
                    "description": "Test Item 2",
                    "quantity": 1,
                    "unit_price": "20.00"
                }
            ]
        }

    def test_create_invoice(self):
        """
        Ensure we can create a new invoice with items
        """
        url = reverse('invoice-create')
        response = self.client.post(url, self.invoice_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer'], self.customer.id)
        self.assertEqual(len(response.data['items']), 2)
        self.assertEqual(response.data['total_amount'], '40.00')  # 2*10 + 1*20

    def test_invoice_validation(self):
        """
        Test invoice validations
        """
        url = reverse('invoice-create')
        
        # Test empty items
        invalid_data = self.invoice_data.copy()
        invalid_data['items'] = []
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)
        
        # Test due date before issue date
        invalid_data = self.invoice_data.copy()
        invalid_data['due_date'] = "2022-12-31"
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('due_date', response.data)
        
        # Test invalid item quantity
        invalid_data = self.invoice_data.copy()
        invalid_data['items'][0]['quantity'] = 0
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)

    def test_get_invoice(self):
        """
        Test retrieving an invoice with calculated total
        """
        # First create an invoice
        create_url = reverse('invoice-create')
        self.client.post(create_url, self.invoice_data, format='json')
        
        # Then retrieve it
        invoice_id = Invoice.objects.first().id
        detail_url = reverse('invoice-retrieve-update', kwargs={'id': invoice_id})
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_amount'], '40.00')
        self.assertEqual(len(response.data['items']), 2)