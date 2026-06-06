from django.urls import path
from . import views

urlpatterns = [
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/<int:pk>/', views.detalle_venta, name='detalle_venta'),
]