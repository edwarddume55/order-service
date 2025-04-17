
from rest_framework import serializers
from .models import Order
from customers.models import Customer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'item', 'amount', 'time']
        extra_kwargs = {
            'customer': {'required': True},
            'time': {'read_only': True}
        }

    def validate_customer(self, value):
        if not Customer.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Customer does not exist")
        return value