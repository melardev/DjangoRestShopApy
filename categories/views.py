from rest_framework import generics

from categories.models import Category
from categories.serializers import CategoryIdAndNameSerializer
from shared.renderers import AppJsonRenderer
from users.authentication import IsAdminOrReadOnly


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoryIdAndNameSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        serializer_context['include_urls'] = True
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)
        return self.get_paginated_response(serialized_data.data)

    def get_serializer_context(self):
        serializer_context = super(CategoryListCreateView, self).get_serializer_context()
        serializer_context['include_urls'] = True
        serializer_context['request'] = self.request
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(CategoryListCreateView, self).get_renderer_context()
        renderer_context['paginator'] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='tags')]

    def perform_create(self, serializer):
        super(CategoryListCreateView, self).perform_create(serializer)
        data = {'success': True, 'full_messages': ['Tag created successfully']}
        serializer.data.update(data)
