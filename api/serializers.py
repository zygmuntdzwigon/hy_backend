from rest_framework import serializers
from rest_framework import fields

from .models import Event, Product, UserProfile, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'houseNumber', 'city', 'postalCode')


class EventListSerializer(serializers.ModelSerializer):
    ownerLogo = serializers.SerializerMethodField()
    ownerName = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    address = AddressSerializer()

    class Meta:
        model = Event
        fields = ['id', 'name', 'address', 'dateFrom', 'dateTo', 'ownerLogo', 'ownerName', 'address',
                  'banner',
                  'tags']

    def get_banner(self, obj):
        return obj.banner.url

    def get_ownerLogo(self, obj):
        return UserProfile.objects.get(user=obj.owner).logo.url

    def get_ownerName(self, obj):
        return UserProfile.objects.get(user=obj.owner).companyName

    def get_tags(self, obj):
        return Product.objects.filter(event=obj).values_list('tag', flat=True).distinct()


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'collectFrom', 'collectTo', 'enabled', 'tag']


class EventDetailsSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(read_only=True)
    owner_logo = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    products = ProductDetailsSerializer(many=True)

    # banner = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'city', 'address', 'dateFrom', 'dateTo', 'ownerLogo', 'ownerName',
                  # 'banner',
                  'products']

    def get_banner(self, obj):
        return obj.banner.url

    def get_ownerLogo(self, obj):
        return UserProfile.objects.get(user=obj.owner).logo.url

    def get_ownerName(self, obj):
        return UserProfile.objects.get(user=obj.owner).companyName


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'quantity',
            'collectFrom',
            'collectTo',
            'enabled',
            'tag'
        ]


class EventCreateSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(read_only=True)
    products = ProductCreateSerializer(many=True)
    address = AddressSerializer()

    class Meta:
        model = Event
        fields = ['id', 'name', 'address', 'dateFrom', 'dateTo', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        address = Address.objects.create(**validated_data.pop('address'))
        event = Event.objects.create(address=address, **validated_data)
        for product_data in products_data:
            Product.objects.create(event=event, **product_data)
        return event
