import csv

from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DRFNEW.pagination import CustomPagination
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from users.authentication import JWTAuthentication


class OrderGenericView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                       mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)


class ExportCSV(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        responce = HttpResponse(content_type='text/csv')
        responce['Content-Disposition'] = 'attachment;filename=order.csv';

        orders = Order.objects.all()
        writer = csv.writer(responce)

        writer.writerow(['ID', 'name', 'email', 'Product Title', 'Price', 'Quantity'])

        for order in orders:
            writer.writerow([order.id, order.name, order.email, '', '', ''])
            orderitem = OrderItem.objects.all().filter(order_id=order.id)
            for item in orderitem:
                writer.writerow(['', '', '', item.product_title, item.price, item.quantity])

        return responce


class ChartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT strftime('%Y-%m-%d',o.created_at) date,sum(t.price*t.quantity) sum
            FROM orders_order o, orders_orderitem t
            WHERE o.id=t.order_id
            GROUP BY date
            """)
            row=cursor.fetchall()

            data=[{
                'date' : result[0],
                'sum': result[1],
            } for result in row]

            return Response({
                'data': data
            })