from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    """Определение пагинации с учётом limit."""

    page_size_query_param = 'limit'
