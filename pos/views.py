from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Venta, Producto
from .serializers import (
    VentaSerializer, VentaSerializerReg, VentaSerializerUpdate,
    ProductoSerializer, ProductoSerializerReg, ProductoSerializerUpdate
)
from django.db import transaction

@api_view(['GET', 'POST'])
def lista_ventas(request):
    """
    GET  /api/ventas/ → retorna todas las ventas.
    POST /api/ventas/ → crea una nueva venta con sus detalles.
    """
    if request.method == 'GET':
        ventas = Venta.objects.all()
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = VentaSerializerReg(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                venta = serializer.save()
            response_serializer = VentaSerializer(venta)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_venta(request, pk):
    """
    GET    /api/ventas/{id}/ → retorna una venta específica.
    PUT    /api/ventas/{id}/ → actualiza una venta.
    DELETE /api/ventas/{id}/ → elimina una venta.
    """
    try:
        venta = Venta.objects.get(pk=pk)
    except Venta.DoesNotExist:
        return Response(
            {'error': 'Venta no encontrada.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = VentaSerializer(venta)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = VentaSerializerUpdate(venta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        venta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def lista_productos(request):
    """
    GET  /api/productos/ → retorna todos los productos.
    POST /api/productos/ → crea un nuevo producto.
    """
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ProductoSerializerReg(data=request.data)
        if serializer.is_valid():
            serializer.save()
            producto = serializer.instance
            response_serializer = ProductoSerializer(producto)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_producto(request, pk):
    """
    GET    /api/productos/{id}/ → retorna un producto específico.
    PUT    /api/productos/{id}/ → actualiza un producto.
    DELETE /api/productos/{id}/ → elimina un producto.
    """
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ProductoSerializerUpdate(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ProductoSerializer(producto)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)