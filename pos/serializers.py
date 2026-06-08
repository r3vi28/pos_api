from rest_framework import serializers
from .models import Cliente, Producto, Venta, DetalleVenta

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']


class DetalleVentaSerializerReg(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'atendido_por', 'fecha', 'descuento', 'total', 'detalles']

class VentaSerializerReg(serializers.ModelSerializer):
    detalles = DetalleVentaSerializerReg(many=True, write_only=True)

    class Meta:
        model = Venta
        fields = ['cliente', 'atendido_por', 'descuento', 'detalles']

    def validate(self, data):
        if not data.get('detalles'):
            raise serializers.ValidationError("La venta debe tener al menos un detalle.")
        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')

        total = 0
        for detalle in detalles_data:
            producto = detalle['producto']
            cantidad = detalle['cantidad']
            total += producto.precio * cantidad

        descuento = validated_data.get('descuento', 0)
        total -= descuento

        venta = Venta.objects.create(**validated_data, total=total)

        for detalle in detalles_data:
            producto = detalle['producto']
            cantidad = detalle['cantidad']
            precio_unitario = producto.precio
            subtotal = precio_unitario * cantidad

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            )

        return venta
    
class VentaSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['cliente', 'atendido_por', 'descuento']