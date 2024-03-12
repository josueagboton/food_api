from rest_framework import status
from rest_framework.response import Response
from authentfication.permissions.permissions import IsAuthenticatedOrReadOnly
from food.models import OrderItem
from food.serializers import OrderItemSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_order_item(request):
    if request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_one_order_item(request,id):
    if request.method =='GET':
       try:
            order_item = OrderItem.objects.get(pk=id)
            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data)
       except OrderItem.DoesNotExist:
           return Response("Order Item not found", status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_order_item_from_order(request, orderId):
    if request.method == 'GET':
        try:
            order_items = OrderItem.objects.filter(order_id=orderId)
            serializer = OrderItemSerializer(order_items, many=True)
            return Response(serializer.data)
        except OrderItem.DoesNotExist:
            return Response({"error": "Aucun élément de commande trouvé pour cette commande"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_order_items(request):
    if request.method =='GET':
           order_items = OrderItem.objects.all()
           paginator = PageNumberPagination()
           paginator.page_size = 5
           result_pages = paginator.paginate_queryset(order_items, request)

           serializer = OrderItemSerializer(result_pages, many=True)
           return Response(serializer.data)