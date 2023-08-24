from rest_framework import pagination

class PageLimitPagination(pagination.PageNumberPagination):
    max_page_size = 100
    page_size_query_param = "_limit"
    page_query_param = "_page"
    page_size = 3
    
