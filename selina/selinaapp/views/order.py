from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from selinaapp.models.order import Order
from selinaapp.models.cart import Cart
from selinaapp.serializers.order.order_serializer import OrderSerializer
from selinaapp.serializers.user.user_serializer import UserSerializer 

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
        try:
            user = self.request.user
            orders = Order.objects.filter(cart_group__buyer = user, is_deleted = False)
            order_response = []
            for order in orders:
                rest_user_serializer = UserSerializer(order.cart_group.seller, fields=('id', 'email', 'fullname', 'phone', 'address', 'gender', 'avatar_url', 'user_type'))

                cart_items = Cart.objects.filter(cart_group=order.cart_group, is_deleted=False)
                cart_item_list = []
                for cart_item in cart_items:
                    cart_item_detail = {
                        'book_in_cart_id': cart_item.id,
                        'book_id': cart_item.book.book_id,
                        'image': str(cart_item.book.image),
                        'name': cart_item.book.name,
                        'desc': cart_item.book.desc,
                        'quantity': cart_item.quantity,
                        'price': cart_item.book.price,
                        'total_price': cart_item.quantity * cart_item.book.price
                    }
                    cart_item_list.append(cart_item_detail)

                order_detail = {
                    'order_id': order.id,
                    "book_group_id": order.cart_group.id,
                    "status": order.status,
                    "delivered_to": order.delivered_to,
                    "phone_number": order.phone_number,
                    "total_price": order.total_price,
                    "payment_method": order.payment_method,
                    'rest_user': rest_user_serializer.data,
                    'books': cart_item_list,
                }

                order_response.append(order_detail)

            return Response({'data': order_response, 'message': 'Thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['patch'], url_path='(?P<pk>[0-9]+)/modify-order-status')
    def modify_order_status(self, request, pk):
        try:
            order = self.get_object()
            serializer = self.get_serializer(instance=order, data=request.data, partial=True)
            if not serializer.is_valid():
                    return Response({'message': serializer.errors, 'status_code': 4}, status=status.HTTP_200_OK)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_200_OK)

        
        
