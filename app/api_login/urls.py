from django.urls import path
from .views import LoginAPI,RegisterAPI

urlpatterns = [
    path("",LoginAPI.as_view(),name="Login"),
    path("register",RegisterAPI.as_view(),name="Register")

]