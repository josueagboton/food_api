from rest_framework.response import Response
from food.models import Restaurant
from food.serializers import RestaurantSerializer
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


@api_view(['POST'])
def add_restaurant(request):
    if request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response_data = {'message': "restaurant added",
                             "data": serializer.data}
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_one_restaurant(request,id):
    if request.method=='GET':
        try:
            restaurant = Restaurant.objects.get(pk=id)
            serializer = RestaurantSerializer(restaurant)
            return Response({"data": serializer.data})
        
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"})
        
@api_view(['GET'])
def get_list_restaurant(request):
    if request.method=='GET':
        restaurants = Restaurant.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        #gestion des pages
        result_page= paginator.paginate_queryset(restaurants,request)
        serialisation = RestaurantSerializer(result_page, many=True)
        return paginator.get_paginated_response(serialisation.data)

@api_view(['PUT'])
def update_restaurant(request, id):
    if request.method == 'PUT':
        try:
            restaurant = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            return Response({"error": f"Restaurant {id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RestaurantSerializer(instance=restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {"message": "Update successfully", "data": serializer.data}
            return Response(response_data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_restaurant(request,id):
    if request.method== 'DELETE':
        try:
            restaurant = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant"+ id +"not found"})
        restaurant.delete()
        return Response({"success": "Success Deleted"})
    

    


   


    
