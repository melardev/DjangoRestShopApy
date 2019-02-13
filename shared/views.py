# Create your views here.
from rest_framework import generics


class ResourceListView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)
        return self.get_paginated_response(serialized_data.data)

    def get_serializer_context(self):
        serializer_context = super(ResourceListView, self).get_serializer_context()
        serializer_context['include_user'] = True
        serializer_context['include_product'] = False
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(ResourceListView, self).get_renderer_context()
        renderer_context['paginator'] = self.paginator
        return renderer_context
