from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializers import UsersSerializers

@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    if Users.objects.filter(email=email).exists():
        return Response({'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UsersSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        usuario = Users.objects.get(email=email)
    except Users.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if usuario.verificar_password(password):
        return Response({
            'mensaje': 'Login exitoso',
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)