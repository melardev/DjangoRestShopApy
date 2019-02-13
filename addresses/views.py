# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from addresses.models import Address
from addresses.serializers import AddressSerializer
from comments.serializers import CommentSerializer
from products.models import Product
from shared.renderers import AppJsonRenderer


# same as extending from generics.ListAPIView, generics.CreateAPIView

class AddressListView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)
        return self.get_paginated_response(serialized_data.data)

    def get_serializer_context(self):
        serializer_context = super(AddressListView, self).get_serializer_context()
        serializer_context['include_user'] = False
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(AddressListView, self).get_renderer_context()
        renderer_context['paginator'] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='addresses')]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
            'include_user': True,
        }

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        data = {'full_messages': ['Address created successfully']}
        data.update(AddressSerializer(address, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)
