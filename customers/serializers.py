from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'code', 'name', 'phone_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']


 