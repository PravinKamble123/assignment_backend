from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

# Create your views here.

from .models import *
from .serializers import *


@api_view(['POST'])
def create_category(request):
    data = request.data.copy()
    serializer = CategorySerializer(data= data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_405_BAD_REQUEST)


@api_view(['PUT'])
def update_category(request, pk):
    try:
        # get the category 
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response("Category not found !", status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(instance=category, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_405_BAD_REQUEST)

@api_view(['GET'])
def get_category_list(request):   
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    if serializer is not None:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_405_BAD_REQUEST)
    
@api_view(['GET'])
def get_category_by_id(request, pk):
    try:
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category)
        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_405_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response("category not found")
    
@api_view(['GET'])
def get_childrens(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response('not found !', status=status.HTTP_404_NOT_FOUND)
        childrens = category.children_category.all()
        serializer = CategorySerializer(childrens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        # retrieve the category
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response("category not found !", status=status.HTTP_404_NOT_FOUND)
    # delete the category
    category.delete()
    return Response("category deleted successfully!", status=status.HTTP_204_NO_CONTENT)



class ProductAPIView(APIView):
    def get(self, request, pk=None):

        queryset = Product.objects.all()
        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category=category_id)
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        elif pk:
            try:
                 product = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response('product not found !', status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductListSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Product.objects.all()
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        serializer = ProductSerializer(data=data,)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    def put(self, request, pk):
        data = request.data.copy()
        try:
            # retrieve the product from the database
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response('product not found', status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance=product,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_405_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            # retrieve the product 
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response('product not found !', status=status.HTTP_404_NOT_FOUND) 
        # delete the product 
        product.delete()
        return Response('product deleted successfully!', status=status.HTTP_204_NO_CONTENT)      



