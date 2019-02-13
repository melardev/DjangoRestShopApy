# Not working
from rest_framework import serializers

from categories.serializers import CategoryIdAndNameSerializer
from comments.serializers import CommentSerializer
from products.models import Product
from tags.serializers import TagIdAndNameSerializer


class ProductListSummarySerializer(serializers.ModelSerializer):
    tags = TagIdAndNameSerializer(many=True, required=False)
    categories = CategoryIdAndNameSerializer(many=True, required=False)
    comments_count = serializers.SerializerMethodField()
    image_urls = serializers.SerializerMethodField()
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'stock', 'comments_count', 'tags', 'image_urls', 'categories']

    def get_comments_count(self, product):
        return getattr(product, 'comments__count', None)

    def get_image_urls(self, product):
        return [x.file_path for x in product.images.all()]


class ProductDetailsSerializer(serializers.ModelSerializer):
    tags = TagIdAndNameSerializer(many=True)
    categories = CategoryIdAndNameSerializer(many=True)
    comments = CommentSerializer(many=True)
    image_urls = serializers.SerializerMethodField()

    def get_image_urls(self, product):
        return [x.file_path for x in product.images.all()]

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'slug', 'comments', 'tags', 'categories', 'image_urls']


class ProductElementalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'id', 'slug', ]
