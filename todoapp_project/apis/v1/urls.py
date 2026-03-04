from django.urls import path, include

urlpatterns = [
    # authentication
    path('auth/', include("authentication_app.urls")),
]