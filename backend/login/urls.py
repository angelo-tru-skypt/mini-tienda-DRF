from django.urls import path
from .views import LoginUserAPIView, RegisterUserAPIView

urlpatterns = [
    path("users/register/", RegisterUserAPIView.as_view(), name="register"),
    path("users/login/", LoginUserAPIView.as_view(), name="login")
]