from django.conf.urls import url

from categories.views import CategoryListCreateView

app_name = 'categories'
urlpatterns = [
    url(r'^categories/?$', CategoryListCreateView.as_view(), name='category_create_list'),
]
