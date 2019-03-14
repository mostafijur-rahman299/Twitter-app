# @Date:   2019-01-11T23:50:01+06:00
# @Last modified time: 2019-01-11T23:51:40+06:00
from rest_framework import pagination

class StandartResultpagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
