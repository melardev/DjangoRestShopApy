from django.conf.urls import url

from addresses.views import AddressListView
from products.views import ProductListView, ProductDetailsView

app_name = 'addresses'
urlpatterns = [
    url(r'^users/addresses$', AddressListView.as_view(), name='address_list'),
]
