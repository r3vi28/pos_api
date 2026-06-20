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
from .services.permisos import requiere_admin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

page_param = openapi.Parameter(
    'page', openapi.IN_QUERY,
    description="Número de página a consultar (por defecto 1).",
    type=openapi.TYPE_INTEGER
)

pagesize_param = openapi.Parameter(
    'pagesize', openapi.IN_QUERY,
    description="Cantidad de resultados por página (por defecto 10).",
    type=openapi.TYPE_INTEGER
)


# VENTAS
@swagger_auto_schema(
    method='get',
    operation_description="Lista todas las ventas de forma paginada.",
    manual_parameters=[page_param, pagesize_param],
    responses={200: 'Exitoso'}
)
@swagger_auto_schema(
    method='post',
    operation_description="Registra una nueva venta con sus detalles anidados.",
    request_body=VentaSerializerReg,
    responses={201: 'Creado', 400: 'Error de validación'}
)
@api_view(['GET', 'POST'])
def lista_ventas(request):
    if request.method == 'GET':
        def action():
            ventas = Venta.objects.all().order_by('-id')
            return Paginar(ventas, VentaSerializer, request)
        return TryCatch(action)

    if request.method == 'POST':
        def action():
            if not request.user.is_authenticated:
                return Result.Error('Debe iniciar sesión para registrar una venta.')
            serializer = VentaSerializerReg(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    venta = serializer.save(atendido_por=request.user)
                response_serializer = VentaSerializer(venta)
                return Result.Exitosa('Venta registrada correctamente.', response_serializer.data, status.HTTP_201_CREATED)
            return Result.Error(serializer.errors)
        return TryCatch(action)


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene un cliente específico por su ID.",
    responses={200: 'Exitoso', 400: 'No encontrado'}
)
@swagger_auto_schema(
    method='put',
    operation_description="Actualiza un cliente existente.",
    request_body=ClienteSerializerUpdate,
    responses={200: 'Actualizado', 400: 'Error de validación'}
)
@swagger_auto_schema(
    method='delete',
    operation_description="Elimina un cliente.",
    responses={200: 'Eliminado', 400: 'No encontrado'}
)
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
            error = requiere_admin(request.user)
            if error:
                return error
            serializer = VentaSerializerUpdate(venta, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_serializer = VentaSerializer(venta)
                return Result.Exitosa('Venta actualizada correctamente.', response_serializer.data, status.HTTP_200_OK)
            return Result.Error(serializer.errors)

        if request.method == 'DELETE':
            error = requiere_admin(request.user)
            if error:
                return error
            venta.delete()
            return Result.Exitosa('Venta eliminada correctamente.', {}, status.HTTP_200_OK)

    return TryCatch(action)


# PRODUCTOS
@swagger_auto_schema(
    method='get',
    operation_description="Lista todos los productos de forma paginada.",
    manual_parameters=[page_param, pagesize_param],
    responses={200: 'Exitoso'}
)
@swagger_auto_schema(
    method='post',
    operation_description="Registra un nuevo producto.",
    request_body=ProductoSerializerReg,
    responses={201: 'Creado', 400: 'Error de validación'}
)
@api_view(['GET', 'POST'])
def lista_productos(request):
    if request.method == 'GET':
        def action():
            productos = Producto.objects.all().order_by('-id')
            return Paginar(productos, ProductoSerializer, request)
        return TryCatch(action)

    if request.method == 'POST':
        def action():
            error = requiere_admin(request.user)
            if error:
                return error
            serializer = ProductoSerializerReg(data=request.data)
            if serializer.is_valid():
                serializer.save()
                producto = serializer.instance
                response_serializer = ProductoSerializer(producto)
                return Result.Exitosa('Producto registrado correctamente.', response_serializer.data, status.HTTP_201_CREATED)
            return Result.Error(serializer.errors)
        return TryCatch(action)


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene un producto específico por su ID.",
    responses={200: 'Exitoso', 400: 'No encontrado'}
)
@swagger_auto_schema(
    method='put',
    operation_description="Actualiza un producto existente.",
    request_body=ProductoSerializerUpdate,
    responses={200: 'Actualizado', 400: 'Error de validación'}
)
@swagger_auto_schema(
    method='delete',
    operation_description="Elimina un producto.",
    responses={200: 'Eliminado', 400: 'No encontrado'}
)
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
            error = requiere_admin(request.user)
            if error:
                return error
            serializer = ProductoSerializerUpdate(producto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_serializer = ProductoSerializer(producto)
                return Result.Exitosa('Producto actualizado correctamente.', response_serializer.data, status.HTTP_200_OK)
            return Result.Error(serializer.errors)

        if request.method == 'DELETE':
            error = requiere_admin(request.user)
            if error:
                return error
            producto.delete()
            producto.delete()
            return Result.Exitosa('Producto eliminado correctamente.', {}, status.HTTP_200_OK)

    return TryCatch(action)


# CLIENTES
@swagger_auto_schema(
    method='get',
    operation_description="Lista todos los clientes de forma paginada.",
    manual_parameters=[page_param, pagesize_param],
    responses={200: 'Exitoso'}
)
@swagger_auto_schema(
    method='post',
    operation_description="Registra un nuevo cliente.",
    request_body=ClienteSerializerReg,
    responses={201: 'Creado', 400: 'Error de validación'}
)
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


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene un cliente específico por su ID.",
    responses={200: 'Exitoso', 400: 'No encontrado'}
)
@swagger_auto_schema(
    method='put',
    operation_description="Actualiza un cliente existente.",
    request_body=ClienteSerializerUpdate,
    responses={200: 'Actualizado', 400: 'Error de validación'}
)
@swagger_auto_schema(
    method='delete',
    operation_description="Elimina un cliente.",
    responses={200: 'Eliminado', 400: 'No encontrado'}
)
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
            error = requiere_admin(request.user)
            if error:
                return error
            cliente.delete()
            return Result.Exitosa('Cliente eliminado correctamente.', {}, status.HTTP_200_OK)

    return TryCatch(action)