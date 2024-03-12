from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from authentfication.permissions.permissions import IsAuthenticatedOrReadOnly
from food.models import Order
from rest_framework.pagination import PageNumberPagination
from food.serializers import OrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_order(request):
    if request.method =='POST':
        #doing serialisation
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'message': 'Oder created successfuly',
                'data': serializer.data
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_one_order(request, id):
    if request.method == 'GET':
        try:
            order = Order.objects.get(pk=id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"})
    
        
@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_order(request, id):
    if request.method=='PUT':
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response("Order not found", status_code=500)   
        serialisation = OrderSerializer(order, data=request.data)
        if serialisation.is_valid():
            serialisation.save()
            return Response(serialisation.data)
        return Response(serialisation.errors, status=status.HTTP_404_NOT_FOUND)
    
#get ALL order
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_all_orders(request):
    if request.method=='GET':
        orders = Order.objects.all()
        print(orders)
        #to do pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_pages = paginator.paginate_queryset(orders, request)
        serialisation = OrderSerializer(result_pages, many=True)
        return paginator.get_paginated_response(serialisation.data)

    
#dete one order
@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_one_orders(request, id):
    if request.method == 'DELETE':
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response("Order not found", status=status.HTTP_404_NOT_FOUND )   
        order.delete()
        return Response("Delete order successfuly", status=500)


