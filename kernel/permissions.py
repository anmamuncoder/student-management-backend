from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response

# Base pagination class for all paginated responses in the application
class BasePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        })
        