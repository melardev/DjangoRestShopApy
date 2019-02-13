import json

from rest_framework import renderers

from shared.serializers import PageMetaSerializer


class AppJsonRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def __init__(self, **kwargs):
        super(AppJsonRenderer, self).__init__()
        self.resources_name = kwargs.get('resources_name', 'resources')

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if type(data) is str or data is None:
            return data
        results = data.get('results')

        if results is not None:
            page_meta = PageMetaSerializer(data, context=renderer_context)

            response = {
                'success': True,
                'page_meta': page_meta.data,
                self.resources_name: results
            }
        else:
            response = {
                'success': False,
                'full_messages': ['Unknown error']
            }
            data['success'] = True
            response = data

        return json.dumps(response)
