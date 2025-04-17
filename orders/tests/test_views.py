from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer

from django.contrib.auth.models import User


class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.customer = Customer.objects.create(
            code="CUST001",
            name="Test Customer",
            phone_number="+254700000000"
        )
        
        self.order_data = {
            "customer": self.customer.id,
            "item": "Test Item",
            "amount": 1000.00
        }
    def test_create_order(self):
        url = reverse('order-list')
        response = self.client.post(url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

