from rest_framework.viewsets import GenericViewSet, ModelViewSet
from selinaapp.serializers.book.book_serializer import BookSerializer
from selinaapp.models.book import Book
from selinaapp.paginations.book_pagination import BookPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class BookViewSet(GenericViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = BookPagination
    permission_classes = [IsAuthenticated]
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True, excludes=('created_at', 'updated_at', 'deleted_at'))
        data = self.get_paginated_response(self.paginate_queryset(serializer.data)).data
        return Response({'data':data,'message':'Thành công','status_code': 1, 'user_role':request.user.user_type}, status=status.HTTP_200_OK)
    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response({'data':serializer.data,'message':'Thành công','status_code': 1, 'user_role':request.user.user_type}, status=status.HTTP_200_OK)
