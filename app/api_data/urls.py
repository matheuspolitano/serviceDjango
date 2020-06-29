from django.urls import path
from .views import DataAPI

urlpatterns = [
    path("",DataAPI.as_view(),name="Data")
]