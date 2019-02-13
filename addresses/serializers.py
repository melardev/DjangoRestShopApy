from rest_framework import serializers

from addresses.models import Address
from users.serializers import UserUsernameAndIdSerializer


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['id', 'first_name', 'last_name', 'address', 'city', 'country', 'zip_code', 'user']

    def get_user(self, address):
        if self.context.get('include_user', False):
            return UserUsernameAndIdSerializer(address.user).data

        return None

    def to_representation(self, instance):
        response = super(AddressSerializer, self).to_representation(instance)
        if response.get('user') is None:
            response.pop('user')

        return response

    def create(self, validated_data):
        return Address.objects.create(user=self.context.get('user'), **validated_data)
