from rest_framework import serializers
from .models import Cliente, Producto, Venta, DetalleVenta

# DETALLE VENTA
# Serializador de lectura para los detalles de una venta.
class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']

# Serializador utilizado para registrar detalles al crear una venta.
class DetalleVentaSerializerReg(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']

# VENTA
# Serializador de lectura para ventas con sus detalles incluidos.
class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'atendido_por', 'fecha', 'descuento', 'total', 'detalles']

# Serializador para registrar una venta y sus detalles.
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

# Serializador para actualizar información general de una venta.
class VentaSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['cliente', 'atendido_por', 'descuento']

# PRODUCTO
# Serializador de lectura para productos.
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'have_code', 'codigo_barra']

# Serializador para registrar productos con validaciones de negocio.
class ProductoSerializerReg(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'have_code', 'codigo_barra']

    def validate(self, data):
        if data.get('precio') <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        if data.get('have_code') and not data.get('codigo_barra'):
            raise serializers.ValidationError("El codigo de barra es requerido cuando have_code es True.")
        if not data.get('have_code') and data.get('codigo_barra'):
            raise serializers.ValidationError("No puede tener codigo de barra cuando have_code es False.")
        return data

# Serializador para actualizar productos con validaciones parciales.
class ProductoSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'have_code', 'codigo_barra']

    def validate(self, data):
        if 'precio' in data and data.get('precio') <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        if data.get('have_code') and not data.get('codigo_barra'):
            raise serializers.ValidationError("El codigo de barra es requerido cuando have_code es True.")
        if not data.get('have_code') and data.get('codigo_barra'):
            raise serializers.ValidationError("No puede tener codigo de barra cuando have_code es False.")
        return data
    

# CLIENTE
# Serializador de lectura para consultar información de clientes.
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'have_rnc', 'rnc', 'email', 'telefono', 'direccion']

# Serializador utilizado para registrar clientes con sus validaciones.
class ClienteSerializerReg(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'have_rnc', 'rnc', 'email', 'telefono', 'direccion']

    def validate(self, data):
        if data.get('have_rnc') and not data.get('rnc'):
            raise serializers.ValidationError("El RNC es requerido cuando have_rnc es True.")
        if not data.get('have_rnc') and data.get('rnc'):
            raise serializers.ValidationError("No puede tener RNC cuando have_rnc es False.")
        if data.get('rnc'):
            rnc = data.get('rnc').replace('-', '').strip()
            if not rnc.isdigit() or len(rnc) not in [9, 11]:
                raise serializers.ValidationError("El RNC debe tener 9 u 11 dígitos numéricos.")
        return data

# Serializador utilizado para actualizar clientes con sus validaciones.
class ClienteSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'have_rnc', 'rnc', 'email', 'telefono', 'direccion']

    def validate(self, data):
        if data.get('have_rnc') and not data.get('rnc'):
            raise serializers.ValidationError("El RNC es requerido cuando have_rnc es True.")
        if not data.get('have_rnc') and data.get('rnc'):
            raise serializers.ValidationError("No puede tener RNC cuando have_rnc es False.")
        if data.get('rnc'):
            rnc = data.get('rnc').replace('-', '').strip()
            if not rnc.isdigit() or len(rnc) not in [9, 11]:
                raise serializers.ValidationError("El RNC debe tener 9 u 11 dígitos numéricos.")
        return data