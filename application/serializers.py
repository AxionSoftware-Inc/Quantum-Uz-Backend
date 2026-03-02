from rest_framework import serializers
from .models import Mahsulot, Category, Tag, Article, Book, Course

class MahsulotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    tags_names = serializers.StringRelatedField(many=True, read_only=True, source='tags')

    class Meta:
        model = Article
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    tags_names = serializers.StringRelatedField(many=True, read_only=True, source='tags')

    class Meta:
        model = Book
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    tags_names = serializers.StringRelatedField(many=True, read_only=True, source='tags')

    class Meta:
        model = Course
        fields = '__all__'