from rest_framework.decorators import api_view
from rest_framework import status
from .models import Venta, Producto, Cliente
from .serializers import (
    VentaSerializer, VentaSerializerReg, VentaSerializerUpdate,
    ProductoSerializer, ProductoSerializerReg, ProductoSerializerUpdate,
    ClienteSerializer, ClienteSerializerReg, ClienteSerializerUpdate
)
from django.db import transaction
from .services.response import Result, TryCatch
from .services.pagination import Paginar


# VENTAS
@api_view(['GET', 'POST'])
def lista_ventas(request):
    if request.method == 'GET':
        def action():
            ventas = Venta.objects.all().order_by('-id')
            return Paginar(ventas, VentaSerializer, request)
        return TryCatch(action)

    if request.method == 'POST':
        def action():
            serializer = VentaSerializerReg(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    venta = serializer.save()
                response_serializer = VentaSerializer(venta)
                return Result.Exitosa('Venta registrada correctamente.', response_serializer.data, status.HTTP_201_CREATED)
            return Result.Error(serializer.errors)
        return TryCatch(action)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_venta(request, pk):
    def action():
        try:
            venta = Venta.objects.get(pk=pk)
        except Venta.DoesNotExist:
            return Result.Error('Venta no encontrada.')

        if request.method == 'GET':
            serializer = VentaSerializer(venta)
            return Result.Exitosa('', serializer.data, status.HTTP_200_OK)

        if request.method == 'PUT':
            serializer = VentaSerializerUpdate(venta, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_serializer = VentaSerializer(venta)
                return Result.Exitosa('Venta actualizada correctamente.', response_serializer.data, status.HTTP_200_OK)
            return Result.Error(serializer.errors)

        if request.method == 'DELETE':
            venta.delete()
            return Result.Exitosa('Venta eliminada correctamente.', {}, status.HTTP_200_OK)

    return TryCatch(action)


# PRODUCTOS
@api_view(['GET', 'POST'])
def lista_productos(request):
    if request.method == 'GET':
        def action():
            productos = Producto.objects.all().order_by('-id')
            return Paginar(productos, ProductoSerializer, request)
        return TryCatch(action)

    if request.method == 'POST':
        def action():
            serializer = ProductoSerializerReg(data=request.data)
            if serializer.is_valid():
                serializer.save()
                producto = serializer.instance
                response_serializer = ProductoSerializer(producto)
                return Result.Exitosa('Producto registrado correctamente.', response_serializer.data, status.HTTP_201_CREATED)
            return Result.Error(serializer.errors)
        return TryCatch(action)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_producto(request, pk):
    def action():
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Result.Error('Producto no encontrado.')

        if request.method == 'GET':
            serializer = ProductoSerializer(producto)
            return Result.Exitosa('', serializer.data, status.HTTP_200_OK)

        if request.method == 'PUT':
            serializer = ProductoSerializerUpdate(producto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_serializer = ProductoSerializer(producto)
                return Result.Exitosa('Producto actualizado correctamente.', response_serializer.data, status.HTTP_200_OK)
            return Result.Error(serializer.errors)

        if request.method == 'DELETE':
            producto.delete()
            return Result.Exitosa('Producto eliminado correctamente.', {}, status.HTTP_200_OK)

    return TryCatch(action)


# CLIENTES
@api_view(['GET', 'POST'])
def lista_clientes(request):
    if request.method == 'GET':
        def action():
            clientes = Cliente.objects.all().order_by('-id')
            return Paginar(clientes, ClienteSerializer, request)
        return TryCatch(action)

    if request.method == 'POST':
        def action():
            serializer = ClienteSerializerReg(data=request.data)
            if serializer.is_valid():
                serializer.save()
                cliente = serializer.instance
                response_serializer = ClienteSerializer(cliente)
                return Result.Exitosa('Cliente registrado correctamente.', response_serializer.data, status.HTTP_201_CREATED)
            return Result.Error(serializer.errors)
        return TryCatch(action)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_cliente(request, pk):
    def action():
        try:
            cliente = Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            return Result.Error('Cliente no encontrado.')

        if request.method == 'GET':
            serializer = ClienteSerializer(cliente)
            return Result.Exitosa('', serializer.data, status.HTTP_200_OK)

        if request.method == 'PUT':
            serializer = ClienteSerializerUpdate(cliente, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_serializer = ClienteSerializer(cliente)
                return Result.Exitosa('Cliente actualizado correctamente.', response_serializer.data, status.HTTP_200_OK)
            return Result.Error(serializer.errors)

        if request.method == 'DELETE':
            cliente.delete()
            return Result.Exitosa('Cliente eliminado correctamente.', {}, status.HTTP_200_OK)

    return TryCatch(action)