from django.conf.urls import url

from tags.views import TagCreateListView

app_name = 'tags'
urlpatterns = [
    url(r'^tags/?$', TagCreateListView.as_view(), name='tag_create_list'),
]
