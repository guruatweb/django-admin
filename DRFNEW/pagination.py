from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFUALT_PAGE_SIZE = 5


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFUALT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'meta': {
                'last_page': int((self.page.paginator.count + (DEFUALT_PAGE_SIZE-1)) // DEFUALT_PAGE_SIZE),
                'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
                'page_size': int(self.request.GET.get('page', self.page_size))
            }
        })
