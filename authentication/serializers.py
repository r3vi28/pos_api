from rest_framework import serializers
from django.contrib.auth.models import User
from pos.models import Rol, Perfil


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        rol_estandar = Rol.objects.get(nombre='Usuario estándar')
        Perfil.objects.create(user=user, rol=rol_estandar)
        return user