from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    page_size = 5

    def get_paginated_response(self, data):
        request = self.request
        search = request.query_params.get('search', '')
        page = request.query_params.get('page', 1)

        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),            # ← balik ke URL penuh
            'previous': self.get_previous_link(),    # ← balik ke URL penuh
            'search': search,        # ← custom field
            'page': page,        # ← custom field
            'results': data
        })