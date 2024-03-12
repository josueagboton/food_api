from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from authentfication.permissions.permissions import IsAuthenticatedOrReadOnly


from food.models import Food, FoodCategory
from food.serializers import FoodSerializer

# Create your views here.
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def food_list(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Nombre d'éléments par page

        foods = Food.objects.all()
        result_page = paginator.paginate_queryset(foods, request)
        serializer = FoodSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_food(request):
    if request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            food = serializer.save()
            # Customize the response for a successful creation
            response_data = {
                'message': 'Food item created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        new_refresh_token = str(token)
        
        return Response({'access_token': access_token, 'refresh_token': new_refresh_token}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def food_detail(request, pk):
    try:
        food = Food.objects.get(pk=pk)
    except Food.DoesNotExist:
        # Customize the response for a food item not found
        return Response({'Error': 'Food not found'}, status=404)

    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Customize the response for a successful update
            response_data = {
                'message': 'Food item updated successfully!',
                'data': serializer.data,
            }
            return Response(response_data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        food.delete()
        # Customize the response for a successful deletion
        return Response({'message': 'Food item deleted successfully!'}, status=204)
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_foods_by_food_category(request, id):
    try:
        foodCategory = FoodCategory.objects.get(pk=id)
    except FoodCategory.DoesNotExist:
        return Response({"error": "FoodCategory not found"}, status=404)
    
    foods = Food.objects.filter(foodCategory=foodCategory)
    paginator = PageNumberPagination()
    paginator.page_size = 4

     # Obtenir la page courante
    page = paginator.paginate_queryset(foods, request)

    # Sérialiser les données de la page
    serializer = FoodSerializer(page, many=True)

    # Retourner les données paginées
    return paginator.get_paginated_response(serializer.data)



