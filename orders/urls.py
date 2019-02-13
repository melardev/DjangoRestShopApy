from django.conf.urls import url

from orders.views import OrderListView, OrderDetailsView

app_name = 'orders'
urlpatterns = [
    url(r'^orders/?$', OrderListView.as_view(), name='order_list'),
    url(r'^orders/(?P<pk>([a-z0-9-])+)$', OrderDetailsView.as_view(), name='order_details'),

]
