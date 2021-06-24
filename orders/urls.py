from django.urls import path

from .views import OrderGenericView,ExportCSV,ChartAPIView
urlpatterns = [
    path('orders', OrderGenericView.as_view()),
    path('orders/<str:pk>', OrderGenericView.as_view()),
    path('export', ExportCSV.as_view()),
    path('chart', ChartAPIView.as_view()),
    ]