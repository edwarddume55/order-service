from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.
from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer