from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Users


class UserAuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register') 
        self.login_url = reverse('login')     
        
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'StrongPassword123'
        }
        self.user = Users.objects.create_user(**self.user_data)


    def test_registro_usuario_exitoso(self):
        """
        Asegura que un nuevo usuario puede registrarse con éxito.
        """
        nuevo_usuario_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'AnotherStrongPassword456'
        }
        # El cliente de pruebas sabe que register_url apunta a /users/register/
        response = self.client.post(self.register_url, nuevo_usuario_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 2) # El setUp + el nuevo
        self.assertEqual(response.data['msg'], 'Usuario creado correctamene')
        self.assertTrue(Users.objects.filter(email='newuser@example.com').exists())

    def test_registro_usuario_existente(self):
        """
        Asegura que no se puede registrar un usuario con un email ya existente.
        """
        # Intentamos registrar con el email del usuario creado en setUp
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Tu vista devuelve un array/lista con el error {"error", "El usuario ya existe"}
        self.assertIn("El usuario ya existe", response.data) 
        self.assertEqual(Users.objects.count(), 1) # Solo sigue existiendo el del setUp

    def test_registro_datos_invalidos(self):
        """
        Asegura que datos incompletos o inválidos fallan el registro.
        """
        datos_invalidos = {'username': 'test', 'email': 'correoinvalido'} # Faltan campos requeridos/formato incorrecto
        response = self.client.post(self.register_url, datos_invalidos, format='json')

        # Tu vista devuelve HTTP_404_NOT_FOUND para errores de serializer.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('email', response.data) # Esperamos errores de validación en la respuesta

    # --- Tests para LoginUserAPIView ---

    def test_login_exitoso(self):
        """
        Asegura que un usuario puede iniciar sesión con credenciales correctas.
        """
        response = self.client.post(self.login_url, 
                                    {'email': self.user_data['email'], 
                                     'password': self.user_data['password']}, 
                                    format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('mensaje', response.data)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_login_usuario_no_encontrado(self):
        """
        Asegura que el login falla si el email no existe.
        """
        response = self.client.post(self.login_url, 
                                    {'email': 'nonexistent@example.com', 
                                     'password': 'AnyPassword123'}, 
                                    format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Usuario no encontrado')

    def test_login_contrasena_incorrecta(self):
        """
        Asegura que el login falla con una contraseña incorrecta.
        """
        response = self.client.post(self.login_url, 
                                    {'email': self.user_data['email'], 
                                     'password': 'WrongPassword123'}, 
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Contraseña incorrecta')
