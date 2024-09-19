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
        fields = ['id', 'product_name', 'category', 'price', 'date']
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    ratings = RatingSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    product = ProductPhotoSerializer(many=True, read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y')
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'product', 'description', 'price', 'product_video', 'created_date',
                  'active', 'average_rating', 'created_date', 'ratings', 'reviews']



    def get_average_rating(self, obj):
        return obj.get_average_rating()