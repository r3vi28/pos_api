from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RegistroSerializer
from pos.services.response import Result, TryCatch
from rest_framework import status

@api_view(['POST'])
def registro(request):
    def action():
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Result.Exitosa('Usuario registrado correctamente.', {}, status.HTTP_201_CREATED)
        return Result.Error(serializer.errors)
    return TryCatch(action)

@api_view(['GET'])
def mi_perfil(request):
    def action():
        if not request.user.is_authenticated:
            return Result.Error('Debe iniciar sesión.')
        perfil = request.user.perfil
        return Result.Exitosa('', {'username': request.user.username, 'rol': perfil.rol.nombre}, status.HTTP_200_OK)
    return TryCatch(action)