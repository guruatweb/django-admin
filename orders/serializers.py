from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    order_total = serializers.SerializerMethodField('get_total')

    def get_total(self, obj):
        items = OrderItem.objects.all().filter(order_id=obj.id)
        return sum((o.quantity * o.price) for o in items)

    class Meta:
        model = Order
        fields = '__all__'
