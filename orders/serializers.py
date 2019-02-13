from rest_framework import serializers

from addresses.serializers import AddressSerializer
from orders.models import Order, OrderItem
from users.serializers import UserUsernameAndIdSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['id', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    tracking_number = serializers.CharField(read_only=True)
    order_items = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    order_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'tracking_number', 'order_status', 'total', 'order_items_count', 'order_items',
                  'address']

    def get_user(self, order):
        if self.context.get('include_user', False):
            return UserUsernameAndIdSerializer(order.user).data
        else:
            return None

    def to_representation(self, instance):
        response = super(OrderSerializer, self).to_representation(instance)
        if response.get('order_items') is None and 'order_items' in response:
            response.pop('order_items')

        if response.get('user') is None and 'user' in response:
            response.pop('user')

        if response.get('address') is None and 'address' in response:
            response.pop('address')

        if response.get('order_items_count') is None and 'order_items_count' in response:
            response.pop('order_items_count')

        return response

    def create(self, validated_data):
        order = Order(address=self.context['address'])
        if self.context['user'] and self.context['user'].is_authenticated:
            order.user = self.context['user']
        order.save()
        return order

    def get_order_status(self, order):
        return Order.ORDER_STATUS[order.order_status][1]

    def get_total(self, order):
        total = 0
        for oi in order.order_items.all():
            total += oi.price
        return total

    def get_address(self, order):
        address = self.context.get('address', None)
        if address is not None:
            address = AddressSerializer(address).data
            return address
        else:
            return None

    def get_order_items(self, order):
        if self.context.get('include_order_items', False):
            order_items = OrderItemSerializer(order.order_items, many=True).data
            return order_items
        else:
            return None

    def get_order_items_count(self, product):
        return getattr(product, 'order_items__count', None)
