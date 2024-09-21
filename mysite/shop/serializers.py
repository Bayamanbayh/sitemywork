from rest_framework import serializers
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Rating
        fields = ['user', 'stars']

class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Review
        fields = ['author', 'text', 'parent_review', 'created_date']

class ProductSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'price', 'created_date']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    ratings = RatingSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    product = ProductPhotoSerializer(many=True, read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y')
    owner = UserProfileSimpleSerializer
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'product', 'description', 'price', 'product_video', 'created_date',
                  'active', 'created_date', 'ratings', 'reviews', 'owner']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()