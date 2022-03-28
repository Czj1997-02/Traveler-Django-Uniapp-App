from rest_framework.pagination import PageNumberPagination


class CommonPagination(PageNumberPagination):
    """
    通用分页配置类
    """
    # 每页的记录数
    page_size = 10
    # url中请求“页”的参数名
    page_query_param = 'page'
    # url中请求“每页记录数”的参数名
    page_size_query_param = 'page_size'
    # 每页最大记录数
    max_page_size = 200
