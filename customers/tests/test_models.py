from django.test import TestCase
from customers.models import Customer

class CustomerModelTest(TestCase):
    def test_create_customer(self):
        customer = Customer.objects.create(
            code="CUST001",
            name="Test Customer",
            phone_number="+254700000000"
        )
        self.assertEqual(str(customer), "Test Customer (CUST001)")