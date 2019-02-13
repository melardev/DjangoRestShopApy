# Create your views here.
import os
from random import choice

from rest_framework import generics, status
from rest_framework.response import Response

from fileuploads.models import TagImage
from shared.renderers import AppJsonRenderer
from tags.models import Tag
from tags.serializers import TagIdAndNameSerializer
from users.authentication import IsAdminOrReadOnly
from string import ascii_lowercase


class TagCreateListView(generics.ListCreateAPIView):
    serializer_class = TagIdAndNameSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        return Tag.objects.all()

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)
        return self.get_paginated_response(serialized_data.data)

    def get_serializer_context(self):
        serializer_context = super(TagCreateListView, self).get_serializer_context()
        serializer_context['include_urls'] = True
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(TagCreateListView, self).get_renderer_context()
        renderer_context['paginator'] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='tags')]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
            'include_urls': True,
        }

        # images = request.FILES.getlist('images')
        images = request.data.getlist('images')

        dir = os.path.join(os.getcwd(), 'static', 'images', 'tags')
        file_name = "".join(choice(ascii_lowercase) for i in range(16)) + ".png"

        if not os.path.exists(dir):
            os.makedirs(dir)

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()

        for image in images:
            file_path = os.path.join(dir, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                    # TODO: improve this
                    # for the moment just hard code the extension
                    TagImage.objects.create(file_name=file_name, original_name=image.name,
                                            file_length=image.size,
                                            tag=tag,
                                            file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))

        data = {'full_messages': ['Tag created successfully']}
        data.update(TagIdAndNameSerializer(tag, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)
