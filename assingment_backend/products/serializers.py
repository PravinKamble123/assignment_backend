import json
from rest_framework import serializers

from .models import  Category, Product


class CategorySerializer(serializers.ModelSerializer):
    childrens = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name','parent_category','childrens']
    
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
    
    def get_childrens(self, instance):
        childrens = instance.children_category.all()
        child = []
        child_dict ={}
        for c in childrens:
            child_dict['id'] = c.id
            child_dict['name'] = c.name
            child.append(child_dict)
        return child


    
    
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