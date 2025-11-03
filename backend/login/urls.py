from django.urls import path
from .views import register_user, login_user

urlpatterns = [
    path("users/register/", register_user, name="register"),
    path("users/login/", login_user, name="login")
]