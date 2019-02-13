from django.conf.urls import url

from products.views import ProductListView, ProductDetailsView

app_name = 'products'
urlpatterns = [
    url(r'^products$', ProductListView.as_view(), name='product_list'),
    url(r'^products/(?P<slug>([a-z0-9-])+)$', ProductDetailsView.as_view(), name='product_details'),
    url(r'^products/by_id/(?P<pk>([a-z0-9-])+)$', ProductDetailsView.as_view(), name='product_details_by_id'),
]
