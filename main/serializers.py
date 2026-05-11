from rest_framework import serializers
from .models import Category, Brand, Product, Review, Order, OrderItem, ContactMessage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)
    

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'brand', 
            'description', 'image', 'specs', 'reviews'
        ]


class OrderSerializer(serializers.ModelSerializer):

   
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'date', 'items']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

