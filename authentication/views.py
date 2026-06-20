from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RegistroSerializer
from pos.services.response import Result, TryCatch


@api_view(['POST'])
def registro(request):
    def action():
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Result.Exitosa('Usuario registrado correctamente.', {}, status.HTTP_201_CREATED)
        return Result.Error(serializer.errors)
    return TryCatch(action)