from django.urls import path
from .apis.auth_view import login

urlpatterns = [
    path("login/", login, name="login")
]