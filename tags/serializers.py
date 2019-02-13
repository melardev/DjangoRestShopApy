from rest_framework import serializers

from tags.models import Tag


class TagIdAndNameSerializer(serializers.ModelSerializer):
    description = serializers.CharField(write_only=True)
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'image_urls']

    def get_image_urls(self, tag):
        if self.context.get('include_urls', False):
            return [x.file_path for x in tag.images.all()]

        return None

    def to_representation(self, instance):
        response = super(TagIdAndNameSerializer, self).to_representation(instance)
        if response.get('image_urls') is None:
            response.pop('image_urls')

        return response
