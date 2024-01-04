from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from selinaapp.models.order import Order
from selinaapp.serializers.order.order_serializer import OrderSerializer

class OrderViewSet(GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='take-an-order')
    def take_an_order(self, request):
        try:
            serializer = self.get_serializer(data=request.data, fields=['delivered_to', 'phone_number', 'cart_group'])
            if not serializer.is_valid():
                return Response({'message': serializer.errors, 'status_code': 4}, status=status.HTTP_200_OK)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Đặt hàng thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'message':str(e), 'status_code': 5}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get-orders')
    def get_orders(self, request):
        pass
