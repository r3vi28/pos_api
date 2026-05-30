from rest_framework import serializers
from .models import Cliente, Producto, Venta, DetalleVenta


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['precio_unitario', 'subtotal']


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'atendido_por', 'fecha', 'descuento', 'total', 'detalles']
        read_only_fields = ['fecha', 'total']