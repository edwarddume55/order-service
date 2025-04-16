from rest_framework import serializers
from .models import Order
from customers.models import Customer
from customers.serializers import CustomerSerializer

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = '__all__'