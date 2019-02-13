import math

from rest_framework import serializers


class PageMetaSerializer(serializers.Serializer):
    has_next_page = serializers.SerializerMethodField()
    has_prev_page = serializers.SerializerMethodField()

    next_page_url = serializers.SerializerMethodField()
    prev_page_url = serializers.SerializerMethodField()

    current_page_number = serializers.SerializerMethodField()
    next_page_number = serializers.SerializerMethodField()
    prev_page_number = serializers.SerializerMethodField()
    total_pages_count = serializers.SerializerMethodField()

    total_items_count = serializers.SerializerMethodField()
    offset = serializers.SerializerMethodField()
    requested_page_size = serializers.SerializerMethodField()
    current_items_count = serializers.SerializerMethodField()

    def get_total_items_count(self, resources):
        return self.context.get('paginator').count

    def get_offset(self, resources):
        return self.context.get('paginator').offset

    def get_requested_page_size(self, resources):
        return self.context.get('paginator').limit

    def get_current_page_number(self, resources):
        return self.context.get('request').query_params.get('page', 1)

    def get_total_pages_count(self, instance):
        return math.ceil(self.get_total_items_count(instance) / self.get_requested_page_size(instance))

    def get_has_next_page(self, resources):
        if self.get_current_page_number(resources) < self.get_total_pages_count(resources):
            return True
        else:
            return True

    def get_current_items_count(self, instance):
        return len(instance)

    def get_next_page_number(self, resources):
        if self.get_current_page_number(resources) < self.get_total_pages_count(resources):
            return self.get_current_page_number(resources) + 1
        else:
            return 1

    def get_prev_page_number(self, resources):
        if self.get_current_page_number(resources) > 1:
            return self.get_current_page_number(resources) - 1
        else:
            return 1

    def get_has_prev_page_number(self, resources):
        if self.get_current_page_number(resources) > 1:
            return True
        else:
            return False

    def get_has_prev_page(self, resources):
        if self.get_current_page_number(resources) > 1:
            return True
        else:
            return False

    def get_next_page_url(self, resources):
        return '%s?page=%d&page_size=%d' % (
            self.context.get('request').path, self.get_next_page_number(resources),
            self.get_requested_page_size(resources))

    def get_prev_page_url(self, resources):
        return '%s?page=%d&page_size=%d' % (
            self.context.get('request').path, self.get_prev_page_number(resources),
            self.get_requested_page_size(resources))


class PageMetaModel():
    def __init__(self, request, paginator):
        if not hasattr(paginator, 'count'):
            return
        self.data = {}
        self.data['total_items_count'] = paginator.count
        self.data['offset'] = paginator.offset
        self.data['requested_page_size'] = paginator.limit
        self.data['current_page_number'] = int(request.query_params.get('page', 1))

        self.data['prev_page_number'] = 1
        self.data['total_pages_count'] = math.ceil(self.data['total_items_count'] / self.data['requested_page_size'])

        if self.data['current_page_number'] < self.data['total_pages_count']:
            self.data['has_next_page'] = True
            self.data['next_page_number'] = self.data['current_page_number'] + 1
        else:
            self.data['has_next_page'] = False
            self.data['next_page_number'] = 1

        if self.data['current_page_number'] > 1:
            self.data['prev_page_number'] = self.data['current_page_number'] - 1
        else:
            self.data['has_prev_page'] = False
            self.data['prev_page_number'] = 1

        self.data['next_page_url'] = '%s?page=%d&page_size=%d' % (
            request.path, self.data['next_page_number'], self.data['requested_page_size'])
        self.data['prev_page_url'] = '%s?page=%d&page_size=%d' % (
            request.path, self.data['prev_page_number'], self.data['requested_page_size'])

        # self.paginator.default_limit

        # self.paginator.offset_query_param
        # self.paginator.limit_query_param

    def get_data(self):
        return self.data
