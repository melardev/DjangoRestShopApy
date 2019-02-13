# Create your views here.
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response

from addresses.models import Address
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from products.models import Product
from shared.renderers import AppJsonRenderer
from shared.views import ResourceListView
from users.authentication import IsAdminOrOwnerOrReadOnly


class OrderListView(ResourceListView, generics.CreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).annotate(Count('order_items'))

    def get_serializer_context(self):
        serializer_context = super(OrderListView, self).get_serializer_context()
        serializer_context['include_user'] = False
        return serializer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='orders')]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
            'include_user': True
        }

        request_data = request.data
        request_data['user'] = request.user

        if 'address_id' in request_data:
            # reusing address, the user has to be authenticated and owning that address
            address = Address.objects.filter(id=request_data['address_id']).only('id', 'user_id').first()
            if request.user is None or not address.user_id == request.user.id:
                return Response({'success': False, 'full_messages': ['Access denied']})

        else:
            address = Address(city=request_data['city'], country=request_data['country'],
                              address=request_data['address'], zip_code=request_data['zip_code'], )
            if request.user is not None and request.user.is_authenticated:
                address.user = request.user
            address.save()

        serializer_context['address'] = address

        serializer = self.serializer_class(
            data=request_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        cart_items = request_data.get('cart_items')
        product_ids = [ci['id'] for ci in cart_items]
        products = Product.objects.filter(id__in=product_ids).only('id', 'name', 'slug', 'price')
        if len(products) != len(cart_items):
            return Response({'success': False, 'full_messages': ['Please make sure all products are still available']},
                            status=status.HTTP_201_CREATED)

        for index, product in enumerate(products):
            order.order_items.add(
                OrderItem.objects.create(order=order, price=product.price,
                                         quantity=cart_items[index]['quantity'], product=product,
                                         name=product.name,
                                         slug=product.slug,
                                         user_id=order.user_id
                                         ))

        data = {'full_messages': ['Order created successfully']}
        serializer_context['include_order_items'] = True
        # data.update(serializer.data)
        data.update(OrderSerializer(order, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)


class OrderDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    renderer_classes = (AppJsonRenderer,)
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_queryset(self):
        return Order.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_context(self):
        context = super(OrderDetailsView, self).get_serializer_context()
        context['include_user'] = True
        context['include_product'] = True
        return context

    def destroy(self, request, *args, **kwargs):
        response = super(OrderDetailsView, self).destroy(request, args, kwargs)
        return Response({'full_messages': ['Removed comment successfully']}, status=status.HTTP_204_NO_CONTENT)
