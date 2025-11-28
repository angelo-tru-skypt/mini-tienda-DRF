from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from rest_framework.views import APIView
from .serializers import UsersSerializers

class RegisterUserAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if Users.objects.filter(email=email).exists():
            return Response({"error", "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsersSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Usuario creado correctamene"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class LoginUserAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            usuario = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        if usuario.verificar_password(password):
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'mensaje': 'Login exitoso',
                'usuario': {
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Contraseña incorrecta'},
            status=status.HTTP_401_UNAUTHORIZED
        )