from rest_framework import serializers
from .models import User, Product, ProductSelection


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']


class ProductSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSelection
        fields = ('user', 'product', 'selected')

    def update(self, instance, validated_data):
        instance.selected = validated_data.get('selected', instance.selected)
        instance.save()
        return instance
