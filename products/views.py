# Create your views here.
import os
import re
from random import choice
from string import ascii_lowercase

from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response

from categories.models import Category
from fileuploads.models import ProductImage
from products.models import Product
from products.serializers import ProductListSummarySerializer, ProductDetailsSerializer
from shared.renderers import AppJsonRenderer
from tags.models import Tag
from users.authentication import IsAdminOrReadOnly


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSummarySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.order_by('-created_at')
        queryset = queryset.annotate(Count('comments'))
        return queryset

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)
        return self.get_paginated_response(serialized_data.data)

    def get_renderer_context(self):
        renderer_context = super(ProductListView, self).get_renderer_context()
        renderer_context['paginator'] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='products')]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
            'include_urls': True,
        }
        tags = []
        categories = []
        for header_key in list(request.data.keys()):
            if 'tags[' in header_key:
                name = header_key[header_key.find("[") + 1:header_key.find("]")]
                description = request.data[header_key]
                tag, created = Tag.objects.get_or_create(name=name, defaults={'description': description})
                tags.append(tag)

            if header_key.startswith('categories['):
                result = re.search('\[(.*?)\]', header_key)
                if len(result.groups()) == 1:
                    name = result.group(1)
                    description = request.data[header_key]
                    category, created = Category.objects.get_or_create(name=name, defaults={'description': description})
                    categories.append(category)

        # images = request.FILES.getlist('images')
        images = request.data.getlist('images[]')
        # TODO this has more work to be done, I have to handle securily file upload feature
        dir = os.path.join(os.getcwd(), 'static', 'images', 'products')
        file_name = "".join(choice(ascii_lowercase) for i in range(16)) + ".png"

        if not os.path.exists(dir):
            os.makedirs(dir)

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )

        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # add expects any number of argument, each one should be the data type expected
        # if we want to pass a list, we have to expaned it, i.e from [tag1, tag2, tag3] to add(tag1, taq2, tag3)
        # that is achieved through `*`
        product.tags.add(*tags)
        product.categories.add(*categories)

        for image in images:
            file_path = os.path.join(dir, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                    ProductImage.objects.create(file_name=file_name, original_name=image.name,
                                                file_length=image.size,
                                                product=product,
                                                file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))

        data = {'full_messages': ['Product created successfully']}
        data.update(ProductDetailsSerializer(product, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)


class ProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    renderer_classes = (AppJsonRenderer,)

    def get_queryset(self):
        if self.kwargs.get('pk', None) is not None:
            return Product.objects.filter(pk=self.kwargs['pk'])
        else:
            return Product.objects.filter(slug=self.kwargs['slug'])

    def get_serializer_context(self):
        context = super(ProductDetailsView, self).get_serializer_context()
        context['include_user'] = True
        context['include_product'] = False
        return context

    @property
    def lookup_field(self):
        if self.kwargs.get('pk', None) is not None:
            return 'pk'
        else:
            return 'slug'


'''
class ProductSelectView(ListAPIView):
    """
    A simple list view, which is used only by the admin backend. It is required to fetch
    the data for rendering the select widget when looking up for a product.
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    serializer_class = app_settings.PRODUCT_SELECT_SERIALIZER
    pagination_class = OnePageResultsSetPagination

    def get_queryset(self):
        term = self.request.GET.get('term', '')
        if len(term) >= 2:
            return ProductModel.objects.select_lookup(term)
        return ProductModel.objects.all()
'''
