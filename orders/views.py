from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from customers.sms_service import send_sms_notification


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        send_sms_notification(order)
        return Response(serializer.data, status=201)