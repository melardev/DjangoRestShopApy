from rest_framework.pagination import LimitOffsetPagination


class AppPaginator(LimitOffsetPagination):

    def get_limit(self, request):
        page_size = int(request.query_params.get('page_size', 5))
        if page_size < 0 or page_size > 20:
            page_size = 5

        return page_size

    def get_offset(self, request):
        page = int(request.query_params.get('page', 1))
        if page < 0:
            page = 1
        offset = (page - 1) * self.get_limit(request)
        return offset
