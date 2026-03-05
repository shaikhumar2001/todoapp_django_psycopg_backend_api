from django.urls import path
from .apis.auth_view import login, register

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
]