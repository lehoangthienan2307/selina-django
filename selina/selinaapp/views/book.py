from rest_framework.viewsets import GenericViewSet, ModelViewSet
from selinaapp.serializers.book.book_serializer import BookSerializer
from selinaapp.models.book import Book
from selinaapp.paginations.book_pagination import BookPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import filters
class BookViewSet(GenericViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = BookPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'author']
    
    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True, excludes=('created_at', 'updated_at', 'deleted_at'))
            data = self.get_paginated_response(self.paginate_queryset(serializer.data)).data
            return Response({'data':data,'message':'Thành công','status_code': 1, 'user_role':request.user.user_type}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk):
        try:
            item = self.get_object()
            serializer = self.get_serializer(item)
            return Response({'data':serializer.data,'message':'Thành công','status_code': 1, 'user_role':request.user.user_type}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], url_path='get-shop-data/(?P<seller_id>[0-9]+)')
    def get_seller_books(self, request, seller_id):
        try:
            seller_books = Book.objects.filter(seller_info__id=seller_id)
            serializer = self.get_serializer(seller_books, many=True, excludes=('created_at', 'updated_at', 'deleted_at'))
            data = self.get_paginated_response(self.paginate_queryset(serializer.data)).data
            return Response({'data': data, 'message': 'Thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)
        
    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': serializer.errors, 'status_code': 4}, status=status.HTTP_200_OK)
            self.perform_create(serializer)
            return Response({'data': serializer.data, 'message': 'Thành công', 'status_code': 1}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)
        
    def perform_create(self, serializer):
        serializer.save(seller_info=self.request.user)

    def destroy(self, request, pk):
        try:
            book = self.get_object()
            book.delete()
            return Response({'message': 'Book deleted successfully', 'status_code': 1}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found', 'status_code': 4}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e), 'status_code': 5}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['patch'], url_path='modify-product-info/(?P<pk>[0-9]+)')
    def modify_book(self, request, pk):
        try:
            book = self.get_object()
            serializer = self.get_serializer(instance=book, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({'message': serializer.errors, 'status_code': 4}, status=status.HTTP_200_OK)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)