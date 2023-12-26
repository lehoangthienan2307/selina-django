from rest_framework import pagination
from rest_framework.response import Response
class BookPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'limit'
    max_page_size = 50
    page_query_param = 'page'
    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'page': self.page.number,
            'count': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'docs': data
        })