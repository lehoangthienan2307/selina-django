from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from selinaapp.models.cart import Cart
from selinaapp.models.cart_group import CartGroup
from selinaapp.serializers.cart.cart_serializer import CartSerializer

class CartViewSet(GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='add-product-to-cart')
    def add_product_to_cart(self, request):
        try:
            serializer = self.get_serializer(data=request.data, fields=['quantity', 'book'])
            if not serializer.is_valid():
                # How to custom "Invalid pk \"100\" - object does not exist." ?
                if 'book' in serializer.errors:
                    return Response({'message': 'Sách không tồn tại', 'status_code': 4}, status=status.HTTP_200_OK)
                return Response({'message': serializer.errors['message'][0], 'status_code': 4}, status=status.HTTP_200_OK)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Thành công', 'status_code': 1}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response({'message':str(e), 'status_code': 5}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], url_path='get-cart-info')
    def get_cart_info(self, request):
        try:
            user = self.request.user
            cart_groups = CartGroup.objects.filter(buyer=user, is_deleted=False)
            cart_info_list = []

            for cart_group in cart_groups:
                cart_items = Cart.objects.filter(cart_group=cart_group, is_deleted=False)
                cart_item_list = []
                total_price = 0

                for cart_item in cart_items:
                    book_id = cart_item.book.book_id
                
                    cart_item_detail = {
                        'book_in_cart_id': cart_item.id,
                        'book_id': book_id,
                        'image': str(cart_item.book.image),
                        'name': cart_item.book.name,
                        'desc': cart_item.book.desc,
                        'quantity': cart_item.quantity,
                        'price': cart_item.book.price,
                        'total_price': cart_item.quantity * cart_item.book.price
                    }
                    total_price+=cart_item_detail['total_price']
                    cart_item_list.append(cart_item_detail)

                cart_info_list.append({
                    'group_id': cart_group.id,
                    'seller_id': cart_group.seller.id,
                    'seller_name': cart_group.seller.fullname,
                    'seller_avt': cart_group.seller.avatar_url,
                    'books': cart_item_list,
                    'total_price': total_price
                })
            return Response({'data':cart_info_list,'message':'Thành công','status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remove-book-in-cart/(?P<pk>[0-9]+)')
    def remove_book_in_cart(self, request, pk):
        try:
            cart = self.get_object()
            cart.delete()
            return Response({'message': 'Cart xóa thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart không tồn tại', 'status_code': 4}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e), 'status_code': 5}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], url_path='remove-book-group/(?P<pk>[0-9]+)')
    def remove_book_group(self, request, pk):
        try:
            # Or use serializer?
            cart_group = CartGroup.objects.get(pk=pk)
            cart_group.delete()
            return Response({'message': 'CartGroup xóa thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except CartGroup.DoesNotExist:
            return Response({'message': 'CartGroup không tồn tại', 'status_code': 4}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e), 'status_code': 5}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='modify-quantity-book-in-cart')
    def modify_quantity_book_in_cart(self, request):
        try:
            cart = Cart.objects.get(pk=request.data.get('book_in_cart_id'))
            quantity = request.data.get('quantity')
            data = {'quantity': quantity,
                    'book': cart.book.book_id}
            serializer = self.get_serializer(instance=cart, data=data, partial=True)
            if not serializer.is_valid():
                return Response({'message': serializer.errors['message'][0], 'status_code': 4}, status=status.HTTP_200_OK)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get-checkout/(?P<checkout_id>[0-9]+)')
    def get_checkout(self, request, checkout_id):
        try:
            cart_group = CartGroup.objects.get(pk=checkout_id)
            user = self.request.user
            user_info = {
                'phone_num': user.phone,
                'address': user.address
            }
            checkout_response = []

            cart_item_list = []
            cart_items = Cart.objects.filter(cart_group=cart_group, is_deleted=False)
            total_price = 0
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
                total_price+=cart_item_detail['total_price']
                cart_item_list.append(cart_item_detail)

            checkout_response.append({
                'group_id': cart_group.id,
                'seller_id': cart_group.seller.id,
                'seller_name': cart_group.seller.fullname,
                'seller_avt': cart_group.seller.avatar_url,
                'books': cart_item_list,
                'total_price': total_price,
                "user_info": user_info
            })
            return Response({'data':checkout_response,'message':'Thành công','status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)
        