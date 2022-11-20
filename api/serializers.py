from rest_framework import serializers
from .models import Event, Product, UserProfile
from django.contrib.auth.models import User

class EventListSerializer(serializers.ModelSerializer):
    owner_logo = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    # banner = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'city', 'address', 'date_from', 'date_to','owner_logo', 'owner_name', 'tags']


    def get_banner(self, obj):
        return obj.banner.url

    def get_owner_logo(self, obj):
        return UserProfile.objects.get(user=obj.owner).logo.url

    def get_owner_name(self, obj):
        return UserProfile.objects.get(user=obj.owner).company_name

    def get_tags(self, obj):
        return Product.objects.filter(event=obj).values_list('tag', flat=True).distinct()


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'collect_from', 'collect_to', 'enabled', 'tag']


class EventDetailsSerializer(serializers.ModelSerializer):
    owner_logo = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    products = ProductDetailsSerializer(many=True) 
    # banner = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'city', 'address', 'date_from', 'date_to','owner_logo', 'owner_name', 
        # 'banner',
        'products']

    def get_banner(self, obj):
        return obj.banner.url

    def get_owner_logo(self, obj):
        return UserProfile.objects.get(user=obj.owner).logo.url

    def get_owner_name(self, obj):
        return UserProfile.objects.get(user=obj.owner).company_name


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'quantity',
            'collect_from',
            'collect_to',
            'enabled',
            'tag'
        ]


class EventCreateSerializer(serializers.ModelSerializer):
    products = ProductCreateSerializer(many=True)

    class Meta:
        model = Event
        fields = ['name', 'city', 'address','date_from', 'date_to', 'banner', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        event = Event.objects.create(**validated_data)
        for product_data in products_data:
            Product.objects.create(event=event, **product_data)
        return event
    
