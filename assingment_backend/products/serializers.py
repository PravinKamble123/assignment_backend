from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category


    
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = '__all__'


    def create(self, validated_data):
        categories_data = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.set(categories_data)
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('category')
        instance.name = validated_data.get('name', instance.name)
        instance.category.set(categories_data)
        instance.save()
        return instance
    

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','name','price','description','category','created_at','updated_at'] 