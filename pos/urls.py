from django.urls import path
from . import views

urlpatterns = [
    # Ventas
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/<int:pk>/', views.detalle_venta, name='detalle_venta'),

    # Productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/<int:pk>/', views.detalle_producto, name='detalle_producto'),

    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:pk>/', views.detalle_cliente, name='detalle_cliente'),
]