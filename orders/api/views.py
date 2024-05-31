from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.data.get('user_id'))

    @action(detail=False, methods=['get'])  
    def filter_by_username(self, request):
        user_id = request.query_params.get('user_id', None)
        if user_id is not None:
            orders = self.queryset.filter(user_id=user_id)
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data)
        return Response({"detail": "User ID not provided"}, status=400)
    
    @action(detail=False, methods=['delete'])
    def delete_all_orders(self, request):
        Order.objects.all().delete()
        return Response({"message": "All orders have been deleted"}, status=204)