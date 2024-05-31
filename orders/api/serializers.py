from rest_framework import serializers
from .models import Order, OrderItem
import requests
from django.conf import settings

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product', 'quantity']

    def get_product(self, obj):
        response = requests.get(f"{settings.EXTERNAL_SERVICES['PRODUCT_SERVICE_URL']}{obj.product_id}/")
        return response.json()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'user', 'created_at','order_cost', 'items']

    def get_user(self, obj):
        response = requests.get(f"{settings.EXTERNAL_SERVICES['USER_SERVICE_URL']}{obj.user_id}/")
        return response.json()

    def get_product(self, obj):
        response = requests.get(f"{settings.EXTERNAL_SERVICES['PRODUCT_SERVICE_URL']}{obj.product_id}/")
        return response.json()

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(user_id=validated_data.get('user_id'))
        total_cost = 0
        for item_data in items_data:
            order_item = OrderItem.objects.create(order=order, **item_data)
            product_data = self.get_product(order_item)  # Use get_product method to fetch product details
            product_price = product_data.get('price', 0)
            total_cost += product_price * order_item.quantity
        order.order_cost = total_cost
        order.save()
        return order
    

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()

        for item_data in items_data:
            item = OrderItem.objects.get(order=instance, product_id=item_data['product_id'])
            item.quantity = item_data.get('quantity', item.quantity)
            item.save()
        return instance
