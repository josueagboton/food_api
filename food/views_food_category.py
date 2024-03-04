from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from authentfication.permissions.permissions import IsAuthenticatedOrReadOnly
from food.models import FoodCategory
from rest_framework.pagination import PageNumberPagination

from food.serializers import FoodCategorySerializer

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_food_category(request):
    if request.method == 'POST':
        print(request.data)
        serializer = FoodCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            response_data = {
                'message': 'Food item created successfully!',
                'data': serializer.data,
            }
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_list_categories(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Nombre d'éléments par page
        food_categories = FoodCategory.objects.all()

        result_page = paginator.paginate_queryset(food_categories, request)
        serializer = FoodCategorySerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_food_category(request, id):
    if request.method== 'PUT':
        try:
            foodCategory = FoodCategory.objects.get(pk=id)
        except FoodCategory.DoesNotExist:
            return Response({"erreur": "categoryFood not found"}, status=404)

        serializer = FoodCategorySerializer(foodCategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "message" : "Update successfully",
                "data": serializer.data
            }
            return Response(response_data)
        return Response(serializer.errors, status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_food_category(request, id):
    if request.method == 'GET':
        try:
            foodcate = FoodCategory.objects.get(pk=id)
            serializer = FoodCategorySerializer(foodcate)
            return Response({"data": serializer.data}, status=202)
        except FoodCategory.DoesNotExist:
            return Response({"error": "CategoryFood not found"}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_food_category(request, id):
    if request.method == 'DELETE':
        try:
            foodCategory = FoodCategory.objects.get(pk=id)
        except:
            return Response({"error", "CategoryFoud not found"}, status=404)
        foodCategory.delete()
        return Response({"success", "Food Category is deleted"}, status=202)
    return Response({"error": "Error request"})



        

    

